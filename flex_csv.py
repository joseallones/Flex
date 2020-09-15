#!/usr/bin/env python
import sys

from methods_flex import obterFlexionsPaquete
from methods_io import gardaDiccionarioNunFicheiro, obtenTermosDoTXT

if(len(sys.argv)!=2):
    print('Hai que pasar a ruta do ficheiro txt. Exemplo: flex_csv.py /home/data/paquete/situación_estado_emocional.txt')
    exit(1)

rutaFicheiroEntrada = sys.argv[1]
listDict = obtenTermosDoTXT(rutaFicheiroEntrada)

rutaFicheiroTermosSenFlexions = rutaFicheiroEntrada.replace(".txt", "_termos_sen_flexions_gl.csv", 1)
listadoResultadosFlexions = obterFlexionsPaquete(listDict, "gl", rutaFicheiroTermosSenFlexions)
#print (listadoResultadosFlexions)

rutaFicheiroSaida = rutaFicheiroEntrada.replace(".txt", "_con_flexions.csv")
gardaDiccionarioNunFicheiro(listadoResultadosFlexions, rutaFicheiroSaida)