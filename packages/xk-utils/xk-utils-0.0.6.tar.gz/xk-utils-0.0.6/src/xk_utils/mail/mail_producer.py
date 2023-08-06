import json
import logging
from redis import Redis

from .config import *


class MailProducer(object):
    def __init__(self, key, send_now=False, **kwargs, ):
        """
        :param key: redis 推送
        :param send_now: 是否立即发送
        :param kwargs:
        """
        if send_now:
            self.key = f'{MAIL_PREFIX_NOW}{key}'
        else:
            self.key = f'{MAIL_PREFIX}{key}'

        self.redis = Redis(**kwargs)
        self.kwargs = kwargs

    def send(self, content: str, code=None):
        """
        :param content:
        :param code:
        :return:
        """
        v = {
            'code': code,
            'content': content
        }
        value = json.dumps(v, ensure_ascii=False)
        self.redis.lpush(self.key, value)


class MailHandler(logging.Handler):
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            cls._instance = super(MailHandler, cls).__new__(cls)
        return cls._instance

    def __init__(self, key, **kwargs):
        logging.Handler.__init__(self)
        self.mail_producer = MailProducer(key, **kwargs)

    def emit(self, record):
        msg = self.format(record)
        self.mail_producer.send(msg)

