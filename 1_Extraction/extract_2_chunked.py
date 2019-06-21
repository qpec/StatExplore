import pandas as pd
import regex as re
from unidecode import unidecode
import fitz
import os

input_txt_dir_path = 'input_output/Extracts[statistics]/txt_clean_extracts/'
chunker_stopwords_path = '1_Extraction/chunker_stopwords.txt'
output_chunked = 'input_output/Extracts[ori]/txt_chunked_stemmed_clean_extracts/'

def get_chunker_stopwords(chunker_stopwords_path):
    txt = get_txtfile_contents(chunker_stopwords_path)
    chunker_words = txt.split('\n')
    return chunker_words

def get_txt_fnames(dir):
    txt_paths = [fname for fname in os.listdir(dir) if fname.endswith('.txt')]
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

def chunker(txt, chunker_stopwords_path):
    chunk_list = get_chunker_stopwords(chunker_stopwords_path)
    txt = re.sub(r'\.', '\n', txt)
    txt = re.sub(r'\,', '\n', txt)
    txt = re.sub(r'[^\na-z ]', '\n', txt)
    for chunk_token in chunk_list:
        txt = re.sub("\s"+chunk_token+"\s", '\n', txt)
    txt = re.sub('\n +', '\n', txt)
    txt = re.sub('\n+', '\n', txt)
    txt = re.sub(r' +', ' ', txt)
    return txt

def extract_2_chunked(input_txt_dir_path, chunker_stopwords_path, output_chunked):
    txt_paths = get_txt_fnames(input_txt_dir_path)
    for txt_path in txt_paths:
        txt = get_txtfile_contents(os.path.join(input_txt_dir_path, txt_path))
        chunked = chunker(txt, chunker_stopwords_path)
        output_path = os.path.join(output_chunked, txt_path)
        write_txt_file(chunked, output_path)

extract_2_chunked(input_txt_dir_path, chunker_stopwords_path, output_chunked)
