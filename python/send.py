import sys
import pika
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--queue", help="Queue name", required=True)
parser.add_argument("--message", help="Message contents", required=True)
args = parser.parse_args()

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue=args.queue)

channel.basic_publish(exchange='', routing_key=args.queue, body=args.message)
print(" [x] Sent '%s'" % args.message)
connection.close()
