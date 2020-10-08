#!/usr/bin/env python
import os
import sys

from methods_flex import obterFlexionsPaquete
from methods_io import gardaDiccionarioNunFicheiro, obtenTermosDoTXT

if(len(sys.argv)!=3):
    print('Hai que pasar a ruta do directorio e o idioma. Exemplo: python3 flex_ficheiros_txt.py /home/data/txt gl')
    exit(1)

rutaDirectorioEntrada = sys.argv[1]
idioma = sys.argv[2]

for file in os.listdir(rutaDirectorioEntrada):

    if file.endswith(".txt"):
        rutaFicheiroEntrada = os.path.join("txt", file)
        print(rutaFicheiroEntrada)

        listDict = obtenTermosDoTXT(rutaFicheiroEntrada, idioma)

        if(idioma=="pt"):
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
