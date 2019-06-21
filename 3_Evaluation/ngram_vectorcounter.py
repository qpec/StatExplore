import pandas as pd
import numpy as np
import regex as re
import scipy.cluster.hierarchy
import os

input_txt_dir_path = 'input_output/Extracts[ori]/ngrams_chunked_extracts'
output_extract_txt_dir_path = 'metadata/'

def get_txt_fnames(dir):
    txt_paths = [os.path.join(dir, fname) for fname in os.listdir(dir) if fname.endswith('.txt')]
    return txt_paths

def get_txtfile_contents(path):
    txt_object = open(path, 'r')
    txt = txt_object.read()
    txt_object.close()
    return txt

def write_txt_file(txt, output_path):
    txt_file = open(output_path, 'w')
    txt_file.write(txt)
    txt_file.close()

def vector_tokenizer(text_path_list):
    vector = {}
    tokens_articles = []
    counter = 0
    for txt_path in text_path_list:
        tokens = get_txtfile_contents(txt_path).split('\n')
        tokens_articles.append(tokens)
        for token in tokens:
            if token not in vector:
                vector[token] = counter
                counter += 1
    return vector, tokens_articles

def counterizer(vector, tokens_articles):
    template_counts = [0 for i in vector]
    counts = template_counts[:]
    print(str(len(counts)) + 'unique tokens')
    for tokens in tokens_articles:
        counts_article = template_counts[:]
        for token in tokens:
            if counts_article[vector[token]] == 0:
                counts_article[vector[token]] = 1
                counts[vector[token]] += 1
    return counts

def dl_ngram_dist(ngram1, ngram2, token_bin_dict):
    distance = 0
    lengram1 = len(ngram1)
    lengram2 = len(ngram2)
    for word in ngram1:
        if word not in ngram2:
            distance += 1
    return distance

def cluster_ngrams(ngrams, token_bin_dict, compute_distance=dl_ngram_dist, max_dist=0, method='average'):
    ngrams_split = [ngram.split() for ngram in ngrams]
    counter = 0
    indices = np.triu_indices(len(ngrams_split), 1)
    pairwise_dists = np.apply_along_axis(
        lambda col: compute_distance(ngrams_split[col[0]], ngrams_split[col[1]], token_bin_dict),
        0, indices)
    hierarchy = scipy.cluster.hierarchy.linkage(pairwise_dists, method=method)
    clusters = dict((i, [i]) for i in range(len(ngrams_split)))
    for (i, iteration) in enumerate(hierarchy):
        cl1, cl2, dist, num_items = iteration
        if dist >  max_dist:
            break
        items1 = clusters[cl1]
        items2 = clusters[cl2]
        del clusters[cl1]
        del clusters[cl2]
        clusters[len(ngrams_split) + i] = items1 + items2
    ngram_clusters = []
    for cluster in clusters.values():
        ngram_clusters.append([ngrams_split[i] for i in cluster])
    return ngram_clusters

def exploration_counter(text_path_list, output_extract_txt_dir_path):
    vector, tokens_articles = vector_tokenizer(text_path_list)
    counts = counterizer(vector, tokens_articles)

    dictionary = {
    'token':[i for i in vector],
    'bins':counts
    }
    output_path = os.path.join(output_extract_txt_dir_path, 'ngrams_evaluation.xlsx')
    sh = pd.DataFrame(dictionary)
    sh = sh[sh.bins > 20]
    sh.to_excel(output_path)

def get_total_count_column_cluster(clusters, vector, counts):
    cluster_counts = []
    for cluster in clusters:
        this_cluster_count = 0
        for item in cluster:
            item = " ".join(item)
            print(item)
            if vector[item]:
                print(vector[item])
                count = counts[vector[item]]
                print(count)
                this_cluster_count += count
        cluster_counts.append(this_cluster_count)
    return cluster_counts

def explore_clusters(text_path_list, output_extract_txt_dir_path):
    vector, tokens_articles = vector_tokenizer(text_path_list)
    counts = counterizer(vector, tokens_articles)
    dictionary = {
    'token':[i for i in vector],
    'bins':counts
    }
    token_bin_df = pd.DataFrame(dictionary)
    token_bin_df = token_bin_df[token_bin_df.bins > 5]
    tokens_articles = token_bin_df["token"].to_list()
    counts_ft = token_bin_df["bins"].to_list()

    '''clusters = cluster_ngrams(tokens_articles, counts)
    cluster_counts = get_total_count_column_cluster(clusters, vector, counts)

    dictionary = {
    'cluster':clusters,
    'cluster_count':cluster_counts,
    }

    cluster_bin_df = pd.DataFrame(dictionary)
    cluster_bin_df = cluster_bin_df[cluster_bin_df.cluster_count > 78]
    clusters = cluster_bin_df["cluster"].to_list()
    cluster_counts = cluster_bin_df["cluster_count"].to_list()'''

    dictionary = {
    'cluster':tokens_articles,
    'cluster_count':counts_ft,
    }

    output_path = os.path.join(output_extract_txt_dir_path, 'ori.xlsx')
    pd.DataFrame(dictionary).to_excel(output_path)

text_path_list = get_txt_fnames(input_txt_dir_path)
explore_clusters(text_path_list, output_extract_txt_dir_path)
