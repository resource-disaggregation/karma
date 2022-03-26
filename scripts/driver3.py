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
import boto3
import uuid
import random
import string

# S3_READ_LAT = 0.0121
# S3_WRITE_LAT = 0.0258


# quit_signal, karma_queues[i], results, dir_host, dir_porta, dir_portb, block_size, backing_path, create_events[i]
def worker(quit_signal, q, resq, dir_host, dir_porta, dir_portb, block_size, backing_path, open_event, tenant_id, selfish, max_files, s3_tenant_id, s3_map, fair_share):
    # Initialize
    # Connect the directory server with the corresponding port numbers
    # monitor_q.cancel_join_thread()
    local_random = random.Random()
    local_random.seed(1995 + int(tenant_id))
    
    client = JiffyClient(dir_host, dir_porta, dir_portb)
    s3 = boto3.client('s3')
    buf = 'a' * block_size
    jiffy_fd = {}
    lat_sum = 0
    lat_count = 0
    total_ops = 0
    good_ops = 0 # when demand > fair-share
    normal_ops = 0 # when demand <= fair-share
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

    quit_flag = False

    while True:
        if quit_signal.is_set() or quit_flag:
            resq.put({'lat_sum': lat_sum, 'lat_count': lat_count, 'jiffy_blocks': jiffy_blocks, 'persistent_blocks': persistent_blocks, 'total_ops': total_ops, 'good_ops': good_ops, 'normal_ops': normal_ops})
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

        if got_task and task and task['op'] == 'quit':
            quit_flag = True
            continue

        if got_task and task and task['op'] == 'update':
            cur_wss = task['wss']
            cur_alloc = task['alloc']
            # TODO: Re-initialize random distribution

        if cur_wss == 0:
            continue

        # Perform access
        access_key = local_random.randint(0, cur_wss-1)
        access_file = '/%s/block%d.txt' % (tenant_id, access_key % max_files)
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
                try:
                    get_resp = s3.get_object(Bucket=backing_path, Key=s3_tenant_id + '/' + s3_map[access_key])
                except s3.exceptions.NoSuchKey:
                    resp = s3.put_object(Bucket=backing_path, Key=s3_tenant_id + '/' + s3_map[access_key], Body=buf)
                    if resp['ResponseMetadata']['HTTPStatusCode'] != 200:
                        raise Exception('S3 write failed')
                    get_resp = s3.get_object(Bucket=backing_path, Key=s3_tenant_id + '/' + s3_map[access_key])
                if get_resp['ResponseMetadata']['HTTPStatusCode'] != 200:
                        raise Exception('S3 read failed')
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
                resp = s3.put_object(Bucket=backing_path, Key=s3_tenant_id + '/' + s3_map[access_key], Body=buf)
                if resp['ResponseMetadata']['HTTPStatusCode'] != 200:
                    raise Exception('S3 write failed')
                elapsed = datetime.datetime.now() - start_time
                lat_sum += elapsed.total_seconds()
                lat_count += 1
                persistent_blocks += 1
                # print('Write key %d to S3' % (access_key))
        total_ops += 1
        if cur_wss > fair_share:
            good_ops += 1
        else:
            normal_ops += 1
        
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

def perform_accesses(in_jiffy, local_random, jiffy_fd, s3, backing_path, s3_key, block_size, buf, duration, stats):
    begin_ts = datetime.datetime.now()
    while ((datetime.datetime.now() - begin_ts).total_seconds() < duration):
        if in_jiffy:
            jiffy_fd.seek(0)
            start_time = datetime.datetime.now()
            if(local_random.random() < 0.5):
                jiffy_fd.read(block_size)
            else:
                jiffy_fd.write(buf)
            elapsed = datetime.datetime.now() - start_time
            stats['latency_sum'] += elapsed.total_seconds()
            stats['jiffy_ops'] += 1
        else:
            # S3
            start_time = datetime.datetime.now()
            if(local_random.random() < 0.5):
                resp = s3.get_object(Bucket=backing_path, Key=s3_key)
            else:
                resp = s3.put_object(Bucket=backing_path, Key=s3_key, Body=buf)
            if resp['ResponseMetadata']['HTTPStatusCode'] != 200:
                raise Exception('S3 op failed')
            elapsed = datetime.datetime.now() - start_time
            stats['latency_sum'] += elapsed.total_seconds()
            stats['persistent_ops'] += 1

        stats['total_ops'] += 1


# Single client thread
if __name__ == "__main__":
    dir_host = sys.argv[1]
    dir_porta = int(sys.argv[2])
    dir_portb = int(sys.argv[3])
    block_size = int(sys.argv[4])
    backing_path = sys.argv[5]
    tenant_id = sys.argv[6]
    block_id = int(sys.argv[7])
    fair_share = int(sys.argv[8])
    demands = get_demands(sys.argv[9], fair_share, tenant_id)
    # demands = [1, 1, 1, 1, 1]
    dur_epoch = 1
    selfish = bool(int(sys.argv[10]))
    allocations = get_allocations(sys.argv[11], tenant_id)
    # allocations = [1, 1, 1, 1, 1]
    # capacity = int(sys.argv[12])

    client = JiffyClient(dir_host, dir_porta, dir_portb)
    print('Jiffy client connected')

    # Create block in Jiffy
    filename = '/%s/block%d.txt' % (tenant_id, block_id)
    jiffy_fd = client.open_or_create_file(filename, 'local://tmp')
    print('Created jiffy file')

    local_random = random.Random()
    local_random.seed(1995 + int(tenant_id))

    # Create block in S3
    s3_tenant_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    s3_block_id = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    s3 = boto3.client('s3')
    buf = 'a' * block_size

    resp = s3.put_object(Bucket=backing_path, Key=s3_tenant_id + '/' + s3_block_id, Body=buf)
    if resp['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise Exception('Initial S3 write failed')

    stats = {}
    stats['total_ops'] = 0
    stats['latency_sum'] = 0
    stats['jiffy_ops'] = 0
    stats['persistent_ops'] = 0
    # Microsecond scale histogram upto 100ms
    stats['latency_hist'] = [0 for _ in range(100000)]


    # Main loop
    for e in range(len(demands)):
        cur_demand = demands[e]
        cur_allocation = allocations[e]
        if cur_demand > block_id:
            perform_accesses(cur_allocation > block_id, local_random, jiffy_fd, s3, backing_path, s3_tenant_id + '/' + s3_block_id, block_size, buf, dur_epoch, stats)
        else:
            time.sleep(dur_epoch)


    # Get stats
    num_epochs = len(demands)
    total_duration = num_epochs*dur_epoch

    type_str = 'selfish' if selfish else 'alt'
    prefix_str = '<' + tenant_id + '>' + ' [' + type_str + '] '
    print(prefix_str + 'Average latency: ' + str(float(stats['latency_sum'])/stats['total_ops']))
    print(prefix_str + 'Jiffy ops: ' + str(stats['jiffy_ops']))
    print(prefix_str + 'Persistent ops: ' + str(stats['persistent_ops']))
    print(prefix_str + 'Total ops: ' + str(stats['total_ops']))
    print(prefix_str + 'Throughput: ' + str(float(stats['total_ops'])/total_duration))

    

    


    
