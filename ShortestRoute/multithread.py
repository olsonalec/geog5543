import geopandas as gpd
import pandas as pd
import data_prep
import time
from pandarallel import pandarallel
import sys


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

    roads_speedlimit = []

    i = 0
    for road in roads.itertuples():
        speedlimit = road.ROUTESPEED
        if speedlimit == 0:
            roads.loc[i, 'ROUTESPEED'] = 30
        i += 1

    roads_time = [] # will store the amount of time it takes to travel each road segment
    for road in roads.itertuples():
        # road_speed = road.Speedlimit    # Plymouth
        road_speed = road.ROUTESPEED    # Ramsey
        road_distance = road.Shape_Length
        roads_time.append(calculate_time(road_speed, road_distance))

    roads_time_df = gpd.GeoDataFrame(pd.Series(roads_time))
    roads['TimeToTravel'] = roads_time_df

    start_time = time.time()

    # roads_newlist = list(np.zeros(intersections.shape[0]))

    # intersections['Roads'] = roads_newlist

    # print(intersections.head())

    pandarallel.initialize(progress_bar=True)
    intersections['Roads'] = intersections.parallel_apply(data_prep.map_function, axis=1, args=(roads,))

    # intersections['Roads'] = intersections.apply(data_prep.map_function, axis=1, args=(roads,))

    roads['Intersections'] = roads.parallel_apply(data_prep.map_function2, axis=1, args=(intersections,))


    # Calculating the speedlimit and time to travel could also be parallelized
    '''
    Only for Plymouth
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
    '''



    end_time = time.time()
    print(f'Total time: {end_time - start_time}')

    intersections.to_file("Plymouth_Intersections_Prepped.geojson")
    roads.to_file("Plymouth_Roads_Prepped.geojson")
