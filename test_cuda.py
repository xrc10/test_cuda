import subprocess
import time
import sys

def get_gpu_memory_map():
    """Get the current gpu usage.

    Returns
    -------
    usage: dict
        Keys are device ids as integers.
        Values are memory usage as integers in MB.
    """
    result = subprocess.check_output(
        [
            'nvidia-smi', '--query-gpu=memory.free',
            '--format=csv,nounits,noheader'
        ], encoding='utf-8')
    # Convert lines into a dictionary
    gpu_memory = [int(x) for x in result.strip().split('\n')]
    gpu_memory_map = dict(zip(range(len(gpu_memory)), gpu_memory))
    return gpu_memory_map

def main():
    if len(sys.argv) > 2:
        n_gpus = int(sys.argv[2])
    else:
        n_gpus = 1

    available_gpus = []
    while True:
        interval = 5 # check every 5 seconds
        minimum = int(sys.argv[1])
        mm = get_gpu_memory_map()
        for k,v in sorted(mm.items(), key = lambda x : x[1], reverse = True):
            # print("GPU:{} |||| free: {}".format(k, v))
            if v > minimum and (not k in available_gpus):
                available_gpus.append(k)
                if len(available_gpus) >= n_gpus:
                    print(','.join(available_gpus))
                sys.exit(0)
        time.sleep(interval)   # Delays for 5 seconds.

if __name__ == '__main__':
    main()
