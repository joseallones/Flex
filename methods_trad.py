import requests
import json
from urllib.parse import quote


from methods_io import gardaDiccionarioNunFicheiro


def obtenTraduccionsMyMemmory(infoPaquete, lang):

    url = 'https://api.mymemory.translated.net/get?langpair=es|' + lang +'&de=joseallones87@gmail.com&q='

    for dict in infoPaquete:

        if lang == "pt":
            dict["trad_por_mymemmory"] = []
        elif lang == "gl":
            dict["trad_glg_mymemmory"] = []

        if lang == "pt" and 'lema_por' in dict.keys() and dict['lema_por']:
            continue

        if lang == "gl" and 'lema_glg' in dict.keys() and dict['lema_glg']:
            continue

        print(url+quote(dict['lema_spa']))
        r = requests.get(url+dict['lema_spa'])
        r.encoding = 'utf-8'
        json_data = json.loads(r.text)

        matches = json_data["matches"]
        listTrad = []
        for match in matches:
            if(match['segment'].lower()==dict['lema_spa']):
                if(match['translation'].lower() not in listTrad):
                    listTrad.append(match['translation'].lower())
                    print(match['segment'])
                    print(match['translation'].lower() + "  " + str(match['quality']) + "  " + str(match['match']) )

        if lang == "pt":
            dict["trad_por_mymemmory"] = listTrad
        elif lang == "gl":
            dict["trad_glg_mymemmory"] = listTrad

#Función para obter os termos asociados aos ILIs. Chama ao servizo de wordnet.pt
def obtenTermos_AsociadosA_ILIs(infoPaquete):

    contador_por_sen_termos_wordnet = 0
    contador_glg_sen_termos_wordnet = 0
    url = 'http://wordnet.pt/package'

    for dict in infoPaquete:

        listaUnIli = []
        listaUnIli.append(dict["ili"])

        r = requests.post(url, json=listaUnIli)
        r.encoding = 'utf-8'
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



    print("\n\nNúmero de ILIs sen termos para o portugués " + str(contador_por_sen_termos_wordnet))
    print("Número de ILIs sen termos para o galego " + str(contador_glg_sen_termos_wordnet))