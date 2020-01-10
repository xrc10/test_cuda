# test_cuda
A simple script to test if there is any GPU memory available 

# Usage
For instance, get 2 GPUs with at least 16000Mb memeory:

`CUDA_VISIBLE_DEVICES=$(python test_cuda.py 16000 2) python ... `

If there is no GPUs available, the process will launch the python code until the requirement is met.
