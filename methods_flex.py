import csv



from methods_io import gardaListadoNunFicheiro


# Función para leer un paquete csv e crear una lista de diccionarios
def csv_dict_list(variables_file):
    reader = csv.DictReader(open(variables_file, 'rt', encoding='utf-8'))
    dict_list = []
    for line in reader:
        if(line['pos'].endswith('D')): #Descarta diminutivos
            continue
        dict_list.append(line)
    return dict_list


# Función para buscar as flexións para un lema
def search(lemma, lang = "pt",  pos = None, gen = None, num = None):

    dict_list = []
    if lang:
        if lang.upper() =="GL":
            dict_list = csv_dict_list("data/nouns_gl.csv")
        elif lang.upper() =="PT":
            dict_list = csv_dict_list("data/nouns_pt.csv")
    else:
        dict_list = csv_dict_list("data/nouns_pt.csv")

    list = [element for element in dict_list if element['lemma'] == lemma.lower()]

    if pos:
        list = [element for element in list if element['pos'][0:2] == pos.upper()]

    if gen:
        list = [element for element in list if element['pos'][2] == gen.upper()]

    if num:
        list = [element for element in list if element['pos'][3] == num.upper()]

    for element in list:
        element['gen'] = element['pos'][2]    #NCMP000 --> M
        element['num'] = element['pos'][3]    #NCMP000 --> P
        element['pos'] = element['pos'][0:1]  #So a primeira letra (NCMP000 --> N)


    return list


# Función para buscar as flexións para un "paquete"
# infoPaquete é unha lista de diccionarios
def obterFlexionsPaquete(infoPaquete, lang, rutaFicheiroTermosSenFlexions):
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

        for lema in lemas:  # Para cada lema

            resultadoAux = search(lemma=lema, lang=lang)
            if resultadoAux:
                for r in resultadoAux:
                    r['ili'] = dict['ili']
                listadoResultadosFlexions = listadoResultadosFlexions + resultadoAux
            else:
                termos_sen_flexions.append(lema)
                listadoResultadosFlexions.append({"form": "", "lemma": lema, "pos": "N", "gen": "", "num": "", "ili": dict["ili"]})

    # print("Lista de flexións para o " + lang + ":" )
    # print(listadoResultadosFlexions)

    print("\n\nTermos do " + lang + " sin flexións:" )
    print(termos_sen_flexions)

    gardaListadoNunFicheiro(termos_sen_flexions, rutaFicheiroTermosSenFlexions)

    return listadoResultadosFlexions