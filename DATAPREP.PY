
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


"""
#empty list - will be used to store calculated distances
time_list = []
distance_list = []
origin_id_list = []
destination_id_list = []

for (i1, row1) in df.iterrows():
  print("origin")
  print(row1['ID'])
  LatOrigin = row1['Location (Latitude)']
  LongOrigin = row1['Location (Longitude)']
  origin = (LatOrigin, LongOrigin)
  origin_id = row1['ID']
  for (i2, row2) in  df.iterrows():
    print("destination id")
    print(row2['ID'])
    LatDestination = row2['Location (Latitude)']
    LongDestination = row2['Location (Longitude)']
    destination_id = row2['ID']
    destination = (LatDestination, LongDestination)
    result = gmaps.distance_matrix(origin, destination, mode='driving')
    result_distance = result["rows"][0]["elements"][0]["distance"]        
    ["value"]
    result_time = result["rows"][0]["elements"][0]["duration"]["value"]
    time_list.append(result_time)
    distance_list.append(result_distance)
    origin_id_list.append(origin_id)
    destination_id_list.append(destination_id)

output = pd.DataFrame(distance_list, columns = ['Distance in meter'])
output['duration in seconds'] = time_list
output['origin_id'] = origin_id_list
output['destination_id'] = destination_id_list

output_v1 = pd.merge(output, df, how = "left", left_on = "origin_id", right_on = "ID")
output_v2 = pd.merge(output_v1, df, how = "left", left_on = "destination_id", right_on = "ID")
print(output_v1)

output_v2[['city_x', 'city_y', 'Distance in meter', 'duration in seconds']]
output_v2.to_excel('Coordinates_distancematrix.xlsx')
"""


"""
#pairwise function implemented to iterate through two consecutive rows (pairs) in a data frame
def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

#empty list - will be used to store calculated distances
list = [0]

# Loop through each row in the data frame using pairwise
for (i1, row1), (i2, row2) in pairwise(df.iterrows()):
      #Assign latitude and longitude as origin/departure points
      LatOrigin = row1['Location (Latitude)'] 
      LongOrigin = row1['Location (Longitude)']
      print(LatOrigin,LongOrigin)
      origins = (LatOrigin,LongOrigin)

      #Assign latitude and longitude from the next row as the destination point
      LatDest = row2['Location (Latitude)']   # Save value as lat
      LongDest = row2['Location (Longitude)'] # Save value as lat
      destination = (LatDest,LongDest)

      #pass origin and destination variables to distance_matrix function# output in meters
      result = gmaps.distance_matrix(origins, destination, mode='driving')["rows"][0]["elements"][0]["distance"]["value"]
      
      #append result to list
      list.append(result)
      print(list)

      #df['Distance'] = list
      #df.to_csv('calculated_distances.csv', sep=';', index=None)
"""

#origin = (-15.760026,-47.882887 ) 


print(len(df.coordinates))  

origin = df.coordinates[0]
destinations = df.coordinates


actual_distance = []


for destination in destinations:
    result = gmaps.distance_matrix(origin, destination, mode='driving')["rows"][0]["elements"][0]["distance"]["value"]  
    result = result/1000
    actual_distance.append(result)
  
#Add the list of coordinates to the main data set

df["distance (Km)"] = actual_distance

#print(df.head(15))
print(df)



#TODO make a for using each row (id 2,3,4...) as origin and transform distance collumn into a list that goes as input to next routing program

for i in range(0,len(df.coordinates)):
  

  origin = df.coordinates[i]
  destinations = df.coordinates


  actual_distance = []


  for destination in destinations:
      result = gmaps.distance_matrix(origin, destination, mode='driving')["rows"][0]["elements"][0]["distance"]["value"]  
      result = result/1000
      actual_distance.append(result)
    
print(actual_distance)
"""
#Add the list of coordinates to the main data set

  df["distance (Km)"] = actual_distance

#print(df.head(15))
print(df)

"""