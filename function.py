# -*- coding: utf-8 -*-
import urllib, BeautifulSoup, re, blockspring, random, string, os, urlparse, sys, pika, types
from konlpy.tag import Hannanum


def getFileNames(path):
  data = {}
  for dir_entry in os.listdir(path):
    dir_entry_path = os.path.join(path, dir_entry)
    if os.path.isfile(dir_entry_path):
      with open(dir_entry_path, 'r') as my_file:
        data[dir_entry] = my_file.read()

  return data

# 해당 url 문서 안에 모든 text를 문자열로 만듬. 개행으로 개채 구문함.
def textParser(url):
  try:
    texts = blockspring.runParsed("get-text-from-url", { "url": url }).params["text"]
    print texts
    saveParseFile(texts)
  except:
    return ''

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


def extractWords(texts):
  hannanum = Hannanum()
  words = ''
  #for word in hannanum.nouns(unicode(texts, 'UTF-8')):
  for word in hannanum.nouns(texts):
    words = words + '\t' + word
  
  print words
  return words     


# 파라미터로 넘어온 문자들을 텍스트 파일로 저장. 파일이름은 랜덤 문자열 사용.
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

# 랜덤 문자 생성기
def randomStringGenerator():
    asciiUpper = string.ascii_uppercase
    asciiLower = string.ascii_lowercase
    digits = string.digits
    return ''.join(random.choice(asciiUpper + asciiLower + digits) for x in range(48))

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

def findFilter(element):
  if re.match('sport', str(element)):
    return False
  if re.match('photo', str(element)):
    return False
  return True

mqhost = '192.168.0.6'
def sendUrlToMq(url):
  connection = pika.BlockingConnection(pika.ConnectionParameters(mqhost))
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

  
