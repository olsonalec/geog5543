Workflow:

Download Metro Road Centerlines from the Minnesota Geospatial Commons (https://gisdata.mn.gov/dataset/us-mn-state-metrogis-trans-road-centerlines-gac) as a shapefile.

Open the shapefile in ArcGIS Pro.

Delete all the roads that are not in the seven-county metro area.

Delete unnecessary attributes. Keep FID, Shape, ROUTE_ID, ST-CONCAT, CTU_NAME_L, CTU_NAME_R, ROUTESPEED, and Shape_Leng.

Follow steps to add intersection points to the roads layer (https://support.esri.com/en-us/knowledge-base/how-to-create-points-on-line-intersections-in-arcgis-pr-000025044). In the "Statistics Fields," select all the attributes, except for Shape_Leng, and select "First" for all of them, with one exception. ROUTESPEED should be "Minimum." Run the tool, then remove the newly-added prefixes from the attribute names.

Use the Multipart to Singlepart feature to get rid of multipart points.
	Problem: Now there are some intersections that have two points associated with them.
	Solution: Use "Add XY Coordinates" tool to add x and y values to the attribute table for the intersections layer.
		  Use "Dissolve" tool on the x and y values to remove duplicate points. You don't need to add any of the attributes to the "Statistics 			  Fields" because it is not important to preserve any of them. Be sure to uncheck the box that says "Create multipart features."

Manually remove intersections that are not possible (ex. 494 and Schmidt Lake Rd; 494 and Chankahda- even though the roads intersect on the 2D map, it is not possible to drive from one onto the other in real life.) Merge the affected road segments together.

Use the "Calculate Geometry Attributes" features to add four attributes to each line segment: starting x coordinate, starting y coordinate, ending x coordinate, and ending y coordinate. Use the "Dissolve" tool on these four attributes to remove duplicate line segments. Do not allow the creation of multipart features. In the "Statistics Fields", select all the attributes and select "First" for the Statistic Type. This will preserve the other attributes through the dissolve operation. Uncheck the "Create multipart features" box.

Manually remove intersections that don't exist. For example, on a 2D map, 494 intersects with Schmidt Lake Road in Plymouth. However, in reality, it is not possible to get from 494 to Schmidt, or vice versa, so these intersections on the map need to be removed.

Use a city county layer, both of which can also be found on the MN Geospatial Commons, to clip the roads and intersections layers based on county or city.

Export Roads layer as GeoJSON.
Export Intersections layer as GeoJSON.

Load both files into GeoPandas.

Warning! My Roads layer for just Ramsey county had about 24,763 road segments, and the Intersections layer for Ramsey had about 13,840 intersection points. The data prep stage (`multithread.py`) for Ramsey County alone took about 25 minutes. The entirety of the dataset (the full seven-county metro area) has about 162,730 road segments and 91,392 intersection points.
