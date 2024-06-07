import numpy as np
import os

data = np.loadtxt('data.txt')

os.mkdir('output/results')

output_file = 'output/results/output_file.txt'

data_shape = np.shape(data)

np_version = np.__version__

with open(output_file, 'a+') as f:
    f.write(f"Data file shape: {data_shape}\n\n")
    f.write(f"Numpy version: {np_version}\n")