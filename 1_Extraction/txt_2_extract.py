from nltk.stem import SnowballStemmer
import pandas as pd
import regex as re
import os

input_txt_dir_path = 'input_output/txt_clean_articles/'
output_extract_txt_dir_path = 'input_output/Extracts[statistics]/txt_clean_extracts/'
output_stemmed_extract_txt_dir_path = 'input_output/Extracts[statistics]/txt_stemmed_clean_extracts/'
output_metadata_dir_path = 'metadata/'

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

def fetcher(txt):
    patterns = [
    #statistical analysis
    r'(\n\s*([a-z]+\s){0,2}statistic(al|s)\s*([a-z]+\s*){0,2}\s*\n).+?(\n\s*([a-z]+\s){0,2}result(|s)\s*([a-z]+\s*){0,2}\s*\n)'
    ]
    return_match = ''
    cycle = 1
    for pattern in patterns:
        p = re.compile(pattern, re.DOTALL)
        match = p.search(txt)
        if match:
            return_match = re.sub(r'\n', ' ', str(match.group()))
            break
        else:
            cycle += 1
            continue
    if cycle > len(patterns):
        cycle = "NO MATCH"
    return return_match, cycle

def txt_2_extracts(input_txt_dir_path, output_extract_txt_dir_path, output_stemmed_extract_txt_dir_path, output_metadata_dir_path):
    stemmer = SnowballStemmer('english')
    txt_paths = get_txt_fnames(input_txt_dir_path)
    cycles = []
    counter = 0
    for txt_path in txt_paths:
        txt = get_txtfile_contents(os.path.join(input_txt_dir_path, txt_path))
        '''if article exceeds x words dont bother analysis'''
        if len(txt.split()) < 12500:
            output_path = os.path.join(output_extract_txt_dir_path, txt_path)
            output_stemmed_path = os.path.join(output_stemmed_extract_txt_dir_path, txt_path)
            if not os.path.isfile(output_stemmed_path):
                print(txt_path)
                match, cycle = fetcher(txt)
                cycles.append(cycle)
                match_stemmed = ' '.join([stemmer.stem(word) for word in match.split()])
                output_path = os.path.join(output_extract_txt_dir_path, txt_path)
                output_stemmed_path = os.path.join(output_stemmed_extract_txt_dir_path, txt_path)
                write_txt_file(match, output_path)
                write_txt_file(match_stemmed, output_stemmed_path)
                print('#' + str(counter) + ' of ' + str(len(txt_paths)) + ' extracted.')
                counter += 1
            else:
                print('#' + str(counter) + ' of ' + str(len(txt_paths)) + ' already exists.')
                counter += 1
        else:
            cycles.append('TOO LARGE')
            print('#' + str(counter) + ' of ' + str(len(txt_paths)) + ' TOOLARGE.')
            counter += 1
    dictionary = {
    'article':txt_paths,
    'cycle':cycles
    }
    df = pd.DataFrame(dictionary)
    filename = 'txt_2_extract.xlsx'
    output_path = os.path.join(output_metadata_dir_path, filename)
    df.to_excel(output_path)

txt_2_extracts(input_txt_dir_path, output_extract_txt_dir_path, output_stemmed_extract_txt_dir_path, output_metadata_dir_path)
