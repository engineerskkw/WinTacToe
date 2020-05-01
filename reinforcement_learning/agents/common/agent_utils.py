import os
import random
import time


def bucketify(data, no_of_buckets, reduce_function):
    bucket_size = len(data) // no_of_buckets

    tmp = [[] for i in range(no_of_buckets)]

    j = 0
    for i in range(no_of_buckets):
        for _ in range(bucket_size):
            tmp[i].append(data[j])
            j += 1

    return [reduce_function(i) for i in tmp]


def safe_return(returns, index):
    return returns[index] if index < len(returns) else 0

def gen_tempfile_path(agent_path):
    unique_number = str(int(float(time.time())*10**7)) + str(random.randint(10**10, 2*10**10))
    return os.path.join(os.path.dirname(agent_path), f"tmp_{unique_number}.h5")