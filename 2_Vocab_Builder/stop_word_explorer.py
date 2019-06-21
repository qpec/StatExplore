import pandas as pd
import regex as re
import os

input_txt_dir_path = 'input_output/ngrams_chunked_extracts/'
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

def explorer(text_path_list, output_extract_txt_dir_path):
    vector = {}
    tokens_articles = []
    counter = 0
    for txt_path in text_path_list:
        tokens = get_txtfile_contents(txt_path).split()
        tokens_articles.append(tokens)
        for token in tokens:
            if token not in vector:
                vector[token] = counter
                counter += 1
    template_counts = [0 for i in vector]
    counts = template_counts[:]
    print(str(len(counts)) + 'unique tokens')
    for tokens in tokens_articles:
        counts_article = template_counts[:]
        for token in tokens:
            if counts_article[vector[token]] == 0:
                counts_article[vector[token]] = 1
                counts[vector[token]] += 1

    dictionary = {
    'token':[i for i in vector],
    'bins':counts
    }
    output_path = os.path.join(output_extract_txt_dir_path, 'stopword_exploration.xlsx')
    pd.DataFrame(dictionary).to_excel(output_path)

text_path_list = get_txt_fnames(input_txt_dir_path)
explorer(text_path_list, output_extract_txt_dir_path)
