import geopandas as gpd
import matplotlib.pyplot as plt
import ast


roads_gpd = gpd.read_file('roads_prepped.json')
intersections_gpd = gpd.read_file('intersections_prepped.json')

# roads_gpd.plot(column='Speedlimit')
# intersections_gpd.loc[[88],'geometry'].plot()

# print(roads_gpd.info())
# print(type(roads_gpd.loc[45]['Speedlimit']))

source = 628     # an intersection
dest = 88       # an intersection

print(intersections_gpd.loc[source])

fig, ax = plt.subplots()

roads = intersections_gpd.loc[source]['Roads']      # these are the roads that connect to the source intersection
intersections_gpd.loc[[source], 'geometry'].plot(ax=ax)
roads = ast.literal_eval(roads)     # GeoPandas thinks that this nested list is a string; so we need to convert it into a list
roads_gpd.loc[roads[0], 'geometry'].plot(ax=ax)

for road in roads[0]:
    new_ints = roads_gpd.loc[road]['Intersections']
    new_ints = ast.literal_eval(new_ints)
    new_ints[0].remove(source)
    for int in new_ints[0]:
        new_roads = intersections_gpd.loc[int]['Roads']
        new_roads = ast.literal_eval(new_roads)
        print(new_roads)
        roads_gpd.loc[new_roads[0], 'geometry'].plot(ax=ax)
    intersections_gpd.loc[new_ints[0], 'geometry'].plot(ax=ax)

# intersections = roads_gpd.loc[source]['Intersections']
# print(intersections)
# intersections = ast.literal_eval(intersections)     # GeoPandas thinks that this nested list is a string; so we need to convert it into a list
# intersections_gpd.loc[intersections[0], 'geometry'].plot(ax=ax)
# roads_gpd.loc[[source], 'geometry'].plot(ax=ax)
# for intersection in intersections[0]:
#     # print(intersection)
#     intersections_gpd.loc[[intersection], 'geometry'].plot()

plt.show()