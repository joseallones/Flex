#!/usr/bin/env python
import os

from methods_flex import obterFlexionsPaquete
from methods_io import gardaDiccionarioNunFicheiro, obtenTermosDoTXT

for file in os.listdir("txt"):

    if file.endswith(".txt"):
        rutaFicheiroEntrada = os.path.join("txt", file)
        print(rutaFicheiroEntrada)

        listDict = obtenTermosDoTXT(rutaFicheiroEntrada)

        rutaFicheiroTermosSenFlexions = rutaFicheiroEntrada.replace(".txt", "_termos_sen_flexions_gl.csv", 1)
        listadoResultadosFlexions = obterFlexionsPaquete(listDict, "gl", rutaFicheiroTermosSenFlexions)
        #print (listadoResultadosFlexions)

        rutaFicheiroSaida = rutaFicheiroEntrada.replace(".txt", "_con_flexions.csv")
        gardaDiccionarioNunFicheiro(listadoResultadosFlexions, rutaFicheiroSaida)
