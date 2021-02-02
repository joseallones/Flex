
import os
import ast
import xlrd
import time
import csv


termos = []
traducidos_wordnet = []
traducidos_wordnet_modif = []
traducidos_mymemmory = []
traducidos_mymemmory_modif = []
traducidos_manual = []

def obtenInfoTradAutomaticas(path_file):

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




termos = []
traducidos_wordnet = []
traducidos_wordnet_modif = []
traducidos_mymemmory = []
traducidos_mymemmory_modif = []
traducidos_manual = []

def obtenTraduccionsAutomaticasDoCsv(path_file, idioma, source):

    # global termos
    # global num_total_traducidos_gl_wordnet
    # global num_total_traducidos_pt_wordnet
    # global num_total_traducidos_gl_mymemmory
    # global num_total_traducidos_pt_mymemmory

    termosPt = []
    termosGl = []

    f = open(path_file, encoding='utf-8')
    for line in f:

        #print("\nLine: " + line.strip())
        if("ili\tlema" in line):
            continue

        data_line = line.rstrip().split('\t')
        #print("data_line: " + str(data_line))

        if("pt" in idioma and data_line[2]!='[]' and ("wordnet" in source or "all" in source) ):
            if("<" not in data_line[2]):
                termosPt.extend(ast.literal_eval(data_line[2]))


        if ("gl" in idioma and data_line[3] != '[]' and ("wordnet" in source or "all" in source)):
            #print("data_line: " + data_line[3])
            if ("<" not in data_line[3]):
                termosGl.extend(ast.literal_eval(data_line[3]))

            # num_total_traducidos_gl_wordnet += 1


        if ("pt" in idioma and data_line[4] != '[]' and ("mymemmory" in source or "all" in source)):
            #print("data_line: " + data_line[4])
            if ("<" not in data_line[4]):
                termosPt.extend(ast.literal_eval(data_line[4]))
            # num_total_traducidos_pt_mymemmory += 1

        if ("gl" in idioma and data_line[5] != '[]' and ("mymemmory" in source or "all" in source)):
            #print("data_line: " + data_line[5])
            if ("<" not in data_line[5]):
                termosGl.extend(ast.literal_eval(data_line[5]))
            # num_total_traducidos_gl_mymemmory += 1

    if ("pt" in idioma):
        #print("termosPt: " + str(termosPt))
        return termosPt

    if ("gl" in idioma):
        #print("termosGl: " + str(termosGl))
        return termosGl

def obtenTraducionesFinalesXlsx(path_file):

    listTrads = []


    try:

        wb = xlrd.open_workbook(path_file)
        sh = wb.sheet_by_index(0)
        #print(sh.ncols)


        for i in range(sh.nrows):
            trad = sh.cell(i, 1).value
            if(trad):
                if(trad not in listTrads):
                    listTrads.append(trad)
                    #print( trad )

        return listTrads

    except:
        print("An exception occurred")
        return None

rutaDirectorio = "/home/jose/PycharmProjects/Flex/paquete/output/"   #RUTA SALIDA
rutaDirectorioRevisado = "/home/jose/PycharmProjects/Flex/paquete/output/cheiro_pt/CHEIRO_FEITO-20201121T202618Z-001"  # RESULTADO FINAL


contadorTotalTradsCorrectas = 0
contadorTotalTradsEliminadas = 0


if(os.path.isdir(rutaDirectorio)):
    for file in os.listdir(rutaDirectorio):
        if(file.endswith("servizoweb.xlsx")):
            time.sleep(0.1)

            print("\n\n"+file)
            rutaFicheroAuto = os.path.join(rutaDirectorio, file)
            # tradGl = obtenTraduccionsDoCsv(rutaFichero,'gl')
            # print("termosGl: " + str(tradGl))

            tradPtAuto = obtenTraduccionsAutomaticasDoCsv(rutaFicheroAuto, 'pt', "all")
            print("termosPt: " + str(tradPtAuto))



            file = "pt_cheiro_"+file[8:].replace("_resultados_servizoweb","").replace("  ","_").replace(" ","_").replace("_.xlsx",".xlsx")
            print(file)
            rutaFichero = os.path.join(rutaDirectorioRevisado, file)
            print(rutaFichero)
            tradPtFinal = obtenTraducionesFinalesXlsx(rutaFichero)



            if(tradPtFinal==None):
                print ("problem")
                continue

            obtenInfoTradAutomaticas(rutaFichero)

            print("termosPt (auto): " + str(tradPtAuto))
            print("termosPt (final): " + str(tradPtFinal))

            contadorCorrecto = 0
            contadorEliminado = 0

            for term in tradPtAuto:
                if( len(term)<3):
                    print(term)
                    continue
                if term in tradPtFinal:
                    contadorCorrecto += 1
                else:
                    contadorEliminado += 1

            contadorTotalTradsCorrectas += contadorCorrecto
            contadorTotalTradsEliminadas += contadorEliminado

            print('\n\ncontadorTotalTradsCorrectas: ' + str(contadorTotalTradsCorrectas))
            print('contadorTotalTradsEliminadas: ' + str(contadorTotalTradsEliminadas))
            print('')

print("\n")
print(len(termos))
print(len(traducidos_wordnet))
print(len(traducidos_wordnet_modif))
print(len(traducidos_mymemmory))
print(len(traducidos_mymemmory_modif))
print(len(traducidos_manual))


print('\n\ncontadorTotalTradsCorrectas: ' + str(contadorTotalTradsCorrectas))
print('contadorTotalTradsEliminadas: ' + str(contadorTotalTradsEliminadas))


# Termos traducidos por Wordnet correctos: 635
# Termos traducidos por Wordnet eliminados: 287

# Termos traducidos por Mymemory correctos: 1822
# Termos traducidos por Mymemory eliminadas: 3749

# Termos traducidos por Wordnet+Mymemory correctos: 2457
# Termos traducidos por Wordnet+Mymemory eliminados: 4036