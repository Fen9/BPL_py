import os
import numpy
import pyro
import matplotlib
import argparse
from scipy.io import loadmat

parser = argparse.ArgumentParser(description='BPL Python Version')
parser.add_argument('--character_id', type=int, default=35)
parser.add_argument('--num_exemplars', type=int, default=9)
parser.add_argument('--path', type=str, default='./model_fits/')

args = parser.parse_args()

 
def main():
    character_id = args.character_id
    num_exemplars = args.num_exemplars
    file_name = args.path + 'model_fits/handwritten' + str(character_id) + '_G' + '.mat'
    G = loadmat(file_name)['G']
    print(G)
    # print(G.scores)

if __name__ == "__main__":
    main()