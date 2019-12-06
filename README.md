# Cluster RabbitMQ :rabbit:

Based on: https://github.com/pardahlman/docker-rabbitmq-cluster

## Install

```shell
> git clone https://github.com/mentels/docker-rabbitmq-cluster.git
> cd docker-rabbitmq-cluster
> docker-compose up
```

Most things will be how you expect:

* The default username and password are `guest`/`guest`
* The broker accepts connections on `localhost:5672`
* The Management interface is found at `localhost:15672`

Additionally each container exposes the broker AMQP and MGMT interface port at:
- 5672+(container no)
- 15672+(container no)
respectively. E.g. `rabbitmq1` can be reached at 5673 (5672+1) for AMQP and 15673 (15672+1) for the Management interface.

## Customize

### The `.env` file

The `.env` file contains the `RABBITMQ_ERLANG_COOKIE` environment variable that can be used to change the erlang cookie.

### The `rabbitmq.conf`

The configuration of the broker is exposed via this file.

### The `enabled_plugins`

The plugins configuration of the broker is exposed via this file.

## Use

### Get admin

 ```shell
curl http://localhost:15672/cli/rabbitmqadmin -o rabbitmqadmin
chmod u+x rabbitmqadmin
``` 
