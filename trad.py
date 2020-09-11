import mysql.connector
import requests
import json
import csv

from methods_flex import search

cnx = mysql.connector.connect(user='DB', password='password', host='127.0.0.1', database='xera_reestructurado')

actante_id = "259";


#Paso 1: Recupera ILIs de un paquete (de la BD)
listaILIs=[]
cursor = cnx.cursor(buffered=True)
cursor.execute("select distinct(referencia_wordnet), lema from xera_actante_formas  "
               "inner join xera_forma on xera_forma.id = xera_actante_formas.forma_id  "
               "inner join xera_lema_formas on xera_actante_formas.forma_id = xera_lema_formas.forma_id "
               "inner join xera_lema on xera_lema_formas.lema_id = xera_lema.id "
               "where xera_actante_formas.actante_id = " + actante_id)
for ( referencia_wordnet,lema ) in cursor:
    #print(referencia_wordnet + " " + lema)
    listaILIs.append(referencia_wordnet)

print("Lista de ILIs asociados al paquete:")
print(listaILIs)



#Paso 2: Obter os términos dos ILIs (synsets) nos distintos idiomas
url = 'http://wordnet.pt/package'
r = requests.post(url, json=listaILIs)
json_data = json.loads(r.text)
#print(r.text)
#print(json_data["por-30"])


#Paso 3.1: Pasar os termos al flexionador para o portugués
package_results_pt = []
terms_no_flex_pt = []
for term in json_data["por-30"]:

    results = search( lemma=term, lang="pt")
    # print(term)
    # json_results = json.dumps(results, sort_keys=False, ensure_ascii=False)
    # print(json_results)
    if results:
        package_results_pt = package_results_pt + results
    else:
        terms_no_flex_pt.append(term)

#Paso 3.2: Pasar os termos al flexionador para o para o galego
package_results_gl = []
terms_no_flex_gl = []
for term in json_data["glg-30"]:
    results = search( lemma=term, lang="gl")
    if results:
        package_results_gl = package_results_gl + results
    else:
        terms_no_flex_gl.append(term)

print("Lista de flexións para pt:")
print(package_results_pt)
print("Termos sin flexións para pt:")
print(terms_no_flex_pt)

print("Lista de flexións para gl:")
print(package_results_gl)
print("Termos sin flexións para pt:")
print(terms_no_flex_gl)

#Paso 4.1: Creación dos ficheiros CSVs com lema, flexión, e indicadores de PoS.  Falta ILI!
keys = package_results_pt[0].keys()
with open('package_pt.csv', 'w', newline='')  as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(package_results_pt)

keys = package_results_gl[0].keys()
with open('package_gl.csv', 'w', newline='')  as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(package_results_gl)

#Paso 4.2: Creación dos ficheiros con términos sin flexións
with open('terms_no_flex_pt.csv', 'w') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(terms_no_flex_pt)

with open('terms_no_flex_gl.csv', 'w') as myfile:
    wr = csv.writer(myfile, quoting=csv.QUOTE_ALL)
    wr.writerow(terms_no_flex_gl)

cnx.close()