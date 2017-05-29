from math import *
#from transform import Transform
from scipy import array
from functools import reduce

class TFIDF:

    delta = 0.005
    min_term_document_occurences = 0.5

    def __init__(self, matrix):
        #Transform.__init__(self, matrix)
        self.matrix = matrix
        self.document_total = len(self.matrix)


    def transform(self):
        """ Apply TermFrequency(tf)*inverseDocumentFrequency(idf) for each matrix element.
        This evaluates how important a word is to a document in a corpus
        With a document-term matrix: matrix[x][y]
        tf[x][y] = frequency of term y in document x / frequency of all terms in document x
        idf[x][y] = log( abs(total number of documents in corpus) / abs(number of documents with term y)  )
        Note: This is not the only way to calculate tf*idf
        """
        matrix1 = array(self.matrix,dtype = float)
        rows,cols = matrix1.shape
        transformed_matrix = matrix1.copy()
        #print(transformed_matrix)

        for row in range(0, rows): #For each document

            word_total = reduce(lambda x, y: x+y, self.matrix[row] )
            word_total = float(word_total)

            for col in range(0, cols): #For each term
                transformed_matrix[row,col] = float(transformed_matrix[row,col])

                if transformed_matrix[row][col] != 0:
                    transformed_matrix[row,col] = self._tf_idf(row, col, word_total)

        #print(word_total)
        #print(transformed_matrix)
        return transformed_matrix


    def _tf_idf(self, row, col, word_total):
        term_frequency = self.matrix[row][col] / float(word_total)   ## Boolean frequencies....can improve(see wiki)
        inverse_document_frequency = log(abs(self.document_total / float(self._get_term_document_occurences(col))))
        # if inverse_document_frequency == 0:
        #     inverse_document_frequency = self.delta
        #print("IDF \n %s" % inverse_document_frequency)
        return term_frequency * inverse_document_frequency


    def _get_term_document_occurences(self, col):
        """ Find how many documents a term occurs in"""

        term_document_occurrences = 0
        matrix1 = array(self.matrix, dtype = float)
        rows, cols = matrix1.shape

        for n in range(0,rows):
            if self.matrix[n][col] > 0: #Term appears in document
                term_document_occurrences +=1
        # if term_document_occurrences == 0:
        #     term_document_occurrences = self.min_term_document_occurences
        return term_document_occurrences