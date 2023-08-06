import random as rd
import copy

class Matrix:
    def __init__(self, value = [[]], random = False, max_rand = 10, dims = (1,1)):
        '''
        Initializes the matrix
        '''
        self.dims = dims
        if random:
            self.value = [[rd.randint(0, max_rand) for j in range(dims[1])] for i in range(dims[0])]
        else:
            self.value = list.copy(value)
            self.dims = (len(self.value), len(self.value[0]))
    
    def changeValues(self, value):
        '''
        Changes the value of the matrix
        '''
        self.value = value
        self.dims = (len(value), len(value[0]))
    
    def __eq__(self, other):
        '''
        Overloads the eq operator
        '''
        if self.dims != other.dims:
            return False
        for i in range(self.dims[0]):
            for j in range(self.dims[1]):
                if self.value[i][j]!=other.value[i][j]:
                    return False
        return True
    
    def __add__(self, other):
        '''
        Overloads the add operator
        '''
        assert(self.dims == other.dims)
        addition_values = [[self.value[i][j] + other.value[i][j] for j in range(self.dims[1])] for i in range(self.dims[0])]
        return Matrix(value = addition_values)
    
    def __repr__(self):
        '''
        Overloads the repr operator
        '''
        res = "["
        for i in range(self.dims[0]):
            res+="["
            for j in range(self.dims[1]):
                res+=str(self.value[i][j])
                if j < self.dims[1]-1:
                    res+=", "
            if i < self.dims[0]-1:
                res+="],\n"
            else:
                res+="]"
        res+="]"
        return res
    
    def __neg__(self):
        '''
        Overloads the neg operator
        '''
        negative = [[-self.value[i][j] for j in range(self.dims[1])] for i in range(self.dims[0])]
        return Matrix(value = negative)
    
    def __sub__(self, other):
        '''
        Overloads the sub operator
        '''
        return self + (-other)
    
    def __mul__(self, other):
        '''
        Overloads the mul operator to have an element wise multiplication
        '''
        assert(self.dims == other.dims)
        multiplication_values = [[self.value[i][j] * other.value[i][j] for j in range(self.dims[1])] for i in range(self.dims[0])]
        return Matrix(value = multiplication_values)
    
    def get(self, i, j):
        return self.value[i][j]
    
    def coef_dot_product(self, B, i, j):
        res = 0
        for k in range(self.dims[1]):
            res+=self.get(i,k)*B.get(k,j)
        return res
    
    def dot(self, other):
        '''
        Implements the matrix multiplication
        '''
        assert(self.dims[1] == other.dims[0])
        m = self.dims[1]
        dot_product = [[self.coef_dot_product(other, i, j) for j in range(other.dims[1])] for i in range(self.dims[0])]
        return Matrix(value = dot_product)
    
    def transpose(self):
        transpose_value = [[self.value[j][i] for j in range(self.dims[1])] for i in range(self.dims[0])]
        return Matrix(value = transpose_value)
    
    def positive_power(self, n):
        assert(n>=0)
        assert(self.dims[0]==self.dims[1])
        if n == 0:
            identity = [[0 for j in range(self.dims[1])] for i in range(self.dims[0])]
            for i in range(self.dims[0]):
                identity[i][i]=1
            return Matrix(value = identity)
        res = copy.copy(self)
        for i in range(n-1):
            res = res.dot(self)
        return res
            
            
        