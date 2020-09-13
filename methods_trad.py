import mysql.connector
import requests
import json
import csv

from methods_flex import search


#Devolve un listado de diccionarios coa información dos ILIS (ili + lema) asociados a un paquete
def obtenInfoPaqueteDaBD(id_actante):

    cnx = mysql.connector.connect(user='DB', password='password', host='127.0.0.1', database='xera_reestructurado')
    listaILIs = []
    listDict = []
    cursor = cnx.cursor(buffered=True)
    cursor.execute("select distinct referencia_wordnet,lema from xera_actante_formas  "
                   "inner join xera_forma on xera_forma.id = xera_actante_formas.forma_id  "
                   "inner join xera_lema_formas on xera_actante_formas.forma_id = xera_lema_formas.forma_id "
                   "inner join xera_lema on xera_lema_formas.lema_id = xera_lema.id "
                   "where xera_actante_formas.actante_id = " + id_actante + " order by lema")
    for (referencia_wordnet, lema) in cursor:

        if (not lema[0].isupper()):  ##Descarto lemas que empezan por maiúsculas (nome de países)
            #print(referencia_wordnet + " " + lema)
            listaILIs.append(referencia_wordnet)
            listDict.append({"ili": referencia_wordnet, "lema_spa": lema})

    cnx.close()
    return listDict


def obtenListadoILIsDePaquete(infoPaquete):
    listaILIs = []
    for dict in infoPaquete:
        if( dict['ili'] not in listaILIs):
            listaILIs.append(dict['ili'])
    print(listaILIs)
    print(len(listaILIs))
    return listaILIs


# Function to convert a csv file to a list of dictionaries.
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



def computoDiferenciasInfo_BD_vs_CSV(infoPaqueteBD, listaILIsBD, infoPaqueteDoCSV, listaILIsCSV):
    # Computo as diferencias entre a información que ven da BD e do CSV
    print("\nILIs na BD non atopados no CSV:")
    for ili in listaILIsBD:
        if (ili not in listaILIsCSV):
            for dict in infoPaqueteBD:
                if (dict['ili'] == ili):
                    print(ili + "\t" + dict['lema_spa'])

    print("\nILIs no CSV non atopados na BD:")
    for ili in listaILIsCSV:
        if (ili not in listaILIsBD):
            for dict in infoPaqueteDoCSV:
                if (dict['ili'] == ili):
                    print(ili + "\t" + dict['lema_spa'])


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

def obtenTermos_AsociadosA_ILIs(infoPaquete):

    contador_por_sen_termos_wordnet = 0
    contador_glg_sen_termos_wordnet = 0
    url = 'http://wordnet.pt/package'

    for dict in infoPaquete:

        listaUnIli = []
        listaUnIli.append(dict["ili"])
        r = requests.post(url, json=listaUnIli)
        json_data = json.loads(r.text)

        dict["lema_por"] = []
        dict["lema_glg"] = []

        if "por-30" in json_data:
            dict["lema_por"] = json_data["por-30"]
        else:
            contador_por_sen_termos_wordnet += 1

        if "glg-30" in json_data:
            dict["lema_glg"] = json_data["glg-30"]
        else:
            contador_glg_sen_termos_wordnet += 1

    # Garda a información dos léxicos atopados nun fichero
    gardaDiccionarioNunFicheiro(infoPaquete, 'resultados_lexico_servizo_web.csv')

    print("\n\nNúmero de ILIs sen termos para o portugués " + str(contador_por_sen_termos_wordnet))
    print("Número de ILIs sen termos para o galego " + str(contador_glg_sen_termos_wordnet))


def obterFlexions(infoPaquete, lang):
    listadoResultadosFlexions = []
    termos_sen_flexions = []

    for dict in infoPaquete:

        lemas = []
        if (lang == "pt"):
            lemas = dict["lema_por"]
        elif (lang == "gl"):
            lemas = dict["lema_glg"]

        if (not lemas):
            continue

        for lema in lemas:  # Para cada lema/termo

            resultadoAux = search(lemma=lema, lang=lang)
            if resultadoAux:
                for r in resultadoAux:
                    r['ili'] = dict['ili']
                listadoResultadosFlexions = listadoResultadosFlexions + resultadoAux
            else:
                termos_sen_flexions.append(lema)

    # print("Lista de flexións para o " + lang + ":" )
    # print(listadoResultadosFlexions)


    print("\n\nTermos do " + lang + " sin flexións:" )
    print(termos_sen_flexions)

    if (lang == "pt"):
        gardaListadoNunFicheiro(termos_sen_flexions, 'termos_sen_flexions_pt.csv')

    elif (lang == "gl"):
        gardaListadoNunFicheiro(termos_sen_flexions, 'termos_sen_flexions_gl.csv')

    return listadoResultadosFlexions

