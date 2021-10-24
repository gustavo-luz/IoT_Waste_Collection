
"""
CHOSE THIS OPTION!
"""


import pandas as pd
import googlemaps
from itertools import tee
import config

#input: CSV file with id,latitude, longitude and capacities
# desired output: list with matrix distance for each point

df = pd.read_excel('IoT_Waste_Collection/IOTSCv2.xlsx')
#print(df)

API_key = config.api_key #enter your google maps api key here
gmaps = googlemaps.Client(key=API_key)

# works but creates a df , no meters found
# https://strategyanalytics.medium.com/create-a-distance-matrix-in-python-with-the-google-maps-api-737dd0fc8081

#empty list - will be used to store calculated distances
time_list = []
distance_list = []
origin_id_list = []
destination_id_list = []

for (i1, row1) in df.iterrows():
  #print("origin")
  #print(row1['ID'])
  LatOrigin = row1['latitude']
  LongOrigin = row1['longitude']
  origin = (LatOrigin, LongOrigin)
  origin_id = row1['ID']
  for (i2, row2) in  df.iterrows():
    #print("destination id")
    #print(row2['ID'])
    LatDestination = row2['latitude']
    LongDestination = row2['longitude']
    destination_id = row2['ID']
    destination = (LatDestination, LongDestination)
    result = gmaps.distance_matrix(origin, destination, mode='driving')
    result_distance = result["rows"][0]["elements"][0]["distance"]["value"]
    result_time = result["rows"][0]["elements"][0]["duration"]["value"]
    time_list.append(result_time)
    distance_list.append(result_distance)
    origin_id_list.append(origin_id)
    destination_id_list.append(destination_id)

size=(len(df.coordinates))
print(distance_list)


from itertools import islice
  
# Input list initialization
Input = distance_list
  
# list of length in which we have to split
length_to_split = [16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16]
  
# Using islice
Inputt = iter(Input)
Output = [list(islice(Inputt, elem))
          for elem in length_to_split]
  
# Printing Output
print("Initial list is:", Input)
print("Split length list: ", length_to_split)
print("List after splitting", Output)




"""
output = pd.DataFrame(distance_list, columns = ['Distance in meter'])
output['duration in seconds'] = time_list
output['origin_id'] = origin_id_list
output['destination_id'] = destination_id_list

output_v1 = pd.merge(output, df, how = "left", left_on = "origin_id", right_on = "ID")
output_v2 = pd.merge(output_v1, df, how = "left", left_on = "destination_id", right_on = "ID")
print(output_v1)

#output_v2[['city_x', 'city_y', 'Distance in meter', 'duration in seconds']]
#output_v2.to_excel('Coordinates_distancematrix.xlsx')
"""


