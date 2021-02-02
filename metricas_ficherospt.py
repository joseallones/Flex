
import os
import csv
import xlrd

termos = []
traducidos_wordnet = []
traducidos_wordnet_modif = []
traducidos_mymemmory = []
traducidos_mymemmory_modif = []
traducidos_manual = []

def obtenInfoPaqueteDoXlsx(path_file):

    global termos
    global traducidos_wordnet
    global traducidos_wordnet_modif
    global traducidos_mymemmory
    global traducidos_mymemmory_modif
    global traducidos_manual

    listDict = []

    wb = xlrd.open_workbook(path_file)
    sh = wb.sheet_by_index(0)
    print(sh.ncols)

    if (sh.ncols <7):
        print("No hay info\n")
        return

    for i in range(sh.nrows):

        primeiraCelda = str(sh.cell(i, 0).value)
        if (primeiraCelda.startswith("##") or primeiraCelda == ""):
            continue

        #id = sh.cell(i, 1).value+"_"+sh.cell(i, 5).value+"_"+path_file
        id = sh.cell(i, 1).value + "_" + path_file
        print(id)

        tecnica = sh.cell(i, 6).value

        if (id not in termos):
            termos.append(id)

        modif = False
        if (sh.ncols > 8):
            if ("odificad" in sh.cell(i, 8).value):
                print(id + "\t" + tecnica + "\t" + sh.cell(i, 8).value)
                modif = True

        if( "wordnet" in tecnica):
            if (id not in traducidos_wordnet):
                traducidos_wordnet.append(id)
            if( modif and id not in traducidos_wordnet_modif):
                traducidos_wordnet_modif.append(id)

        elif ("mymemmory" in tecnica):
            if (id not in traducidos_mymemmory):
                traducidos_mymemmory.append(id)
            if (modif and id not in traducidos_mymemmory_modif):
                traducidos_mymemmory_modif.append(id)

        elif ("manual" in tecnica):
            print(id + "\t" + tecnica)

            if (id not in traducidos_manual):
                traducidos_manual.append(id)
    return listDict


#rutaDirectorio = "/home/jose/PycharmProjects/Flex/paquete/output/cheiro_pt/CHEIRO-20201110T184807Z-001/CHEIRO"   #RESULTADO FINAL
rutaDirectorio = "/home/jose/PycharmProjects/Flex/paquete/output/cheiro_pt/CHEIRO_FEITO-20201121T202618Z-001/"   #RESULTADO FINAL

if(os.path.isdir(rutaDirectorio)):
    for file in os.listdir(rutaDirectorio):
        if(file.endswith(".xlsx")):
            print(file)
            rutaFichero = os.path.join(rutaDirectorio, file)
            infoPaquete = obtenInfoPaqueteDoXlsx(rutaFichero)

print("\n")
print(len(termos))
print(len(traducidos_wordnet))
print(len(traducidos_wordnet_modif))
print(len(traducidos_mymemmory))
print(len(traducidos_mymemmory_modif))
print(len(traducidos_manual))