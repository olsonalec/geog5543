'''
Written by Alec Olson
Last Edited 10/03/2024
'''

import requests
import time

start_time = time.time()

'''
Section 1
Get the current temperature at the MSP airport and print this temp to the terminal.
'''
mpls = requests.get('https://api.weather.gov/stations/KMSP/observations/latest')
mpls = mpls.json()
mplsTemp = mpls['properties']['temperature']['value']
print(f'Mpls Temp: {mplsTemp}')

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
    zoneID = zones['features'][i]['properties']['id']
    observationStations = zones['features'][i]['properties']['observationStations']
    if observationStations != []:
        station = observationStations[0][33:]
        stations.append(station)

stations = list(set(stations))

'''
Section 3
Iterate through all the Observation Stations and, if they return a valid response (200), grab the current temperature.
'''
stationTempList = []
print(f'There are {len(stations)} stations to compare.')
for station in stations:
    weather = requests.get(f'https://api.weather.gov/stations/{station}/observations/latest')
    if weather.status_code == 200:
        weather = weather.json()
        temp = weather['properties']['temperature']['value']
        if temp != None:
            stationTempList.append([station, temp])

'''
Section 4
Find the Observation Station that has a temperature most similar to MSP airport.
'''
closestTemp = 1000
closestTempDiff = 1000
closestStation = ''
for station in stationTempList:
    tempDiff = mplsTemp - station[1]
    if abs(tempDiff) < abs(closestTempDiff):
        closestStation = station[0]
        closestTemp = station[1]
        closestTempDiff = tempDiff
        
'''
Section 5
Find the name of the location where the Observation Station is located.
'''
closestStationName = requests.get(f'https://api.weather.gov/stations/{closestStation}').json()
closestStationName = closestStationName['properties']['name']
print(f'The current temperature at {closestStationName} is {closestTemp} degrees Celsius.')
print(f'The current temperature at MSP airport is {mplsTemp} degrees Celsius.')


end_time = time.time()
print(f'The total time to compare 100 cities was {end_time - start_time} seconds.')
