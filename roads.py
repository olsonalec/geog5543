import geopandas as gpd
import pandas as pd
import time
import matplotlib.pyplot as plt

roads = gpd.read_file(r"C:\Users\alec.olson\Documents\Centerlines\Plymouth_Roads.geojson")

intersections = gpd.read_file(r"C:\Users\alec.olson\Documents\Centerlines\Plymouth_Intersections.geojson")

print(roads.head())
print(intersections.head())

start_time = time.time()

roads_newlist = [] # a list of roads that connect to each intersections
                    # this is a list of lists; each outer element is an intersection
                    # each inner element is an index into the 'roads' GeoDataFrame
for intersection in intersections.itertuples():
    indices = []
    for road in roads.itertuples():
        if intersection.geometry.intersects(road.geometry):
            indices.append(road.Index)
            # indices.append(road.OBJECTID)
    roads_newlist.append(indices)


newDF = gpd.GeoDataFrame(pd.Series(roads_newlist))
intersections['Roads'] = newDF
print(intersections.head())



intersections_newlist = [] # a list of roads that connect to each intersections
                    # this is a list of lists; each outer element is an intersection
                    # each inner element is an index into the 'roads' GeoDataFrame
for road in roads.itertuples():
    indices = []
    for intersection in intersections.itertuples():
        if road.geometry.intersects(intersection.geometry):
            indices.append(intersection.Index)
            # indices.append(intersection.OBJECTID)
    intersections_newlist.append(indices)

roads_speedlimit = []
for road in roads.itertuples():
    road_type = road.ROUTE_SI_1
    if road_type in ['U.S.', 'State', 'Interstate']:
        roads_speedlimit.append(60)
    elif road_type in ['County']:
        roads_speedlimit.append(45)
    elif road_type in ['Municipal', 'Signed, Other', 'Not Signed or Not Applicable']:
        roads_speedlimit.append(30)

print(roads_speedlimit)

speedlimit_df = gpd.GeoDataFrame(pd.Series(roads_speedlimit))

road_intersection_df = gpd.GeoDataFrame(pd.Series(intersections_newlist))
roads['Intersections'] = road_intersection_df
roads['Speedlimit'] = speedlimit_df
print(roads.head())

roads.plot()
plt.show()



intersections.to_file("intersections_with_indices.geojson", driver="GeoJSON")
roads.to_file("roads_with_indices.geojson", driver="GeoJSON")


end_time = time.time()
print(f"Total time: {end_time - start_time}")