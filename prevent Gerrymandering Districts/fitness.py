from copy import deepcopy 

def set_fitness_score(candidate,grafo):
        
        sumaDiferencias = 0
        
        for distrito in candidate.distritos:# hallamos la suma de las diferencias de los habitantes de un distrito con la media de los demas
            
            sumaDiferencias += abs(distrito.Habitantes - candidate.mediaHabitantesDistrito)
        #radial compactness
        compacidad = 0 
        
        for distrito in candidate.distritos:
            for pueblos in distrito.poblaciones:
            
                compacidad += pueblos.centro.distance(distrito.centro.centro)
        
        
        fitness = float(sumaDiferencias + compacidad + penalizaIslotes(candidate, grafo))
        
        return fitness, compacidad
    
def penalizaIslotes(candidato,grafo):
    
    for distrito in candidato.distritos:
        
        for pueblo in distrito.poblaciones:
            
            if not estaConectado(distrito.centro.id,pueblo.id,deepcopy(grafo),candidato) and (distrito.centro.id is not pueblo.id):
                
                return 1000000
    
    return 0 # si no ha detectado islotes no penalizamos
    

def estaConectado(id1,id2,grafo,candidato):
    
   listaEdges = grafo.get_edgelist()

   for edge in listaEdges:
             
       if not estanMismoDistrito(edge[0],edge[1],candidato): # los id de los nodos coinciden con los guardados en las poblaciones
            
           idEdge = grafo.get_eid(edge[0],edge[1])# si no estan en el mismo distrito cortamos el enlace entre poblaciones colindantes
           grafo.delete_edges(idEdge)
    
   return type(grafo.shortest_paths(id1,id2)[0][0]) == int 
# si los nodos estan conectados la funcion shortest_path dara un entero, de lo contrario dara infinito




def perteneceAlDistrito(i,candidate): #dada la id de una poblacion nos dice la id del distrito asignado
    
    for distrito in candidate.distritos:
        for pueblo in distrito.poblaciones:
            
            if pueblo.id == i:
                
                return distrito.id

def estanMismoDistrito(i,j,candidate):
    
    return perteneceAlDistrito(i,candidate) == perteneceAlDistrito(j,candidate)
                
                
                
                
                
                
            
            
            
            
            
    
    
            
        
        