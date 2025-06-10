import geopandas as gpd
import time

roads = gpd.read_file(r"C:\Users\alec.olson\Documents\Centerlines\Plymouth_Roads.geojson")

intersections = gpd.read_file(r"C:\Users\alec.olson\Documents\Centerlines\Plymouth_Intersections.geojson")

start_time = time.time()

i = 0
for row in intersections.itertuples():
    if i < 100:
        print(row.OBJECTID)
        for road in roads.itertuples():
            if row.geometry.intersects(road.geometry):
                print(road.ROUTE_ID)
        # for road in roads:
        #     if intersection.geometry.intersects(road.geometry):
        #         print(intersection["OBJECTID"])
        
        i += 1
    else:
        break

end_time = time.time()
print(f"Total time: {end_time - start_time}")