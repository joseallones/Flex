import csv



from methods_io import gardaListadoNunFicheiro

dict_list_subs_gl = []
dict_list_subs_pt = []
dict_list_subs_ge = []
dict_list_subs_fr = []
dict_list_adxs_gl = []
dict_list_adxs_pt = []
dict_list_adxs_ge = []
dict_list_adxs_fr = []

# Función para leer un paquete csv e crear una lista de diccionarios
def csv_dict_list(variables_file):
    reader = csv.DictReader(open(variables_file, 'rt', encoding='utf-8'))
    dict_list = []
    for line in reader:
        if(line['pos'].endswith('D')): #Descarta diminutivos
            continue
        dict_list.append(line)
    return dict_list


def recupera_diccionario(tipo):

    global dict_list_subs_gl
    global dict_list_subs_pt
    global dict_list_subs_ge
    global dict_list_subs_fr
    global dict_list_adxs_gl
    global dict_list_adxs_pt
    global dict_list_adxs_ge
    global dict_list_adxs_fr


    if(tipo == "nouns_gl"):
        if dict_list_subs_gl:
            return dict_list_subs_gl
        else:
            dict_list_subs_gl = csv_dict_list("data/nouns_gl.csv")
            return dict_list_subs_gl

    elif (tipo == "nouns_pt"):
        if dict_list_subs_pt:
            return dict_list_subs_pt
        else:
            dict_list_subs_pt = csv_dict_list("data/nouns_pt.csv")
            return dict_list_subs_pt

    elif (tipo == "nouns_ge"):
        if dict_list_subs_ge:
            return dict_list_subs_ge
        else:
            dict_list_subs_ge = csv_dict_list("data/nouns_ge.csv")
            return dict_list_subs_ge

    elif (tipo == "nouns_fr"):
        if dict_list_subs_fr:
            return dict_list_subs_fr
        else:
            dict_list_subs_fr = csv_dict_list("data/nouns_fr.csv")
            return dict_list_subs_fr

    elif (tipo == "adxs_pt"):
        if dict_list_adxs_pt:
            return dict_list_adxs_pt
        else:
            dict_list_adxs_pt = csv_dict_list("data/adxs_pt.csv")
            return dict_list_adxs_pt

    elif (tipo == "adxs_gl"):
        if dict_list_adxs_gl:
            return dict_list_adxs_gl
        else:
            dict_list_adxs_gl = csv_dict_list("data/adxs_gl.csv")
            return dict_list_adxs_gl

    elif (tipo == "adxs_ge"):
        if dict_list_adxs_ge:
            return dict_list_adxs_ge
        else:
            dict_list_adxs_ge = csv_dict_list("data/adxs_ge.csv")
            return dict_list_adxs_ge

    elif (tipo == "adxs_fr"):
        if dict_list_adxs_fr:
            return dict_list_adxs_fr
        else:
            dict_list_adxs_fr = csv_dict_list("data/adxs_fr.csv")
            return dict_list_adxs_fr

    else:
        return []

# Función para buscar as flexións para un lema
def search(lemma, lang = "pt",  pos = None, gen = None, num = None):

    dict_list_subs = []
    dict_list_adx = []

    if lang:
        if lang.upper() =="GL" or lang.upper() == "GAL" or lang.upper() == "GLG":
            dict_list_subs = recupera_diccionario("nouns_gl")
            dict_list_adx = recupera_diccionario("adxs_gl")
        elif lang.upper() =="GE" or lang.upper() =="DE" or lang.upper() =="ALE":
            dict_list_subs = recupera_diccionario("nouns_ge")
            dict_list_adx = recupera_diccionario("adxs_ge")
        elif lang.upper() =="FR":
            dict_list_subs = recupera_diccionario("nouns_fr")
            dict_list_adx = recupera_diccionario("adxs_fr")
        elif lang.upper() == "PT" or lang.upper() == "POR":
            dict_list_subs = recupera_diccionario("nouns_pt")
            dict_list_adx = recupera_diccionario("adxs_pt")

    listSubs = []
    listAdxs = []
    listSubsNormalizados = []
    listAdxsNormalizados = []

    if(not pos or (pos and pos.upper().startswith("N")) ):
        listSubs = [element for element in dict_list_subs if element['lemma'] == lemma.lower()]

        if pos:
            if(len(pos)==1):
                listSubs = [element for element in listSubs if element['pos'][0:1] == pos.upper()]
            elif (len(pos) == 2):
                listSubs = [element for element in listSubs if element['pos'][0:2] == pos.upper()]

        if gen:
            if (lang.upper() == "GE" or lang.upper() =="DE" or lang.upper() =="ALE"):
                listSubs = [element for element in listSubs if element['pos'][3] == gen.upper()]
            else:
                listSubs = [element for element in listSubs if element['pos'][2] == gen.upper()]

        if num:
            if (lang.upper() == "GE" or lang.upper() =="DE" or lang.upper() =="ALE"):
                listSubs = [element for element in listSubs if element['pos'][4] == num.upper()]
            else:
                listSubs = [element for element in listSubs if element['pos'][3] == num.upper()]

        for element in listSubs:
            elementNormalizado = element.copy()
            if (lang.upper() == "GE" or lang.upper() =="DE" or lang.upper() =="ALE"):
                elementNormalizado['gen'] = element['pos'][3]  # NCDMP0  --> M
                elementNormalizado['num'] = element['pos'][4]  # NCDMP0 --> P
                elementNormalizado['type'] = element['pos'][1]
                elementNormalizado['case'] = element['pos'][2]

            else:
                elementNormalizado['gen'] = element['pos'][2]    #NCMP000 --> M
                elementNormalizado['num'] = element['pos'][3]    #NCMP000 --> P
            elementNormalizado['pos'] = element['pos'][0:1]  #So a primeira letra (NCMP000 --> N)
            listSubsNormalizados.append(elementNormalizado)

    if (not pos or (pos and pos.upper().startswith("A")) ):
        listAdxs = [element for element in dict_list_adx if element['lemma'] == lemma.lower()]

        if pos:
            listAdxs = [element for element in listAdxs if element['pos'][0:1] == pos.upper()]

        if gen:
            listAdxs = [element for element in listAdxs if element['pos'][3] == gen.upper()]

        if num:
            listAdxs = [element for element in listAdxs if element['pos'][4] == num.upper()]

        for element in listAdxs:
            elementNormalizado = element.copy()
            if (lang.upper() == "GE" or lang.upper() =="DE" or lang.upper() =="ALE"):
                elementNormalizado['type'] = element['pos'][1]  # AQAFSC --> Q
                elementNormalizado['case'] = element['pos'][2]  # AQAFSC --> A
            elementNormalizado['gen'] = element['pos'][3]  # AQ0FS --> F
            elementNormalizado['num'] = element['pos'][4]  # AQ0FS --> S
            elementNormalizado['pos'] = element['pos'][0:1]  # So a primeira letra (AQ0FS --> A)
            if (lang.upper() == "GE" or lang.upper() =="DE" or lang.upper() =="ALE"):
                elementNormalizado['degree'] = element['pos'][5]  # AQAFSC --> C

            listAdxsNormalizados.append(elementNormalizado)

    listTotal = listSubsNormalizados + listAdxsNormalizados
    return listTotal


