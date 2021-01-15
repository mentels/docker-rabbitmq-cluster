import sys
import pika
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--vhost", help="Virtual host", default="/")
parser.add_argument("--queue", help="Queue name", required=True)
parser.add_argument("--message", help="Message contents", required=True)
args = parser.parse_args()

conn_params = pika.ConnectionParameters('localhost', 5672, args.vhost)
connection = pika.BlockingConnection(conn_params)
channel = connection.channel()

channel.queue_declare(queue=args.queue)

channel.basic_publish(exchange='', routing_key=args.queue, body=args.message)
print(" [x] Sent '%s'" % args.message)
connection.close()
