from methods_trad import *



#Paso 1: Recupera ILIs de un paquete (de un fichero CSV)
infoPaqueteDoCSV=obtenInfoPaqueteDoCsv("data/paquete/es_discusión_estr1_animado_humano_origen.csv")
print("\nLista de ILIs asociados al paquete (csv):")
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


#Paso 3: Obter flexións
resultadosFlexionsPt = obterFlexions(infoPaquete, "pt")
resultadosFlexionsGl = obterFlexions(infoPaquete, "gl")


#Paso 4: Creación dos ficheiros CSVs con flexión, lema,indicadores de PoS e ILI
gardaDiccionarioNunFicheiro(resultadosFlexionsPt, 'package_pt.csv')
gardaDiccionarioNunFicheiro(resultadosFlexionsGl, 'package_gl.csv')

print("\nFeito! Paquetes xerados!")