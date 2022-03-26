# Workload driver program
# python3 driver.py 127.0.0.1 9090 9091 92 1 /home/midhul/snowflake_demands_nogaps10.pickle $((4 * 1024)) /home/midhul/nfs/jiffy_dump 0 0

from itertools import count
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

def worker(idx, task_q, results, dir_host, dir_porta, dir_portb, block_size, backing_path, tenant_id, selfish, fair_share):

    client = JiffyClient(dir_host, dir_porta, dir_portb)
    print('Jiffy client connected')

    # Create block in Jiffy
    filename = '/%s/block%d.txt' % (tenant_id, idx)
    jiffy_fd = client.open_or_create_file(filename, 'local://tmp')
    print('Created jiffy file')

    local_random = random.Random()
    local_random.seed(1995 + int(tenant_id) + idx)

    # Create block in S3
    s3_tenant_id = ''.join(local_random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    s3_block_id = ''.join(local_random.choice(string.ascii_uppercase + string.digits) for _ in range(10))
    s3 = boto3.client('s3')
    buf = 'a' * block_size

    resp = s3.put_object(Bucket=backing_path, Key=s3_tenant_id + '/' + s3_block_id, Body=buf)
    if resp['ResponseMetadata']['HTTPStatusCode'] != 200:
        raise Exception('Initial S3 write failed')
    print('Created S3 key')

    stats = {}
    stats['total_ops'] = 0
    stats['latency_sum'] = 0
    stats['jiffy_ops'] = 0
    stats['persistent_ops'] = 0
    # 10-microsecond scale histogram upto 100ms
    stats['latency_hist'] = [0 for _ in range(10000)]


    # Main loop
    for i in range(len(task_q)):
        task = task_q[i]
        perform_accesses(task['in_jiffy'], local_random, jiffy_fd, s3, backing_path, s3_tenant_id + '/' + s3_block_id, block_size, buf, task['duration'], stats)

    results.put(stats)
    print('Worker exiting')
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

# TODO: Handle selfish
if __name__ == "__main__":
    dir_host = sys.argv[1]
    dir_porta = int(sys.argv[2])
    dir_portb = int(sys.argv[3])
    block_size = int(sys.argv[4])
    backing_path = sys.argv[5]
    tenant_id = sys.argv[6]
    fair_share = int(sys.argv[7])
    if sys.argv[8] == 'foobar':
        demands = [1, 1, 1, 1, 1]
    else:
        demands = get_demands(sys.argv[8], fair_share, tenant_id)
    # demands = [1, 1, 1, 1, 1]
    dur_epoch = 1
    selfish = bool(int(sys.argv[9]))
    if sys.argv[10] == 'foobar':
        allocations = [1, 1, 1, 1, 1]
    else:    
        allocations = get_allocations(sys.argv[10], tenant_id)
    
    # capacity = int(sys.argv[12])

    para = fair_share
    task_queues = []
    for i in range(para):
        task_queues.append([])

    # Create tasks and assign then to queues in round-robin
    widx = 0
    for e in range(len(demands)):
        cur_demand = demands[e]
        cur_allocation = allocations[e]
        for i in range(cur_demand):
            task = {'block_id': i, 'in_jiffy': (cur_allocation > i), 'duration': dur_epoch}
            task_queues[wid].append(task)
            wid = (wid + 1)%para

    results = Queue()

    # Create workers
    workers = []
    for i in range(para):
        p = Process(target=worker, args=(i, task_queues[i], results, dir_host, dir_porta, dir_portb, block_size, backing_path, tenant_id, selfish, fair_share))
        workers.append(p)

    # Start workers
    for i in range(para):
        workers[i].start()

    print('Started workers')

    # Wait for workers to finish
    for i in range(para):
        workers[i].join()


    # Aggregate stats
    stats = {}
    stats['total_ops'] = 0
    stats['latency_sum'] = 0
    stats['jiffy_ops'] = 0
    stats['persistent_ops'] = 0
    # Microsecond scale histogram upto 100ms
    stats['latency_hist'] = [0 for _ in range(10000)]

    for i in range(para):
        res = results.get()
        stats['total_ops'] += res['total_ops']
        stats['latency_sum'] += res['latency_sum']
        stats['jiffy_ops'] += res['jiffy_ops']
        stats['persistent_ops'] += res['persistent_ops']
        for y in range(10000):
            stats['latency_hist'][y] += res['latency_hist'][y]

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

    p50_count = int(0.5 * stats['total_ops'])
    p90_count = int(0.9 * stats['total_ops'])
    p99_count = int(0.99 * stats['total_ops'])
    p999_count = int(0.999 * stats['total_ops'])
    p9999_count = int(0.9999 * stats['total_ops'])

    p50_lat = -1
    p90_lat = -1
    p99_lat = -1
    p999_lat = -1
    p9999_lat = -1

    
    cnt = 0
    for y in range(10000):
        cnt += stats['latency_hist'][y]
        if p50_lat == -1 and cnt >= p50_count:
            p50_lat = y*10
        if p90_lat == -1 and cnt >= p90_count:
            p90_lat = y*10
        if p99_lat == -1 and cnt >= p99_count:
            p99_lat = y*10
        if p999_lat == -1 and cnt >= p999_count:
            p999_lat = y*10
        if p9999_lat == -1 and cnt >= p9999_count:
            p9999_lat = y*10

    print(prefix_str + 'p50 latency: ' + str(p50_lat))
    print(prefix_str + 'p90 latency: ' + str(p90_lat))
    print(prefix_str + 'p99 latency: ' + str(p99_lat))
    print(prefix_str + 'p999 latency: ' + str(p999_lat))
    print(prefix_str + 'p9999 latency: ' + str(p9999_lat))

    

    

    


    
