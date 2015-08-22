#!/usr/bin/env python
#-*- encoding: utf-8 -*-
import nltk
import MeCab
import urllib2
from urllib2 import HTTPError
from itertools import chain
from BeautifulSoup import BeautifulSoup

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def tfidf(doc,docs):
  """対象の文書と全文の形態素解析した単語リストを指定すると対象の文書のTF-IDFを返す"""
  tokens = list(chain.from_iterable(docs)) #flatten
  A = nltk.TextCollection(docs)
  token_types = set(tokens)
  return [{"word":token_type,"tfidf":A.tf_idf(token_type, doc)} for token_type in token_types]


def extract_words(text):
  """テキストを与えると名詞のリストにして返す"""
  text =  text.encode("utf-8") if isinstance(text,unicode) else text
  mecab = MeCab.Tagger("")
  node = mecab.parseToNode(text)
  words = []
  while node:
    fs = node.feature.split(",")
    if (node.surface is not None) and node.surface != "" and fs[0] in [u'名詞']:
      words.append(node.surface)
    node = node.next
  return words

import unittest

class MachineLearningTest(unittest.TestCase):
  def test_extract_words(self):
    """形態素解析のテスト"""
    text = "textを形態素解析して、名詞のリストを返す"
    keywords = extract_words(text)
    self.assertEqual(keywords, ["text","形態素","解析","名詞","リスト"])
  def test_tfidf(self):
    """tfidfのテスト"""
    urls = ["http://qiita.com/puriketu99/items/"+str(i) for i in range(1,10)]
    def url2words(url):
      try:
        html = urllib2.urlopen(url).read()
      except HTTPError:
        html = ""
      #plain_text = nltk.clean_html(html).replace('\n','')#nltk.clean_html is not implement. instead of use beautifulsoup...
      soup = BeautifulSoup(html)
      
      #kill script tag and style tag
      for script in soup(["script","style"]):
        script.extract()
        
      plain_text = soup.getText()#plain_text がうまくいかないよ...
      #print plain_text
      words = extract_words(plain_text)
      return words
    docs = [url2words(url) for url in urls]
    tfidfs_fizzbuzz = tfidf(docs[0],docs)
    #print docs
    
    tfidfs_fizzbuzz.sort(cmp=lambda x,y:cmp(x["tfidf"],y["tfidf"]),reverse=True)
    result = [e for i,e in enumerate(tfidfs_fizzbuzz) if len(e["word"]) > 2 and i < 30]
    print result
    self.assertEqual(result[3]["word"],"yaotti")#Qiita側がデザイン変えるとテスト失敗するかも
    #[{'tfidf': 0.08270135278254376, 'word': 'quot'},
    # {'tfidf': 0.02819364299404901, 'word': 'FizzBuzz'},
    # {'tfidf': 0.02067533819563594, 'word': 'fizzbuzz'},
    # {'tfidf': 0.02067533819563594, 'word': 'Buzz'},
    # {'tfidf': 0.016916185796429405, 'word': 'Fizz'},
    # {'tfidf': 0.016726267030018446, 'word': 'end'},
    # {'tfidf': 0.015036609596826138, 'word': 'map'},
    # {'tfidf': 0.015036609596826138, 'word': 'yaotti'},
    # {'tfidf': 0.011277457197619604, 'word': 'def'}]

if __name__ == '__main__':
  unittest.main()





