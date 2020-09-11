
git clone https://github.com/joseallones/Flex.git
cd Flex
chmod 755 flex.py

Script Usage:
usage: flex.py [-h] [-n NUM] [-p POS] [-g GEN] lemma lang

positional arguments:
  lemma              Base form
  lang               Language: pt: Portuguese, gl: Galician

optional arguments:
  -h, --help         show this help message and exit
  -n NUM, --num NUM  Number: S:singular; P:plural; N:invariable
  -p POS, --pos POS  POS: NC: Noun Common; NP: Noun Proper
  -g GEN, --gen GEN  Genre: F:feminine; M:masculine; C:common; N:neuter

Examples:
./flex.py neno gl --num=p --pos=NC
Output: [{"form": "nenas", "lemma": "neno", "pos": "NC", "gen": "F", "num": "P"}, {"form": "nenos", "lemma": "neno", "pos": "NC", "gen": "M", "num": "P"}]

./flex.py cativo pt --num=p --gen=f --pos=NC
Output: [{"form": "cativas", "lemma": "cativo", "pos": "NC", "gen": "F", "num": "P"}]


Dictionaries were obtained from freeling:
https://github.com/TALP-UPC/FreeLing/tree/master/data
https://github.com/TALP-UPC/FreeLing/releases

Tagsets
https://freeling-user-manual.readthedocs.io/en/latest/tagsets/tagset-gl/
https://freeling-user-manual.readthedocs.io/en/latest/tagsets/tagset-pt/#part-of-speech-noun
