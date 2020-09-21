from methods_flex import obterFlexionsPaquete
from methods_io import obtenInfoPaqueteDoCsv,obtenInfoPaqueteDoXlsx
from methods_trad import *
import sys
import os
import time


def obtenListadoILIsDePaquete(infoPaquete):
    listaILIs = []
    for dict in infoPaquete:
        if( dict['ili'] not in listaILIs):
            listaILIs.append(dict['ili'])
    print(listaILIs)
    print(len(listaILIs))
    return listaILIs


if(len(sys.argv)!=2):
    print('Hai que pasar a ruta do ficheiro csv. Exemplo: flex_csv.py /home/data/paquete/es_discusión_estr1_animado_humano_origen.csv')
    exit(1)

ruta = sys.argv[1]
print(ruta)

listadoRutas = []

if(os.path.isdir(ruta)):
    print("Directorio")
    # if not ruta.endswith("/"):
    #     ruta = ruta + "/"

    for file in os.listdir(ruta):
        if file.startswith("es_") and  (file.endswith(".csv") or  file.endswith(".xlsx")):
            rutaFichero = os.path.join(ruta, file)
            print(rutaFichero)
            listadoRutas.append(rutaFichero)

elif(os.path.isfile(ruta)):
    print("File")
    listadoRutas.append(ruta)
    exit(1)

print("\n\n")
time.sleep(2)

for rutaFicheiroEntrada in listadoRutas:

    #Paso 1: Recupera ILIs de un paquete (de un fichero CSV)
    print (rutaFicheiroEntrada)

    if not rutaFicheiroEntrada.endswith("csv"):
        infoPaqueteDoCSV = obtenInfoPaqueteDoXlsx(rutaFicheiroEntrada)
    else:
        infoPaqueteDoCSV=obtenInfoPaqueteDoCsv(rutaFicheiroEntrada)


    #infoPaqueteDoCSV=obtenInfoPaqueteDoCsv("data/paquete/es_discusión_estr1_animado_humano_origen.csv")
    #infoPaqueteDoCSV=obtenInfoPaqueteDoCsv("data/paquete/es_estancia_estr1_animado_humano_profesión_educación.csv")

    print("\nLista de ILIs asociados ao paquete (csv):")
    listaILIsCSV=obtenListadoILIsDePaquete(infoPaqueteDoCSV)


    #Uso a información que ven do CSV para os seguintes pasos!!!
    infoPaquete = infoPaqueteDoCSV
    listaILIs = listaILIsCSV


    #Paso 2: Obter termos asociados ao ILIs (synsets) en galego e portugués
    obtenTermos_AsociadosA_ILIs(infoPaquete)

    # Garda a información dos léxicos atopados nun fichero
    rutaFicheiroSaidaServizoWeb = rutaFicheiroEntrada.replace(".csv", "_resultados_servizoweb.csv", 1)
    if (rutaFicheiroSaidaServizoWeb == rutaFicheiroEntrada):
        rutaFicheiroSaidaServizoWeb = rutaFicheiroSaidaServizoWeb.replace(".xlsx", "_resultados_servizoweb.xlsx", 1)
    gardaDiccionarioNunFicheiro(infoPaquete, rutaFicheiroSaidaServizoWeb)


    #Paso 3: Obter flexións
    rutaFicheiroTermosSenFlexions = rutaFicheiroEntrada.replace(".csv", "_termos_sen_flexions_pt.csv", 1)
    if(rutaFicheiroTermosSenFlexions == rutaFicheiroEntrada):
        rutaFicheiroTermosSenFlexions = rutaFicheiroEntrada.replace(".xlsx", "_termos_sen_flexions_pt.xlsx", 1)
    resultadosFlexionsPt = obterFlexionsPaquete(infoPaquete, "pt", rutaFicheiroTermosSenFlexions)

    rutaFicheiroTermosSenFlexions = rutaFicheiroEntrada.replace(".csv", "_termos_sen_flexions_gl.csv", 1)
    if (rutaFicheiroTermosSenFlexions == rutaFicheiroEntrada):
        rutaFicheiroTermosSenFlexions = rutaFicheiroEntrada.replace(".xlsx", "_termos_sen_flexions_gl.xlsx", 1)
    resultadosFlexionsGl = obterFlexionsPaquete(infoPaquete, "gl", rutaFicheiroTermosSenFlexions)


    rutaFicheiroSaidaPt=rutaFicheiroEntrada.replace("es_", "pt_", 1)
    if( rutaFicheiroSaidaPt == rutaFicheiroEntrada):
        rutaFicheiroSaidaPt = rutaFicheiroEntrada.replace(".csv", "_pt.csv", 1)
        rutaFicheiroSaidaPt = rutaFicheiroSaidaPt.replace(".xlsx", "_pt.xlsx", 1)

    rutaFicheiroSaidaGl = rutaFicheiroEntrada.replace("es_", "gl_", 1)
    if( rutaFicheiroSaidaGl == rutaFicheiroEntrada):
        rutaFicheiroSaidaGl = rutaFicheiroEntrada.replace(".csv", "_gl.csv", 1)
        rutaFicheiroSaidaGl = rutaFicheiroSaidaGl.replace(".xlsx", "_gl.xlsx", 1)



    #Paso 4: Creación dos ficheiros CSVs con flexión, lema,indicadores de PoS e ILI
    gardaDiccionarioNunFicheiro(resultadosFlexionsPt, rutaFicheiroSaidaPt)
    gardaDiccionarioNunFicheiro(resultadosFlexionsGl, rutaFicheiroSaidaGl)


print("\nFeito! Paquetes xerados!")