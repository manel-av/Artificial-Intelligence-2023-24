# This file contains all the required routines to make an A* search algorithm.
#
__author__ = '1668213'
# _________________________________________________________________________________________
# Intel.ligencia Artificial
# Curs 2023 - 2024
# Universitat Autonoma de Barcelona
# _______________________________________________________________________________________

from SubwayMap import *
from utils import *
import os
import math
import copy


def expand(path, map):
    """
     It expands a SINGLE station and returns the list of class Path.
     Format of the parameter is:
        Args:
            path (object of Path class): Specific path to be expanded
            map (object of Map class):: All the information needed to expand the node
        Returns:
            path_list (list): List of paths that are connected to the given path.
    """
    pathList = []
    
    for connection in map.connections[path.last]: #Se accede a las conexiones del último del camino
       auxPath = Path(path.route + [connection]) #Se crea un camino con el constructor
       
       #Se añaden los costes del camino original
       auxPath.g = path.g
       auxPath.h = path.h
       auxPath.f = path.f
       pathList.append(auxPath)
          
    return pathList


def remove_cycles(path_list):
    """
     It removes from path_list the set of paths that include some cycles in their path.
     Format of the parameter is:
        Args:
            path_list (LIST of Path Class): Expanded paths
        Returns:
            path_list (list): Expanded paths without cycles.
    """
    newList = []
    
    for path in path_list:
        
        #set() elimina duplicados de la lista, si hay ciclos las medidas no serán iguales
        if len(path.route) == len(set(path.route)):
            newList.append(path)
            
    return newList


def insert_depth_first_search(expand_paths, list_of_path):
    """
     expand_paths is inserted to the list_of_path according to DEPTH FIRST SEARCH algorithm
     Format of the parameter is:
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            list_of_path (LIST of Path Class): The paths to be visited
        Returns:
            list_of_path (LIST of Path Class): List of Paths where Expanded Path is inserted
    """
    return expand_paths + list_of_path


def depth_first_search(origin_id, destination_id, map):
    """
     Depth First Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): the route that goes from origin_id to destination_id
    """
    pathList = [Path(origin_id)]
    while(pathList[0].last != destination_id) and (pathList is not None):
        
        #Coge el primer elelmeneto de la lista
        first_element = pathList.pop(0)
        
        #Expande el primer elememento para "descubrir" el camino
        expanded_path = expand(first_element, map)
        
        #Elimina posibles ciclos que se creen al expandir
        expanded_path = remove_cycles(expanded_path)
        
        #Inserta el camino expandido al principio de la lista de caminos
        pathList = insert_depth_first_search(expanded_path, pathList)
        
    if pathList[0].last == destination_id:
        return pathList[0]
    else:
        return ("No existeix Solucio")



