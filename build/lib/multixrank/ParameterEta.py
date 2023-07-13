#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np


class ParameterEta(object):
    """

	The aim of this class is to determine the value of eta
        for a homogeneneous exploration of the system of multiplexes.

	"""

    def __init__(self, n: int, alpha: list):
        """

    	Args :
    	    n (int) : Number of multiplex in the system

            alpha (list) : List of number of seeds for each multiplex

    	"""

        self.n = n
        self.alpha = alpha
        self.size = (self.n - self.alpha.count(0))
        self.X = np.zeros(n)

    def matrix_A(self) -> np.ndarray:
        """

    	method to determine the matrix A of the linear system to solve in order
        to determine the value of tau for homogeneous exploration.
        This matrix take all the constraints on parameters.
        X = A^{1}*Y

        Returns :
        	A (np.ndarray) : Matrix A of linear system.

    	"""

        A = np.zeros((self.size, self.size))
        A[0, :] = np.ones(self.size)
        index = [idx for idx, val in enumerate(self.alpha) if val != 0]
        for i in range(1, self.size):
            for j in range(1, self.size):
                if (i == j):
                    A[i, 0] = self.alpha[index[0]]
                    A[i, j] = -self.alpha[index[i]]
        return A

    def vect_Y(self) -> np.ndarray:
        """

    	Other part of the linear system to determine the value of parameters.
        X = A^{1}*Y

        Returns :
        	Y (np.ndarray) : Vector Y of linear system.

    	"""

        Y = np.zeros(self.size)
        Y[0] = 1
        return Y

    def vect_X(self) -> np.ndarray:
        """

    	Vector of value of eta determine by the solution of linear system.
        X = A^{1}*Y

        Returns :
        	X (np.ndarray) : Vector of value of eta for homogeneous exploration,
                solution of the linear system.

    	"""

        index = [idx for idx, val in enumerate(self.alpha) if val != 0]
        if (self.alpha.count(0) != self.n - 1):
            A_inverse = np.linalg.inv(self.matrix_A())
            temp = np.dot(A_inverse, self.vect_Y())
            for k in range(self.size):
                self.X[index[k]] = temp[k]
        else:
            self.X = np.array(self.alpha)
            self.X[index] = 1
        return self.X
