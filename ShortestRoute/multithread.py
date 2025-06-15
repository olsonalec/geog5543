import geopandas as gpd
import pandas as pd
import data_prep
import time
from pandarallel import pandarallel


def mph_to_ms(speed):
    # converts mph to m/s
    return (speed * 1609.344) / (60 * 60)

def calculate_time(speed, distance):
    # speed is in mph, distance is in meters
    speed_in_ms = mph_to_ms(speed)
    return distance / speed_in_ms


if __name__ == '__main__':
    roads = gpd.read_file('Plymouth_Roads.geojson')
    intersections = gpd.read_file('Plymouth_Intersections.geojson')

    start_time = time.time()

    # roads_newlist = list(np.zeros(intersections.shape[0]))

    # intersections['Roads'] = roads_newlist

    # print(intersections.head())

    pandarallel.initialize(progress_bar=True)
    intersections['Roads'] = intersections.parallel_apply(data_prep.map_function, axis=1, args=(roads,))

    # intersections['Roads'] = intersections.apply(data_prep.map_function, axis=1, args=(roads,))

    roads['Intersections'] = roads.parallel_apply(data_prep.map_function2, axis=1, args=(intersections,))


    # Calculating the speedlimit and time to travel could also be parallelized
    roads_speedlimit = []       # will store the speed limit on each road segment
    for road in roads.itertuples():
        road_type = road.ROUTE_SI_1
        if road_type in ['U.S.', 'State', 'Interstate']:
            roads_speedlimit.append(60)
        elif road_type in ['County']:
            roads_speedlimit.append(45)
        elif road_type in ['Municipal', 'Signed, Other', 'Not Signed or Not Applicable']:
            roads_speedlimit.append(30)
    
    speedlimit_df = gpd.GeoDataFrame(pd.Series(roads_speedlimit))
    roads['Speedlimit'] = speedlimit_df

    roads_time = [] # will store the amount of time it takes to travel each road segment
    for road in roads.itertuples():
        road_speed = road.Speedlimit
        road_distance = road.Shape_Length
        roads_time.append(calculate_time(road_speed, road_distance))

    roads_time_df = gpd.GeoDataFrame(pd.Series(roads_time))
    roads['TimeToTravel'] = roads_time_df



    end_time = time.time()
    print(f'Total time: {end_time - start_time}')

    intersections.to_file("intersections_prepped2.geojson")
    roads.to_file("roads_prepped2.geojson")
