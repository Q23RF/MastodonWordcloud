"""
文字雲部分參考: https://tech.havocfuture.tw/blog/python-wordcloud-jieba
Colab筆記本: https://colab.research.google.com/drive/11o6RFfKxEW_CD1tCTpb8FWotOrSsrgfD
"""

import requests
import json
from bs4 import BeautifulSoup

my_handle = "qrf"
my_instance = "klog.tw"

response = requests.get("https://{instance}/api/v1/accounts/lookup?acct={handle}".format(
    instance=my_instance, handle=my_handle))
my_id = json.loads(response.text)['id']

response = requests.get("https://{instance}/api/v1/accounts/{id}/statuses".format(
   instance=my_instance, id=my_id))
statuses = json.loads(response.text)
last = statuses[-1]['id']
toots = ""
for s in statuses:
  soup = BeautifulSoup(s['content'], 'html.parser')
  cur = soup.get_text()
  toots += cur

while True:
  try:
    response = requests.get("https://{instance}/api/v1/accounts/{id}/statuses?max_id={max_id}".format(
        instance=my_instance, id=my_id, max_id=last))
    statuses = json.loads(response.text)
    last = statuses[-1]['id']
    for s in statuses:
      soup = BeautifulSoup(s['content'], 'html.parser')
      cur = soup.get_text()
      toots += cur
  except:
    break

#print(toots)

from wordcloud import WordCloud, STOPWORDS
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import jieba
import jieba.analyse
from collections import Counter

dictfile = "dict.txt"
stopfile = "stopwords.txt"
fontpath = "msjh.ttc"

jieba.set_dictionary(dictfile)
jieba.analyse.set_stop_words(stopfile)

text = toots

tags = jieba.analyse.extract_tags(text, topK=25)

seg_list = jieba.lcut(text, cut_all=False)
dictionary = Counter(seg_list)

freq = {}
for ele in dictionary:
    if ele in tags:
        freq[ele] = dictionary[ele]


wordcloud = WordCloud(font_path=fontpath).generate_from_frequencies(freq)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()