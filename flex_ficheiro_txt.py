#!/usr/bin/env python
import sys

from methods_flex import obterFlexionsPaquete
from methods_io import gardaDiccionarioNunFicheiro, obtenTermosDoTXT

if(len(sys.argv)!=3):
    print('Hai que pasar a ruta do directorio. Exemplo: python3 flex_ficheiro_txt.py /home/data/paquete/situación_estado_emocional.txt pt')
    exit(1)

rutaFicheiroEntrada = sys.argv[1]
idioma = sys.argv[2]
listDict = obtenTermosDoTXT(rutaFicheiroEntrada, idioma)

if (idioma == "pt"):
    rutaFicheiroTermosSenFlexions = rutaFicheiroEntrada.replace(".txt", "_termos_sen_flexions_pt.csv", 1)
else:
    rutaFicheiroTermosSenFlexions = rutaFicheiroEntrada.replace(".txt", "_termos_sen_flexions_gl.csv", 1)

listadoResultadosFlexions = obterFlexionsPaquete(listDict, idioma, rutaFicheiroTermosSenFlexions)
#print (listadoResultadosFlexions)

if (idioma == "pt"):
    rutaFicheiroSaida = rutaFicheiroEntrada.replace(".txt", "_con_flexions_pt.csv")
else:
    rutaFicheiroSaida = rutaFicheiroEntrada.replace(".txt", "_con_flexions_gl.csv")

gardaDiccionarioNunFicheiro(listadoResultadosFlexions, rutaFicheiroSaida)