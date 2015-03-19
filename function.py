# -*- coding: utf-8 -*-
import urllib, BeautifulSoup, re, blockspring, random, string, os, urlparse, sys, pika, types
from konlpy.tag import Hannanum


## 
# @ description - 디렉토리 안에 모든 파일의 파일이름을 구해서 리스트로 리턴.
# @ param  path - 디렉토리 이름.
# @ return - 파일 이름들이 있는 리스트
##
def getFileNames(path):
  data = {}
  for dir_entry in os.listdir(path):
    dir_entry_path = os.path.join(path, dir_entry)
    if os.path.isfile(dir_entry_path):
      with open(dir_entry_path, 'r') as my_file:
        data[dir_entry] = my_file.read()

  return data
## 
# @ deprecated
# @ description - 해당 url 문서 안에 모든 text를 문자열로 만듬. 개행으로 개채 구문함.
#               현재 사용하지 않음.  
# @ param  url - 파싱할 문서의 주소.
# @ return - 파일 이름들이 있는 리스트
##
def textParser(url):
    texts = blockspring.runParsed("get-text-from-url", { "url": url }).params["text"]
    print texts
    saveParseFile(texts)


## 
# @ description - 다음 뉴스기사의 타이틀과 내용을 파싱.
# @ param  url - 파싱할 문서의 주소..
# @ return - 파일 이름들이 있는 리스트
##
def dNewsParser(url):
  html = urllib.urlopen(url)
  soup = BeautifulSoup.BeautifulSoup(html)

  titles = ''
  try :
    for title in soup.find(id = 'newsTitleShadow' ).findAll(text=True, recursive=False):
      if title == None : return ''
      if re.search(r"(\w+[\w\.]*)@(\w+[\w\.]*)\.([A-Za-z]+)", title) : continue
      titles = titles + title
  except :
    return ''

  bodys = ''
  for body in soup.find(id = 'newsBodyShadow' ).findAll(text=True, recursive=False):
    if re.search(r"(\w+[\w\.]*)@(\w+[\w\.]*)\.([A-Za-z]+)", body) : continue
    bodys = bodys + body
  

  #contents = 'title : ' + title  + '\n' + 'bodys : ' + bodys
  saveParseFile(bodys)
  #saveParseFile(extractWords(bodys))

## 
# @ description - 텍스트의 행태소 분석을 수행 후 결과값을 스트링으로 리턴.
# @ param  texts - 분석할 문자열.
# @ return - 분석된 단어들.
##
def extractWords(texts):
  hannanum = Hannanum()
  words = ''
  #for word in hannanum.nouns(unicode(texts, 'UTF-8')):
  for word in hannanum.nouns(texts):
    words = words + '\t' + word
  
  print words
  return words     

## 
# description - param으로 넘어온 문자열을 파일로 저장함. 파일이름은 랜덤 문자열
# param  content - 저장할 문자열.
##
def saveParseFile(content):
  # data 폴더 없으면 생성
  if not os.path.exists('./data'):
    os.makedirs('./data')

  fname = randomStringGenerator();
  if os.path.isfile('data/' + fname):
    print "duplicate !!"
    saveParseFile(content)
  else:
    f = open('data/' + fname, 'w')
    f.write(content.encode("UTF-8"))
    f.close()
    
## 
# @ description - 랜덤 문자 생성
# @ return - 생성된 랜덤 문자
##
def randomStringGenerator():
    asciiUpper = string.ascii_uppercase
    asciiLower = string.ascii_lowercase
    digits = string.digits
    return ''.join(random.choice(asciiUpper + asciiLower + digits) for x in range(48))


## 
# @ description - 해당 url 페이지 안에 모든 링크를 구함.
# @ param  url - 링크를 검색할 url 문서의 주소.
# @ return - 발견된 링크 주소들을 리스트 형태로 리턴.
##
def extractUrlLink(url):
  try:
    html = urllib.urlopen(url)
  except:
    print 'not found'
    return ''

  soup = BeautifulSoup.BeautifulSoup(html)
  urlLinks = []
  for tag in soup.findAll('a', href=True):
    tag['href'] = urlparse.urljoin(url, tag['href'])
    #if (re.search('\/v\/', tag['href']) != None ) or (re.search('economic', tag['href']) != None):
    if re.search('\/v\/', tag['href']) != None :
      #print 'find !!'
      filterPos = tag['href'].find('#')
      if filterPos != -1 :
        tag['href'] = tag['href'][:filterPos]

      urlLinks.append(tag['href'])

    #if re.match('economic', tag['href']):
    #  urlLinks.append(tag['href'])

  #return urlLinks
  return list(set(urlLinks))


## 
# @ deprecated
# @ description - url 추출 중에 필터링 기능을 할 함수. 현재 사용하지 않음.... 미완성.
# @ param  element - url 주소.
# @ return boolean - 해당 url 주소를 필터링 할지 말지에 대한 boolean 값.
##
def findFilter(element):
  if re.match('sport', str(element)):
    return False
  if re.match('photo', str(element)):
    return False
  return True

## 
# @ description - 기사의 내용을 파싱할 url 주소값을 rabbitmq 에 넘김.
# @ param  url - 파싱할 url의 주소값.
##
def sendUrlToMq(url):
  connection = pika.BlockingConnection(pika.ConnectionParameters(mqhost='your mqhost'))
  channel = connection.channel()

  channel.queue_declare(queue='parse_queue', durable=True)

  channel.basic_publish(exchange='',
                      routing_key='parse_queue',
                      body=url,
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))
  print " [x] Sent %r" % (url,)
  connection.close()
