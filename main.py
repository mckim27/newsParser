# -*- coding: utf-8 -*-

import sys
from function import *

parseUrlLinks = ['http://media.daum.net/economic/']


i = 0;
urlCounts = len(parseUrlLinks)

while i < urlCounts:
  print i

  addUrlLinks = extractUrlLink(parseUrlLinks[i])
  if addUrlLinks == '' :  
    i = i + 1
    continue

  sendUrlToMq(parseUrlLinks[i])

  parseUrlLinks = list(set(parseUrlLinks + addUrlLinks))

  urlCounts = len(parseUrlLinks)
  print urlCounts

  i = i + 1
  #if i == 5 : break


f = open('links', 'w')
for url in parseUrlLinks :
  f.write(url + '\n')
f.close
