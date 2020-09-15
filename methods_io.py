import csv


def gardaDiccionarioNunFicheiro(infoPaquete, nomeFicheiro):
    keys = infoPaquete[0].keys()
    with open(nomeFicheiro, 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(infoPaquete)


def gardaListadoNunFicheiro(listado, nomeFicheiro):
     with open(nomeFicheiro, 'w') as myfile:
        wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
        wr.writerow(listado)


def obtenInfoPaqueteDoCsv(path_file):

    f = open(path_file)
    listaILIsUnicos = []
    listDict = []

    for line in f:
        data_line = line.rstrip().split(',')
        if(data_line[5] not in listaILIsUnicos):
            listaILIsUnicos.append(data_line[5])
            listDict.append({"ili": data_line[5], "lema_spa": data_line[1]})
            #print(data_line[5] + " " + data_line[1])
    return listDict


def obtenTermosDoTXT(path_file):
    try:
        f = open(path_file)

        listDict = []

        for line in f:
            if "#" in line[0] or " " in line[0] or "\n" in line[0]:
                continue

            elif line[0].isdigit():
                data_line = line.rstrip().split(' ')
                ili = data_line[1]

            else:
                if(ili):
                    listTermsGlg = []
                    listTermsGlg.append(line.strip())
                    listDict.append({"ili": ili, "lema_glg": listTermsGlg})
                ili = ""

        return listDict

    except:
        print("\nNon atopo o ficheiro .txt. A ruta do ficheiro pode ser incorrecta.")
        exit(2)