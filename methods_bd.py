import mysql.connector


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