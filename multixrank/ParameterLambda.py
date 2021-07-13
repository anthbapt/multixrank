#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np


class ParameterLambda(object):
    """

	The aim of this class is to determine the value of lambda
        for a homogeneneous exploration of the system of multiplexes.


	"""

    def __init__(self, n: int, N: list):
        """

    	Args :
    		n (int) : Number of multiplex in the system

    		N (list) : List of number of layers in each multiplexes

    	"""

        self.n = n
        self.N = 1 / np.array(N)
        self.X = np.zeros((n, n))

    def block(self, compt: int) -> np.ndarray:
        """

    	method to determine sub-blocks of the matrix A.

    	"""

        T = np.zeros((self.n - 1, self.n))
        compt2 = -1
        for i in range(self.n):
            for j in range(self.n):
                if (j == compt):
                    T[i - 1, j] = self.N[compt]
                    compt2 += 1
                else:
                    if (j == compt2):
                        T[i - 1, j] = -self.N[compt2]
        return T

    def matrix_A(self) -> np.ndarray:
        """

    	method to determine the matrix A of the linear system to solve in order
    	to determine the value of lambda for homogeneous exploration.
        This matrix take all the constraints on parameters and sub-blocks are
        determine with the function block().
        X = A^{1}*Y

    	"""

        A = np.zeros((self.n ** 2, self.n ** 2))
        for i in range(self.n):
            A[i, self.n * i:self.n * (i + 1)] = np.ones(self.n)
        compt = 0
        start = self.n
        for i in range(1, self.n + 1):
            T = self.block(compt)
            end = start + self.n - 1
            A[start:end, self.n * compt:self.n * (compt + 1)] = T
            compt += 1
            start = end
        # print(A)
        return A

    def vect_Y(self) -> np.ndarray:
        """

    	Other part of the linear system to determine the value of parameters.
        X = A^{1}*Y

    	"""

        a = np.ones(self.n)
        b = np.zeros(self.n * (self.n - 1))
        Y = np.concatenate((a, b), axis=None)
        return Y

    def vect_X(self) -> np.ndarray:
        """

    	Vector of value of lambda determine by the solution of linear system.
        X = A^{1}*Y

    	"""

        A_inverse = np.linalg.inv(self.matrix_A())
        temp_X = np.dot(A_inverse, self.vect_Y())
        return temp_X

    def matrix_X(self) -> np.ndarray:
        """

    	Reshape of the vector of value of lambda, solution of linear system.
        Vector of size n**2 become a square matrix of size n*n.

    	"""

        temp_X = self.vect_X()
        compt = 0
        for i in range(self.n):
            for j in range(self.n):
                self.X[j, i] = temp_X[compt]
                compt += 1
        return self.X

