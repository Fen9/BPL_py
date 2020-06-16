import os
import numpy as np
import pyro
import argparse
from scipy.io import loadmat
from scipy.special import logsumexp

parser = argparse.ArgumentParser(description='BPL Python Version')
parser.add_argument('--character_id', type=int, default=35)
parser.add_argument('--num_exemplars', type=int, default=9)
parser.add_argument('--path', type=str, default='./model_fits/')

args = parser.parse_args()


def rescore_by_rank(scores):
    scores = [item[0] for item in scores]
    rank_idx = np.argsort(scores)[::-1]
    weighted_scores = [1/(idx+1) for idx in rank_idx]
    log_weighted_scores = np.log(weighted_scores)
    weighted_scores = np.exp(log_weighted_scores - logsumexp(log_weighted_scores))
    sum_wts = np.sum(weighted_scores)
    return weighted_scores/sum_wts    


def sample_from_discrete_distribution(vector, num_samples ,weights):
    samples = np.random.choice(len(vector), num_samples, p=weights, replace=True)
    return vector[samples[0]], samples[0]


def task_generate_exemplars(log_weighted_scores, G, lib, num_exemplars):
    weighted_scores = np.exp(log_weighted_scores - logsumexp(log_weighted_scores))
    models = G['models'][0][0]
    samples_type = G['samples_type'][0][0]
    for i in range(0, num_exemplars):
        # choose the parse
        model, idx = sample_from_discrete_distribution(models, 1, weighted_scores)
        print(models[idx], idx)
        # choose the type-level resampling
        q = sample_from_discrete_distribution(samples_type, 1, np.ones(len(samples_type))/np.sum(np.ones(len(samples_type))))
        print(q)
        exit()


def generate_exemplars(template, lbclass):
    


def main():
    character_id = args.character_id
    num_exemplars = args.num_exemplars
    file_name = args.path + 'model_fits/handwritten' + str(character_id) + '_G' + '.mat'
    G = loadmat(file_name)['G']
    scores = G['scores'][0][0]

    weighted_scores = rescore_by_rank(scores)
    print(weighted_scores)
    task_generate_exemplars(weighted_scores, G, None, num_exemplars)


if __name__ == "__main__":
    main()