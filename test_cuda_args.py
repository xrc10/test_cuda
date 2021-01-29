import subprocess
import time
import sys
import argparse


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
    # if len(sys.argv) > 2:
    #     n_gpus = int(sys.argv[2])
    # else:
    #     n_gpus = 1

    # if len(sys.argv) > 3:
    #     splitter = sys.argv[3]
    # else:
    #     splitter = ','

    parser = argparse.ArgumentParser(description='Find Free CUDA GPU')
    parser.add_argument('-min_free_mb', type=int, default=1000,
                    help='free memory in Mb')
    parser.add_argument('-num_gpus', type=int, default=1,
                    help='number of GPUs')
    parser.add_argument('-splitter',
                    help='char to split outputs', default=',')
    parser.add_argument('-block_gpu_id', type=int, nargs='+', default=[],
                    help='gpu ids to block (for hardware issues)')
    args = parser.parse_args()

    available_gpus = []
    while True:
        interval = 5 # check every 5 seconds
        minimum = args.min_free_mb
        mm = get_gpu_memory_map()
        for k,v in sorted(mm.items(), key = lambda x : x[1], reverse = True):
            # print("GPU:{} |||| free: {}".format(k, v))
            if v > minimum and (not k in available_gpus) and (not k in args.block_gpu_id):
                available_gpus.append(str(k))
                if len(available_gpus) >= args.num_gpus:
                    print(args.splitter.join(available_gpus))
                    sys.exit(0)
        time.sleep(interval)   # Delays for 5 seconds.

if __name__ == '__main__':
    main()
