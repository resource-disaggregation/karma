# Workload driver program
# python3 driver.py 127.0.0.1 9090 9091 92 1 /home/midhul/snowflake_demands_nogaps10.pickle $((4 * 1024)) /home/midhul/nfs/jiffy_dump 0 0

from threading import local
import time
import os
import sys
from jiffy import JiffyClient
from multiprocessing import Process, Queue, Event
import pickle
import math
import datetime
import queue
# import boto3
import uuid
import random

S3_READ_LAT = 0.0121
S3_WRITE_LAT = 0.0258


# quit_signal, karma_queues[i], results, dir_host, dir_porta, dir_portb, block_size, backing_path, create_events[i]
def worker(quit_signal, q, resq, dir_host, dir_porta, dir_portb, block_size, backing_path, open_event, tenant_id, selfish, max_files):
    # Initialize
    # Connect the directory server with the corresponding port numbers
    # monitor_q.cancel_join_thread()
    local_random = random.Random()
    local_random.seed(1995 + int(tenant_id))
    
    client = JiffyClient(dir_host, dir_porta, dir_portb)
    # s3 = boto3.client('s3')
    buf = 'a' * block_size
    jiffy_fd = {}
    lat_sum = 0
    lat_count = 0
    total_ops = 0
    jiffy_blocks = 0
    persistent_blocks = 0
    print('Worker connected')

    # Open files
    max_files = capacity
    for i in range(max_files):
        filename = '/%s/block%d.txt' % (tenant_id, i)
        jiffy_fd[filename] = client.open_file(filename)
    open_event.set()
    print('Worker opened files')

    cur_wss = 0
    cur_alloc = 0

    while True:
        if quit_signal.is_set():
            resq.put({'lat_sum': lat_sum, 'lat_count': lat_count, 'jiffy_blocks': jiffy_blocks, 'persistent_blocks': persistent_blocks, 'total_ops': total_ops})
            print('Worker exiting')
            break

        # Check if there is an update
        task = None
        got_task = False
        try:
            task = q.get(True if cur_wss == 0 else False)
            got_task = True
        except queue.Empty:
            # no update
            got_task = False

        if got_task and task and task['op'] == 'update':
            cur_wss = task['wss']
            cur_alloc = task['alloc']
            # TODO: Re-initialize random distribution

        if cur_wss == 0:
            continue

        # Perform access
        access_key = local_random.randint(0, cur_wss-1)
        access_file = '/%s/block%d.txt' % (tenant_id, access_key)
        jiffy_fd[access_file].seek(0)
        if(local_random.random() < 0.5):
            if(access_key < cur_alloc):
                start_time = datetime.datetime.now()
                jiffy_fd[access_file].read(block_size)
                elapsed = datetime.datetime.now() - start_time
                lat_sum += elapsed.total_seconds()
                lat_count += 1
                jiffy_blocks += 1
                # print('Read key %d from Jiffy' % (access_key))
            else:
                # Read from S3
                start_time = datetime.datetime.now()
                time.sleep(S3_READ_LAT)
                elapsed = datetime.datetime.now() - start_time
                lat_sum += elapsed.total_seconds()
                lat_count += 1
                persistent_blocks += 1
                # print('Read key %d from S3' % (access_key))
        else:
            if(access_key < cur_alloc):
                start_time = datetime.datetime.now()
                jiffy_fd[access_file].write(buf)
                elapsed = datetime.datetime.now() - start_time
                lat_sum += elapsed.total_seconds()
                lat_count += 1
                jiffy_blocks += 1
                # print('Write key %d to Jiffy' % (access_key))
            else:
                # Write to S3
                start_time = datetime.datetime.now()
                time.sleep(S3_WRITE_LAT)
                elapsed = datetime.datetime.now() - start_time
                lat_sum += elapsed.total_seconds()
                lat_count += 1
                persistent_blocks += 1
                # print('Write key %d to S3' % (access_key))
        total_ops += 1
        
    return


# def s3_worker(quit_signal, q, resq, block_size, backing_path):
#     # Initialize
#     # Connect the directory server with the corresponding port numbers
#     # monitor_q.cancel_join_thread()
#     s3 = boto3.client('s3')
#     buf = 'a' * block_size
#     # in_jiffy = {}
#     # jiffy_create_ts = {}
#     # jiffy_fd = {}
#     lat_sum = 0
#     lat_count = 0
#     total_block_time = 0
#     jiffy_blocks = 0
#     persistent_blocks = 0
#     print('S3 Worker connected')

