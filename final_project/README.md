# Final Project, GEOG 5543
Arlan Hegenbarth and Alec Olson

## Realtime Ideal Weather Finder
This program finds the locations in the U.S. that currently have the most similar weather conditions to those specified by the user. The user sets their ideal weather, using temperature, relative humidity, windspeed, and sky conditions (cloudy, rainy, or snowy). Then, the program returns locations in the contiguous United States where the weather is most similar to those conditions.\
The cell in which the user should specify their weather conditions is at the bottom of the notebook, clearly labeled. the user can also specify two advanced settings. One determines what percentage of the U.S. to return. The default setting finds the top 2% of locations in the U.S. that are most similar to the user's desired weather. The user can adjust this percentage up or down.\
The user can also adjust the weights that are given to each parameters. By default, the program gives the most weight to temperature and the least weight to sky conditions.

### Structure
All the code to run this program is in the `Final_Project.ipynb` notebook. More specifics regarding the structure of the program can be found above each cell in the notebook.\
The program begins by retrieving current weather data from every NOAA weather station in the contiguous United States that has data. This data is converted into a GeoPandas GeoDataFrame. Next, the program uses Inverse Distance Weighting to interpolate a score for each 0.1 x 0.1 degree square in the U.S. Locations with low scores have weather that is very similar to the what the user entered as input. Finally, the program returns the top 2% of polygons in the U.S. that have the lowest score. These are the areas that have current weather that is most similar to what the user requested.

### How to run
Run each code cell in order. As mentioned above, the final code cell contains the parameters that the user can adjust. The place to do this is clearly marked in the final cell. The user can adjust six different weather parameters as well as the weights given to each parameter and the percentage of polygons returned.\
If the user wishes to update their desired weather parameters, only section 6 (the final section) needs to be run again. If the user wishes to refresh the weather data, sections 3, 5, and 6 need to be run again. All sections need to be run on intial opening and setup.