from evolutive import Evolutive
from pandas import read_csv
import geopandas as gpd
from unidadArea import UnidadArea
from copy import deepcopy

    
population_size = 6

mutation_rate = 0.1

child_generation = 3

max_generations = 1

distritos= 4


datos = read_csv("PAD2020.csv", sep=";")
datosGeometricos = gpd.read_file("districts_geometry.geojsonl")
datosGeometricos = datosGeometricos.to_crs(crs='EPSG:3857')

listaPueblos = []


for i in range(len(datos)): 
    #obtenemos los datos vectoriales de la poblacion que tenga el codigo de la fila por la que vamos
    
    shape = gpd.GeoSeries(datosGeometricos['geometry'][i])
    listaPueblos.append(UnidadArea(i, datos.Habitantes[i], shape.centroid, datos.Poblacion[i], shape))
    


modelo = Evolutive(population_size, mutation_rate, max_generations,
                   child_generation, distritos, listaPueblos = deepcopy(listaPueblos))

modelo.resultado()







