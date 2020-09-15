from methods_flex import obterFlexionsPaquete
from methods_io import obtenInfoPaqueteDoCsv
from methods_trad import *
import sys


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
rutaFicheiroEntrada = sys.argv[1]

#Paso 1: Recupera ILIs de un paquete (de un fichero CSV)
infoPaqueteDoCSV=obtenInfoPaqueteDoCsv(rutaFicheiroEntrada)
#infoPaqueteDoCSV=obtenInfoPaqueteDoCsv("data/paquete/es_discusión_estr1_animado_humano_origen.csv")
#infoPaqueteDoCSV=obtenInfoPaqueteDoCsv("data/paquete/es_estancia_estr1_animado_humano_profesión_educación.csv")

print("\nLista de ILIs asociados ao paquete (csv):")
listaILIsCSV=obtenListadoILIsDePaquete(infoPaqueteDoCSV)

#Descomentar si se quere recuperar os ILIs da BD
# #Paso 1.A: Recupera ILIs de un paquete (de la BD)
# infoPaqueteBD=obtenInfoPaqueteDaBD("259")
# # Nota: ActanteID=259 corresponde ao paquete https://docs.google.com/spreadsheets/d/1ZjJXtK1_qE2rYPdo9UgrOOOPyH69C_0J6C9q6kQNWfU
# print("\nLista de ILIs asociados al paquete (bd):")
# listaILIsBD=obtenListadoILIsDePaquete(infoPaqueteBD)

# computoDiferenciasInfo_BD_vs_CSV(infoPaqueteBD, listaILIsBD, infoPaqueteDoCSV, listaILIsCSV )

#Uso a información que ven do CSV para os seguintes pasos!!!
infoPaquete = infoPaqueteDoCSV
listaILIs = listaILIsCSV


#Paso 2: Obter termos asociados ao ILIs (synsets) en galego e portugués
obtenTermos_AsociadosA_ILIs(infoPaquete)

# Garda a información dos léxicos atopados nun fichero
rutaFicheiroSaidaServizoWeb = rutaFicheiroEntrada.replace(".csv", "_resultados_servizoweb.csv", 1)
gardaDiccionarioNunFicheiro(infoPaquete, rutaFicheiroSaidaServizoWeb)


#Paso 3: Obter flexións
rutaFicheiroTermosSenFlexions = rutaFicheiroEntrada.replace(".csv", "_termos_sen_flexions_pt.csv", 1)
resultadosFlexionsPt = obterFlexionsPaquete(infoPaquete, "pt", rutaFicheiroTermosSenFlexions)

rutaFicheiroTermosSenFlexions = rutaFicheiroEntrada.replace(".csv", "_termos_sen_flexions_gl.csv", 1)
resultadosFlexionsGl = obterFlexionsPaquete(infoPaquete, "gl", rutaFicheiroTermosSenFlexions)


rutaFicheiroSaidaPt = rutaFicheiroEntrada.replace("es_", "pt_", 1)
if( rutaFicheiroSaidaPt == rutaFicheiroEntrada):
    rutaFicheiroSaidaPt = rutaFicheiroEntrada.replace(".csv", "_pt.csv", 1)

rutaFicheiroSaidaGl = rutaFicheiroEntrada.replace("es_", "gl_", 1)
if( rutaFicheiroSaidaGl == rutaFicheiroEntrada):
    rutaFicheiroSaidaGl = rutaFicheiroEntrada.replace(".csv", "_gl.csv", 1)

#Paso 4: Creación dos ficheiros CSVs con flexión, lema,indicadores de PoS e ILI
gardaDiccionarioNunFicheiro(resultadosFlexionsPt, rutaFicheiroSaidaPt)
gardaDiccionarioNunFicheiro(resultadosFlexionsGl, rutaFicheiroSaidaGl)

print("\nFeito! Paquetes xerados!")