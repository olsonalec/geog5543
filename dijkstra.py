import geopandas as gpd
import matplotlib.pyplot as plt
import ast
import time


roads_gpd = gpd.read_file('roads_prepped.json')
intersections_gpd = gpd.read_file('intersections_prepped.json')


source = 741     # an intersection
dest = 1708       # an intersection

# print(intersections_gpd.loc[source])

class Road:
    def __init__(self, index, cost):
        self.index = index      # the index into the roads_gpd where this road is stored
        self.travel_time = cost        # the cost to travel this road segment

class Vertex:
    def __init__(self, index):
        self.cost = float("inf")        # the total cost of the path to reach this vertex
        self.prev = None    # the previous Vertex in the path
        self.index = index      # the index into the intersections_gpd where this vertex is stored
        self.connections = {}   # a dict of Vertex objects that can be reached by this Vertex - i.e. intersections that are one road segment away; keys are Vertex objects and values are Road objects

'''
A function to intialize the Vertex objects.

Parameters:
    gdf (Geodataframe) - a GeoPandas Geodataframe containing intersection points
    source (int) - the starting vertex; this is an index into the Geodataframe

Return Value:
    vertex_list (list) - a list of Vertex objects
'''
def initialize_vertices(gdf, source):
    vertex_list = []        # a list to store a Vertex object associated with each intersection
    for intersection in gdf.itertuples():
        index = intersection.Index
        new_vertex = Vertex(index)
        vertex_list.append(new_vertex)

    # Change the starting vertex's cost to 0
    vertex_list[source].cost = 0

    return vertex_list

'''
A function to initialize the connection attribute for each Vertex object.
The connection attribute stores the index of other intersections that are one road segment away from a given intersection.
Parameters:
    int_gdf - a GeoPandas Geodataframe containing intersection points
    road_gdf - a GeoPandas Geodataframe containing roads
    vertices - a list of Vertex objects
'''
def initialize_ints(int_gdf, road_gdf, vertices):
    for vertex in vertices:
        roads = int_gdf.loc[vertex.index]['Roads']
        roads = convert_string_to_list(roads)

        # find the intersections that are one road segment away from the current intersection
        connections = {}
        for road in roads:
            new_intersections = road_gdf.loc[road]['Intersections']
            new_intersections = convert_string_to_list(new_intersections)
            for intersection in new_intersections:
                if (intersection != vertex.index) and (intersection not in connections):
                    connections[vertices[intersection]] = Road(road, road_gdf.loc[road]['TimeToTravel'])
                    # connections.append(vertices[intersection])
            vertex.connections = connections
    
'''
A function to find the index of the minimum element in a list of unsorted objects.

Parameter:
    list_of_vertices (list) - a list of Vertex objects

Return Value:
    min_value_idx (int) - the index of the minimum element in the list
'''
def find_min(list_of_vertices):
    min_value = float("inf")
    min_value_idx = -1
    n = len(list_of_vertices)
    for i in range(n):
        if list_of_vertices[i].cost < min_value:
            min_value = list_of_vertices[i].cost
            min_value_idx = i
    return min_value_idx

'''
The 'Intersections' and 'Roads' attributes in the Roads and Intersections Geodataframes, respectively, are represented as a nested list.
If they were a one-dimensional list, GeoPandas would think that they represent geometry, which they don't.
However, when reading these attributes from the dataframe, Python interprets them as strings.
This is an example: '[[180, 240, 360]]'
This function converts this string representation of a nested list into a 1-dimensional Python list.
The example output would be [180, 240, 360], where each value is an integer.

Parameter:
    bad_string - a string representation of a nested list

Return Value:
    new_list[0] - a Python list representation of the input
'''
def convert_string_to_list(bad_string):
    new_list = ast.literal_eval(bad_string)
    return new_list[0]

