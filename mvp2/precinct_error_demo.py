import geopandas as gpd

mn_precincts_gdb = gpd.read_file('mn_precincts_2019.json')
mn_precincts_gdb.head()

for index, row in mn_precincts_gdb.iterrows():
  # print(row['Precinct'])

  # Attempt to find all the neighboring precincts
  neighbors = mn_precincts_gdb[mn_precincts_gdb.geometry.touches(row['geometry'])]

  '''
  The first error occurs with the precinct Detroit Lakes W-1 P-1, (Precinct ID 270050055) at the point [-95.9041,46.8113].


  Error message:

  shapely.errors.GEOSException: TopologyException: side location conflict at -95.9041 46.811300000000003.
  This can occur if the input geometry is invalid.
  '''