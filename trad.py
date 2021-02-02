from methods_flex import *
from methods_io import *
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
    print('Hai que pasar a ruta do directorio. Exemplo: python3 trad.py /home/user/Flex/paquete')
    exit(1)

ruta = sys.argv[1]
print(ruta)

listadoRutas = []

if(os.path.isdir(ruta)):
    print("Directorio")
    # if not ruta.endswith("/"):
    #     ruta = ruta + "/"


    ruta_salida = os.path.join(ruta, 'output')
    #ruta_salida = ruta + "output/"
    print(ruta)
    print(ruta_salida)
    if not os.path.exists(ruta_salida):
        os.makedirs(ruta_salida)


    for file in os.listdir(ruta):
        if file.startswith("es_") and  (file.endswith(".csv") or  file.endswith(".xlsx")):
            rutaFichero = os.path.join(ruta, file)


            file_exists = os.path.join(ruta, "output", file.replace("es","pt",1))

            if os.path.exists(file_exists):
                print("\texiste " + file_exists)
            else:
                print("\t\tno existe " + file_exists)
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

    print("\nLista de ILIs asociados ao paquete (csv):")
    listaILIsCSV=obtenListadoILIsDePaquete(infoPaqueteDoCSV)


    #Empregase a información que ven do CSV para os seguintes pasos!!!
    infoPaquete = infoPaqueteDoCSV
    listaILIs = listaILIsCSV

    #Paso 2: Obter traduccions

    #Paso 2.1: Obter termos asociados aos ILIs (synsets) en galego e portugués
    obtenTermos_AsociadosA_ILIs(infoPaquete)

    #Paso 2.2: Obter traduccións de API MyMemory + Apertium
    detailsTradPt = obtenTraduccionsMyMemmory(infoPaquete, "pt")
    rutaFicheiroDetallesMyMemmory_pt = rutaFicheiroEntrada.replace(".xlsx", "_detallesMyMemmory_pt.xlsx", 1)
    rutaFicheiroDetallesMyMemmory_pt = rutaFicheiroDetallesMyMemmory_pt.replace(ruta, ruta_salida)
    gardaDiccionarioNunFicheiro(detailsTradPt, rutaFicheiroDetallesMyMemmory_pt )


    detailsTradGl = obtenTraduccionsMyMemmory(infoPaquete, "gl")
    rutaFicheiroDetallesMyMemmory_gl = rutaFicheiroEntrada.replace(".xlsx", "_detallesMyMemmory_gl.xlsx", 1)
    rutaFicheiroDetallesMyMemmory_gl = rutaFicheiroDetallesMyMemmory_gl.replace(ruta, ruta_salida)
    gardaDiccionarioNunFicheiro(detailsTradGl, rutaFicheiroDetallesMyMemmory_gl )

    #obtenTraduccionsApertium(infoPaquete, "gl")
    #obtenTraduccionsApertium(infoPaquete, "pt")

    #Paso 2.3: Garda a información dos léxicos atopados nun fichero
    rutaFicheiroSaidaServizoWeb = rutaFicheiroEntrada.replace(".csv", "_resultados_servizoweb.csv", 1)
    if (rutaFicheiroSaidaServizoWeb == rutaFicheiroEntrada):
        rutaFicheiroSaidaServizoWeb = rutaFicheiroSaidaServizoWeb.replace(".xlsx", "_resultados_servizoweb.xlsx", 1)
    rutaFicheiroSaidaServizoWeb = rutaFicheiroSaidaServizoWeb.replace(ruta, ruta_salida)
    print(rutaFicheiroSaidaServizoWeb)
    gardaDiccionarioNunFicheiroDelimiterTab(infoPaquete, rutaFicheiroSaidaServizoWeb)


    #Paso 3: Obter flexións
    rutaFicheiroTermosSenFlexions = rutaFicheiroEntrada.replace(".csv", "_termos_sen_flexions_pt.csv", 1)
    if(rutaFicheiroTermosSenFlexions == rutaFicheiroEntrada):
        rutaFicheiroTermosSenFlexions = rutaFicheiroEntrada.replace(".xlsx", "_termos_sen_flexions_pt.xlsx", 1)
    rutaFicheiroTermosSenFlexions = rutaFicheiroTermosSenFlexions.replace(ruta, ruta_salida)
    resultadosFlexionsPt = obterFlexionsPaquete(infoPaquete, "pt", rutaFicheiroTermosSenFlexions)

    rutaFicheiroTermosSenFlexions = rutaFicheiroEntrada.replace(".csv", "_termos_sen_flexions_gl.csv", 1)
    if (rutaFicheiroTermosSenFlexions == rutaFicheiroEntrada):
        rutaFicheiroTermosSenFlexions = rutaFicheiroEntrada.replace(".xlsx", "_termos_sen_flexions_gl.xlsx", 1)
    rutaFicheiroTermosSenFlexions = rutaFicheiroTermosSenFlexions.replace(ruta, ruta_salida)
    resultadosFlexionsGl = obterFlexionsPaquete(infoPaquete, "gl", rutaFicheiroTermosSenFlexions)


    rutaFicheiroSaidaPt=rutaFicheiroEntrada.replace("es_", "pt_", 1)
    if( rutaFicheiroSaidaPt == rutaFicheiroEntrada):
        rutaFicheiroSaidaPt = rutaFicheiroEntrada.replace(".csv", "_pt.csv", 1)
        rutaFicheiroSaidaPt = rutaFicheiroSaidaPt.replace(".xlsx", "_pt.xlsx", 1)

    rutaFicheiroSaidaGl = rutaFicheiroEntrada.replace("es_", "gl_", 1)
    if( rutaFicheiroSaidaGl == rutaFicheiroEntrada):
        rutaFicheiroSaidaGl = rutaFicheiroEntrada.replace(".csv", "_gl.csv", 1)
        rutaFicheiroSaidaGl = rutaFicheiroSaidaGl.replace(".xlsx", "_gl.xlsx", 1)

    rutaFicheiroSaidaPt = rutaFicheiroSaidaPt.replace(ruta, ruta_salida)
    rutaFicheiroSaidaGl = rutaFicheiroSaidaGl.replace(ruta, ruta_salida)

    #Paso 4: Creación dos ficheiros CSVs con flexión, lema, indicadores de PoS e ILI
    gardaDiccionarioNunFicheiro(resultadosFlexionsPt, rutaFicheiroSaidaPt)
    gardaDiccionarioNunFicheiro(resultadosFlexionsGl, rutaFicheiroSaidaGl)


print("\nFeito! Paquetes xerados!")