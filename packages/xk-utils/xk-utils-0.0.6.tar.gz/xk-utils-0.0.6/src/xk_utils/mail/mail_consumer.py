import json
import os
import time
import redis

from xk_utils.logger import get_logger
from xk_utils.mail.config import *

from xk_utils.mail.send import do_send_mail

logger = get_logger("mail_log", write_file=False, send_mail=False)


def mail_consumer(mail_prefix, redis_config, mysql_config, mail_config):
    """
    :param mail_prefix: redis mail key 前缀
    :param redis_config:
    :param mysql_config:
    :return:
    """
    redis_conn = redis.Redis(**redis_config)
    keys = redis_conn.keys(mail_prefix + '*')
    for key in keys:
        if isinstance(key, bytes):
            key = key.decode('utf8')
        contents = []
        while True:
            # 从redis获取数据， 500 或者为空时结束
            value = redis_conn.rpop(key)
            if value:
                data = json.loads(value.decode('utf8'))
                content = data.get('content') or json.dumps(data)
                contents.append(content)
            else:
                break

            if len(contents) >= 500:
                break

        do_send_mail(key.replace(mail_prefix, ''), '\n'.join(contents), mysql_config, mail_config)


def main():
    redis_config = {
        'host': os.environ['REDIS_HOST'],
        'port': os.environ['REDIS_PORT'],
        'password': os.environ['REDIS_PASSWORD'],
        'db': os.environ['REDIS_MAIL_DB'],
    }

    mysql_config = {
        'host': os.environ['MYSQL_HOST'],
        'port': os.environ['MYSQL_PORT'],
        'user': os.environ['MYSQL_USER'],
        'password': os.environ['MYSQL_PASSWORD'],
        'database': os.environ['MYSQL_MAIL_DB'],
    }
    mail_config = {
        'mail_host': os.environ['MAIL_HOST'],
        'mail_port': os.environ['MAIL_PORT'],
        'mail_user': os.environ['MAIL_USER'],
        'from_addr': os.environ['MAIL_USER'],
        'mail_password': os.environ['MAIL_PASSWORD']
    }
    from apscheduler.schedulers.background import BlockingScheduler
    scheduler = BlockingScheduler()
    scheduler.add_job(mail_consumer, trigger='interval', args=(MAIL_PREFIX, redis_config, mysql_config, mail_config), seconds=5 * 60)
    scheduler.add_job(mail_consumer, trigger='interval', args=(MAIL_PREFIX_NOW, redis_config, mysql_config, mail_config), seconds=5)
    scheduler.start()


if __name__ == '__main__':
    main()
