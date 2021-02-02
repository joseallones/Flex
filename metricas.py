
import os

#Do traducido automáticamente mira canto é de wordnet e canto de mymemmory

termos = 0
num_total_traducidos_gl_wordnet = 0
num_total_traducidos_pt_wordnet = 0
num_total_traducidos_gl_mymemmory = 0
num_total_traducidos_pt_mymemmory = 0

def obtenInfoPaqueteDoCsv(path_file):

    global termos
    global num_total_traducidos_gl_wordnet
    global num_total_traducidos_pt_wordnet
    global num_total_traducidos_gl_mymemmory
    global num_total_traducidos_pt_mymemmory

    f = open(path_file, encoding='utf-8')
    for line in f:

        print("\nLine: " + line.strip())
        if("ili\tlema" in line):
            continue

        termos += 1

        data_line = line.rstrip().split('\t')
        print("data_line: " + str(data_line))

        if(data_line[2]!='[]'):
            num_total_traducidos_pt_wordnet += 1

        if (data_line[3] != '[]'):
            num_total_traducidos_gl_wordnet += 1


        if (data_line[4] != '[]'):
            print("data_line: " + data_line[4])
            num_total_traducidos_pt_mymemmory += 1

        if (data_line[5] != '[]'):
            num_total_traducidos_gl_mymemmory += 1



rutaDirectorio = "/home/jose/PycharmProjects/Flex/paquete/output/"   #RUTA SALIDA

if(os.path.isdir(rutaDirectorio)):
    for file in os.listdir(rutaDirectorio):
        if(file.endswith("servizoweb.xlsx")):
            print(file)
            rutaFichero = os.path.join(rutaDirectorio, file)
            infoPaquete = obtenInfoPaqueteDoCsv(rutaFichero)
            print(termos)
            print(num_total_traducidos_pt_wordnet)
            print(num_total_traducidos_gl_wordnet)
            print(num_total_traducidos_pt_mymemmory)
            print(num_total_traducidos_gl_mymemmory)
            print(num_total_traducidos_pt_wordnet + num_total_traducidos_pt_mymemmory)
            print(num_total_traducidos_gl_wordnet + num_total_traducidos_gl_mymemmory)

print('\n\nTotal')
print("num_total_termos " + str(termos))
print("num_total_traducidos_pt_wordnet " + str(num_total_traducidos_pt_wordnet ) + "\t" + str(num_total_traducidos_pt_wordnet * 100 / termos))
print("num_total_traducidos_gl_wordnet " + str(num_total_traducidos_gl_wordnet) + "\t" + str(num_total_traducidos_gl_wordnet * 100 / termos))
print("num_total_traducidos_pt_mymemmory " + str(num_total_traducidos_pt_mymemmory) + "\t" + str(num_total_traducidos_pt_mymemmory * 100 / termos))
print("num_total_traducidos_gl_mymemmory " + str(num_total_traducidos_gl_mymemmory) + "\t" + str(num_total_traducidos_gl_mymemmory * 100 / termos))
print("num_total_traducidos_pt " + str(num_total_traducidos_pt_wordnet + num_total_traducidos_pt_mymemmory) + "\t" + str((num_total_traducidos_pt_wordnet + num_total_traducidos_pt_mymemmory) * 100 / termos))
print("num_total_traducidos_gl " + str(num_total_traducidos_gl_wordnet + num_total_traducidos_gl_mymemmory) + "\t" + str((num_total_traducidos_gl_wordnet + num_total_traducidos_gl_mymemmory) * 100 / termos))