def insert_breadth_first_search(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to BREADTH FIRST SEARCH algorithm
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where Expanded Path is inserted
    """
    return list_of_path + expand_paths


def breadth_first_search(origin_id, destination_id, map):
    """
     Breadth First Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    pathList = [Path(origin_id)]
    while(pathList[0].last != destination_id) and (pathList is not None):
        
        #Coge el primer elelmeneto de la lista
        first_element = pathList.pop(0)
        
        #Expande el primer elememento para "descubrir" el camino
        expanded_path = expand(first_element, map)
        
        #Elimina posibles ciclos que se creen al expandir
        expanded_path = remove_cycles(expanded_path)
        
        #Inserta el camino expandido al final de la lista de caminos
        pathList = insert_breadth_first_search(expanded_path, pathList)
        
    if pathList[0].last == destination_id:
        return pathList[0]
    else:
        return ("No existeix Solucio")


def calculate_cost(expand_paths, map, type_preference=0):
    """
         Calculate the cost according to type preference
         Format of the parameter is:
            Args:
                expand_paths (LIST of Paths Class): Expanded paths
                map (object of Map class): All the map information
                type_preference: INTEGER Value to indicate the preference selected:
                                0 - Adjacency
                                1 - minimum Time
                                2 - minimum Distance
                                3 - minimum Transfers
            Returns:
                expand_paths (LIST of Paths): Expanded path with updated cost
    """
    
    #Se le suma un 1 porque pasas por 1 parada más
    if type_preference == 0:
        for path in expand_paths:
            path.update_g(1)
            
    #Coge el coste(tiempo) que hay de la penúltima estación hasta la última de la lista
    if type_preference == 1:
        for path in expand_paths:
            time = map.connections[path.penultimate][path.last]
            path.update_g(time)
            
    #Se tiene que calcular la distáncia: V=D/T -> D=V*T
    if type_preference == 2:
        for path in expand_paths:
            station1 = map.stations[path.penultimate]['name']
            station2 = map.stations[path.last]['name']
            
            #Se comprueba que las estaciones no sean iguales
            if station1 != station2:
                time = map.connections[path.penultimate][path.last]
                velocity = map.velocity[map.stations[path.last]['line']]
                path.update_g(velocity * time)
            
    #Se tiene que comprovar si la última parada esta en otra línea que la penúltima
    if type_preference == 3:
        for path in expand_paths:
            line1 = map.stations[path.penultimate]['line']
            line2 = map.stations[path.last]['line']
            
            #Solo se actualizan los transbordos si son líneas diferentes
            if line1 != line2:
                path.update_g(1)

    return expand_paths


def insert_cost(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to COST VALUE
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where expanded_path is inserted according to cost
    """
    paths = list_of_path + expand_paths
    return sorted(paths, key=lambda path: path.g)


def uniform_cost_search(origin_id, destination_id, map, type_preference=0):
    """
     Uniform Cost Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    pathList = [Path(origin_id)]
    while(pathList[0].last != destination_id) and (pathList is not None):
        
        #Coge el primer elelmeneto de la lista
        first_element = pathList.pop(0)
        
        #Expande el primer elememento para "descubrir" el camino
        expanded_path = expand(first_element, map)
        
        #Elimina posibles ciclos que se creen al expandir
        expanded_path = remove_cycles(expanded_path)
        
        #Calcula el coste de los caminos expandidos
        expanded_path = calculate_cost(expanded_path, map, type_preference)
        
        #Inserta el camino expandido al final de la lista de caminos
        pathList = insert_cost(expanded_path, pathList)
        
    if pathList[0].last == destination_id:
        return pathList[0]
    else:
        return ("No existeix Solucio")


def calculate_heuristics(expand_paths, map, destination_id, type_preference=0):
    """
     Calculate and UPDATE the heuristics of a path according to type preference
     WARNING: In calculate_cost, we didn't update the cost of the path inside the function
              for the reasons which will be clear when you code Astar (HINT: check remove_redundant_paths() function).
     Format of the parameter is:
        Args:
            expand_paths (LIST of Path Class): Expanded paths
            map (object of Map class): All the map information
            destination_id (int): Final station id
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            expand_paths (LIST of Path Class): Expanded paths with updated heuristics
    """
    #Se marca como 1 a cualquier nodo que no sea el objetivo
    if type_preference == 0:
        for path in expand_paths:
            if path.last != destination_id:
                path.update_h(1)
            else:
                path.update_h(0)
    
    #Se calcula el minimo tiempo de nodo actual a objetivo con la fórmula de la velocidad
    if type_preference == 1:
        
        # Fórmula: time = distance / velocity
         
        #Calcular la distáncia de nodo actual(last) hasta el objetivo
        distances = distance_to_stations([map.stations[destination_id]['x'], map.stations[destination_id]['y']], map)
        
        #Buscar a cuánta velocidad máxima se puede ir
        velocity = max(map.velocity.values())
        
        #Calcular el tiempo estimado
        for path in expand_paths:
            path.update_h(distances[path.last]/velocity)
            
    #Se calcula una estimación de la distancia que se tiene que recorrer
    if type_preference == 2:
        
        #Calcular la distáncia de nodo actual(last) hasta el objetivo
        distances = distance_to_stations([map.stations[destination_id]['x'], map.stations[destination_id]['y']], map)
        
        for path in expand_paths:
            path.update_h(distances[path.last])
        
    #Se pone un 1 si el nodo actual no esta en la misma linea que el objetivo
    if type_preference == 3:
        for path in expand_paths:
            if map.stations[path.last]['line'] != map.stations[destination_id]['line']:
                path.update_h(1)
            else:
                path.update_h(0)
    
    return expand_paths


def update_f(expand_paths):
    """
      Update the f of a path
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
         Returns:
             expand_paths (LIST of Path Class): Expanded paths with updated costs
    """
    for path in expand_paths:
        path.update_f()
        
    return expand_paths


def remove_redundant_paths(expand_paths, list_of_path, visited_stations_cost):
    """
      It removes the Redundant Paths. They are not optimal solution!
      If a station is visited and have a lower g-cost at this moment, we should remove this path.
      Format of the parameter is:
         Args:
             expand_paths (LIST of Path Class): Expanded paths
             list_of_path (LIST of Path Class): All the paths to be expanded
             visited_stations_cost (dict): All visited stations cost
         Returns:
             new_paths (LIST of Path Class): Expanded paths without redundant paths
             list_of_path (LIST of Path Class): list_of_path without redundant paths
             visited_stations_cost (dict): Updated visited stations cost
    """  
    #Bucle que recorre todos los caminos expandidos
    for exp in expand_paths:
        
        #Combrobaciones para asegurarse de eliminar todos los caminos que tengan mayor coste
        if exp.last in visited_stations_cost.keys():
            
            #Si el coste del nuevo camino es menor se modifica el diccionario. En caso contrario se elimina el camino
            if exp.g < visited_stations_cost[exp.last]:
                visited_stations_cost[exp.last] = exp.g
            else:
                if exp in expand_paths:
                    expand_paths.remove(exp)
        
        #Bucle que recorre toda la lista de caminos
        for path in list_of_path:
            
            #Si el origen y el final del camino expandido coincide con alguno existente se comprovará el coste
            if exp.head == path.head and exp.last == path.last:
                if exp.g < path.g:
                    
                    #Se actualiza la información del camino óptimo
                    visited_stations_cost[exp.last] = exp.g
                    if path in list_of_path:
                        list_of_path.remove(path)
                else:
                    if exp in expand_paths:
                        expand_paths.remove(exp)       
                    
    return expand_paths, list_of_path, visited_stations_cost


def insert_cost_f(expand_paths, list_of_path):
    """
        expand_paths is inserted to the list_of_path according to f VALUE
        Format of the parameter is:
           Args:
               expand_paths (LIST of Path Class): Expanded paths
               list_of_path (LIST of Path Class): The paths to be visited
           Returns:
               list_of_path (LIST of Path Class): List of Paths where expanded_path is inserted according to f
    """
    paths = list_of_path + expand_paths
    update_f(paths)
    return sorted(paths, key=lambda path: path.f)


def distance_to_stations(coord, map):
    """
        From coordinates, it computes the distance to all stations in map.
        Format of the parameter is:
        Args:
            coord (list): Two REAL values, which refer to the coordinates of a point in the city.
            map (object of Map class): All the map information
        Returns:
            (dict): Dictionary containing as keys, all the Indexes of all the stations in the map, and as values, the
            distance between each station and the coord point
    """
    distances = []
    coordinates = []
    
    #Bucle para obtener todas las coordenadas de las estaciones
    for stationValue in map.stations.values():
        coordinates.append([stationValue['x'],stationValue['y']])
        
    #Bucle donde se calculan las distancias de cada estacion y se guardan en orden (1-14)
    for pos,c in enumerate(coordinates,1):
        aux = math.sqrt(pow(coordinates[pos-1][0]-coord[0],2)+pow(coordinates[pos-1][1]-coord[1],2))
        distances.append([pos,aux])
    
    #sorted() ordena los elementos de la lista, primero los ordena por distancia y luego por número
    sorted_distances = sorted(distances, key=lambda x: (x[1], x[0]))
    
    distance_to_stations = {}
    
    #Bucle para guardar los elementos de la lista en el diccionario
    for station,distance in sorted_distances:
        distance_to_stations[station] = distance
    
    return distance_to_stations


def Astar(origin_id, destination_id, map, type_preference=0):
    """
     A* Search algorithm
     Format of the parameter is:
        Args:
            origin_id (int): Starting station id
            destination_id (int): Final station id
            map (object of Map class): All the map information
            type_preference: INTEGER Value to indicate the preference selected:
                            0 - Adjacency
                            1 - minimum Time
                            2 - minimum Distance
                            3 - minimum Transfers
        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_id to destination_id
    """
    pathList = [Path(origin_id)]
    TCP = {}
    while(pathList[0].last != destination_id) and (pathList is not None):
        
        #Coge el primer elelmeneto de la lista
        first_element = pathList.pop(0)
        
        #Expande el primer elememento para "descubrir" el camino
        expanded_path = expand(first_element, map)
        
        #Elimina posibles ciclos que se creen al expandir
        expanded_path = remove_cycles(expanded_path)
        
        #Calcula el coste de los caminos expandidos
        expanded_path = calculate_cost(expanded_path, map, type_preference)
        
        #Calcula la heurística
        expanded_path = calculate_heuristics(expanded_path, map, destination_id, type_preference)
        
        #Elimina de la lista los caminos redundantes
        remove_redundant_paths(expanded_path, pathList, TCP)
        
        #Inserta el camino expandido al final de la lista de caminos
        pathList = insert_cost_f(expanded_path, pathList)
        
    if pathList[0].last == destination_id:
        return pathList[0]
    else:
        return ("No existeix Solucio")
    

def Astar_improved(origin_coord, destination_coord, map):
    """
     A* Search algorithm
     Format of the parameter is:
        Args:
            origin_coord (list): Two REAL values, which refer to the coordinates of the starting position
            destination_coord (list): Two REAL values, which refer to the coordinates of the final position
            map (object of Map class): All the map information

        Returns:
            list_of_path[0] (Path Class): The route that goes from origin_coord to destination_coord
    """
    #Se busca cuál es la estación más cercana a las coordenadas del destino
    end = None
    possible_ends = []
    distances = distance_to_stations(destination_coord, map)
    for station in distances.keys():
        possible_ends.append(station)
    
    maxVel = 0
    for it in range(len(possible_ends) - 1):
        if map.stations[possible_ends[it]]['velocity'] > map.stations[possible_ends[it+1]]['velocity']:
            end = possible_ends[it]
            break
    
    #Se busca que estaciones estan en la misma línea que la estación destino
    stations_same_line = []
    for station,value in enumerate(map.stations.values(), 1):
        if value['line'] == map.stations[end]['line'] and station != end:
            stations_same_line.append(station)
            
    #Se comprueba que estación de la linea esta más cerca de la persona
    distances = distance_to_stations(origin_coord, map)
    min_dist_station = stations_same_line[0] #Esta variable será la estación inicial
    for station in stations_same_line[1:]:
        if distances[station] < distances[min_dist_station]:
            min_dist_station = station
    
    #Calcular coste para ir a la primera estación (t = d / v)
    first_station_coord = [map.stations[min_dist_station]['x'],map.stations[min_dist_station]['y']]
    init_cost = euclidean_dist(origin_coord, first_station_coord) / 5 #Velocidad de la persona
    
    #Aquí se calcula el coste de la estación final hacia el destino
    last_station_coord = [map.stations[end]['x'],map.stations[end]['y']]
    final_cost = euclidean_dist(last_station_coord, destination_coord) / 5 #Velocidad de la persona
    
    #Aquí se calcula el coste de ir de origen a destino caminando
    walking_distance = euclidean_dist(origin_coord, destination_coord)
    total_time = walking_distance / 5 #Velocidad de la persona
    
    #Algoritmo A*
    pathList = [Path([0, min_dist_station])]
    pathList[0].update_g(init_cost)
    TCP = {}
    
    if total_time > init_cost + final_cost:
        while(pathList[0].last != end) and (pathList is not None):
            
            #Coge el primer elelmeneto de la lista
            first_element = pathList.pop(0)
            
            #Expande el primer elememento para "descubrir" el camino
            expanded_path = expand(first_element, map)
            
            #Elimina posibles ciclos que se creen al expandir
            expanded_path = remove_cycles(expanded_path)
            
            #Calcula el coste de los caminos expandidos
            expanded_path = calculate_cost(expanded_path, map, 1)
            
            #Calcula la heurística
            expanded_path = calculate_heuristics(expanded_path, map, end, 1)
            
            #Elimina de la lista los caminos redundantes
            remove_redundant_paths(expanded_path, pathList, TCP)
            
            #Inserta el camino expandido al final de la lista de caminos
            pathList = insert_cost_f(expanded_path, pathList)
    
    #Condición para saber si ha ido en metro o caminando
    if pathList[0].last == end:
         
        #Se añade un -1 porque ha llegado a su destino
        pathList[0].route.append(-1)
        pathList[0].update_g(final_cost)
        pathList[0].update_f()
        return pathList[0]
    else:
        walk_path = Path([0,-1])
        walk_path.update_g(total_time)
        walk_path.update_f()
        return walk_path