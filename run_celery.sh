#!/bin/sh

# wait for RabbitMQ server to start
sleep 10

su -c "celery  -A config worker -l info"