#     while True:
#         task = q.get()
#         if quit_signal.is_set() or task is None:
#             resq.put({'lat_sum': lat_sum, 'lat_count': lat_count, 'total_block_time': total_block_time, 'jiffy_blocks': jiffy_blocks, 'persistent_blocks': persistent_blocks})
#             print('Worker exiting')
#             break
#         filename = task['filename']
#         if task['op'] == 'write':
#             start_time = datetime.datetime.now()
#             resp = s3.put_object(Bucket=backing_path, Key=uuid.uuid4().hex + '/' + filename, Body=buf)
#             if resp['ResponseMetadata']['HTTPStatusCode'] != 200:
#                 raise Exception('S3 write failed')
#             elapsed = datetime.datetime.now() - start_time
#             total_elapsed = datetime.datetime.now() - task['start_ts']
#             print('Wrote to persistent storage ' + str(elapsed.total_seconds()))
#             # time.sleep(0.1)
#             lat_sum += total_elapsed.total_seconds()
#             lat_count += 1
#             persistent_blocks += 1
            
#     return

def get_demands(filename, scale_factor, t):
    with open(filename, 'rb') as handle:
        norm_d = pickle.load(handle)

    ret = []
    
    for i in range(len(norm_d[t])):
        ret.append(math.ceil(norm_d[t][i] * scale_factor))

    return ret

def get_allocations(filename, t):
    with open(filename, 'rb') as handle:
        allocs = pickle.load(handle)

    return allocs[t]


if __name__ == "__main__":
    dir_host = sys.argv[1]
    dir_porta = int(sys.argv[2])
    dir_portb = int(sys.argv[3])
    block_size = int(sys.argv[7])
    backing_path = sys.argv[8]
    tenant_id = sys.argv[4]
    para = int(sys.argv[5])
    fair_share = 100
    demands = get_demands(sys.argv[6], fair_share, tenant_id)
    # demands = [1, 1, 1, 1, 1]
    dur_epoch = 1
    oracle = bool(int(sys.argv[9]))
    selfish = bool(int(sys.argv[10]))
    allocations = get_allocations(sys.argv[11], tenant_id)
    capacity = int(sys.argv[12])
    # allocations = [1, 1, 1, 1, 1]

    # Create queues
    karma_queues = []
    for i in range(para):
        karma_queues.append(Queue())

    for i in range(para):
        karma_queues[i].cancel_join_thread()

    open_events = []
    for i in range(para):
        open_events.append(Event())

    results = Queue()
    quit_signal = Event()

    client = JiffyClient(dir_host, dir_porta, dir_portb)
    print('Jiffy client connected')

    # Pre-create files
    max_files = capacity
    for i in range(max_files):
        filename = '/%s/block%d.txt' % (tenant_id, i)
        client.create_file(filename, 'local://tmp')
    print('Pre-created files')
        

    # Create workers
    workers = []
    for i in range(para):
        p = Process(target=worker, args=(quit_signal, karma_queues[i], results, dir_host, dir_porta, dir_portb, block_size, backing_path, open_events[i], tenant_id, selfish, max_files))
        workers.append(p)

    # Start workers
    for i in range(para):
        workers[i].start()

    print('Started workers')


    # Wait for workers to open files
    for i in range(para):
        open_events[i].wait()

    print('Workers opened files')

    time_start = time.time()

    for e in range(len(demands)):
        cur_demand = demands[e]
        cur_allocation = allocations[e]
        print('Epoch ' + str(e) + ', demand=' + str(cur_demand) +', alloc='+ str(cur_allocation))

        # Send WSS and allocation updates to all workers 
        for i in range(para):
            karma_queues[i].put({'op': 'update', 'wss': cur_demand, 'alloc': cur_allocation})

        time.sleep(dur_epoch)


    for i in range(para):
        karma_queues[i].put(None)
    
    quit_signal.set()
    print('Epochs complete')

    time_end = time.time()
    

    # Wait for workers to finish
    for i in range(para):
        karma_queues[i].close()
        workers[i].join()



    # Get stats
    lat_sum = 0
    lat_count = 0
    jiffy_blocks = 0
    persistent_blocks = 0
    total_ops = 0
    for i in range(para):
        res = results.get()
        lat_sum += res['lat_sum']
        lat_count += res['lat_count']
        jiffy_blocks += res['jiffy_blocks']
        persistent_blocks += res['persistent_blocks']
        total_ops += res['total_ops']

    type_str = 'selfish' if selfish else 'alt'
    prefix_str = '<' + tenant_id + '>' + ' [' + type_str + '] '
    print(prefix_str + "Execution time: " + str(time_end -  time_start))
    print(prefix_str + 'Average latency: ' + str(float(lat_sum)/lat_count))
    print(prefix_str + 'Latency sum: ' + str(lat_sum))
    print(prefix_str + 'Latency count: ' + str(lat_count))
    print(prefix_str + 'Jiffy ops: ' + str(jiffy_blocks))
    print(prefix_str + 'Persistent ops: ' + str(persistent_blocks))
    print(prefix_str + 'Total ops: ' + str(total_ops))
    print(prefix_str + 'Throughput: ' + str(float(total_ops)/(time_end-time_start)))

    

    


    
