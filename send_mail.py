#!/usr/bin/python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from config import mail_info

def sendmail(something):
    # 第三方 SMTP 服务
    mail_host=mail_info[0]  #设置服务器
    mail_user=mail_info[1]   #用户名
    mail_pass=mail_info[2]   #口令
    sender = 'norxxxxxxxxx.com'
    receivers = mail_info[3]  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    #  创建一个带附件的实例
    message = MIMEMultipart()
    message['From'] = Header("norxxxxxxxxx.com", 'utf-8')
    message['To'] = Header('huangyisan', 'utf-8')
    subject = '服务down告警'
    message['Subject'] = Header(subject, 'utf-8')
    # 邮件正文内容
    message.attach(MIMEText('Hi all:\n\t\t 下列服务可能down，请注意 \n' + something +'\n\t\t' + '谢谢！', 'plain', 'utf-8'))
    try:
        smtpObj = smtplib.SMTP_SSL(mail_host, 994)
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, message.as_string())
        print('邮件发送成功')
    except smtplib.SMTPException:
        print('Error: 无法发送邮件')
