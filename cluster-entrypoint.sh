#!/bin/bash

set -e

# Start RMQ from entry point.
# This will ensure that environment variables passed
# will be honored
/usr/local/bin/docker-entrypoint.sh rabbitmq-server -detached

# Make sure the server is up
rabbitmqctl wait /var/lib/rabbitmq/mnesia/rabbit@$(hostname).pid
# https://www.rabbitmq.com/rabbitmqctl.8.html#wait

# Give some time to rabbit@rabbitmq1
sleep 2

# Do the cluster dance
rabbitmqctl stop_app
rabbitmqctl join_cluster rabbit@rabbitmq1

# Stop the entire RMQ server. This is done so that we
# can attach to it again, but without the -detached flag
# making it run in the forground
#
# Wait a while for the app to really stop
rabbitmqctl stop /var/lib/rabbitmq/mnesia/rabbit@$(hostname).pid
# https://www.rabbitmq.com/rabbitmqctl.8.html#stop

# Start it
rabbitmq-server