__authors__ = ['1668213','1665951','1668826']
__group__ = 'noneyet'

import numpy as np
import utils


class KMeans:

    def __init__(self, X, K=1, options=None):
        """
         Constructor of KMeans class
             Args:
                 K (int): Number of cluster
                 options (dict): dictionary with options
            """
        self.num_iter = 0
        self.K = K
        self._init_X(X)
        self._init_options(options) # DICT options
        self.centroids = 0
        self.old_centroids = 0

    def _init_X(self, X):
       """Initialization of all pixels, sets X as an array of data in vector form (PxD)
            Args:
                X (list or np.array): list(matrix) of all pixel values
                    if matrix has more than 2 dimensions, the dimensionality of the sample space is the length of
                    the last dimension
        """

       if isinstance(X, float) is False:
            # Si X NO es float la convertimos en float y almacenamos el valor en self.X
            self.X = X.astype(np.float64)
       if len(X[0]) != 3:
            # Si X no tiene 3 columnas (para r, g y b) se calcula el número de filas (val) y se
            # cambia el tamaño de la matriz X por el de val x 3
            val = np.int64(np.divide(np.size(self.X), 3))
            self.X = np.reshape(self.X, (val, 3))

    def _init_options(self, options=None):
        """
        Initialization of options in case some fields are left undefined
        Args:
            options (dict): dictionary with options
        """
        if options is None:
            options = {}
        if 'km_init' not in options:
            options['km_init'] = 'first'
        if 'verbose' not in options:
            options['verbose'] = False
        if 'tolerance' not in options:
            options['tolerance'] = 0
        if 'max_iter' not in options:
            options['max_iter'] = np.inf
        if 'fitting' not in options:
            options['fitting'] = 'WCD'  # within class distance.

        # If your methods need any other parameter you can add it to the options dictionary
        self.options = options

    def _init_centroids(self):
        """
        Initialization of centroids
        """
        self.old_centroids = np.empty([self.K, 3])
        self.centroids = np.empty([self.K, 3])
        self.centroids[0] = self.X[0]
        
        #first = 0, random = 1, custom = 2
        opcion = np.dtype(np.int64)
        if self.options['km_init'].lower() == 'first':
            opcion = 0
            
        elif self.options['km_init'].lower() == 'random':
            opcion = 1
        
        else:
            opcion = 2
        
        #"swich-case"
        if opcion == 0: #case first
            i = 0
            for casilla in self.X:
                if i == self.K:
                    break
                
                is_centroid = any((casilla == element).all() for element in self.centroids[:i])
                
                if not is_centroid:
                    self.centroids[i] = casilla
                    i = np.add(i, 1)

        elif opcion == 1: #case random
            i = 0
            while i != self.K:
                np.random.seed()
                aux = np.random.randint(low = 0, high = len(self.X) - 1)
                is_centroid = any((self.X[aux] == element).all() for element in self.centroids[:i])
                
                if not is_centroid:
                    self.centroids[i] = self.X[aux]
                    i = np.add(i, 1)
                
        elif opcion == 2: #case custom
            i = 0
            for casilla in reversed(self.X):
                if i == self.K:
                    break
                
                is_centroid = any((casilla == element).all() for element in self.centroids[:i])
                
                if not is_centroid:
                    self.centroids[i] = casilla
                    i = np.add(i, 1)
    
    def get_labels(self):
        """
        Calculates the closest centroid of all points in X and assigns each point to the closest centroid
        """
        self.labels = np.argmin(distance(self.X, self.centroids), axis = 1)

    def get_centroids(self):
        """
        Calculates coordinates of centroids based on the coordinates of all the points assigned to the centroid
        """ 
        self.old_centroids = np.array(self.centroids, copy = True)

        for k in range(len(self.centroids)):
            puntos_centroides = np.where(self.labels == k)[0]
            centroides = self.X[puntos_centroides]
            self.centroids[k] = np.mean(centroides, axis = 0)

    def converges(self):
        """
        Checks if there is a difference between current and old centroids
        """
        return np.allclose(self.old_centroids, self.centroids, rtol = self.options['tolerance'])

    def fit(self):
        """
        Runs K-Means algorithm until it converges or until the number of iterations is smaller
        than the maximum number of iterations.
        """
        self._init_centroids()
        while not self.converges() and self.num_iter < self.options['max_iter']:
            self.get_labels()
            self.get_centroids()
            self.num_iter = np.add(self.num_iter, 1)

    def withinClassDistance(self):
        """
         returns the within class distance of the current clustering
        """
        aux = np.divide(1, len(self.X))
        return np.multiply(aux, sum(np.square(np.amin(distance(self.X, self.centroids), axis = 1))))

    def interClassDistance(self):
        suma = 0

        for i in range(len(self.centroids)):
            for j in range(i + 1, len(self.centroids)):
                suma += np.mean(np.square(self.centroids[i] - self.centroids[j]))

        return suma

    
    def fisher(self):
        intraClassDist = self.withinClassDistance()
        interClassDist = self.interClassDistance()
        return np.divide(intraClassDist, interClassDist)

    def find_bestK(self, max_K):
        """
         sets the best k analysing the results up to 'max_K' clusters
        """
        self.K = 2
        self.fit()
        WCD = self.withinClassDistance()
        #WCD = self.interClassDistance()
        #WCD = self.fisher()
        for k in range(3, max_K):
            self.K = k
            self.fit()
            
            WCD_Ant = WCD
            WCD = self.withinClassDistance()
            #WCD = self.interClassDistance()
            #WCD = self.fisher()
            porcentaje = np.multiply(100, np.divide(WCD, WCD_Ant))
            
            if np.subtract(100, porcentaje) < 20:
                self.K = np.subtract(self.K, 1)
                self.fit()
                break    


def distance(X, C):
    """
    Calculates the distance between each pixel and each centroid
    Args:
        X (numpy array): PxD 1st set of data points (usually data points)
        C (numpy array): KxD 2nd set of data points (usually cluster centroids points)

    Returns:
        dist: PxK numpy array position ij is the distance between the
        i-th point of the first set an the j-th point of the second set
    """
    #d = √((x₂ – x₁)² + (y₂ – y₁)² + (z₂ – z₁)² +…)
    red = np.square(np.subtract(X[:, 0, np.newaxis], C[:, 0]))   #(x₂ – x₁)²
    green = np.square(np.subtract(X[:, 1, np.newaxis], C[:, 1])) #(y₂ – y₁)²
    blue = np.square(np.subtract(X[:, 2, np.newaxis], C[:, 2]))  #(z₂ – z₁)²
    rgb = np.add(red, np.add(green, blue))
    return np.sqrt(rgb)

def get_colors(centroids):
    """
    for each row of the numpy matrix 'centroids' returns the color label following the 11 basic colors as a LIST
    Args:
        centroids (numpy array): KxD 1st set of data points (usually centroid points)

    Returns:
        labels: list of K labels corresponding to one of the 11 basic colors
    """
    prob = utils.get_color_prob(centroids)
    colors = np.empty(len(centroids), dtype = object) 
    for c in range(len(centroids)):
        colors[c] = utils.colors[np.argmax(prob[c])] #argmax agafa el primer en cas d'empat
    return colors
