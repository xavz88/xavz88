from random import random
import matplotlib.pyplot as plt
from fitness import set_fitness_score

class Candidate:

    def __init__(self,listaPoblaciones):
        
        self.fitness = 0
        self.distritos = []
        self.listaPoblaciones = listaPoblaciones
        self.mediaHabitantesDistrito = None
        self.compacidad = 0
    
    def __le__(self, otro):
        
        return self.fitness <= otro.fitness
    
    def __lt__(self, otro):
        
        return self.fitness < otro.fitness
    
    def __ge__(self, otro):
        
        return self.fitness >= otro.fitness
    
    def __gt__(self, otro):
        
        return self.fitness > otro.fitness
    
    def __eq__(self,otro):
        
        return round(self.fitness) == round(otro.fitness)

   
    # Dibuja los distritos uno de cada color
    def plot(self):
        
        
        fig, ax1 = plt.subplots(1, 1, figsize=(20,20))
        fig.set_dpi(500.0)
        for i,distrito in enumerate(self.distritos):
           
            
            if len(self.distritos) <= 15: # asignamos 15 colores diferentes, si se seleccionan mas de 10 distritos se elegirán aleatoriamente
               
                   colors = ['red', 'darkblue', 'springgreen', 'chocolate', 'goldenrod', 'yellow', 'olive', 'darksalmon', 'rebeccapurple', 'magenta','silver','chartreuse','cyan','black','tomato']
                   color = colors[i]
              
            else:
               
                    r = random()
                    b = random()
                    g = random()
                    
                    color = (r, g, b)
           
            for poblacion in distrito.poblaciones:
                
                 poblacion.geometria.plot(color=color,ax=ax1,label=i)
                 
                    
         
    
    def calculaMediaHabitantesDistrito(self):
        
        listaHabitantes = [pueblo.Habitantes for pueblo in self.distritos]
        self.mediaHabitantesDistrito = sum(listaHabitantes)/len(listaHabitantes)
    
    def calculaFitness(self, grafo):
        
        self.fitness,self.compacidad = set_fitness_score(self, grafo)
                    
            
            
                
            
           
                
               
        
        
        
        
        

