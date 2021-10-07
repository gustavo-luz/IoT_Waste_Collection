"""Capacited Vehicles Routing Problem (CVRP)."""

# small version, for 1 truck visiting 4 places
#code to validate with a small sample: trying to validate this sample! input from other code
import argparse
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import pandas as pd
import googlemaps
from itertools import tee
import config

#input: CSV file with id,latitude, longitude and capacities
# desired output: list with matrix distance for each point

df = pd.read_excel('IoT_Waste_Collection/IOTSCv2.xlsx')
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
length_to_split = [16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16]
  
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

    data['demands'] = [800,800,800,500,450,400,350,550,420,390,350,700,400,300,470,500]

    # 1 vehicle
    # capacity: 9000 to 12000 kg
    data['vehicle_capacities'] = [10000]
    data['num_vehicles'] = 1

    data['depot'] = 0
    return data



###########
# Printer #
###########
class GoogleColorPalette(object):
    """Google color codes palette."""

    def __init__(self):
        """Initialize Google ColorPalette."""
        self._colors = [('blue', r'#4285F4'), ('red', r'#EA4335'),
                        ('yellow', r'#FBBC05'), ('green', r'#34A853'),
                        ('black', r'#101010'), ('white', r'#FFFFFF')]

    def __getitem__(self, key):
        """Gets color name from idx."""
        return self._colors[key][0]

    def __len__(self):
        """Gets the number of colors."""
        return len(self._colors)

    @property
    def colors(self):
        """Gets the colors list."""
        return self._colors

    def name(self, idx):
        """Return color name from idx."""
        return self._colors[idx][0]

    def value(self, idx):
        """Return color value from idx."""
        return self._colors[idx][1]

    def value_from_name(self, name):
        """Return color value from name."""
        return dict(self._colors)[name]


class SVG(object):
    """SVG draw primitives."""

    @staticmethod
    def header(size, margin):
        """Writes header."""
        print(r'<svg xmlns:xlink="http://www.w3.org/1999/xlink" '
              'xmlns="http://www.w3.org/2000/svg" version="1.1"\n'
              'width="{width}" height="{height}" '
              'viewBox="-{margin} -{margin} {width} {height}">'.format(
                  width=size[0] + 2 * margin,
                  height=size[1] + 2 * margin,
                  margin=margin))

    @staticmethod
    def definitions(colors):
        """Writes definitions."""
        print(r'<!-- Need this definition to make an arrow marker,'
              ' from https://www.w3.org/TR/svg-markers/ -->')
        print(r'<defs>')
        for color in colors:
            print(
                r'  <marker id="arrow_{colorname}" viewBox="0 0 16 16" '
                'refX="8" refY="8" markerUnits="strokeWidth" markerWidth="5" markerHeight="5" '
                'orient="auto">'.format(colorname=color[0]))
            print(
                r'    <path d="M 0 0 L 16 8 L 0 16 z" stroke="none" fill="{color}"/>'
                .format(color=color[1]))
            print(r'  </marker>')
        print(r'</defs>')

    @staticmethod
    def footer():
        """Writes svg footer."""
        print(r'</svg>')

    @staticmethod
    def draw_line(position_1, position_2, size, fg_color):
        """Draws a line."""
        line_style = (
            r'style="stroke-width:{sz};stroke:{fg};fill:none"').format(
                sz=size, fg=fg_color)
        print(r'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" {style}/>'.format(
            x1=position_1[0],
            y1=position_1[1],
            x2=position_2[0],
            y2=position_2[1],
            style=line_style))

    @staticmethod
    def draw_polyline(position_1, position_2, size, fg_color, colorname):
        """Draws a line with arrow maker in the middle."""
        polyline_style = (r'style="stroke-width:{sz};stroke:{fg};fill:none;'
                          'marker-mid:url(#arrow_{colorname})"').format(
                              sz=size, fg=fg_color, colorname=colorname)
        print(r'<polyline points="{x1},{y1} {x2},{y2} {x3},{y3}" {style}/>'.
              format(x1=position_1[0],
                     y1=position_1[1],
                     x2=(position_1[0] + position_2[0]) / 2,
                     y2=(position_1[1] + position_2[1]) / 2,
                     x3=position_2[0],
                     y3=position_2[1],
                     style=polyline_style))

    @staticmethod
    def draw_circle(position, radius, size, fg_color, bg_color='white'):
        """Print a circle."""
        circle_style = (
            r'style="stroke-width:{sz};stroke:{fg};fill:{bg}"').format(
                sz=size, fg=fg_color, bg=bg_color)
        print(r'<circle cx="{cx}" cy="{cy}" r="{r}" {style}/>'.format(
            cx=position[0], cy=position[1], r=radius, style=circle_style))

    @staticmethod
    def draw_text(text, position, size, fg_color='none', bg_color='black'):
        """Print a middle centred text."""
        text_style = (r'style="text-anchor:middle;font-weight:bold;'
                      'font-size:{sz};stroke:{fg};fill:{bg}"').format(
                          sz=size, fg=fg_color, bg=bg_color)
        print(r'<text x="{x}" y="{y}" dy="{dy}" {style}>{txt}</text>'.format(
            x=position[0],
            y=position[1],
            dy=size / 3,
            style=text_style,
            txt=text))






