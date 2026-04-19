FROM rabbitmq:3.13-management-alpine

COPY definitions.json /etc/rabbitmq/

RUN echo "management.load_definitions = /etc/rabbitmq/definitions.json" > /etc/rabbitmq/rabbitmq.conf

EXPOSE 5672 15672