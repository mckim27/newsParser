# -*- coding: utf-8 -*-

import sys
from function import *

# 파싱할 url
parseUrlLinks = ['http://media.daum.net/economic/']


i = 0;
urlCounts = len(parseUrlLinks)

while i < urlCounts:
  print i

  addUrlLinks = extractUrlLink(parseUrlLinks[i])
  if addUrlLinks == '' :  
    i = i + 1
    continue
  
  # text를 파싱할 주소를 rabbitmq에 전달.
  sendUrlToMq(parseUrlLinks[i])
  
  # url문서 내부에 외부 링크 url이 있을 경우 루프를 돌고 있는 해당 url list에 추가함.
  parseUrlLinks = list(set(parseUrlLinks + addUrlLinks))

  urlCounts = len(parseUrlLinks)
  print urlCounts

  i = i + 1
  #if i == 5 : break


# 링크가 정상적으로 추출됬는지 확인을 위해... 추후 삭제 해야...
f = open('links', 'w')
for url in parseUrlLinks :
  f.write(url + '\n')
f.close
