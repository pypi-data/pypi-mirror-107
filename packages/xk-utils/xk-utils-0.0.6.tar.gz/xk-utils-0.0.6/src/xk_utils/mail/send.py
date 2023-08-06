from email.mime.text import MIMEText
from smtplib import SMTP_SSL

from xk_utils.logger import get_logger


def do_send_mail(key, contents, mysql_config=None, mail_config=None, _subtype='plain',):
    logger = get_logger("mail_log", write_file=False, send_mail=False)

    """
    :param title: 邮件标题
    :param contents: 邮件内容
    :param from_addr: 来源地址， 如果不提供， 用config mail_user 参数
    :param to_addrs: 发送地址，list, 如果不提供， 用name参数
    :param _subtype: 数据类型 plain, html
    :param name: 对应邮件地址，在数据库中查询
    :return:
    """
    mail_host = mail_config['mail_host']
    mail_port = mail_config['mail_port']
    mail_user = mail_config['mail_user']
    from_addr = mail_config['from_addr']
    mail_password = mail_config['mail_password']
    import pymysql
    sql = f'select mail_addr, title from mail_send1 where name=%s'
    conn = pymysql.Connection(**mysql_config)
    with conn.cursor() as cursor:
        cursor.execute(sql, args=(key,))
        result = cursor.fetchone()
        if not result:
            logger.error(f'mail_send不存在{key}, 请管理员添加邮件配置')
            return
        to_addrs = result[0]
        title = result[1]

    conn.close()
    message = MIMEText(contents, _subtype, 'utf-8')
    message['Subject'] = title
    message['From'] = from_addr
    message['To'] = to_addrs

    smtp = SMTP_SSL(
        host=mail_host,
        port=mail_port,
    )
    smtp.login(
        user=mail_user,
        password=mail_password,
    )
    smtp.sendmail(from_addr, to_addrs, message.as_string())
    logger.info('发送邮件成功')