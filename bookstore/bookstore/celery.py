from __future__ import absolute_import, unicode_literals

import os

import kombu
from celery import Celery, bootsteps

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookstore.settings')

app = Celery('bookstore')


app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


# setting publisher
with app.pool.acquire(block=True) as conn:
    exchange = kombu.Exchange(
        name='myexchange',
        type='direct',
        durable=True,
        channel=conn,
    )
    exchange.declare()

    queue = kombu.Queue(
        name='myqueue',
        exchange=exchange,
        routing_key='mykey',
        channel=conn,
        message_ttl=600,
        queue_arguments={
            'x-queue-type': 'classic'
        },
        durable=True
    )
    queue.declare()


# setting consumer
class MyConsumerStep(bootsteps.ConsumerStep):

    def get_consumers(self, channel):
        return [kombu.Consumer(channel,
                               queues=[queue],
                               callbacks=[self.handle_message],
                               accept=['json'])]

    def handle_message(self, body, message):
        print('Received message: {0!r}'.format(body))
        message.ack()


app.steps['consumer'].add(MyConsumerStep)