class SVGPrinter(object):  # pylint: disable=too-many-instance-attributes
    """Generate Problem as svg file to stdout."""

    # pylint: disable=too-many-arguments
    def __init__(self, args, data, manager=None, routing=None, assignment=None):
        """Initializes the printer."""
        self._args = args
        self._data = data
        self._manager = manager
        self._routing = routing
        self._assignment = assignment
        # Design variables
        self._color_palette = GoogleColorPalette()
        self._svg = SVG()
        # City block size 114mx80m
        self._radius = min(114, 80) / 3
        self._stroke_width = self._radius / 4

    @property
    def data(self):
        """Gets the Data Model."""
        return self._data

    @property
    def manager(self):
        """Gets the RoutingIndexManager."""
        return self._manager

    @property
    def routing(self):
        """Gets the Routing solver."""
        return self._routing

    @property
    def assignment(self):
        """Gets the assignment."""
        return self._assignment

    @property
    def color_palette(self):
        """Gets the color palette."""
        return self._color_palette

    @property
    def svg(self):
        """Gets the svg."""
        return self._svg

    def draw_grid(self):
        """Draws the city grid."""
        print(r'<!-- Print city streets -->')
        color = '#969696'
        # Horizontal streets
        for i in range(9):
            p_1 = [0, i * 80]
            p_2 = [8 * 114, p_1[1]]
            self._svg.draw_line(p_1, p_2, 2, color)
        # Vertical streets
        for i in range(9):
            p_1 = [i * 114, 0]
            p_2 = [p_1[0], 8 * 80]
            self._svg.draw_line(p_1, p_2, 2, color)

    def draw_depot(self):
        """Draws the depot."""
        print(r'<!-- Print depot -->')
        color = self._color_palette.value_from_name('black')
        loc = self._data.locations[self._data.depot]
        self._svg.draw_circle(loc, self._radius, self._stroke_width, color,
                              'white')
        self._svg.draw_text(self._data.depot, loc, self._radius, 'none', color)

    def draw_depots(self):
        """Draws the depot."""
        print(r'<!-- Print depots -->')
        # print starts
        for vehicle_idx, start in enumerate(self._data.starts):
            del vehicle_idx
            color = self._color_palette.value_from_name('black')
            # color = self._color_palette.value(vehicle_idx)
            loc = self._data.locations[start]
            self._svg.draw_circle(loc, self._radius, self._stroke_width, color,
                                  'white')
            self._svg.draw_text(start, loc, self._radius, 'none', color)
        # print end
        color = self._color_palette.value_from_name('black')
        loc = self._data.locations[0]
        self._svg.draw_circle(loc, self._radius, self._stroke_width, color,
                              'white')
        self._svg.draw_text(0, loc, self._radius, 'none', color)

    def draw_locations(self):
        """Draws all the locations but the depot."""
        print(r'<!-- Print locations -->')
        color = self._color_palette.value_from_name('blue')
        if not self._args['starts_ends']:
            for idx, loc in enumerate(self._data.locations):
                if idx == self._data.depot:
                    continue
                self._svg.draw_circle(loc, self._radius, self._stroke_width,
                                      color, 'white')
                self._svg.draw_text(idx, loc, self._radius, 'none', color)
        else:
            for idx, loc in enumerate(self._data.locations):
                if idx in self._data.starts + self._data.ends:
                    continue
                self._svg.draw_circle(loc, self._radius, self._stroke_width,
                                      color, 'white')
                self._svg.draw_text(idx, loc, self._radius, 'none', color)

    def draw_demands(self):
        """Draws all the demands."""
        print(r'<!-- Print demands -->')
        for idx, loc in enumerate(self._data.locations):
            if idx == self._data.depot:
                continue
            demand = self._data.demands[idx]
            position = [
                x + y
                for x, y in zip(loc, [self._radius * 1.2, self._radius * 1.1])
            ]
            color = self._color_palette.value_from_name('red')
            # color = self._color_palette.value(int(math.log(demand, 2)))
            self._svg.draw_text(demand, position, self._radius, 'none', color)

    def draw_pickups_deliveries(self):
        """Draws all pickups deliveries."""
        print(r'<!-- Print pickups deliveries -->')
        colorname = 'red'
        color = self._color_palette.value_from_name(colorname)
        for pickup_delivery in self._data.pickups_deliveries:
            self._svg.draw_polyline(self._data.locations[pickup_delivery[0]],
                                    self._data.locations[pickup_delivery[1]],
                                    self._stroke_width, color, colorname)

    def draw_time_windows(self):
        """Draws all the time windows."""
        print(r'<!-- Print time windows -->')
        for idx, loc in enumerate(self._data.locations):
            if idx == self._data.depot:
                continue
            time_window = self._data.time_windows[idx]
            position = [
                x + y
                for x, y in zip(loc, [self._radius * 0, -self._radius * 1.6])
            ]
            color = self._color_palette.value_from_name('red')
            self._svg.draw_text(
                '[{t1},{t2}]'.format(t1=time_window[0], t2=time_window[1]),
                position, self._radius * 0.75, 'white', color)

