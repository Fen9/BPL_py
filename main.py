import os
import numpy as np
import copy
import argparse
from scipy.io import loadmat
from scipy.special import logsumexp
import scipy.io as sio

from mat_utils import load_mat_G, process_mat
from generate_exemplars.generate_exemplars import generate_exemplar

parser = argparse.ArgumentParser(description='BPL Python Version')
parser.add_argument('--character_id', type=int, default=35)
parser.add_argument('--num_exemplars', type=int, default=9)
parser.add_argument('--path', type=str, default='./model/G/')

args = parser.parse_args()


def rescore_by_rank(scores):
    rank_idx = np.argsort(scores)[::-1]
    weighted_scores = [1/(idx+1) for idx in rank_idx]
    log_weighted_scores = np.log(weighted_scores)
    weighted_scores = np.exp(log_weighted_scores - logsumexp(log_weighted_scores))
    sum_wts = np.sum(weighted_scores)
    return weighted_scores/sum_wts


def rand_discrete(models, wts):
    samples = np.random.choice(len(models), 1, p=wts, replace=True)
    return models[samples[0]], samples[0]


def task_generate_exemplars(G, lib, num_exemplars):
    log_wts = G['scores']
    wts = np.exp(log_wts - logsumexp(log_wts))
    samples = [None for i in range(0, num_exemplars)]
    types = [None for i in range(0, num_exemplars)]

    for i in range(0, num_exemplars):
        # choose the parse
        M, idx = rand_discrete(G['models'], wts)
        # choose the type-level resampling
        Q, q_idx = rand_discrete(G['samples_type'][idx], np.ones(len(G['samples_type']))/np.sum(np.ones(len(G['samples_type']))))
        # Q = Q.copy()
        Q._I = copy.deepcopy(M._I)

        types[i] = copy.deepcopy(Q)
        Q = generate_exemplar(copy.deepcopy(Q), lib)
        samples[i] = copy.deepcopy(Q)
        print(samples[i])
    print(samples)


def task_generate_exemplars_1overk(G, lib, num_exemplars):
    wts = rescore_by_rank(G['scores'])
    G['scores'] = copy.deepcopy(np.log(wts))
    task_generate_exemplars(G, lib, num_exemplars)


def main():
    character_id = args.character_id
    num_exemplars = args.num_exemplars
    file_name = args.path + str(character_id) +'G.mat'
    G = load_mat_G(file_name)
    lib_py = sio.loadmat("lib_py.mat", squeeze_me=True)['lib_py']
    lib = process_mat(lib_py)
    task_generate_exemplars_1overk(G, lib, num_exemplars)


if __name__ == "__main__":
    main()