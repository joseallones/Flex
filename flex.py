#!/usr/bin/env python
 
import csv
import json
import argparse, sys


# Function to convert a csv file to a list of dictionaries.
def csv_dict_list(variables_file):
    reader = csv.DictReader(open(variables_file, 'rt'))
    dict_list = []
    for line in reader:
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
        element['gen'] = element['pos'][2]
        element['num'] = element['pos'][3]
        element['pos'] = element['pos'][0:2]

    return list

def parseArguments():
    # Create argument parser
    parser = argparse.ArgumentParser()

    # Positional mandatory arguments
    parser.add_argument("lemma", help="Base form", type=str)
    parser.add_argument("lang", help="Language: pt: Portuguese, gl: Galician ", type=str)

    # Optional arguments
    parser.add_argument("-n", "--num", help="Number: S:singular; P:plural; N:invariable", type=str, default="")
    parser.add_argument("-p", "--pos", help="POS: NC: Noun Common; NP: Noun Proper", type=str, default="")
    parser.add_argument("-g", "--gen", help="Genre: F:feminine; M:masculine; C:common; N:neuter", type=str, default="")

    # Parse arguments
    args = parser.parse_args()

    return args

args = parseArguments()

results = search( args.lemma, args.lang, pos=args.pos, gen=args.gen, num=args.num )
json_results = json.dumps(results, sort_keys=False, ensure_ascii=False)
print(json_results)