##############
##  ROUTES  ##
##############

    def draw_drop_nodes(self):
        """Draws the dropped nodes."""
        print(r'<!-- Print drop nodes -->')
        if self._assignment is None:
            print('<!-- No solution found. -->')
        # Display dropped nodes.
        dropped_nodes = []
        for node in range(self._routing.Size()):
            if self._routing.IsStart(node) or self._routing.IsEnd(node):
                continue
            if self._assignment.Value(self._routing.NextVar(node)) == node:
                dropped_nodes.append(self._manager.IndexToNode(node))
        color = self._color_palette.value_from_name('black')
        for node_idx in dropped_nodes:
            loc = self._data.locations[node_idx]
            self._svg.draw_circle(loc, self._radius, self._stroke_width, color,
                                  'white')
            self._svg.draw_text(node_idx, loc, self._radius, 'none', color)

    def routes(self):
        """Creates the route list from the assignment."""
        if self._assignment is None:
            print('<!-- No solution found. -->')
            return []
        routes = []
        for vehicle_id in range(self._data.num_vehicles):
            index = self._routing.Start(vehicle_id)
            route = []
            while not self._routing.IsEnd(index):
                node_index = self._manager.IndexToNode(index)
                route.append(node_index)
                index = self._assignment.Value(self._routing.NextVar(index))
            node_index = self._manager.IndexToNode(index)
            route.append(node_index)
            routes.append(route)
        return routes

    def draw_route(self, route, color, colorname):
        """Draws a Route."""
        # First print route
        previous_loc_idx = None
        for loc_idx in route:
            if previous_loc_idx and previous_loc_idx != loc_idx:
                self._svg.draw_polyline(self._data.locations[previous_loc_idx],
                                        self._data.locations[loc_idx],
                                        self._stroke_width, color, colorname)
            previous_loc_idx = loc_idx
        # Then print location along the route
        for loc_idx in route:
            if loc_idx != self._data.depot:
                loc = self._data.locations[loc_idx]
                self._svg.draw_circle(loc, self._radius, self._stroke_width,
                                      color, 'white')
                self._svg.draw_text(loc_idx, loc, self._radius, 'none', color)

    def draw_routes(self):
        """Draws the routes."""
        print(r'<!-- Print routes -->')
        for route_idx, route in enumerate(self.routes()):
            print(r'<!-- Print route {idx} -->'.format(idx=route_idx))
            color = self._color_palette.value(route_idx)
            colorname = self._color_palette.name(route_idx)
            self.draw_route(route, color, colorname)

    def tw_routes(self):
        """Creates the route time window list from the assignment."""
        if self._assignment is None:
            print('<!-- No solution found. -->')
            return []
        time_dimension = self._routing.GetDimensionOrDie('Time')
        loc_routes = []
        tw_routes = []
        for vehicle_id in range(self._data.num_vehicles):
            index = self._routing.Start(vehicle_id)
            # index = self._assignment.Value(self._routing.NextVar(index))
            loc_route = []
            tw_route = []
            while True:
                node_index = self._manager.IndexToNode(index)
                loc_route.append(node_index)
                time_var = time_dimension.CumulVar(index)
                t_min = self._assignment.Min(time_var)
                t_max = self._assignment.Max(time_var)
                tw_route.append((t_min, t_max))
                if self._routing.IsEnd(index):
                    break
                index = self._assignment.Value(self._routing.NextVar(index))
            loc_routes.append(loc_route)
            tw_routes.append(tw_route)
        return zip(loc_routes, tw_routes)

    def draw_tw_route(self, route_idx, locations, tw_route, color):
        """Draws the time windows for a Route."""
        is_start = -1
        for loc_idx, time_window in zip(locations, tw_route):
            loc = self._data.locations[loc_idx]
            if loc_idx == 0:  # special case for depot
                position = [
                    x + y for x, y in zip(loc, [
                        self._radius * is_start, self._radius *
                        (1.8 + route_idx)
                    ])
                ]
                is_start = 1
            else:
                position = [
                    x + y
                    for x, y in zip(loc, [self._radius * 0, self._radius * 1.8])
                ]
            self._svg.draw_text('[{t_min}]'.format(t_min=time_window[0]),
                                position, self._radius * 0.75, 'white', color)

    def draw_tw_routes(self):
        """Draws the time window routes."""
        print(r'<!-- Print time window routes -->')
        for route_idx, loc_tw in enumerate(self.tw_routes()):
            print(r'<!-- Print time window route {} -->'.format(route_idx))
            color = self._color_palette.value(route_idx)
            self.draw_tw_route(route_idx, loc_tw[0], loc_tw[1], color)

    def print_to_console(self):
        """Prints a full svg document on stdout."""
        margin = self._radius * 2 + 2
        size = [8 * 114, 8 * 80]
        self._svg.header(size, margin)
        self._svg.definitions(self._color_palette.colors)
        self.draw_grid()###########
