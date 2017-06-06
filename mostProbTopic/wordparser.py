import os
from mostProbTopic.PorterStemmer import PorterStemmer
from mostProbTopic.spelling import *
import os


class Parser:
    #STOP_WORDS_FILE = '%s/../data/english.stop' % os.path.dirname(os.path.realpath(__file__))

    stemmer = None
    stopwords = []
    dir_name = os.path.dirname(os.path.abspath(__file__)) + "\\"

    def __init__(self, stopwords_io_stream=None,keywords=None):
        self.stemmer = PorterStemmer()

        if (not stopwords_io_stream):
            file_name = dir_name + "stop.txt"
            stopwords_io_stream = open(file_name, 'r')

        if (not keywords):
            file_name = dir_name + "donot.txt"
            keywords = open(file_name,'r')

        self.keywords_list = keywords.read().split()

        self.stopwords = stopwords_io_stream.read().split()

    def tokenise_and_remove_stop_words(self, document_list):
        if not document_list:
            return []

        vocabulary_string = " ".join(document_list)
        #vocabulary_string = document_list

        tokenised_vocabulary_list = self._tokenise(vocabulary_string)
        #print(tokenised_vocabulary_list)
        clean_word_list = self._remove_stop_words(tokenised_vocabulary_list)
        clean_word_list = self._stem(clean_word_list)
        return clean_word_list
        #return tokenised_vocabulary_list

    def _remove_stop_words(self, list):
        """ Remove common words which have no search value """
        return [word for word in list if word not in self.stopwords]

    def _tokenise(self, string):
        """ break string up into tokens and stem words """
        string = self._clean(string)
        #print(string)
        words = string.split()
        #print(words)
        #words = [correct(word) for word in words]
        return [correct(word) if word not in self.keywords_list else word for word in words]

    def _stem(self, words):
        """ break string up into tokens and stem words """
        #string = self._clean(string)
        #print(string)
        #words = string.split()
        #print(words)
        #words = [correct(word) for word in words]
        return [self.stemmer.stem(word, 0, len(word) - 1) if word not in self.keywords_list else word for word in words]

    def _clean(self, string):
        """ remove any nasty grammar tokens from string """
        string = string.replace(".", "")
        string = string.replace("?", "")
        string = string.replace(",", "")
        string = string.replace(";", "")
        string = string.replace("-", " ")
        string = string.replace("\s+", " ")
        string = string.lower()
        return string