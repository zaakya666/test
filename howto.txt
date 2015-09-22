#cloud9 で mecab python を使用する
$ sudo apt-get install mecab libmecab-dev mecab-ipadic
$ sudo apt-get install aptitude
$ sudo aptitude install mecab-ipadic-utf8
$ sudo apt-get install python-mecab
$ python
>>> import nltk
>>> nltk.download()
>>> d
>>> jeita
>>> d
>>> knbc
>>> q
>>> quit()

================================================================
#!/usr/bin/env python

# encoding: utf-8

# JEITAコーパスをNLTKで読み込むサンプル
#
from nltk_jp import *

from nltk.corpus.reader import *

from nltk.corpus.util import LazyCorpusLoader

# Pythonで日本語を含むオブジェクトを表示するための関数

import re, pprint

def pp(obj):

pp = pprint.PrettyPrinter(indent=4, width=160)

str = pp.pformat(obj)

return re.sub(r"\\u([0-9a-f]{4})", lambda x: unichr(int("0x"+x.group(1), 16)), str)

# コーパスを読み込み

#jeita = ChasenCorpusReader('home/ubuntu/nltk_data/corpora/jeita', r'.*chasen', encoding='utf-8')

jeita = LazyCorpusLoader('jeita', ChasenCorpusReader, r'.*chasen', encoding='utf-8')

print pp(jeita.words()[:10])

print pp(jeita.tagged_sents()[1])

=================================================================
