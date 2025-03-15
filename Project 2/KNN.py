__authors__ = ['1668213','1665951','1668826']
__group__ = 'noneyet'

import numpy as np
import math
import operator
from scipy.spatial.distance import cdist


class KNN:
    def __init__(self, train_data, labels):
        self._init_train(train_data)
        self.labels = np.array(labels)

    def _init_train(self, train_data):
        """
        initializes the train data
        :param train_data: PxMxNx3 matrix corresponding to P color images
        :return: assigns the train set to the matrix self.train_data shaped as PxD (P points in a D dimensional space)
        """
        if not isinstance(train_data, float):
            self.train_data = train_data.astype(np.float64)
        
        N = len(train_data)
        dim = train_data[0].size
        self.train_data = np.reshape(train_data,(N, dim))

    def get_k_neighbours(self, test_data, k):
        """
        given a test_data matrix calculates de k nearest neighbours at each point (row) of test_data on self.neighbors
        :param test_data: array that has to be shaped to a NxD matrix (N points in a D dimensional space)
        :param k: the number of neighbors to look at
        :return: the matrix self.neighbors is created (NxK)
                 the ij-th entry is the j-th nearest train point to the i-th test point
        """
        if not isinstance(test_data, float):
            test_data = test_data.astype(np.float64)
       
        N = len(test_data)
        dim = test_data[0].size
        test_data = np.reshape(test_data,(N, dim))

        dist = cdist(test_data, self.train_data) # euclidiana
        #dist = cdist(test_data, self.train_data, 'cityblock') # manhattan
        #dist = cdist(test_data, self.train_data, 'minkowski') # minkowski
        indices_ordenados = np.argsort(dist)
        self.neighbors = self.labels[indices_ordenados[:,:k]]

    def get_class(self):
        """
        Get the class by maximum voting
        :return: 1 array of Nx1 elements. For each of the rows in self.neighbors gets the most voted value
                (i.e. the class at which that row belongs)
        """  
        mas_votados = []

        for vecino in self.neighbors:
            contador_max = 0

            for elemento in vecino:
                contador = 0
                
                for elementoAux in vecino:
                    
                    if elemento == elementoAux:
                        contador += 1
                        
                if contador > contador_max:
                    contador_max = contador
                    mas_votado = elemento
                    
            mas_votados.append(mas_votado)

        return np.array(mas_votados)
      
    
    def predict(self, test_data, k):
        """
        predicts the class at which each element in test_data belongs to
        :param test_data: array that has to be shaped to a NxD matrix (N points in a D dimensional space)
        :param k: the number of neighbors to look at
        :return: the output form get_class a Nx1 vector with the predicted shape for each test image
        """
        self.get_k_neighbours(test_data, k)
        return self.get_class()
