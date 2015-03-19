# -*- coding: utf-8 -*-

import pika
import time
from function import *

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='192.168.0.6'))
channel = connection.channel()

channel.queue_declare(queue='parse_queue', durable=True)
print ' [*] Waiting for messages. To exit press CTRL+C'

def callback(ch, method, properties, url):
    print " [x] Received %r" % (url,)
    dNewsParser(url)
    time.sleep( url.count('.') )
    print " [x] Done"
    ch.basic_ack(delivery_tag = method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='parse_queue')

channel.start_consuming()



