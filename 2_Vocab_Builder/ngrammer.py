import pandas as pd
import regex as re
import os
import nltk
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
nltk.download('stopwords')
input_txt_dir_path = 'input_output/Extracts[ori]/txt_chunked_stemmed_clean_extracts/'
output_extract_txt_dir_path = 'input_output/Extracts[ori]/ngrams_chunked_extracts/'

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

def multi_ngrammer(text_path_list, output_extract_txt_dir_path, min_ngram=1, max_ngram=3, sw=stopwords.words('english')):
    stemmer = SnowballStemmer('english')
    stem_sw = [stemmer.stem(w) for w in sw]
    max = max_ngram + 1
    min = min_ngram
    counter = 0
    article_counter = 1
    for txt_path in text_path_list:
        txt = get_txtfile_contents(txt_path)
        if (article_counter % 50) == 0:
            print(str(article_counter) + " of " + str(len(text_path_list)) + " Processed...")
        article_counter += 1
        this_article_ngrams = []
        chunks = txt.split('\n')
        for chunk in chunks:
            chunk = [word for word in chunk.split() if word not in stem_sw]
            for i in range(0, len(chunk)):
                if i < len(chunk) - min:
                    for n in range(min, max):
                        if i+n <= len(chunk):
                            ngram = " ".join(chunk[i:i+n])
                            this_article_ngrams.append(ngram)
        output_chunked_path = os.path.join(output_extract_txt_dir_path, os.path.basename(txt_path))
        ngrams_text = '\n'.join(this_article_ngrams)
        write_txt_file(ngrams_text, output_chunked_path)

def single_ngrammer(text_path_list, output_extract_txt_dir_path, min_ngram=1, max_ngram=3, sw=stopwords.words('english')):
    stemmer = SnowballStemmer('english')
    stem_sw = [stemmer.stem(w) for w in sw]
    max = max_ngram + 1
    min = min_ngram
    counter = 0
    article_counter = 1
    for txt_path in text_path_list:
        txt = get_txtfile_contents(txt_path)
        if (article_counter % 50) == 0:
            print(str(article_counter) + " of " + str(len(text_path_list)) + " Processed...")
        article_counter += 1
        this_article_ngrams = []
        chunks = txt.split('\n')
        for chunk in chunks:
            chunk = [word for word in chunk.split() if word not in stem_sw]
            for n in range(min, max):
                ngram = " ".join(chunk[:n])
                this_article_ngrams.append(ngram)
        output_chunked_path = os.path.join(output_extract_txt_dir_path, os.path.basename(txt_path))
        ngrams_text = '\n'.join(this_article_ngrams)
        write_txt_file(ngrams_text, output_chunked_path)

text_path_list = get_txt_fnames(input_txt_dir_path)
multi_ngrammer(text_path_list, output_extract_txt_dir_path)
