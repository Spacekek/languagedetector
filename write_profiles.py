'''
Luc Hampsink            8980713
Siebe Tolsma            9829261
Tsjerk Piter Walinga    0962414

write_profiles.py is a program that creates ngram profiles for each language in path.
when run as a script, it will create bigram and trigram profiles for each language in training data.
'''

import langdetect
import os


def make_profiles(path, n, max_size):
    '''
    Creates ngram profiles for each language in path.
    n is ngram size
    max_size is max size of ngram tables
    path is the path to the directory containing the multilingual reference corpus
    if directory ./models/<n>-<limit>/ is not present, it will be created
    '''
    if not os.path.exists("./models/"):
        os.mkdir("./models/")
    if not os.path.exists("./models/" + str(n) + '-' + str(max_size) + '/'):
        os.mkdir("./models/" + str(n) + '-' + str(max_size) + '/')
    # The part before the hyphen is the language name. The part after the hyphen is the encoding.
    for file in os.listdir(path):
        encoding = file.split('-')[1]
        language = file.split('-')[0]
        # read the file
        file = open(path + file, 'r', encoding=encoding)
        text = file.read()
        ngram_table = langdetect.ngram_table(text, n, max_size)
        file.flush()
        # write the file
        langdetect.write_ngrams(ngram_table, "./models/" + str(n) + '-' 
                                + str(max_size) + '/' + language)


if __name__ == "__main__":
    '''
    running this as a script will create bigram and trigram profiles for each language in training data.
    '''
    make_profiles("datafiles/training/", 3, 200)
    make_profiles("datafiles/training/", 2, 200)
