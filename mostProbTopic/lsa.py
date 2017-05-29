from numpy import dot,matrix
from scipy import linalg,array

#from transform import Transform

#class LSA(Transform):
class LSA:


    def __init__(self,matrix):
        self.matrix = matrix

    """ Latent Semantic Analysis(LSA).
        Apply transform to a document-term matrix to bring out latent relationships.
        These are found by analysing relationships between the documents and the terms they 
        contain.
    """

    def transform(self, dimensions=1):
        """ Calculate SVD of objects matrix: U . SIGMA . VT = MATRIX
            Reduce the dimension of sigma by specified factor producing sigma'. 
            Then dot product the matrices:  U . SIGMA' . VT = MATRIX'
            AP : Do change the dimensions to reduce sigma further by more than 1 dimension
        """

        # print("Okay1")
        matrix1 = array(self.matrix, dtype=float)
        rows,cols = matrix1.shape
        # print(rows)
        if dimensions <= rows: #Its a valid reduction

            #print(self.matrix)
            #self.matrix = self.matrix.transpose()
            #Sigma comes out as a list rather than a matrix
            u,sigma,vt = linalg.svd(self.matrix)
            # print(len(sigma))
            #Dimension reduction, build SIGMA'
            # if rows > 1:
            for index in range(rows - dimensions, rows):
            # for index in range(len(sigma) - dimensions, len(sigma)):
                sigma[index] = 0

            #Reconstruct MATRIX'
            transformed_matrix = dot(dot(u, linalg.diagsvd(sigma, len(self.matrix), len(vt))) ,vt)
            # print(u)
            # print(len(u))
            # print(vt)
            # print(len(vt))
            # print(sigma)

            return transformed_matrix

        else:
            print("dimension reduction cannot be greater than %s" % rows)