# coding: utf-8
import glob
import csv
from datetime import datetime
from vrpy import VehicleRoutingProblem
import re
import math
from networkx import DiGraph, from_numpy_matrix, relabel_nodes, set_node_attributes
from numpy import array


def f_configura_datos(archivoDataset):
    DataSet = list(csv.reader(open(archivoDataset), delimiter=":"))
    nombre=DataSet[0][1]
    nodos=int(DataSet[3][1])
    capacidadVehiculo=int(DataSet[5][1])
    coordenada=nodos*[[],]
    demanda={}
    bLeyendoCoordenadas=False
    bLeyendoDemanda=False
    bTerminando=False
    for fila in DataSet:
        if bLeyendoCoordenadas and not(bLeyendoDemanda):
            coordenadas=re.findall(r"[\d]+", fila[0])
            if coordenadas:
                coordenada[int(coordenadas[0])-1]=[int(coordenadas[1]),int(coordenadas[2])]
        if bLeyendoDemanda and not(bTerminando):
            demandas=re.findall(r"[\d]+", fila[0])
            if demandas:
                demanda[int(demandas[0])-1]=int(demandas[1])
        bLeyendoCoordenadas=bLeyendoCoordenadas or (fila[0]=='NODE_COORD_SECTION')
        bLeyendoDemanda=bLeyendoDemanda or (fila[0]=='DEMAND_SECTION')
        bTerminando=bTerminando or (fila[0]=='DEPOT_SECTION')
    distancia=[]
    for nodoI in range(0,nodos+1): #len(demanda)):
        fila=[]
        for nodoJ in range(0,nodos+1):
            i=nodoI
            j=nodoJ
            try:
                distancia_ij=int(round(math.sqrt((coordenada[nodoI][0]-coordenada[nodoJ][0])**2+                                                  (coordenada[nodoI][1]-coordenada[nodoJ][1])**2),0))
            except:
                distancia_ij=0
            fila.append(distancia_ij)
        distancia.append(fila)
    
    for j in range(0,nodos+1):
        distancia[j][nodos]=distancia[j][0]
        distancia[j][0]=0

    if nodos<20:
        for i in range(0,nodos+1): #len(demanda)):
            fila=''
            for j in range(0,nodos+1):
                fila=fila+"{0:>5d}".format(distancia[i][j])
            #print(fila)

    # The matrix is transformed into a DiGraph
    A = array(distancia, dtype=[("cost", int)])
    G = from_numpy_matrix(A, create_using=DiGraph())

    # The demands are stored as node attributes
    set_node_attributes(G, values=demanda, name="demand")

    # The depot is relabeled as Source and Sink
    G = relabel_nodes(G, {0: "Source", nodos: "Sink"})    
    return {"G":G,"nombre":nombre,"nodos":nodos,"capacidadVehiculo":capacidadVehiculo,"demanda":demanda,"distancia":distancia}

def ImprimeEnArchivo (nombreDataSet,hrInicio,resultados,extension):
    fechaHoraFin =  datetime.now()
    segundos=(fechaHoraFin-fechaHoraIni).seconds+(fechaHoraFin-fechaHoraIni).microseconds/10**6
    minRecorrido=10**12
    with open(nombreDataSet + extension, mode='wt', encoding='utf-8') as myfile:
        myfile.write(nombreDataSet+'\t-\t'+'Inicio:'+'\t'+fechaHoraIni.strftime("%H:%M:%S.%f")+'\n') 
        myfile.write(nombreDataSet+'\t-\t'+'Fin:'+'\t'+fechaHoraFin.strftime("%H:%M:%S.%f")+'\n') 
        myfile.write(nombreDataSet+'\t-\t'+'Tiempo empleado:'+'\t'+str(segundos)+'\n')
        for resultado in resultados:
            if len(resultado)==5:
                if minRecorrido>resultado[4]:
                    minRecorrido=resultado[4]
                myfile.write(nombreDataSet+'\t'+resultado[1]+'\t'+resultado[2]+'\t'+str(resultado[3])+'\t'+str(resultado[4])+'\n')
        myfile.write(nombreDataSet+'\t-\t'+'Mínimo recorrido:'+'\t'+str(minRecorrido)+'\n')

fechaHoraIni =  datetime.now()
archivosDataSet='C:/Users/TECH SENATI/Ciencia de Datos_Python/VRP/DataSet\XML8_1111_61.vrp'
print(archivosDataSet)
for archivoDataSet in glob.glob(archivosDataSet):
    nombreInstancia=archivoDataSet.split('\\')[-1].split('.')[0]
    print(nombreInstancia,'Inicio:',fechaHoraIni)
    data=f_configura_datos(archivoDataSet)
    G=data["G"]
    
    prob = VehicleRoutingProblem(G, load_capacity=data["capacidadVehiculo"])
    #prob.solve(greedy="True",time_limit=10)
    prob.solve(pricing_strategy="BestEdges1",time_limit=10)
    #prob.solve(pricing_strategy="BestEdges2",time_limit=10)
    #prob.solve(pricing_strategy="BestPaths",time_limit=10)
    #prob.solve(pricing_strategy="Hyper",time_limit=10)


    print(nombreInstancia,prob.best_value)
    print(nombreInstancia,prob.best_routes)
fechaHoraFin =  datetime.now()
segundos=(fechaHoraFin-fechaHoraIni).seconds+(fechaHoraFin-fechaHoraIni).microseconds/10**6




print(nombreInstancia,'Fin:',fechaHoraFin)
print(nombreInstancia,'Tiempo empleado:',segundos)
#XML8_1111_61	-	Inicio:	16:24:57.106485
#XML8_1111_61	-	Fin:	16:25:57.305338
#XML8_1111_61	-	Tiempo empleado:	60.198853





