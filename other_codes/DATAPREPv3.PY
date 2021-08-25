
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
"""
print(df)


#TODO make a for using each row (id 2,3,4...) as origin and transform distance collumn into a list that goes as input to next routing program

for i in range(0,len(df.coordinates)):
  

  origin = df.coordinates[i]
  print("origem",origin)
  destinations = df.coordinates
  print("destino",destinations)


  actual_distance = []

  for destination in destinations:
      
      result = gmaps.distance_matrix(origin, destination, mode='driving')["rows"][0]["elements"][0]["distance"]["value"]  
      result = result/1000
      actual_distance.append(result)
      print("lista",i,actual_distance)
      #put it inside a df

      #print(df)
    
print(actual_distance)
#print(df)
"""
#Add the list of coordinates to the main data set

  df["distance (Km)"] = actual_distance

#print(df.head(15))
print(df)

"""