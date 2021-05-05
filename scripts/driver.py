# Workload driver program
# python3 driver.py 127.0.0.1 9090 9091 92 1 /home/midhul/snowflake_demands_nogaps10.pickle $((4 * 1024)) /home/midhul/nfs/jiffy_dump 0 0

import time
import os
import sys
from jiffy import JiffyClient
from multiprocessing import Process, Queue, Event
import pickle
import math
import datetime
import queue
import boto3
import uuid

# Deterministic mapping from filename to worker
def map_file_to_worker(filename, num_workers):
    return abs(hash(filename)) % num_workers

# def run_monitor(q, dir_host, dir_porta, dir_portb, tenant_id):
#     client = JiffyClient(dir_host, dir_porta, dir_portb)
#     print('Monitor connected')

#     exit_flag = False
#     cur_jiffy_blocks = 0

#     while True:
#         extra_persistent_blocks = 0
#         while True:
#             try:
#                 stat = q.get_nowait()
#                 if stat is None:
#                     exit_flag = True
#                 elif stat == 'put_jiffy':
#                     cur_jiffy_blocks += 1
#                 elif stat == 'remove_jiffy':
#                     cur_jiffy_blocks -= 1
#                 elif stat == 'put_persistent':
#                     extra_persistent_blocks += 1
#                 # Ignore remove_persistent 
#             except queue.Empty:
#                 break

#         if exit_flag:
#             print('Monitor exiting')
#             break
#         adv_demand = cur_jiffy_blocks + extra_persistent_blocks
#         assert adv_demand >= 0
#         client.fs.add_tags('advertise_demand', {'tenant_id': tenant_id, 'demand': str(adv_demand)})
#         time.sleep(1)


# quit_signal, karma_queues[i], results, dir_host, dir_porta, dir_portb, block_size, backing_path, create_events[i]
def worker(quit_signal, q, resq, dir_host, dir_porta, dir_portb, block_size, backing_path, create_event):
    # Initialize
    # Connect the directory server with the corresponding port numbers
    # monitor_q.cancel_join_thread()
    
    client = JiffyClient(dir_host, dir_porta, dir_portb)
    # s3 = boto3.client('s3')
    buf = 'a' * block_size
    in_jiffy = {}
    jiffy_create_ts = {}
    jiffy_fd = {}
    lat_sum = 0
    lat_count = 0
    total_block_time = 0
    jiffy_blocks = 0
    persistent_blocks = 0
    print('Worker connected')

    while True:
        task = q.get()
        if quit_signal.is_set() or task is None:
            resq.put({'lat_sum': lat_sum, 'lat_count': lat_count, 'total_block_time': total_block_time, 'jiffy_blocks': jiffy_blocks, 'persistent_blocks': persistent_blocks})
            print('Worker exiting')
            break
        
        if task['op'] == 'create':
            filename = task['filename']
            start_time = datetime.datetime.now()
            f = client.create_file(filename, 'local:/' + backing_path)
            elapsed = datetime.datetime.now() - start_time
            print('Create time: ' + str(elapsed.total_seconds()))
            jiffy_fd[filename] = f

        if task['op'] == 'create_fin':
            create_event.set()

        if task['op'] == 'write':
            filename = task['filename']
            start_time = datetime.datetime.now()
            jiffy_fd[filename].seek(0)
            jiffy_fd[filename].write(buf)
            elapsed = datetime.datetime.now() - start_time
            total_elapsed = datetime.datetime.now() - task['start_ts']
            print('Wrote to jiffy: ' + str(elapsed.total_seconds()))
            lat_sum += total_elapsed.total_seconds()
            lat_count += 1
            jiffy_blocks += 1

        # if task['op'] == 'remove':
        #     # monitor_q.put(('remove_dequeue', filename))
        #     if in_jiffy[filename]:
        #         # monitor_q.put(('out_jiffy', filename))
        #         try:
        #             jiffy_fd[filename].clear()
        #             client.remove(filename)
        #             duration_used = datetime.datetime.now() - jiffy_create_ts[filename]
        #             total_block_time += duration_used.total_seconds()
        #             print('Removed from jiffy')
        #         except:
        #             print('Remove from jiffy failed')
        #         del jiffy_create_ts[filename]
        #         del jiffy_fd[filename]
        #     # else:
        #     #     monitor_q.put('remove_persistent')
            
        #     del in_jiffy[filename]
        #     # monitor_q.put('remove_complete')
        
    return


def s3_worker(quit_signal, q, resq, block_size, backing_path):
    # Initialize
    # Connect the directory server with the corresponding port numbers
    # monitor_q.cancel_join_thread()
    s3 = boto3.client('s3')
    buf = 'a' * block_size
    # in_jiffy = {}
    # jiffy_create_ts = {}
    # jiffy_fd = {}
    lat_sum = 0
    lat_count = 0
    total_block_time = 0
    jiffy_blocks = 0
    persistent_blocks = 0
    print('S3 Worker connected')

    while True:
        task = q.get()
        if quit_signal.is_set() or task is None:
            resq.put({'lat_sum': lat_sum, 'lat_count': lat_count, 'total_block_time': total_block_time, 'jiffy_blocks': jiffy_blocks, 'persistent_blocks': persistent_blocks})
            print('Worker exiting')
            break
        filename = task['filename']
        if task['op'] == 'write':
            resp = s3.put_object(Bucket=backing_path, Key=uuid.uuid4().hex + '/' + filename, Body=buf)
            if resp['ResponseMetadata']['HTTPStatusCode'] != 200:
                raise Exception('S3 write failed')
            # time.sleep(0.1)
            elapsed = datetime.datetime.now() - task['start_ts']
            lat_sum += elapsed.total_seconds()
            lat_count += 1
            persistent_blocks += 1
            print('Wrote to persistent storage ' + str(elapsed.total_seconds()))

    return

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


