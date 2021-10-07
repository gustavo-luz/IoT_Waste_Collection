"""Capacited Vehicles Routing Problem (CVRP)."""

# small version, for 1 truck visiting 4 places
#code to validate with a small sample: trying to validate this sample! input from other code

from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import pandas as pd
import googlemaps
from itertools import tee
import config

#input: CSV file with id,latitude, longitude and capacities
# desired output: list with matrix distance for each point

df = pd.read_excel('IoT_Waste_Collection/rota_nova.xlsx')
#print(df)

API_key = config.api_key #enter your google maps api key here
gmaps = googlemaps.Client(key=API_key)

# works but creates a df , no meters found
# https://strategyanalytics.medium.com/create-a-distance-matrix-in-python-with-the-google-maps-api-737dd0fc8081

#empty list - will be used to store calculated distances
time_list = []
distance_list = []
origin_id_list = []
destination_id_list = []

for (i1, row1) in df.iterrows():
  #print("origin")
  #print(row1['ID'])
  LatOrigin = row1['latitude']
  LongOrigin = row1['longitude']
  origin = (LatOrigin, LongOrigin)
  origin_id = row1['ID']
  for (i2, row2) in  df.iterrows():
    #print("destination id")
    #print(row2['ID'])
    LatDestination = row2['latitude']
    LongDestination = row2['longitude']
    destination_id = row2['ID']
    destination = (LatDestination, LongDestination)
    result = gmaps.distance_matrix(origin, destination, mode='driving')
    #uncomment for cool api logs
    #print(result)
    result_distance = result["rows"][0]["elements"][0]["distance"]["value"]
    result_time = result["rows"][0]["elements"][0]["duration"]["value"]
    time_list.append(result_time)
    distance_list.append(result_distance)
    origin_id_list.append(origin_id)
    destination_id_list.append(destination_id)

size=(len(df.coordinates))
print(distance_list)


from itertools import islice
  
# Input list initialization
Input = distance_list
  
# list of length in which we have to split
number_containers = len(df['ID'])

length_to_split = number_containers*[number_containers]
print(length_to_split)
  
# Using islice
Inputt = iter(Input)
Output = [list(islice(Inputt, elem))
          for elem in length_to_split]
  


# Printing Output
print("Initial list is:", Input)
print("Split length list: ", length_to_split)
print("List after splitting", Output)
def create_data_model():
    """Stores the data for the problem."""
    data = {}
   

    #always 1 number bigger, because it has to return to base
    data['distance_matrix'] = Output
    # TODO make demands be like the distributtion roberto tells me
    # full container: 600 to 800kg
    # normal: a cada 10, 3 cheios, outros 7 de 50% pra cima
    # 30% cheios, outros 70% de 50% pra cima
    capacities = df['PESAGENS']
    print(capacities)

    data['demands'] = df['PESAGENS'].values.tolist()
    print(data['demands'])
    #data['demands'] = [0,800,800,800,500,450,400,350,550,420,390,350,700,400,300]
    #rint(data['demands'])

    # 1 vehicle
    # capacity: 9000 to 12000 kg
    data['vehicle_capacities'] = [10000]
    data['num_vehicles'] = 1

    data['depot'] = 0
    return data


def print_solution(data, manager, routing, solution):
    """Prints solution on console."""
    print(f'Objective: {solution.ObjectiveValue()}')
    total_distance = 0
    total_load = 0
    for vehicle_id in range(data['num_vehicles']):
        index = routing.Start(vehicle_id)
        plan_output = 'Route for vehicle {}:\n'.format(vehicle_id)
        route_distance = 0
        route_load = 0
        while not routing.IsEnd(index):
            node_index = manager.IndexToNode(index)
            route_load += data['demands'][node_index]
            plan_output += ' {0} Load({1}) -> '.format(node_index, route_load)
            previous_index = index
            index = solution.Value(routing.NextVar(index))
            route_distance += routing.GetArcCostForVehicle(
                previous_index, index, vehicle_id)
        plan_output += ' {0} Load({1})\n'.format(manager.IndexToNode(index),
                                                 route_load)
        plan_output += 'Distance of the route: {}m\n'.format(route_distance)
        plan_output += 'Load of the route: {}\n'.format(route_load)
        print(plan_output)
        total_distance += route_distance
        total_load += route_load
        # TODO print total cost
    print('Total distance of all routes: {}m'.format(total_distance))
    print('Total load of all routes: {}'.format(total_load))


def main():
    """Solve the CVRP problem."""
    # Instantiate the data problem.
    data = create_data_model()

    # Create the routing index manager.
    manager = pywrapcp.RoutingIndexManager(len(data['distance_matrix']),
                                           data['num_vehicles'], data['depot'])

    # Create Routing Model.
    routing = pywrapcp.RoutingModel(manager)


    # Create and register a transit callback.
    def distance_callback(from_index, to_index):
        """Returns the distance between the two nodes."""
        # Convert from routing variable Index to distance matrix NodeIndex.
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return data['distance_matrix'][from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)

    # Define cost of each arc.
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)


    # Add Capacity constraint.
    def demand_callback(from_index):
        """Returns the demand of the node."""
        # Convert from routing variable Index to demands NodeIndex.
        from_node = manager.IndexToNode(from_index)
        return data['demands'][from_node]

    demand_callback_index = routing.RegisterUnaryTransitCallback(
        demand_callback)
    routing.AddDimensionWithVehicleCapacity(
        demand_callback_index,
        0,  # null capacity slack
        data['vehicle_capacities'],  # vehicle maximum capacities
        True,  # start cumul to zero
        'Capacity')

    # Setting first solution heuristic.
    #TODO select different heuristics
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (
        routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)
    search_parameters.local_search_metaheuristic = (
        routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH)
    search_parameters.time_limit.FromSeconds(1)

    # Solve the problem.
    solution = routing.SolveWithParameters(search_parameters)

    # Print solution on console.
    if solution:
        print_solution(data, manager, routing, solution)
    else:
        print("no solution found")


if __name__ == '__main__':
    main()