# Printer #
###########
class GoogleColorPalette(object):
    """Google color codes palette."""

    def __init__(self):
        """Initialize Google ColorPalette."""
        self._colors = [('blue', r'#4285F4'), ('red', r'#EA4335'),
                        ('yellow', r'#FBBC05'), ('green', r'#34A853'),
                        ('black', r'#101010'), ('white', r'#FFFFFF')]

    def __getitem__(self, key):
        """Gets color name from idx."""
        return self._colors[key][0]

    def __len__(self):
        """Gets the number of colors."""
        return len(self._colors)

    @property
    def colors(self):
        """Gets the colors list."""
        return self._colors

    def name(self, idx):
        """Return color name from idx."""
        return self._colors[idx][0]

    def value(self, idx):
        """Return color value from idx."""
        return self._colors[idx][1]

    def value_from_name(self, name):
        """Return color value from name."""
        return dict(self._colors)[name]


class SVG(object):
    """SVG draw primitives."""

    @staticmethod
    def header(size, margin):
        """Writes header."""
        print(r'<svg xmlns:xlink="http://www.w3.org/1999/xlink" '
              'xmlns="http://www.w3.org/2000/svg" version="1.1"\n'
              'width="{width}" height="{height}" '
              'viewBox="-{margin} -{margin} {width} {height}">'.format(
                  width=size[0] + 2 * margin,
                  height=size[1] + 2 * margin,
                  margin=margin))

    @staticmethod
    def definitions(colors):
        """Writes definitions."""
        print(r'<!-- Need this definition to make an arrow marker,'
              ' from https://www.w3.org/TR/svg-markers/ -->')
        print(r'<defs>')
        for color in colors:
            print(
                r'  <marker id="arrow_{colorname}" viewBox="0 0 16 16" '
                'refX="8" refY="8" markerUnits="strokeWidth" markerWidth="5" markerHeight="5" '
                'orient="auto">'.format(colorname=color[0]))
            print(
                r'    <path d="M 0 0 L 16 8 L 0 16 z" stroke="none" fill="{color}"/>'
                .format(color=color[1]))
            print(r'  </marker>')
        print(r'</defs>')

    @staticmethod
    def footer():
        """Writes svg footer."""
        print(r'</svg>')

    @staticmethod
    def draw_line(position_1, position_2, size, fg_color):
        """Draws a line."""
        line_style = (
            r'style="stroke-width:{sz};stroke:{fg};fill:none"').format(
                sz=size, fg=fg_color)
        print(r'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" {style}/>'.format(
            x1=position_1[0],
            y1=position_1[1],
            x2=position_2[0],
            y2=position_2[1],
            style=line_style))

    @staticmethod
    def draw_polyline(position_1, position_2, size, fg_color, colorname):
        """Draws a line with arrow maker in the middle."""
        polyline_style = (r'style="stroke-width:{sz};stroke:{fg};fill:none;'
                          'marker-mid:url(#arrow_{colorname})"').format(
                              sz=size, fg=fg_color, colorname=colorname)
        print(r'<polyline points="{x1},{y1} {x2},{y2} {x3},{y3}" {style}/>'.
              format(x1=position_1[0],
                     y1=position_1[1],
                     x2=(position_1[0] + position_2[0]) / 2,
                     y2=(position_1[1] + position_2[1]) / 2,
                     x3=position_2[0],
                     y3=position_2[1],
                     style=polyline_style))

    @staticmethod
    def draw_circle(position, radius, size, fg_color, bg_color='white'):
        """Print a circle."""
        circle_style = (
            r'style="stroke-width:{sz};stroke:{fg};fill:{bg}"').format(
                sz=size, fg=fg_color, bg=bg_color)
        print(r'<circle cx="{cx}" cy="{cy}" r="{r}" {style}/>'.format(
            cx=position[0], cy=position[1], r=radius, style=circle_style))

    @staticmethod
    def draw_text(text, position, size, fg_color='none', bg_color='black'):
        """Print a middle centred text."""
        text_style = (r'style="text-anchor:middle;font-weight:bold;'
                      'font-size:{sz};stroke:{fg};fill:{bg}"').format(
                          sz=size, fg=fg_color, bg=bg_color)
        print(r'<text x="{x}" y="{y}" dy="{dy}" {style}>{txt}</text>'.format(
            x=position[0],
            y=position[1],
            dy=size / 3,
            style=text_style,
            txt=text))
        #if not self._args['solution']:
        #    if self._args['pickup_delivery']:
        self.draw_pickups_deliveries()
        self.draw_locations()
        self.draw_routes()
        self.draw_drop_nodes()
    
        self.draw_depots()
    #    else:
        self.draw_depot()
     #   if self._args['capacity']:
        self.draw_demands()
      #  if self._args['drop_nodes']:
        self.draw_demands()
       # if self._args['time_windows'] or self._args['resources']:
        self.draw_time_windows()
        #if ((self._args['time_windows'] or self._args['resources']) and
        #self._args['solution']):
        self.draw_tw_routes()
        self._svg.footer()



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
            # Print the solution.
        printer = SVGPrinter(data, manager, routing)
        printer.print_to_console()
        return 0
    else:
        print("no solution found")








if __name__ == '__main__':
    main()