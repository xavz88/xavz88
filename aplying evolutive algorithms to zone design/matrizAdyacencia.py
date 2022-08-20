import numpy as np

def matrizAdyacencia(listaPueblos):
    
    n = len(listaPueblos)
    
    matriz = np.zeros((n,n))
    
    
    for i,pueblo in enumerate(listaPueblos):
        for j in range(len(listaPueblos)):
        
            if listaPueblos[i].geometria.touches(listaPueblos[j].geometria)[0]:
                
                matriz[i,j] = 1
        
        
    
    return matriz