'''
Converts seconds into minutes and seconds.

Parameter:
    seconds (float) - the value of seconds

Return Values:
    min (int) - an integer representing the number of minutes
    sec (int) - an integer representing the number of seconds
'''
def convert_sec_to_min(seconds):
    min = int(seconds // 60)
    sec = int(seconds % 60)
    return min, sec    

'''
A function to find the shortest path between two intersections.

Parameters:
    graph - a list containing all the unvisited vertices in the graph; this is the list returned by the initialize() function
    dest - the index into the intersections Geodataframe of the destination vertex

Return Value:
    visited_intersections (list) - a list of all the Vertex objects that were visited by the algorithm
                                    This list contains Vertex objects that are on the shortest path as well as Vertex objects that are not in the shortest path
                                    The prev attribute of each Vertex object will be used to determine the shortest path. After this function returns, simply find
                                        the ending vertex, and use the prev attribute to work your way backwards until you reach the starting vertex. This process
                                        returns the shortest path.
'''
def Dijkstra(graph, dest):
    visited_vertices = []       # a list containing all the indices of all the vertices that have been visited so far
    visited_intersections = []  # a list containing all the Vertex objects that have been visited so far
    chosen_roads = []           # a list containing indicies for all the roads for the route
    while dest not in visited_vertices:
        min_value_idx = find_min(graph)
        vertex = graph[min_value_idx]

        # update distances to the neighbor nodes
        neighbors = vertex.connections
        for neighbor, road in neighbors.items():
            new_cost = vertex.cost + road.travel_time
            if new_cost < neighbor.cost:
                neighbor.cost = new_cost
                neighbor.prev = vertex
        
        # find the neighbor with the lowest cost
        # lowest_cost = float("inf")
        # lowest_cost_neighbor = None
        # for neighbor, cost in neighbors.items():
        #     if cost < lowest_cost:
        #         lowest_cost = cost
        #         lowest_cost_neighbor = neighbor


        # neighbor_roads = intersections_gpd.loc[vertex.index]['Roads']
        # neighbor_roads = convert_string_to_list(neighbor_roads)
        # neighbor_intersections = {}     # each key is an intersection that is reachable by the current vertex; each value is the cost to get there
        # for road in neighbor_roads:
            # road_cost = roads_gpd.loc[road]['TimeToTravel']
            # new_cost = road_cost + vertex.cost
            # intersections = vertex.connections
            # intersections = roads_gpd.loc[road]['Intersections']
            # intersections = convert_string_to_list(intersections)
            # for i in range(len(intersections)):
                # if (intersections[i].index != vertex.index) and (intersections[i].index not in neighbor_intersections):
                    # neighbor_intersections[intersections[i].index] = new_cost
                    # neighbor_intersections.append(intersections[i])
            # print(f'intersections: {neighbor_intersections}')
        # neighbors = roads_gpd.loc[vertex.index]['Intersections']      # get the list of neighbor nodes from the roads_gpd
        
        # convert neighbors into a 1D list and remove the current node from the list
        # neighbors = ast.literal_eval(neighbors)
        # neighbors = neighbors[0]
        # neighbors.remove(vertex.index)

        # for each neighbor node, update the cost (and it's previous Vertex) if it's less than the current cost
        # current_cost = vertex.cost
        # for key, value in neighbor_intersections.items():
        #     old_cost = graph[key].cost
        #     if value < old_cost:
        #         vertex.cost = new_cost
        #         vertex.prev = key
        # for i in range(len(neighbor_intersections)):
        #     new_cost = neighbor_intersections
        #     new_cost = roads_gpd.loc[vertex.index]['TimeToTravel'] + current_cost
        #     if new_cost < graph[neighbor_intersections[i]].cost:
        #         graph[neighbor_intersections[i]].cost = new_cost
        #         graph[neighbor_intersections[i]].prev = vertex.index
        
        # find the neighbor with the lowest cost
        # lowest_cost = float("inf")
        # lowest_cost_vertex = -1
        # for key, value in neighbor_intersections.items():
        #     if graph[key].cost < lowest_cost:
        #         lowest_cost = graph[key].cost
        #         lowest_cost_vertex = graph[key]

        # for i in range(len(neighbor_intersections)):
        #     if graph[neighbor_intersections[i]].cost < lowest_cost:
        #         lowest_cost = graph[neighbor_intersections[i]].cost
        #         lowest_cost_vertex = neighbor_intersections[i]
        
        # add the current node to the set of visited nodes
        visited_vertices.append(vertex.index)
        visited_intersections.append(vertex)
        chosen_roads.append(vertex.connections)


        # remove the current node from the set of unvisited nodes
        graph.pop(min_value_idx)
    
    return visited_intersections
    
        
list_of_vertices = initialize_vertices(intersections_gpd, source)
initialize_ints(intersections_gpd, roads_gpd, list_of_vertices)

start_time = time.time()
visited_vertices = Dijkstra(list_of_vertices, source, dest)
end_time = time.time()

print('Path: ', end='')
# for i in range(len(visited_vertices)):
#     print(f'{visited_vertices[i].index} {visited_vertices[i].cost}')

# print()

chosen_vertices = []
chosen_vertices_idxs = []
dest_idx = -1
for i in range(len(visited_vertices)):
    if visited_vertices[i].index == dest:
        dest_idx = i
        break

prev_intersection = visited_vertices[dest_idx].prev
total_travel_time = visited_vertices[dest_idx].cost
min, sec = convert_sec_to_min(total_travel_time)
while prev_intersection != None:
    chosen_vertices.append(prev_intersection)
    chosen_vertices_idxs.append(prev_intersection.index)
    prev_intersection = prev_intersection.prev

# for i in range(len(chosen_vertices)):
#     print(f'{chosen_vertices[i].index} {chosen_vertices[i].cost}')

print(chosen_vertices_idxs)
print(f'The time it will take to travel this route is {min} minutes and {sec} seconds.')
print(f'Time taken to run Dijkstra\'s Algorithm: {end_time - start_time}')


fig, ax = plt.subplots()

# intersections_gpd.plot(ax=ax)

roads_gpd.plot(ax=ax)

intersections_gpd.loc[chosen_vertices_idxs, 'geometry'].plot(ax=ax, color='r')



# roads = intersections_gpd.loc[source]['Roads']      # these are the roads that connect to the source intersection
# intersections_gpd.loc[[source], 'geometry'].plot(ax=ax)
# roads = ast.literal_eval(roads)     # GeoPandas thinks that this nested list is a string; so we need to convert it into a list
# roads_gpd.loc[roads[0], 'geometry'].plot(ax=ax)

# for road in roads[0]:
#     new_ints = roads_gpd.loc[road]['Intersections']
#     new_ints = ast.literal_eval(new_ints)
#     new_ints[0].remove(source)
#     for int in new_ints[0]:
#         new_roads = intersections_gpd.loc[int]['Roads']
#         new_roads = ast.literal_eval(new_roads)
#         print(new_roads)
#         roads_gpd.loc[new_roads[0], 'geometry'].plot(ax=ax)
#     intersections_gpd.loc[new_ints[0], 'geometry'].plot(ax=ax)

# intersections = roads_gpd.loc[source]['Intersections']
# print(intersections)
# intersections = ast.literal_eval(intersections)     # GeoPandas thinks that this nested list is a string; so we need to convert it into a list
# intersections_gpd.loc[intersections[0], 'geometry'].plot(ax=ax)
# roads_gpd.loc[[source], 'geometry'].plot(ax=ax)
# for intersection in intersections[0]:
#     # print(intersection)
#     intersections_gpd.loc[[intersection], 'geometry'].plot()

plt.show()