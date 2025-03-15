from SearchAlgorithm import *
from SubwayMap import *
from utils import *

def print_list_of_path_with_heu(path_list):
    for p in path_list:
        print("Route: {}, \t Cost: {}".format(p.route, round(p.h,2)))

if __name__=="__main__":
    ROOT_FOLDER = '../CityInformation/Lyon_SmallCity/'
    map = read_station_information(os.path.join(ROOT_FOLDER, 'Stations.txt'))
    connections = read_cost_table(os.path.join(ROOT_FOLDER, 'Time.txt'))
    map.add_connection(connections)

    infoVelocity_clean = read_information(os.path.join(ROOT_FOLDER, 'InfoVelocity.txt'))
    map.add_velocity(infoVelocity_clean)



    ###BELOW HERE YOU CAN CALL ANY FUNCTION THAT YOU HAVE PROGRAMED TO ANSWER THE QUESTIONS FOR THE TEST###

    #example
    #example_path = expand(Path([5]), map)
    #print_list_of_path(example_path)
    print("Estaciones:\n")
    print(map.stations)
    
    expanded = expand(Path([3]), map)
    print("Expand:")
    print_list_of_path(expanded)
    print("\n")
    
    removed = remove_cycles([Path([2,3,4,5]),Path([2,3,6,3]),Path([1,2,3,4])])
    print("Remove_cycles:")
    print_list_of_path(removed)
    print("\n")
    
    coste = calculate_cost([Path([2,3,4,5])], map,2)
    print("Calculate_cost:")
    print_list_of_path_with_cost(coste)
    print("\n")
    
    dist = distance_to_stations([200, 314], map)
    print("Distances:\n", dist)
    
    path1 = breadth_first_search(4, 12, map)
    print("BFS:\n",path1.route, path1.g)
    
    path2 = depth_first_search(4, 12, map)
    print("DFS:\n",path2.route, path2.g)
    
    path3 = uniform_cost_search(4, 12, map)
    print("UCS:\n",path3.route, path3.g)
    
    path4 = Astar(4, 12, map)
    print("A*:\n",path4.route, path4.f)
    
    path5 = Astar_improved([0,0], [200,314], map)
    print("A* improved:\n",path5.route, path5.f)