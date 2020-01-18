from channels.generic.websocket import JsonWebsocketConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
from django.core import exceptions
from django.db import models

import datetime
import uuid
import logging
import time

from bgapp.bgModels import *
from .consumer_utils import *
from .error_msgs import *
from .tasks import *

logger = logging.getLogger('batground')
class TestConsumer(JsonWebsocketConsumer):
    user_id_channel_map = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.i = 0

    def connect(self):
        self.accept()

    def receive_json(self, data, **kwargs):
        logger.debug('received: {}'.format(data))
        self.handlers[data['cmd']](self, data)

    def inform_client_of_error(self, **kwargs):
        if 'log_msg' in kwargs:
            logging.warning(kwargs['log_msg'])

        json_content = {
            'cmd': kwargs['type'],
        }
        if 'data' in kwargs:
            json_content['data'] = kwargs['data']
        self.send_json(content=json_content)

    def exec(self, q):
        if q[0].__name__ == 'inform_client_of_error':
            q[0](type=q[1])

        elif q[0].__name__ == 'send_json':
            q[0](q[1])

    def start_chat(self, data):
        logger.info(data)
        lib = [
            [self.inform_client_of_error, ['start_chat_err.no_opponents',
                                           'start_chat_err.could_not_start']],
            [self.send_json, ['start_chat_success']]
        ]

    def end_chat(self, data):
        logger.info(data)

    def get_topics_by_kw(self, data):
        pass

    def get_topics_suggest(self, data):
        class topic:
            def __init__(self, content, num):
                self.content = content
                self.num_convo = num

        topics = [
            topic('gay', 10),
            topic('gun control', 43),
            topic('long duong', 126),
            topic('iran bomb', 234)
        ]
        topics.sort(key=lambda x: x.num_convo)
        self.send_json(content={
            'cmd': 'topics_suggest',
            'id': data['id'],
            'topics': [[tp.content, tp.num_convo] for tp in topics]
        })

    def user_id(self, data):
        print(data)

    handlers = {
        'start_chat': start_chat,
        'end_chat': end_chat,
        'get_topics_by_kw': get_topics_by_kw,
        'get_topics_suggest': get_topics_suggest,
        'user_id': user_id
    }