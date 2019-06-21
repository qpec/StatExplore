import pandas as pd
import numpy as np
import regex as re
import scipy.cluster.hierarchy
import os

input_term_path = '2_Vocab_Builder/included_terms.txt'
output_extract_txt_dir_path = 'metadata/'

def get_txtfile_contents(path):
    txt_object = open(path, 'r')
    txt = txt_object.read()
    txt_object.close()
    return txt

def dl_ngram_dist(ngram1, ngram2):
    distance = 0
    lengram1 = len(ngram1)
    lengram2 = len(ngram2)
    for word in ngram1:
        if word not in ngram2:
            distance += 1
        else:
            distance -= 1
    return distance

def cluster_ngrams(ngrams, compute_distance=dl_ngram_dist, max_dist=1, method='average'):
    counter = 0
    indices = np.triu_indices(len(ngrams), 1)
    pairwise_dists = np.apply_along_axis(
        lambda col: compute_distance(ngrams[col[0]], ngrams[col[1]]),
        0, indices)
    hierarchy = scipy.cluster.hierarchy.linkage(pairwise_dists, method=method)
    clusters = dict((i, [i]) for i in range(len(ngrams)))
    for (i, iteration) in enumerate(hierarchy):
        cl1, cl2, dist, num_items = iteration
        if dist >  max_dist:
            break
        items1 = clusters[cl1]
        items2 = clusters[cl2]
        del clusters[cl1]
        del clusters[cl2]
        clusters[len(ngrams) + i] = items1 + items2
    ngram_clusters = []
    for cluster in clusters.values():
        ngram_clusters.append([ngrams[i] for i in cluster])
    return ngram_clusters

def explore_term_clusters(txt_path, output_extract_txt_dir_path):
    text = get_txtfile_contents(txt_path)
    unf_ngrams = text.split('\n')
    ngrams = []
    for unf_ngram in unf_ngrams:
        ngrams.append(unf_ngram.split(','))
    clusters = cluster_ngrams(ngrams)
    dictionary = {
    'cluster':clusters,
    }
    output_path = os.path.join(output_extract_txt_dir_path, 'term_clusters.xlsx')
    pd.DataFrame(dictionary).to_excel(output_path)

text_path = '2_Vocab_Builder/included_terms.txt'
explore_term_clusters(text_path, output_extract_txt_dir_path)
