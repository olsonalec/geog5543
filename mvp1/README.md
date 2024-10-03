# MVP 1: Finding Similar Weather in Different Locations on Earth

## Problem
The final iteration of this project is a program that will tell the user what city on Earth currently has the most similar weather conditions compared to the user's location.

## Solution
The user will enter the name of their current city, and then the program will gather real-time weather data from thousands of cities around the globe. This data will include air temperature, wind speed, relative humidity, precipitation, and possibly other things. The program will generate a score for each city, with a higher score indicating that the city's weather is more similar to the user's city. Then, the program will return the name of the city with the highest score to the user, as well as the weather conditions in both cities.

## Challenges
1. Logistical: It will be logistically difficult to gather real-time weather data from locations around the world. The program will need to interact with many different governmental agencies' APIs (for example, NOAA in the U.S. and ECMWF in Europe) in order to build a representative sample of global weather conditions.
2. Scientific: How should the program quantify different aspects of weather? How should it produce a single score that combines many different aspects of weather? For example, how does a 10 degree difference in temperature compare to a 10 mph difference in wind speed? What units should be used? Even within the same unit system, there are different standards of measurement. For example, m/s and km/h are both common measurements of wind speed in the metric system.

## My MVP
My MVP features many simplifications compared to the final product. First of all, my MVP will use Minneapolis as the starting city and will only compare cities within the U.S. This allows me to only worry about gathering data from one source: the NOAA. 

## The Program
`mvp1.py` features all the code for this MVP. It is divided into multiple sections.
1. The first block of code gathers the current weather conditions in Minneapolis and prints the current temperature to the terminal.
2. The second block finds all the NOAA-defined zones in the U.S. and the weather Observation Stations that are in those zones.
3. The third block gathers the current weather conditions from each Observation Station.
4. The fourth block finds the Observation Station that has the most similar weather compared to Minneapolis.
5. The fifth block finds the name of the location where the Observation Station is located. The program then prints out the name of this location, along with the current weather conditions both here and in Minneapolis.