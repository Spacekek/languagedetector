'''
Luc Hampsink            8980713
Siebe Tolsma            9829261
Tsjerk Piter Walinga    0962414

langdetect.py is a program that contains functions to prepare text for ngrams, create ngram tables, read ngram tables from files,
write ngram tables to files, and calculate the cosine similarity between two ngram tables.
'''

def prepare(text):
    '''
    prepare text for ngrams
    removes punctuation and invisible characters
    splits text into words
    returns list of words
    '''

    #list of all characters to be removed
    char_list = ["!", "?", "\"", ".", ",", "(", ")", "<", ">", "\n", "\r"]

    #remove all characters in char_list from text
    for char in char_list:
        text = text.replace(char, "")
    
    # list of all invisible characters
    invisible = [u"\u0009", u"\u00A0", u"\u034F", u"\u00AD", u"\u061C", 
                u"\u115F", u"\u1160", u"\u17B4", u"\u17B5", u"\u180E", 
                u"\u2000", u"\u2001", u"\u2002", u"\u2003", u"\u2004", 
                u"\u2005", u"\u2006", u"\u2007", u"\u2008", u"\u2009", 
                u"\u200A", u"\u200B", u"\u200C", u"\u200D", u"\u200E", 
                u"\u200F", u"\u202F", u"\u205F", u"\u2060", u"\u2061", 
                u"\u2062", u"\u2063", u"\u2064", u"\u206A", u"\u206B", 
                u"\u206C", u"\u206D", u"\u206E", u"\u206F", u"\u3000", 
                u"\u2800", u"\u3164", u"\uFEFF", u"\uFFA0", u"\u1D159", 
                u"\u1D173", u"\u1D174", u"\u1D175", u"\u1D176", u"\u1D177", 
                u"\u1D178", u"\u1D179", u"\u1D17A"]

    # replace invisible characters with space
    for i in invisible:
        text = text.replace(i, " ")

    # split text into words
    text_split = text.split(" ")

    # Remove empty strings and spaces
    text_split = [x for x in text_split if x != ' ' and x != '']
    return text_split


def ngrams(seq, n=3):
    '''
    Generate ngrams from sequence.
    '''
    ngram_list = []
    for i in range(len(seq) - n + 1):
        ngram_list.append(seq[i:i+n])
    return ngram_list


def ngram_table(text, n=3, limit=0):
    '''
    Generate ngram table from text.
    '''
    text = prepare(text)
    text = ["<" + x + ">" for x in text]
    ngrams_List = []
    for i in range(len(text)):
        ngrams_List.extend(ngrams(text[i], n))
    ngrams_dict = dict.fromkeys(ngrams_List, 0)
    # Count ngrams.
    for ngram in ngrams_List:
        ngrams_dict[ngram] += 1
    # Sort ngrams by frequency.
    ngrams_dict = sorted(ngrams_dict.items(), key=lambda x: x[1])
    # Limit ngrams.
    if limit > 0:
        ngrams_dict = ngrams_dict[-limit:]
    return dict(ngrams_dict)


def read_ngrams(filename):
    '''
    Reads ngrams from file.
    returns dictionary of ngrams with frequency
    '''
    with open(filename, 'r', encoding="utf-8") as f:
        ngrams_list = f.readlines()
    ngrams_list = [x.split() for x in ngrams_list]
    ngrams_words = [x[1] for x in ngrams_list]
    ngrams_freqs = [int(x[0]) for x in ngrams_list]
    ngrams_dict = dict(zip(ngrams_words, ngrams_freqs))
    return ngrams_dict


def write_ngrams(table, filename):
    '''
    Writes ngram table to file.
    '''
    with open(filename, 'w', encoding="utf-8") as f:
        for ngram in table:
            f.write(str(table[ngram]) + ' ' + ngram + '\n')


def cosine_similarity(known, unknown):
    '''
    Calculates cosine similarity between two ngram tables.
    '''
    known_words = list(known.keys())
    unknown_words = list(unknown.keys())
    known_freqs = list(known.values())
    unknown_freqs = list(unknown.values())
    magnitude_known = 0
    magnitude_unknown = 0

    # Calculate magnitude of known ngrams.
    for i in range(len(known_freqs)):
        magnitude_known += known_freqs[i] ** 2
    for i in range(len(unknown_freqs)):
        magnitude_unknown += unknown_freqs[i] ** 2

    magnitude_known = magnitude_known ** 0.5
    magnitude_unknown = magnitude_unknown ** 0.5
    similarity = 0

    # Calculate similarity.
    for i in range(len(known_words)):
        for j in range(len(unknown_words)):
            if known_words[i] == unknown_words[j]:
                similarity += known_freqs[i] * unknown_freqs[j]
    similarity = similarity / (magnitude_known * magnitude_unknown)
    return similarity