# def compute_demand(tenant_id, files_in_jiffy, outstanding_puts, outstanding_removes_jiffy):
#     # adv_demand = cur_demand + inflight_puts
#     print('outstanding puts: ' + str(len(outstanding_puts)))
#     print('outstanding removes: ' + str(len(outstanding_removes)))
#     print('outstanding jiffy removes: ' + str(len(outstanding_removes_jiffy)))
#     # adv_demand = max(0, prev_demand + inflight_puts - inflight_removes)
#     adv_demand = max(0, len(files_in_jiffy) + len(outstanding_puts) - len(outstanding_removes_jiffy))
#     assert adv_demand >= 0
#     return adv_demand

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
    # demands = [4, 4, 4, 4, 0]
    dur_epoch = 1
    micro_epochs = 1 # Micro-epochs per epoch
    dur_micro_epoch = 1 # Micro-epoch duration
    oracle = bool(int(sys.argv[9]))
    selfish = bool(int(sys.argv[10]))
    allocations = get_allocations(sys.argv[11], tenant_id)
    # allocations = [4, 2, 1, 10, 3]

    file_limit = 100

    if not os.path.exists('%s/%s' % (backing_path, tenant_id)):
        os.makedirs('%s/%s' % (backing_path, tenant_id))

    # Create queues
    karma_queues = []
    for i in range(para):
        karma_queues.append(Queue())
    
    s3_queues = []
    for i in range(para):
        s3_queues.append(Queue())

    for i in range(para):
        karma_queues[i].cancel_join_thread()
        s3_queues[i].cancel_join_thread()

    create_events = []
    for i in range(para):
        create_events.append(Event())

    results = Queue()
    # monitor_queue = Queue()
    quit_signal = Event()

    # Create monitor
    # monitor = Process(target=run_monitor, args=(monitor_queue, dir_host, dir_porta, dir_portb, tenant_id))

    # Start monitor
    # monitor.start()
    client = JiffyClient(dir_host, dir_porta, dir_portb)
    print('Monitor connected')
    
    # Create workers
    workers = []
    for i in range(para):
        p = Process(target=worker, args=(quit_signal, karma_queues[i], results, dir_host, dir_porta, dir_portb, block_size, backing_path, create_events[i]))
        workers.append(p)

    # Create S3 workers
    s3_workers = []
    for i in range(para):
        p = Process(target=s3_worker, args=(quit_signal, s3_queues[i], results, block_size, backing_path))
        s3_workers.append(p)

    # Start workers
    for i in range(para):
        workers[i].start()

    for i in range(para):
        s3_workers[i].start()

    print('Started workers')

    cur_files = []

    # Pre-create files
    max_files = max(allocations)
    max_files = min(file_limit, max_files)
    for i in range(max_files):
        filename = '/%s/block%d.txt' % (tenant_id, i)
        cur_files.append(filename)
        wid = map_file_to_worker(filename, para)
        karma_queues[wid].put({'op': 'create', 'filename': filename})
    
    for i in range(para):
        karma_queues[i].put({'op': 'create_fin'})

    for i in range(para):
        create_events[i].wait()

    print('Files pre-created')

    time_start = time.time()

    cur_demand = 0
    prev_demand = 0

    for e in range(len(demands)):
        cur_demand = demands[e]
        cur_allocation = allocations[e]
        print('Epoch ' + str(e) + ', demand=' + str(cur_demand) +', alloc='+ str(cur_allocation))

        num_to_karma = min(cur_demand, cur_allocation)
        for i in range(num_to_karma):
            filename = cur_files[i%len(cur_files)]
            wid = map_file_to_worker(filename, para)
            karma_queues[wid].put({'op': 'write', 'filename': filename, 'start_ts': datetime.datetime.now()})

        for i in range(num_to_karma, cur_demand):
            filename = 'blablablabla'
            wid = map_file_to_worker(filename, para)
            s3_queues[wid].put({'op': 'write', 'filename': filename, 'start_ts': datetime.datetime.now()})

        time.sleep(dur_epoch)


    for i in range(para):
        karma_queues[i].put(None)

    for i in range(para):
        s3_queues[i].put(None)
    
    quit_signal.set()
    print('Epochs complete')

    # Wait for worker to finish
    for i in range(para):
        karma_queues[i].close()
        # queues[i].join_thread()
        workers[i].join()

        s3_queues[i].close()
        s3_workers[i].join()

    # monitor_queue.put(None)
    # Wait for monitor to exit
    # monitor_queue.close()
    # monitor_queue.join_thread()
    # monitor.join()

    # Get stats
    lat_sum = 0
    lat_count = 0
    total_block_time = 0
    jiffy_blocks = 0
    persistent_blocks = 0
    for i in range(2 * para):
        res = results.get()
        lat_sum += res['lat_sum']
        lat_count += res['lat_count']
        total_block_time += res['total_block_time']
        jiffy_blocks += res['jiffy_blocks']
        persistent_blocks += res['persistent_blocks']

    type_str = 'selfish' if selfish else 'alt'
    prefix_str = '<' + tenant_id + '>' + ' [' + type_str + '] '
    print(prefix_str + 'Average latency: ' + str(float(lat_sum)/lat_count))
    print(prefix_str + 'Latency sum: ' + str(lat_sum))
    print(prefix_str + 'Latency count: ' + str(lat_count))
    print(prefix_str + 'Total block time: ' + str(total_block_time))
    print(prefix_str + 'Jiffy blocks: ' + str(jiffy_blocks))
    print(prefix_str + 'Persistent blocks: ' + str(persistent_blocks))

    time_end = time.time()
    print(prefix_str + "Execution time: " + str(time_end -  time_start))


    
