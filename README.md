# IoT_Waste_Collection


Codes to optimize the route of a truck that collects weight. Input is .xlsx file with locations and weights of gargabe bins and output is route of the trucks.

Requires api access to google matrix distance api and google maps, free trial is available


relevant links: 

matrix distance: 
https://strategyanalytics.medium.com/create-a-distance-matrix-in-python-with-the-google-maps-api-737dd0fc8081
https://medium.com/how-to-use-google-distance-matrix-api-in-python/how-to-use-google-distance-matrix-api-in-python-ef9cd895303c



rota nova:

url completa
https://www.google.com/maps/dir/'-15.7954282,-47.9870223'/'-15.738114,-47.7712792'/'-15.6892512,-47.8219172'/'-15.7188221,-47.8874016'/'-15.7416731,-47.893982'/'-15.7383457,-47.8949742'/'-15.7580608,-47.8917449'/'-15.7593062,-47.8893499'/'-15.7616948,-47.8845576'/'-15.7683904,-47.8812069'/@-15.7385694,-47.947259,12z/data=!3m1!4b1!4m42!4m41!1m3!2m2!1d-47.9870223!2d-15.7954282!1m3!2m2!1d-47.7712792!2d-15.738114!1m3!2m2!1d-47.8219172!2d-15.6892512!1m3!2m2!1d-47.8874016!2d-15.7188221!1m3!2m2!1d-47.893982!2d-15.7416731!1m3!2m2!1d-47.8949742!2d-15.7383457!1m3!2m2!1d-47.8917449!2d-15.7580608!1m3!2m2!1d-47.8893499!2d-15.7593062!1m3!2m2!1d-47.8845576!2d-15.7616948!1m3!2m2!1d-47.8812069!2d-15.7683904!3e0?hl=pt


url ate o limite
https://www.google.com/maps/dir/'-15.7954282,-47.9870223'/'-15.738114,-47.7712792'/'-15.6892512,-47.8219172'/'-15.7188221,-47.8874016'/'-15.7416731,-47.893982'/'-15.7383457,-47.8949742'/'-15.7580608,-47.8917449'/'-15.7593062,-47.8893499'/'-15.7616948,-47.8845576'/'-15.7683904,-47.8812069'/'-15.7683904,-47.8812069'/'-15.7954282,-47.9870223'/

outras rotas
https://www.google.com/maps/dir/'-15.7683904,-47.8812069'/'-15.7954282,-47.9870223'/@-15.7635859,-47.9677222,13z/data=!3m1!4b1!4m10!4m9!1m3!2m2!1d-47.8812069!2d-15.7683904!1m3!2m2!1d-47.9870223!2d-15.7954282!3e0?hl=pt


https://www.google.com/maps/dir/'-15.7954282,-47.9870223'/'-15.738114,-47.7712792'/'-15.6892512,-47.8219172'/'-15.7188221,-47.8874016'/'-15.7416731,-47.893982'/'-15.7383457,-47.8949742'/'-15.7580608,-47.8917449'/'-15.7593062,-47.8893499'/'-15.7616948,-47.8845576'/'-15.7683904,-47.8812069'/'-15.7683904,-47.8812069'/'-15.7954282,-47.9870223'/


rota antiga
https://www.google.com/maps/dir/'-15.7954282,-47.9870223'/'-15.738114,-47.7712792'/'-15.6892512,-47.8219172'/'-15.7188221,-47.8874016'/'-15.7416731,-47.893982'/'-15.7383457,-47.8949742'/'-15.7580608,-47.8917449'/'-15.7593062,-47.8893499'/'-15.7600264,-47.8828874'/'-15.7559142,-47.8848515'/'-15.7616948,-47.8845576'/'-15.7683904,-47.8812069'/'-15.7775305,-47.8835358'/'-15.7744312,-47.9002624'/'-15.788844,-47.8938437'/'-15.7954282,-47.9870223'/

###Trying other heuristics

86562
5240
0-2-1-3-6-7-8-9-5-4-0

N ACHOU: EVALUATOR STRATEGY, SWEEP, ALL UNPERFORMED, BEST INSERTION, 
MAIOR DISTANCIA: SAVINGS 

OUTROS: MESMA COISA

METAheuristica
OBJECTIVE TABU N FUNCIONOU

ver como escrever as unidades e siglas, se usar adicionar na lista
O programa rodou em um computador com processador Intel(R) Core(TM) i7-8565U CPU @ 1.80GHz com 8gb de memória RAM.

rota atual:
Tempo para rodar API: 29.227086067199707
Tempo para rodar OR-Tools: 1.006389856338501

rota nova: 
Tempo para rodar API: 13.201993942260742
Tempo para rodar OR-Tools: 1.0198352336883545


