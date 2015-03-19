# -*- coding: utf-8 -*-

import pika, sys
import time

url = 'http://media.daum.net/economic/'
mqhost = '192.168.0.6'
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

