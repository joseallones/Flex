import csv


# Function to convert a csv file to a list of dictionaries.
def csv_dict_list(variables_file):
    reader = csv.DictReader(open(variables_file, 'rt'))
    dict_list = []
    for line in reader:
        if(line['pos'].endswith('D')): #Descarta diminutivos
            continue
        dict_list.append(line)
    return dict_list

# Function to search for inflections based on various criteria
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

