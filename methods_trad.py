import requests
import json

from methods_io import gardaDiccionarioNunFicheiro


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