'''
Luc Hampsink            8980713
Siebe Tolsma            9829261
Tsjerk Piter Walinga    0962414

evaluate.py is a program that evaluates the model on the given test data using the given model path
when run as a script, it will evaluate on the test data with bigram and trigram models
'''

import match_language
import os

languages = {
    "da": "Danish",
    "de": "German",
    "el": "Greek",
    "en": "English",
    "es": "Spanish",
    "fi": "Finnish",
    "fr": "French",
    "it": "Italian",
    "nl": "Dutch",
    "pt": "Portuguese",
    "sv": "Swedish"
    }

def eval(model_path, test_path):
    '''
    evaluate the model on the test data using the given model path
    prints file name, language, and Error + actual language if the language is not correct
    prints the amount of correct and incorrect matches for the dataset
    '''

    matcher = match_language.MatchLang(model_path)

    correct, incorrect = 0, 0

    # loop through all files in test_path and compare to the guess with the known language
    for file in os.listdir(test_path):
        matched_language = list(matcher.recognize(os.path.join(test_path, file)).keys())[0]

        if matched_language == languages[file[-2:]]:
            print(file + ' ' + matched_language)
            correct += 1
        else:
            print(file + ' ' + matched_language + " ERROR " + languages[file[-2:]])
            incorrect += 1

    # print bigram results
    if model_path.split("/")[1][0] == '2':
        print("Bigram models for " + test_path[-2:] + "-word sentences: " + str(correct) 
                + " correct, " + str(incorrect) + " incorrect")
    # print trigram results
    elif model_path.split("/")[1][0] == '3':
        print("Trigram models for " + test_path[-2:] + "-word sentences: " 
                + str(correct) + " correct, " + str(incorrect) + " incorrect")
    # print other ngram results
    else:
        print(model_path.split("/")[1][0] + "-gram models for " + test_path[-2:] + "-word sentences: " 
                + str(correct) + " correct, " + str(incorrect) + " incorrect")

if __name__ == "__main__":
    '''
    if running this file directly, run the evaluation on the test data with bigram and trigram models
    '''
    eval('models/2-200', 'datafiles/test/europarl-10')
    eval('models/3-200', 'datafiles/test/europarl-10')
    eval('models/2-200', 'datafiles/test/europarl-30')
    eval('models/3-200', 'datafiles/test/europarl-30')
    eval('models/2-200', 'datafiles/test/europarl-90')
    eval('models/3-200', 'datafiles/test/europarl-90')