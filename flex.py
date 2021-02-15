#!/usr/bin/env python

import json
import argparse

from methods_flex import search


def parseArguments():
    # Create argument parser
    parser = argparse.ArgumentParser()

    # Positional mandatory arguments
    parser.add_argument("lemma", help="Base form", type=str)
    parser.add_argument("lang", help="Language: pt: Portuguese, gl: Galician, de: German, fr: French", type=str)

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