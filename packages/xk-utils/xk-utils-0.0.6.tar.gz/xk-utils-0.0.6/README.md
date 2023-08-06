# xk-utils

xk-utils存放星矿公用模块，包括邮件模块, 日志模块等

### 打包

```shell script
python3 -m pip install --upgrade build
python3 -m build
```

### 发布

```shell script
pip install --upgrade twine
python3 -m twine upload --repository pypi dist/*
```

### 安装

```shell script
pip install xk-utils
```

### 使用

1、发送邮件

```python
from xk_utils.mail import MailProducer

redis_config = {
    'host':'127.0.0.1',
    'port': 6379,
    'password': '****',
    'db': 99
}

# 定义邮件key， 在服务端需要配置相关收件人， 邮件标题
m = MailProducer(key='log', **redis_config)
m.send(f'<邮件内容>')
```

2、记录日志

```python
# 记录文件日志
import os
from xk_utils.logger import get_logger

logger = get_logger('log', 'werkzeug', write_file=True, file_path=os.path.join(os.path.dirname(__file__), 'log'))
logger.info("记录文件")


# 记录可以发送邮件的日志
logger = get_logger('log', 'celery', send_mail=True,
                    host='127.0.0.1',
                    port=6379,
                    password='****',
                    db=99
)
logger.info('这是一条正常日志， 不发送邮件')
logger.error('这是一条错误日志， 发送邮件， 邮件联系人、标题，请在服务器端配置， key=<log>')
```


