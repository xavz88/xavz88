from matrizAdyacencia import matrizAdyacencia
import numpy as np
import igraph as ig
import matplotlib.pyplot as plt
from models.evolutive.candidate import Candidate
from random import randrange,sample, uniform
from distrito import Distrito
from copy import deepcopy
from itertools import chain
import csv

class Evolutive:

    def __init__(self, population_size,  mutation_rate, max_generations, child_generation, distritos,  listaPueblos = []):
        
        
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.max_generations = max_generations
        self.child_generation = child_generation
        self.distritos = distritos
        self.matrizAdyacencia = []
        self.listaPueblos = listaPueblos
        self.grafo = None
        
        if (self.population_size < 2
            or self.max_generations == 0):
            raise "Parametros invalidos"

    def resultado(self):
        
        self.matrizAdyacencia = matrizAdyacencia(self.listaPueblos)
        self.grafo = ig.Graph.Adjacency(self.matrizAdyacencia) # creamos un grafo a partir de la matriz de adyacencia

        candidatos = []
        mejorFitness = []

        

        for i in range(self.population_size):
            
            temp = deepcopy(self.listaPueblos) # asi evitamos que la lista quede alterada entre iteraciones, hacemos copias de las instancias para que al modificar uno no se modifiquen los demas
            candidatos.append(self.candidatoAleatorio(temp))
            
        for generation in range(self.max_generations):
            
            #seleccion de padres
            
            for i in range(0,self.child_generation):
                
                padre,madre = self.seleccionaPadres(deepcopy(candidatos))
                
                hijo =self.combination(padre,madre,self.mutation_rate)
                
                if hijo not in candidatos:
                    candidatos.append(hijo)
                    
            
            # a continuación decidimos que individuos pasan a la siguiente generación, dependiendo de population_size se cogeran los que tienen menos fitness
            
            candidatos = self.seleccionSupervivientes(candidatos)
            
            mejorFitness.append(candidatos[0].fitness)
            print("En la generación ", generation, " el fitness es ", candidatos[0].fitness )

        plt.plot(mejorFitness)
        plt.xlabel("Generaciones")
        plt.ylabel("Mejor Fitness")
        mejorCandidato = candidatos[0]
        mejorCandidato.plot() #ploteamos el mejor candidato, recordemos que estan ordenados de mejor a peor
        self.exportarResultados(mejorCandidato)

        
        

    
    def exportarResultados(self, candidato):
        
        colors = ['red', 'darkblue', 'springgreen', 'chocolate', 'goldenrod', 'yellow', 'olive', 'darksalmon', 'rebeccapurple', 'magenta','silver','chartreuse','cyan','black','tomato']

        with open("distritos.txt","w") as f:
            write = csv.writer(f)
            
            write.writerow(
                "Se ha obtenido un fitness de {} con una compacidad de {}, ademas la distribución de poblaciones ha quedado de la siguiente manera: ".format(candidato.fitness,candidato.compacidad))
            
            for i,distrito in enumerate(candidato.distritos):
                if self.distritos <= 15:
                    write.writerow(["El distrito {} ({}) tiene: {} habitantes.".format(i,colors[i], distrito.Habitantes)])
                else: 
                    write.writerow(["El distrito {} tiene: {} habitantes.".format(i, distrito.Habitantes)])
                write.writerow(['\n'])
            write.writerow(["El desglose de poblaciones:"])
            write.writerow(['\n\n\n'])
                
            for i,distrito in enumerate(candidato.distritos):
                write.writerow(['\n'])
                write.writerow(["Distrito {}".format(i)])
                write.writerow(['-------------'])
                for pueblo in distrito.poblaciones:
                    
                    write.writerow([pueblo.nombre])
        print("Resultados exportados a distritos.txt")
            
    def combination(self, madre:Candidate, padre:Candidate, tasaMutacion=0):
        
  
        hijo = Candidate(deepcopy(self.listaPueblos))
        
   
        # seleccionamos partes iguales del padre y de la madre si el numero de distritos es par
        #si es impar habra que cojer mas de uno que de otro
        if (self.distritos % 2) == 0 :
            
            cromosomasPadre = sample(padre.distritos, int(self.distritos/2))
            cromosomasMadre = sample(madre.distritos, int(self.distritos/2))
        else:
            cromosomasPadre = sample(padre.distritos, int(self.distritos/2 - 0.5))
            cromosomasMadre = sample(madre.distritos, int(self.distritos/2 + 0.5))
        
        
        #obtenemos la lista de poblaciones que estan en cromosomasPadre y cromosomasMadre
        listaSolapamientos = list(set(chain(*[deepcopy(cromosoma.poblaciones) for cromosoma in cromosomasPadre])) &
                                  set(chain(*[deepcopy(cromosoma.poblaciones) for cromosoma in cromosomasMadre])))
        
       
        
        
        copia = deepcopy(cromosomasPadre) # hacemos una copia asi cuando quitemos los solapamientos no nos afectara al recorrido
        
        for i, cromosoma in enumerate(copia):
            for j,pueblo in enumerate(cromosoma.poblaciones):
                
                if pueblo in listaSolapamientos:
                    
                    cromosomasPadre[i].poblaciones.remove(pueblo)
                    
        
        adnHijo = cromosomasMadre + cromosomasPadre
        
        for i in range(len(adnHijo)): #reasignamos las id
                
            adnHijo[i].id = i
        
        hijo.distritos = adnHijo
        
        #despues de juntar las dos partes y de rellenar los huecos, seguramente nos queden poblaciones sin asignar, la siguiente función lo soluciona
        hijo = self.rellenarHuecos(hijo)
        
        #procedemos con la mutación si se ha especificado el parametro
        
        if uniform(0,1) < tasaMutacion:
            
            #guardamos el indice para no volver a poner la poblacion en el mismo
            i = sample(range(self.distritos),1)[0]
            
            
            pueblo = sample(hijo.distritos[i].poblaciones,1)[0]
            hijo.distritos[i].poblaciones.remove(pueblo)
            
            #ahora lo asignamos a cualquier otro distrito diferente de i
            
            indicesDistritos = list(range(self.distritos))
            #quitamos el distrito del que hemos obtenido la poblacion
            indicesDistritos.pop(i)
            
            hijo.distritos[sample(indicesDistritos,1)[0]].poblaciones.append(pueblo)
            print("Se ha producido una mutación.")
            
        hijo.calculaMediaHabitantesDistrito()
        
        hijo.calculaFitness(deepcopy(self.grafo))
      
        return hijo
    
    
    
    #funcion que busca las poblaciones que no han sido asignadas  durante el proceso de combinacion, "huecos"
    #se le asigna el distrito colindante con menor poblacion, tambien asigna un centro a los distritos vacios
    def rellenarHuecos (self, candidato:Candidate):
        
        contadorPueblos = deepcopy(self.listaPueblos )
        
        #obtenemos los no asignados borrando de la lista general todos los asignados
        for distrito in candidato.distritos:
            for pueblo in distrito.poblaciones:
                if pueblo in contadorPueblos:
                    #print(pueblo.nombre,len(contadorPueblos))
                    contadorPueblos.remove(pueblo)
        
        if len(contadorPueblos) == 0: return candidato
        
        #en el siguiente fragmento asignamos una poblacion no asignada aleatoriamente a un distrito vacio
        for i,distrito in enumerate(candidato.distritos):
            
            if len(distrito.poblaciones) == 0:
                
                asigna = sample(contadorPueblos,1)
                candidato.distritos[i].poblaciones = asigna
                contadorPueblos.remove(asigna[0])
                
      
        while len(contadorPueblos) != 0:
            for puebloUnasigned in contadorPueblos:
                DistritosColindantes = []
                for distrito in candidato.distritos:
                    for pueblo in distrito.poblaciones:
                        
                       
                        if self.matrizAdyacencia[pueblo.id,puebloUnasigned.id]:#pueblo.geometria.touches(puebloUnasigned.geometria)[0]:
                            
                            DistritosColindantes.append({
                                'id':distrito.id,
                                'habitantes':distrito.Habitantes})
                
                if len(DistritosColindantes) != 0:
                    
                    distritoGanador = min(DistritosColindantes, key = lambda x: x['habitantes'])#la asignamos al distrito que menos  poblacion tiene
                    
                    candidato.distritos[distritoGanador['id']].poblaciones.append(puebloUnasigned)
                    candidato.distritos[distritoGanador['id']].hallarCentro()
                    candidato.distritos[distritoGanador['id']].sumaHabitantes()
                    contadorPueblos.remove(puebloUnasigned)
                
        return candidato
            
        
        
    #donat un conjunt de poblacions y una matriu de conectivitat, directament generarem els districtes continus.
    
    def candidatoAleatorio(self,listaPoblaciones):
        
        # inicializamos un objeto de tipo candidato
        candidate = Candidate(listaPoblaciones)
        
        
        # creamos los distritos  y a cada uno le asignamos aleatoriamente una población
        
        for i in range(self.distritos):
            
            unidadArea = listaPoblaciones.pop(randrange(0,len(listaPoblaciones)))
            
            #creamos un distrito con el array de poblaciones vacio y a continuacion asignamos la unidad administrativa
            candidate.distritos.append(Distrito(i))
            candidate.distritos[i].poblaciones.append(unidadArea)
            
        #ahora a cada iteración iremos agregando una poblacion a un distrito aleatorio comprobando que esta es contigua a alguna de las ya presentes en el distrito
        
        
        result = self.listaPueblos_a_distritos(listaPoblaciones,candidate)
        
        
        # una vez hallamos completado la asignacion de poblaciones guardamos en cada objeto la siguiente informacion de interes
        for distrito in result.distritos:
            distrito.hallarCentro()
            distrito.sumaHabitantes()
        result.calculaMediaHabitantesDistrito()
        result.calculaFitness(deepcopy(self.grafo))
        print("Candidato aleatorio generado")
        return result
        

         
    def listaPueblos_a_distritos(self,listaPoblaciones,candidate):
       
        for  poblacionNoAsignada in listaPoblaciones:
            
            distrito = sample(candidate.distritos,1)[0]
            
            for poblacionAsignada in distrito.poblaciones:
                
                if self.matrizAdyacencia[poblacionAsignada.id,poblacionNoAsignada.id]:
                    
                    listaPoblaciones.remove(poblacionNoAsignada)
                    distrito.poblaciones.append(poblacionNoAsignada)
                    break
                
        if  len(listaPoblaciones) !=0:
            
             self.listaPueblos_a_distritos(listaPoblaciones,candidate)
            
        
        return candidate
    
    
    def seleccionaPadres(self, poblacion): #usamos el metodo de la ruleta
    
        padresSeleccionados = []
        population = deepcopy(poblacion)
        
        for _ in range(2): #seleccionaremos 2 padres
            #debemos invertirlo porque en nuestro caso menos fitness es mejor
            listaFitnessInv = [1/candidate.fitness for candidate in population]
            
            fitnessTotal = sum(listaFitnessInv)
            
            listaProbabilidades = [float(fitness/fitnessTotal) for fitness in listaFitnessInv]
            
            seleccionado = np.random.choice(population, p=listaProbabilidades)
            padresSeleccionados.append(seleccionado)
            idx = population.index(seleccionado)
            population.pop(idx)
          
        return padresSeleccionados[0],padresSeleccionados[1]
    
    
    def seleccionSupervivientes(self, population):
        
        population.sort()#ordenamos de menor a mayor segun su fitness
        
        return population[:self.population_size]
        
        