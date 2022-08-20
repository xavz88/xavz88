# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 10:27:59 2022

@author: Xavz88
"""
from shapely.geometry import Point


class Distrito():
    
    def __init__(self, idd):
        
        self.poblaciones = []
        self.id = idd
        self.centro = None
        self.Habitantes = None
        
    def __eq__(self,otro):
        
        return self.Habitantes == otro.Habitantes
    
    def contiene(self, unidad):
        
        return unidad in self.poblaciones
    
    def hallarCentro(self):
        
        tempX = 0
        tempY = 0
        
        n = len(self.poblaciones)
        
        for pueblo in self.poblaciones:
            
            tempX += float(pueblo.centro.x)
            tempY += float(pueblo.centro.y)
            
        X = tempX/n
        Y = tempY/n
        
        centro = Point(X,Y)
        # buscamos a que centro de poblacion esta mas cerca este centro hallado
        
        listaDistancias = []
        
        for i,pueblo in enumerate(self.poblaciones):
            
            listaDistancias.append(float(pueblo.centro.distance(centro)))
        
        posicionCentro = listaDistancias.index(min(listaDistancias))
        
        for pueblo in self.poblaciones:
            pueblo.esCentro = False
        
        self.poblaciones[posicionCentro].esCentro = True
        
        self.centro = self.poblaciones[posicionCentro]
        
        
    def sumaHabitantes(self):
        
        listaHabitantes = [pueblo.habitantes for pueblo in self.poblaciones]
        self.Habitantes = sum(listaHabitantes)  
        
            
                
                
            
        
        
    
  
