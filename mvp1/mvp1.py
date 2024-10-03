import requests

#response = requests.get('https://api.weather.gov/stations?limit=1')
#formatted = response.json()
stationList = []
# for i in range(len(formatted['features'])):
#     #print(formatted['features'][i]['properties']['stationIdentifier'])
#     stationList.append(formatted['features'][i]['properties']['stationIdentifier'])
# print(stationList)
# print(len(stationList))

#response = requests.get('https://api.weather.gov/stations/003HE/observations/latest')
# station = '001HE'
# response = requests.get(f'https://api.weather.gov/stations/{station}/observations/latest')
# print(response.content)
# print(response.status_code)

# for station in stationList:
#     print(station)
#     #print(f'https://api.weather.gov/stations/{station}/observations/latest')
#     response = requests.get('https://api.weather.gov/stations/{station}/forecast')
#     print(response.status_code)
#     if response.status_code == 200:
#         print(response.json())

#print(formatted['features'])
# for i in range(len(formatted['results'])):
#     print(formatted['results'][i])




#Get the current temperature at the MSP airport
mpls = requests.get('https://api.weather.gov/stations/KMSP/observations/latest')
mpls = mpls.json()
mplsTemp = mpls['properties']['temperature']['value']
print(f'Mpls Temp: {mplsTemp}')


# Get a list of NOAA zones in the US (this list might be comprehensive)
zones = requests.get('https://api.weather.gov/zones?type=land')
zones = zones.json()

# Iterate through the zones and grab the Observation Stations (from which we can grab current weather data)
stations = []
for i in range(len(zones['features'])):
    zoneID = zones['features'][i]['properties']['id']
    observationStations = zones['features'][i]['properties']['observationStations']
    if observationStations != []:
        station = observationStations[0][33:]
        stations.append(station)

# Remove duplicates from the list of Observation Stations
stations = list(set(stations))

# Iterate through all the Observation Stations and, if they return a valid response (200), grab the current temp
stationTempList = []
for station in stations[0:100]:
    #print(station)
    weather = requests.get(f'https://api.weather.gov/stations/{station}/observations/latest')
    #print(weather.status_code)
    if weather.status_code == 200:
        weather = weather.json()
        temp = weather['properties']['temperature']['value']
        if temp != None:
            print(f'{station} {temp}')
            stationTempList.append([station, temp])

# Find the Observation Station that has a temperature most similar to MSP airport
closestTemp = 1000
closestTempDiff = 1000
closestStation = ''
for station in stationTempList:
    tempDiff = mplsTemp - station[1]
    if abs(tempDiff) < abs(closestTempDiff):
        closestStation = station[0]
        closestTemp = station[1]
        closestTempDiff = tempDiff
        

# Find the name of the location where the Observation Station is located
closestStationName = requests.get(f'https://api.weather.gov/stations/{closestStation}').json()
closestStationName = closestStationName['properties']['name']
print()
print(f'The current temperature at {closestStationName} is {closestTemp} degrees Celsius.')
#print(f'{closestStation} {closestTemp}')
print(f'The current temperature at MSP airport is {mplsTemp} degrees Celsius.')


        #print(f'{station} {weather['properties']['temperature']['value']}')
#        weather = requests.get('')
    #observation = requests.get(f'https://api.weather.gov/zones/forecast/{zones['features'][i]['properties']['id']}/observations')
    #print(observation.status_code)