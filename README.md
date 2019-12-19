# Cluster RabbitMQ :rabbit:

Based on: https://github.com/pardahlman/docker-rabbitmq-cluster

- [Cluster RabbitMQ :rabbit:](#cluster-rabbitmq-rabbit)
  - [Install](#install)
  - [Customize](#customize)
    - [The .env file](#the-env-file)
    - [The config/rabbitmq.conf](#the-configrabbitmqconf)
    - [The config/advanced.config](#the-configadvancedconfig)
    - [The config/enabled_plugins](#the-configenabledplugins)
  - [Use](#use)
    - [With rabbitmqadmin tool](#with-rabbitmqadmin-tool)
    - [With Python snippets](#with-python-snippets)
  - [Clean-up](#clean-up)

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
respectively. 

E.g. `rabbitmq1` can be reached at 5673 (5672+1) for AMQP and 15673 (15672+1) for the Management interface.

## Customize

### The `.env` file

The `.env` file contains:

1. `RABBITMQ_ERLANG_COOKIE` environment variable that can be used to change the [Erlang cookie](https://www.rabbitmq.com/clustering.html#erlang-cookie).
2. `RABBITMQ_DOCKER_TAG` environment variable that can be used to change the [RabbitMQ Docker image tag](https://hub.docker.com/_/rabbitmq?tab=tags). By default it is set to `3.8-management`.

### The `config/rabbitmq.conf`

[Configuration of the broker](https://www.rabbitmq.com/configure.html#config-file) 
is exposed via this file.

### The `config/advanced.config`

[Advanced configuration of the broker](https://www.rabbitmq.com/configure.html#advanced-config-file)
is exposed by this file (empty by default).

### The `config/enabled_plugins`

[Enabled plugins](https://www.rabbitmq.com/plugins.html#ways-to-enable-plugins)
can be changed via this file.

## Use

### With `rabbitmqadmin` tool

Make sure the RabbitMQ cluster is running. Then get the `rabbitmqadmin` tool:

 ```shell
curl http://localhost:15672/cli/rabbitmqadmin -o rabbitmqadmin
chmod u+x rabbitmqadmin
``` 

Then declare a queue, publish some message and get that message from a queue:
```shell
./rabbitmqadmin declare queue name=my_queue
./rabbitmqadmin publish routing_key=my_queue payload=szkolarabbita
./rabbitmqadmin get queue=my_queue ackmode=ack_requeue_false
```

Now using the Management Plugin one can see stats for the `my_queue` to see that the message really went through it: http://localhost:15672/#/queues/%2F/my_queue

> **NOTE**: When using the `rabbitmqadmin` all the interactions with broker go through the [HTTP API](http://localhost:15672/api/index.html) exposed by the [Management Plugin](https://www.rabbitmq.com/management.html).

### With Python snippets

Make sure the RabbitMQ cluster is running. Then install python dependencies:

> **NOTE:** For this to work you need to have [pipenv](https://github.com/pypa/pipenv) installed.

```shell
cd python/ && pipenv install
```

Then once you are in the `python/` directory start a consumer and attach it to a 
`another_queue`:

```shell
pipenv run python consume.py --queue another_queue
# => [*] Waiting for messages. To exit press CTRL+C
```

Then publish a message to our queue:
```shell
pipenv run python send.py --queue another_queue --message hello
# => [x] Sent 'hello'
```

Finally, you can check the `another_queue` stats at http://localhost:15672/#/queues/%2F/another_queue.

## Clean-up

To stop and remove the containers run:

```shell
docker-compose down
```