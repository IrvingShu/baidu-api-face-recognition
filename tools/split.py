import sys
import os

gpu_num = 73
input_file = './img_below_5.lst'
out_dir = './imglist'

if __name__ == '__main__':
    lines = ''
    with open(input_file) as f:
        lines = f.readlines()
    count = len(lines)
    for i in range(gpu_num):
        out_path = os.path.join(out_dir, str(i)+'.txt')
        f = open(out_path, 'w')
        f.writelines(lines[i * count/gpu_num : (i+1) * count/gpu_num ])      

