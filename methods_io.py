import csv
import xlrd


def gardaDiccionarioNunFicheiro(infoPaquete, nomeFicheiro):


    with open(nomeFicheiro, 'w', newline='', encoding='utf-8') as output_file:
        if infoPaquete:
            keys = infoPaquete[0].keys()
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(infoPaquete)

def gardaDiccionarioNunFicheiroDelimiterTab(infoPaquete, nomeFicheiro):

    with open(nomeFicheiro, 'w', newline='', encoding='utf-8') as output_file:
        if infoPaquete:
            keys = infoPaquete[0].keys()
            dict_writer = csv.DictWriter(output_file, keys, delimiter='\t')
            dict_writer.writeheader()
            dict_writer.writerows(infoPaquete)

def gardaListadoNunFicheiro(listado, nomeFicheiro):
     with open(nomeFicheiro, 'w', encoding='utf-8') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(listado)


def obtenInfoPaqueteDoCsv(path_file):

    f = open(path_file, encoding='utf-8')
    listaILIsUnicos = []
    listDict = []

    for line in f:
        print (line)
        data_line = line.rstrip().split(',')
        if(data_line[5] not in listaILIsUnicos):
            listaILIsUnicos.append(data_line[5])
            listDict.append({"ili": data_line[5], "lema_spa": data_line[1]})
            #print(data_line[5] + " " + data_line[1])
    return listDict

def obtenInfoPaqueteDoXlsx(path_file):

    listDict = []
    listaILIsUnicos = []

    wb = xlrd.open_workbook(path_file)
    sh = wb.sheet_by_index(0)
    for i in range(sh.nrows):

        # print(sh.cell(i, 0).value)
        primeiraCelda = sh.cell(i, 0).value
        primeiraCelda = str(primeiraCelda)
        if(primeiraCelda.startswith("##") or primeiraCelda==""):
            continue

        # print(sh.cell(i, 5).value)
        if ( sh.cell(i, 5).value not in listaILIsUnicos):
            listDict.append({"ili": sh.cell(i, 5).value, "lema_spa": sh.cell(i, 1).value})
            listaILIsUnicos.append(sh.cell(i, 5).value)

    return listDict

def obtenTermosDoTXT(path_file, lang):
    try:
        f = open(path_file, encoding='utf-8')

        listDict = []

        for line in f:
            if "#" in line[0] or " " in line[0] or "\n" in line[0]:
                continue

            elif line[0].isdigit():
                data_line = line.rstrip().split(' ')
                ili = data_line[1]

            else:
                if(ili):
                    listTerms = []
                    listTerms.append(line.strip())

                    if(lang=="pt"):
                        listDict.append({"ili": ili, "lema_por": listTerms})
                    else:
                        listDict.append({"ili": ili, "lema_glg": listTerms})
                ili = ""

        return listDict

    except:
        print("\nNon atopo o ficheiro .txt. A ruta do ficheiro pode ser incorrecta.")
        exit(2)