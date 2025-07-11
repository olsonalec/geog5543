`dijkstra_overhaul_naive.py`
- This script implements Dijkstra's Algorithm using a naive approach to store information about the vertices. It uses an unsorted list that does not grow or shrink. This means that, for every iteration of the algorithm where it searches for the vertex with the lowest cost, the algorithm has to conduct a linear search through the list, resulting in a runtime of O(n) for each iteration. Not only that, but the search also has to check if each node has already been visited. This is also a linear time problem. If the node has already been visited, it is skipped because Dijkstra's Algorithm only visits each node once.


### Structure
There are two main data structures used in this algorithm.
1. `graph`
    - This data structure represents the network of roads and intersections. It is implemented as a dictionary. Each key is an index that corresponds with an intersection in the intersections GeoDataFrame. Each value is a list of tuples. The first value of each tuple is an index that corresponds with another intersection in the intersections GeoDataFrame - these are intersections that are one road segment away from the original intersection. The second value of each tuple is the weight (in this case, the number of seconds to travel) to reach that next intersection.
2. `vertex_array`
    - This array stores the current total cost to reach each intersection from the source intersection. It is implemented as a list, and each element is a `Vertex` object. Each `Vertex` object has three attributes:
        - The cost to reach that vertex from the starting intersection. This attribute is initialized to `infinity` for each vertex except the starting vertex, which gets initialized to `0`.
        - A pointer to the `Vertex` object that comes before this node in the path. This attribute is used to construct the shortest path to the destination intersection after Dijkstra's Algorithm is finished.
        - The index into the intersections GeoDataFrame where the data about this intersection is stored.

### Implementation of Dijkstra's Algorithm
- This code follows the general implementation of Dijkstra's Algorithm. I am not going to replicate the complete pseudocode here.
- Briefly:
    - The algorithm starts with the source intersection. Each neighboring intersection's cost is updated to reflect the cost of traveling there from the source intersection. The intersection with the lowest cost is selected to examine next. From this new intersection, its neighboring intersections are examined, and the cost to reach these neighbors is calculated. The process continues, and the intersection with the new lowest cost is selected to examine next. This process continues until the destination vertex is found.
    - Dijkstra's Algorithm does not visit the same node twice. Therefore, it is important to keep track of which nodes have been visited. I accomplish this through the use of a list (`visited_vertices`) that contains the indices of the intersections that have already been visited. When the algorithm is searching for the intersection with the lowest cost, it must skip these intersections that have already been visited.

### Runtime and Inefficiences
With each iteration of the algorithm, many inefficient checks must be made:\
*None of the following lists are sorted*
1. The algorithm must first check if the destination intersection has already been visited. If the destination intersection has already been visited, the algorithm will terminate. This is accomplished through a linear search of the `visited_vertices` list mentioned above.
2. The algorithm must find the intersection with the lowest cost that that has also not yet been visited. This is accomplished through a linear search of the `vertex_array` list. However, it is possible that the intersection with the absolute lowest cost has already been visited. Therefore, when the algorithm finds a new lowest-cost intersection, it must check to see if this intersection has already been visited, which requires a linear search through the `visited_vertices` array.