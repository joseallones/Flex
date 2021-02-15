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


if(len(sys.argv)!=3):
    print('Hai que pasar o idioma e a ruta do directorio onde están os paquetes. Exemplo: python3 trad.py pt /home/user/Flex/paquete')
    exit(1)

#pt,gl,fr,de
idioma = sys.argv[1]
print(idioma)

ruta = sys.argv[2]
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
        if file.startswith("es_") and (file.endswith(".csv") or  file.endswith(".xlsx")):
            rutaFichero = os.path.join(ruta, file)


            file_exists = os.path.join(ruta, "output", file.replace("es",idioma,1))

            #Descomentar no caso de querer evitar traducir paquetes xa traducidos
            # if os.path.exists(file_exists):
            #     print("\texiste " + file_exists)
            # else:
            #     print("\t\tno existe " + file_exists)
            #     print(rutaFichero)
            #     listadoRutas.append(rutaFichero)

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
        infoPaqueteDoCSV = obtenInfoPaqueteDoCsv(rutaFicheiroEntrada)

    print("\nLista de ILIs asociados ao paquete (csv):")
    listaILIsCSV=obtenListadoILIsDePaquete(infoPaqueteDoCSV)


    #Empregase a información que ven do CSV para os seguintes pasos!!!
    infoPaquete = infoPaqueteDoCSV
    listaILIs = listaILIsCSV

    #Paso 2: Obter traduccions

    #Paso 2.1: Obter termos asociados aos ILIs (synsets) en galego e portugués
    obtenTermos_AsociadosA_ILIs(infoPaquete)

    #Paso 2.2: Obter traduccións de API MyMemory
    detailsTrad = obtenTraduccionsMyMemmory(infoPaquete, idioma)
    rutaFicheiroDetallesMyMemmory = rutaFicheiroEntrada.replace(".xlsx", "_detallesMyMemmory_" + idioma + ".xlsx", 1)
    rutaFicheiroDetallesMyMemmory = rutaFicheiroDetallesMyMemmory.replace(ruta, ruta_salida)
    gardaDiccionarioNunFicheiro(detailsTrad, rutaFicheiroDetallesMyMemmory)




    #Paso 2.3: Garda a información dos léxicos atopados nun fichero
    rutaFicheiroSaidaServizoWeb = rutaFicheiroEntrada.replace(".csv", "_resultados_servizoweb.csv", 1)
    if (rutaFicheiroSaidaServizoWeb == rutaFicheiroEntrada):
        rutaFicheiroSaidaServizoWeb = rutaFicheiroSaidaServizoWeb.replace(".xlsx", "_resultados_servizoweb.xlsx", 1)
    rutaFicheiroSaidaServizoWeb = rutaFicheiroSaidaServizoWeb.replace(ruta, ruta_salida)
    print(rutaFicheiroSaidaServizoWeb)
    gardaDiccionarioNunFicheiroDelimiterTab(infoPaquete, rutaFicheiroSaidaServizoWeb)


    #Paso 3: Obter flexións
    rutaFicheiroTermosSenFlexions = rutaFicheiroEntrada.replace(".csv", "_termos_sen_flexions_"+idioma+".csv", 1)
    if(rutaFicheiroTermosSenFlexions == rutaFicheiroEntrada):
        rutaFicheiroTermosSenFlexions = rutaFicheiroEntrada.replace(".xlsx", "_termos_sen_flexions_"+idioma+".xlsx", 1)
    rutaFicheiroTermosSenFlexions = rutaFicheiroTermosSenFlexions.replace(ruta, ruta_salida)
    resultadosFlexions = obterFlexionsPaquete(infoPaquete, idioma, rutaFicheiroTermosSenFlexions)


    rutaFicheiroSaida=rutaFicheiroEntrada.replace("es_", idioma+"_", 1)
    if( rutaFicheiroSaida == rutaFicheiroEntrada):
        rutaFicheiroSaida = rutaFicheiroEntrada.replace(".csv", "_"+idioma+".csv", 1)
        rutaFicheiroSaida = rutaFicheiroSaida.replace(".xlsx", "_"+idioma+".xlsx", 1)

    rutaFicheiroSaida = rutaFicheiroSaida.replace(ruta, ruta_salida)


    #Paso 4: Creación dos ficheiros CSVs con flexión, lema, indicadores de PoS e ILI
    gardaDiccionarioNunFicheiro(resultadosFlexions, rutaFicheiroSaida)


print("\nFeito! Paquetes xerados!")