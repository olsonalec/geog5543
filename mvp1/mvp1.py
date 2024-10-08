'''
Written by Alec Olson
Last Edited 10/03/2024
'''

import requests
import time

start_time = time.time()

current_time = time.asctime()

'''
Section 1
Get the current temperature and relative humidity at the MSP airport.
'''
mpls = requests.get('https://api.weather.gov/stations/KMSP/observations/latest')
mpls = mpls.json()
mplsTemp = mpls['properties']['temperature']['value']
mplsHumidity = mpls['properties']['relativeHumidity']['value']

'''
Section 2
Get a list of NOAA zones in the U.S.
Iterate through the zones and grab the Observation Stations (from which we can grab current weather data).
Remove duplicates from the list of Observation Stations.
'''
zones = requests.get('https://api.weather.gov/zones?type=land')
zones = zones.json()

stations = []
for i in range(len(zones['features'])):
    if zones['features'][i]['properties']['state'] != 'MN':         # exclude MN weather stations from comparison
        zoneID = zones['features'][i]['properties']['id']
        observationStations = zones['features'][i]['properties']['observationStations']
        if observationStations != []:
            station = observationStations[0][33:]
            stations.append(station)

stations = list(set(stations))

'''
Section 3
Iterate through all the Observation Stations and, if they return a valid response (200), grab the current temperature and relative humidity.
Store all these values in a list [stationID, temp, relativeHumidity], and then store all these lists in stationWeatherList.
'''
stationWeatherList = []
stationsToCompare = stations[:]     # if we want, we can compare only a subset of the total stations

print(f'\nThere are {len(stationsToCompare)} stations in the U.S. to compare.\n')

for station in stationsToCompare:
    weather = requests.get(f'https://api.weather.gov/stations/{station}/observations/latest')
    if weather.status_code == 200:
        weather = weather.json()
        temp = weather['properties']['temperature']['value']
        relativeHumidity = weather['properties']['relativeHumidity']['value']
        weatherList = [station, temp, relativeHumidity]
        validData = True
        for item in weatherList:
            if item == None:
                validData = False
        if validData == True:
            stationWeatherList.append(weatherList)


'''
Section 4
Find the Observation Station that has a temperature and relatively humidity most similar to the MSP airport.
'''
for station in stationWeatherList:

    # calculate absolute difference in temp
    tempDiff = abs(mplsTemp - station[1])

    # calculate absolute difference in humidity - this is given half the weight that temp is given
    humidityDiff = abs(mplsHumidity - station[2]) / 2

    # calculate the total score for the station
    totalScore = tempDiff + humidityDiff
    station.insert(0, totalScore)

# sort the list of weather stations so that the most similar station is at the front of the list
stationWeatherList.sort()

        
'''
Section 5
Find the name of the location where the Observation Station is located.
Print out the current weather at MSP airport.
Print out the other Observation Station's name and its current weather.
'''

closestStation = stationWeatherList[0]
closestStationID = closestStation[1]
closestStationTemp = closestStation[2] * 1.8 + 32       # convert Celsius to Fahrenheit
closestStationHumidity = closestStation[3]

closestStationName = requests.get(f'https://api.weather.gov/stations/{closestStationID}').json()
closestStationName = closestStationName['properties']['name']

mplsTemp = mplsTemp * 1.8 + 32      # convert Celsius to Fahrenheit

print(f'At {current_time}, the weather at MSP airport is {round(mplsTemp)} degrees Fahrenheit with {round(mplsHumidity)}% humidity.\n')
print(f'The location with the most similar current weather is {closestStationName}.\n')
print(f'The current weather at {closestStationName} is {round(closestStationTemp)} degrees Fahrenheit with {round(closestStationHumidity)}% humidity.\n')


end_time = time.time()
print(f'The total time to compare {len(stationsToCompare)} cities was {end_time - start_time} seconds.\n')
