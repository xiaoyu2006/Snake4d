# -*- coding: utf-8 -*-
"""
Created on Fri May 18 20:44:22 2018

@author: Mauro
"""

#==============================================================================
# Matrix class
#   utilities for an nxm 2D matrix
#==============================================================================

# errors
class MatExcept(Exception):
    pass

# class
class Matrix:
    ''' MxN matrix class
    - can be initializated with aa nested list or with sizes
    - item setters and getters throw MathException
    - implemented:
        - operator +
        - operator -
        - operator *
    - can multy by scalar
    - can be transposed
    - cam be printed
    '''
    
    def __init__(self, m, n = None):
        # store matrix in a linear vector
        self.mat = []
        
        # if the first argument is a list and is a list of list
        # construct the matrix starting with that as an element
        if type(m) == list and type(m[0]) is list and n is None:
            self.m = len(m)
            self.n = len(m[0])
            
            self.init_mat()
            for i in range(self.m):
                for j in range(self.n):
                    self[i, j] = m[i][j]
        
        # if the first argument is a list, yet not a list of list
        # assume the user wants to create a mx1 vector
        elif type(m) is list and n is None:
            self.m = len(m)
            self.n = 1
            
            self.init_mat()
            for i in range(self.m):
                self[i, 0] = m[i]
                
        # else initialize a 0ed mxn matrix
        else:
            self.m = m
            self.n = n
            self.init_mat()

    def init_mat(self):
        for i in range(self.m):
            for j in range(self.n):
                self.mat.append(0)        
    
    # getter    
    def __getitem__(self, idx):
        linear_index = idx[1] * self.m + idx[0]      
        return self.mat[linear_index]
    
    # setter
    def __setitem__(self, idx, c):
        if idx[0] >= self.m or idx[0] < 0: raise MatExcept("Matrix: row out of range")
        if idx[1] >= self.n or idx[1] < 0: raise MatExcept("Matrix: col out of range")        
        
        linear_index = idx[1] * self.m + idx[0]
        self.mat[linear_index] = c
     
    # operator + elementwise sum
    def __add__(self, m2):
        if self.m == m2.m and self.n == m2.n:
            new_mat = []
            for i in range(len(self.mat)):
                new_mat.append(self.mat[i] + m2.mat[i])
            
            mnew = Matrix(self.m, self.n)
            mnew.mat = new_mat
            return mnew
            
        else:
            raise MatExcept("Matrix: addition matrices not same size")
    
    # operator - elementwise
    def __sub__(self, m2):
        if self.m == m2.m and self.n == m2.n:
            new_mat = []
            for i in range(len(self.mat)):
                new_mat.append(self.mat[i] - m2.mat[i])
            
            mnew = Matrix(self.m, self.n)
            mnew.mat = new_mat
            return mnew
            
        else:
            raise MatExcept("Matrix: subtraction matrices not same size") 
    
    # matrix multiplication
    def __mul__(self, m2):
        if self.n == m2.m:
            mulmat = Matrix(self.m, m2.n)
            for i in range(mulmat.m):
                for j in range(mulmat.n):
                    for m in range(self.n):
                        mulmat[i, j] += self[i, m] * m2[m, j]
            return mulmat       
        else:
            raise MatExcept("Matrix: multiplication matrix columns different then other matrix rows")
    
    def scalar(self, k):
        mat_new = []
        for m in self.mat:
            mat_new.append(m * k)
        
        mres = Matrix(self.m, self.n)
        mres.mat = mat_new
        
        return mres
    
    def transpose(self):
        tmat = Matrix(self.n, self.m)
        
        for i in range(self.m):
            for j in range(self.n):
                tmat[j, i] = self[i, j]
        return tmat
            
    
    def __str__(self):
        s = ""
        for i in range(self.m):
            for j in range(self.n):
                
                s += str(self[i, j]) + " "
            s += "\n"
        
        return s

#==============================================================================
# Squared Matrix utilities
#   for a squared matrix (mxm)
#==============================================================================

class SquareMatrix(Matrix):
    
    def __init__(self, m):
        if type(m) is list:
            if len(m) != len(m[0]): raise MatExcept("SqMat: Not a square matrix")
            super().__init__(m)
        else:
            super().__init__(m, m)
    
    def is_diagonal(self):
        for i in range(self.m):
            for j in range(self.n):
                if i == j and self[i, j] == 0:
                    return False
                
                if i != j and self[i, j] != 0:
                    return False
        return True
    
    def is_lower_triangular(self):
        for i in range(self.m):
            for j in range(self.n):
                if j <= i and self[i, j] == 0:
                    return False
                
                if j > i and self[i, j] != 0:
                    return False
        return True
        
    def is_upper_triangular(self):
        for i in range(self.m):
            for j in range(self.n):
                if i <= j and self[i, j] == 0:
                    return False
                
                if i > j and self[i, j] != 0:
                    return False
        return True
    
    def get_identity(self):
        
        imatrix = SquareMatrix(self.m)
        for i in range(self.m):
            imatrix[i, i] = 1
            
        return imatrix

if __name__ == "__main__":

    print("Test size initialization")
    m = Matrix(2, 3)
    print(m)
    
    print ("Test list initialization")
    
    m_ini = [ [2, 3, 4],
              [1, 0, 0] ]
    
    m = Matrix(m_ini)
    
    print(m)
    
    print("Test setter")
    m[1, 2] = 1
    print(m)
    
    print("Test transpose")
    
    m2 = Matrix(2, 3)
    m2[1, 2] = 3
    print(m2)
    print(m2.transpose())
    
    print("Test addition and scalar multiplication")
    print("m + m2*4")
    
    print(m + m2.scalar(4))
    
    print("Test multiplication")
    
    m1 = Matrix(2, 3)
    m1[0, 0] = 2
    m1[0, 1] = 3
    m1[0, 2] = 4
    m1[1, 0] = 1
    
    print(m1)
    
    m2 = Matrix(3, 2)
    m2[0, 1] = 1000
    m2[1, 0] = 1
    m2[1, 1] = 100
    m2[2, 1] = 10
    print(m2)
    
    print("m1 * m2")
    
    print(m1 * m2)
    
    print("m1 and m2")
    
    m1 = [ [1, 2],
           [3, 4] ]
    m1 = Matrix(m1)
    
    print(m1)
    
    m2 = [ [0, 1],
           [0, 0] ]
    m2 = Matrix(m2)
    
    print(m2)
    
    mres = m1 * m2
    print(mres)
    
    print("m1 * m2")
    
    mres = m2 * m1
    print(mres)
    

    
    print("Test square matrix")
    
    m = [ [1, 1, 1],
          [0, 1, 1],
          [0, 0, 1] ]
    
    m = SquareMatrix(m)
    
    print(m)
    print("Is diagonal, is lower, is upper triangular")
    print(m.is_diagonal())
    print(m.is_lower_triangular())    
    print(m.is_upper_triangular()) 
    
    print()

    print("Test identity")
    print(m.get_identity())    
    
    
    
    
    
    