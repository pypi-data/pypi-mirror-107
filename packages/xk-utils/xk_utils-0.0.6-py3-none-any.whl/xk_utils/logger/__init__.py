import logging
import os
from logging import StreamHandler, Formatter

from .handler import TimeFileHandler
from xk_utils.mail.mail_producer import MailHandler

logging_format = "[%(asctime)s]-[%(levelname)s] <-%(filename)s-%(funcName)s-line %(lineno)s>: %(message)s"
level = logging.DEBUG


def get_stream_handler(level, logging_format):
    # 屏幕显示
    stream_handler = StreamHandler()
    stream_handler.setLevel(level)
    stream_handler.setFormatter(
        Formatter(logging_format),
    )
    return stream_handler


def get_file_handler(filename, level, logging_format):
    file_handler = TimeFileHandler(filename)
    file_handler.setLevel(level)
    file_handler.setFormatter(
        Formatter(logging_format),
    )
    return file_handler


def get_mail_handler(**kwargs):
    m = MailHandler(**kwargs)
    m.setLevel(logging.ERROR)
    m.setFormatter(
        Formatter(logging_format),
    )
    return m


def has_handler(handle: logging.Handler, handles):
    for i in handles:
        if handle.__class__ == i.__class__:
            return True

    return False


def get_logger(key=None, name='root', write_file=False, file_path=None, send_mail=False, host=None, port=None,
               db=None, password=None):
    """获取logger
    :param key: 发送邮件时区分标记， example: write_draft_log
    :param name: logger name
    :param write_file: 是否记录文件
    :param file_path: 记文件时，文件路径
    :param send_mail: 是否发送邮件
    :param host: 如果send_mail为True， 需要设置缓存邮件的redis
    :param port: redis host
    :param db: redis
    :param password:
    :return:
    """
    if write_file:
        if file_path is None:
            raise Exception('write_file 为True时，需要指定文件路径')

    if send_mail:
        if host is None or port is None or db is None or key is None:
            raise Exception('send_mail 为True 时，需要指定redis的来接受邮件缓存数据, 指定key对应服务端收件人'
                            'key: 服务端根据key来查询收件人'
                            'host: redis host'
                            'port: redis port'
                            'db: redis db'
                            'password: redis password')

    _logger = logging.getLogger(name)
    _logger.setLevel(level)

    # 屏幕显示
    stream_handler = get_stream_handler(level, logging_format)
    if not has_handler(stream_handler, _logger.handlers):
        _logger.addHandler(stream_handler)

    # 屏幕显示
    if write_file:
        file_path = os.path.abspath(file_path)
        if not os.path.exists(file_path):
            os.makedirs(file_path)

        filename = os.path.join(file_path, name)
        file_handler = get_file_handler(filename, level, logging_format)
        if not has_handler(file_handler, _logger.handlers):
            _logger.addHandler(file_handler)

    # 邮件
    if send_mail:
        m_handler = get_mail_handler(key=key, host=host, port=port, db=db, password=password)
        if not has_handler(m_handler, _logger.handlers):
            _logger.addHandler(m_handler)

    return _logger


