import geopandas as gpd
import pandas as pd
import time
from multiprocessing import Pool

def mph_to_ms(speed):
    # converts mph to m/s
    return (speed * 1609.344) / (60 * 60)

def calculate_time(speed, distance):
    # speed is in mph, distance is in meters
    speed_in_ms = mph_to_ms(speed)
    return distance / speed_in_ms


roads = gpd.read_file(r"Plymouth_Roads.geojson")

intersections = gpd.read_file(r"Plymouth_Intersections.geojson")

print(roads.head())
print(intersections.head())


def map_function(intersection, road_geodataframe):
    indices = [[]]
    for road in road_geodataframe.itertuples():
        if intersection['geometry'].intersects(road.geometry):
            indices[0].append(road.Index)
    return indices

def map_function2(road, intersection_geodataframe):
    indices = [[]]
    for intersection in intersection_geodataframe.itertuples():
        if road.geometry.intersects(intersection.geometry):
            indices[0].append(intersection.Index)
    return indices

'''
start_time = time.time()


roads_newlist = [] # a list of roads that connect to each intersections
                    # this is a list of lists; each outer element is an intersection
                    # each inner element is an index into the 'roads' GeoDataFrame
for intersection in intersections.itertuples():
    indices = [[]]  # this needs to be a nested list because if it was a 1D list, GeoPandas would think that it's storing coordinate data, which it's not
    for road in roads.itertuples():
        if intersection.geometry.intersects(road.geometry):
            indices[0].append(road.Index)
    roads_newlist.append(indices)


newDF = gpd.GeoDataFrame(pd.Series(roads_newlist))
intersections['Roads'] = newDF
print(intersections.head())


intersections_newlist = [] # a list of roads that connect to each intersections
                    # this is a list of lists; each outer element is an intersection
                    # each inner element is an index into the 'roads' GeoDataFrame
for road in roads.itertuples():
    indices = [[]]      # this needs to be a nested list because if it was a 1D list, GeoPandas would think that it's storing coordinate data, which it's not
    for intersection in intersections.itertuples():
        if road.geometry.intersects(intersection.geometry):
            indices[0].append(intersection.Index)
    intersections_newlist.append(indices)



roads_speedlimit = []       # will store the speed limit on each road segment
for road in roads.itertuples():
    road_type = road.ROUTE_SI_1
    if road_type in ['U.S.', 'State', 'Interstate']:
        roads_speedlimit.append(60)
    elif road_type in ['County']:
        roads_speedlimit.append(45)
    elif road_type in ['Municipal', 'Signed, Other', 'Not Signed or Not Applicable']:
        roads_speedlimit.append(30)

road_intersection_df = gpd.GeoDataFrame(pd.Series(intersections_newlist))
speedlimit_df = gpd.GeoDataFrame(pd.Series(roads_speedlimit))
roads['Intersections'] = road_intersection_df
roads['Speedlimit'] = speedlimit_df

roads_time = [] # will store the amount of time it takes to travel each road segment
for road in roads.itertuples():
    road_speed = road.Speedlimit
    road_distance = road.Shape_Length
    roads_time.append(calculate_time(road_speed, road_distance))

roads_time_df = gpd.GeoDataFrame(pd.Series(roads_time))
roads['TimeToTravel'] = roads_time_df

print(roads.head())




intersections.to_file("intersections_prepped.geojson")
roads.to_file("roads_prepped.geojson")


end_time = time.time()
print(f"Total time: {end_time - start_time}")
'''