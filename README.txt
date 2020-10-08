
git clone https://github.com/joseallones/Flex.git
cd Flex

Repo contains several scripts:
flex.py  --> to flex one term
flex_ficheiro_txt.py --> to flex terms included in a txt file
flex_ficheiros_txt.py --> to flex terms included in all txt files from a directory
trad.py --> to translate and flex terms included in all txt files from a directory

##  Flex.py

Script Usage:
python3 flex.py [-h] [-n NUM] [-p POS] [-g GEN] lemma lang

positional arguments:
 lemma              Base form
 lang  					Language: pt: Portuguese, gl: Galician

optional arguments:
  -h, --help         show this help message and exit
  -n NUM, --num NUM Number: S:singular; P:plural; N:invariable
  -p POS, --pos POS POS: NC: Noun Common; NP: Noun Proper
  -g GEN, --gen GEN Genre: F:feminine; M:masculine; C:common; N:neuter

Examples:
 python3 flex.py neno gl --num=p --pos=NC
Output: [{"form": "nenas", "lemma": "neno", "pos": "NC", "gen": "F", "num": "P"}, {"form": "nenos", "lemma": "neno", "pos": "NC", "gen": "M", "num": "P"}]

 python3 flex.py cativo pt --num=p --gen=f --pos=NC
Output: [{"form": "cativas", "lemma": "cativo", "pos": "NC", "gen": "F", "num": "P"}]

##  flex_ficheiro_txt.py

Script Usage:
python3 flex_ficheiro_txt.py path_file lang

Positional arguments (required):
path_file :   path of the txt file with the terms to be flexed
lang : Language: pt: Portuguese, gl: Galician

Example:
python3 flex_ficheiro_txt.py txt/adx_familia.txt pt


##  flex_ficheiros_txt.py

Script Usage:
python3 flex_ficheiros_txt.py path_directory lang

Positional arguments (required):
path_directory :   path of the directory with the files to be flexed
lang : Language: pt: Portuguese, gl: Galician

Example:
python3 flex_ficheiro_txt.py /home/data/txt pt


##  trad.py


The script performs translations (using the Wordnet and MyMemmory services) and inflections in Galician and Portuguese

Script Usage:
python3 trad.py path_directory

Positional arguments (required):
path_directory :   path of the directory with the files to be translated

Example:
python3 flex_ficheiro_txt.py /home/data/txt pt


## Dictionaries and services

Dictionaries were obtained from freeling:
https://github.com/TALP-UPC/FreeLing/tree/master/data
https://github.com/TALP-UPC/FreeLing/releases

Tagsets
https://freeling-user-manual.readthedocs.io/en/latest/tagsets/tagset-gl/
https://freeling-user-manual.readthedocs.io/en/latest/tagsets/tagset-pt/#part-of-speech-noun

Translate services:
http://wordnet.pt/api
https://mymemory.translated.net/doc/spec.php
