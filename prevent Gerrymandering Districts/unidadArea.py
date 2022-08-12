# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 00:30:50 2022

@author: Xavz88
"""

class UnidadArea():
    
    def __init__(self, id_, habitantes, centro, nombre, geometria):
        
        self.id = id_
        self.nombre = nombre
        self.habitantes = habitantes
        self.centro = centro
        self.geometria = geometria
        self.esCentro = False
    
    def __eq__ (self, unidad):
        
        return self.nombre == unidad.nombre
    
    def __hash__ (self):
        
        return hash(self.nombre)
    
    