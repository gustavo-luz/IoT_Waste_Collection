import pandas as pd

length_to_split = [16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16]



number_containers = 14
lista = number_containers*[number_containers]

print(lista)
#tamanho = len(list)

#print(tamanho*list)

df = pd.read_excel('IoT_Waste_Collection/rota_nova.xlsx')

print(len(df['ID'])-1)

capacities = df['PESAGENS']
#print(capacities)

demands = df['PESAGENS'].values.tolist()
#print(demands)

#data['demands'] = [800,800,800,500,450,400,350,550,420]
#print(data['demands'])