# Función para buscar as flexións para un "paquete"
# infoPaquete é unha lista de diccionarios
def obterFlexionsPaquete(infoPaquete, lang, rutaFicheiroTermosSenFlexions):
    listadoResultadosFlexions = []
    termos_sen_flexions = []

    for dict in infoPaquete:

        source = "wordnet"

        lemas = []
        if (lang == "pt"):
            lemas = dict["lema_por"]
        elif (lang == "gl"):
            lemas = dict["lema_glg"]
        elif (lang == "de"):
            lemas = dict["lema_ale"]
        elif (lang == "fr"):
            lemas = dict["lema_fra"]


        if (not lemas):
            source = "mymemmory"
            if (lang == "pt"):
                lemas = dict["trad_por_mymemmory"]
            elif (lang == "gl"):
                lemas = dict["trad_glg_mymemmory"]
            elif lang == "fr":
                lemas = dict["trad_fra_mymemmory"]
            elif lang == "de":
                lemas = dict["trad_ale_mymemmory"]

        if (not lemas or dict['ili']==""):
            continue

        for lema in lemas:  # Para cada lema

            lema = lema.replace("_", " ")

            pos = ""
            if dict['ili'][-1].lower() == 'a':
                pos = 'A'
                #print(pos + " " + dict['ili'])
            elif dict['ili'][-1].lower() == 'n':
                pos = 'NC'
            else:
                print("ILI sin terminación " + dict['ili'])

            resultadoAux = []
            if pos:
                resultadoAux = search(lemma=lema, lang=lang, pos = pos)

            else:  #se pos (ili) non definido non se filtra por pos
                resultadoAux = search(lemma=lema, lang=lang)

            term = str(dict['lema_spa']).replace("_", " ")

            if resultadoAux:
                for r in resultadoAux:
                    r['ili'] = dict['ili']
                    r['source'] = source
                    r['lema_spa'] = term
                listadoResultadosFlexions = listadoResultadosFlexions + resultadoAux
            else:
                termos_sen_flexions.append(lema)

                if (pos=="NC"):
                    pos = "N"

                if(lang == "de"):

                    if(pos=="A"):
                        listadoResultadosFlexions.append(
                            {"form": "", "lemma": lema, "pos": pos, "gen": "", "num": "", "type": "", "case":"", "degree":"",
                             "ili": dict["ili"], "source": source, "lema_spa": term})
                    else:
                        listadoResultadosFlexions.append(
                            {"form": "", "lemma": lema, "pos": pos, "gen": "", "num": "", "type": "", "case": "",
                             "ili": dict["ili"], "source": source, "lema_spa": term})
                else:
                    listadoResultadosFlexions.append({"form": "", "lemma": lema, "pos": pos, "gen": "", "num": "", "ili": dict["ili"], "source": source, "lema_spa": term})

    # print("Lista de flexións para o " + lang + ":" )
    # print(listadoResultadosFlexions)

    print("Termos do " + lang + " sin flexións:" )
    print(termos_sen_flexions)

    gardaListadoNunFicheiro(termos_sen_flexions, rutaFicheiroTermosSenFlexions)

    return listadoResultadosFlexions


