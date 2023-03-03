'''
Luc Hampsink            8980713
Siebe Tolsma            9829261
Tsjerk Piter Walinga    0962414

match_language.py is a program that compares given files to language profiles. and returns the language of the file.
'''

import os
import sys
import langdetect


class MatchLang:
    '''
    language matcher class for a single ngram size and max size
    contains functions to match a file to a language
    '''
    def __init__(self, lang_dir):
        '''
        initialize language matcher
        lang_dir is the path to the directory containing the multilingual reference corpus
        reads ngram table for each language
        '''
        self.lang_dir = lang_dir
        self.lang_dict = {}
        # read ngram files of each language
        for lang in os.listdir(lang_dir):
            self.lang_dict[lang] = langdetect.read_ngrams(lang_dir + '/' + lang)

    def score(self, text, k_best=1):
        '''
        scores text against all languages
        returns a dictionary of languages and scores
        k_best is the number of languages to return
        '''
        filename = os.path.basename(self.lang_dir)
        # part before the hyphen is the language name. 
        # The part after the hyphen is the encoding.
        nAndMaxsize = filename.split('-')
        n = int(nAndMaxsize[0])
        maxsize = int(nAndMaxsize[1])
        # create ngram table
        ngram_table = langdetect.ngram_table(text, n, maxsize)
        scores = {}
        # calculate scores for each language
        for lang in self.lang_dict:
            scores[lang] = langdetect.cosine_similarity(self.lang_dict[lang], ngram_table)
        # sort by score
        sorted_scores = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return dict(sorted_scores[:k_best])

    def recognize(self, filename, encoding="utf-8"):
        '''
        recognize language of file
        '''
        with open(filename, encoding=encoding) as f:
            text = f.read()
        return self.score(text)


if __name__ == "__main__":
    '''
    if run as a script, run the language matcher on the given files
    
    accept 2 or more command line arguments
    1st argument: language directory, rest are filenames for text to be recognized
    '''
    if len(sys.argv) < 2:
        print("Usage: python3 match_language.py <lang_dir> <filename> [<filename> ...]")
        sys.exit(1)
    lang_dir = sys.argv[1]
    matcher = MatchLang(lang_dir)
    # all files after the first argument are filenames for text to be recognized
    for filename in sys.argv[2:]:
        match = matcher.recognize(filename)
        print(os.path.basename(filename),list(match)[0] ,match[max(match, key=match.get)])