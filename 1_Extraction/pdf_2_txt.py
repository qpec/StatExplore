import pandas as pd
import regex as re
from unidecode import unidecode
import fitz
import os

input_pdf_dir_path = 'input_output/pdf_articles/'
output_txt_dir_path = 'input_output/txt_articles/'
output_clean_txt_dir_path = 'input_output/txt_minor_clean_articles/'

def get_pdf_fnames(dir):
    pdf_paths = [fname for fname in os.listdir(dir) if fname.endswith('.pdf')]
    return pdf_paths

def clean_txt(txt):
    txt = txt.lower()
    txt = unidecode(txt)
    txt = re.sub(r'-\n', '', txt)
    txt = re.sub(r'\n', ' ', txt)
    return txt

def get_txt_from_pdf(input_pdf_fname):
    output_txt = ''
    pdf_object = fitz.Document(input_pdf_fname)
    for page in pdf_object:
        txt = page.getText('txt')
        output_txt += ' ' + str(txt)
    pdf_object.close()
    return output_txt

def write_txt_file(txt, output_path):
    txt_file = open(output_path, 'w')
    txt_file.write(txt)
    txt_file.close()

def pdf_2_txt(input_pdf_dir_path, input_pdf_fname, output_txt_dir_path, output_clean_txt_dir_path):
    output_txt_name = re.sub('\.pdf', '.txt', input_pdf_fname)
    output_txt_dir_path = output_txt_dir_path + output_txt_name
    output_clean_txt_dir_path = output_clean_txt_dir_path + output_txt_name
    if not os.path.isfile(output_clean_txt_dir_path):
        print(output_txt_name)
        txt = get_txt_from_pdf(input_pdf_dir_path + input_pdf_fname)
        cleaned_txt = clean_txt(txt)
        write_txt_file(txt, output_txt_dir_path)
        write_txt_file(cleaned_txt, output_clean_txt_dir_path)
    else:
        print('skip')

def main(input_pdf_dir_path, output_txt_dir_path, output_clean_txt_dir_path):
    pdf_paths = get_pdf_fnames(input_pdf_dir_path)
    len_pdfs = len(pdf_paths)
    counter = 1
    for pdf_path in pdf_paths:
        pdf_2_txt(input_pdf_dir_path, pdf_path, output_txt_dir_path, output_clean_txt_dir_path)
        print('#' + str(counter) + ' of ' + str(len(pdf_paths)) + ' pdf2text and clean processed.')
        counter += 1
    print("Finished process.")
    print("")

main(input_pdf_dir_path, output_txt_dir_path, output_clean_txt_dir_path)
