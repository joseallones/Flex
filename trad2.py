
from methods_trad import *

listDict = []
listDict.append({"ili": "0000A", "lema_spa": "Zurich"})
listDict.append({"ili": "0000B", "lema_spa": "Ámsterdam"})
listDict.append({"ili": "0000C", "lema_spa": "Ankara"})
listDict.append({"ili": "0000D", "lema_spa": "Antioquía"})




#detailsTradPt = obtenTraduccionsMyMemmory(listDict, "pt")

detailsTradPt = obtenTraduccionsMyMemmory(listDict, "gl")
print(listDict)