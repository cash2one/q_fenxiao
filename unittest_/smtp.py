#encoding:utf-8
__author__ = 'wangjinkuan'

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import smtplib
import os


msg = MIMEMultipart()
att1 = MIMEText(open('pay.xls', 'r').read(), 'base64', 'utf-8')
att1["Content-Type"] = 'application/octet-stream'
att1["Content-Disposition"] = 'attachment; filename="pay.xls"'
msg.attach(att1)

msg['From'] = '全球抢购每日售出商品<admin.qqqg.com>'
msg['To'] = "周战国<wangjinkuan@qqqg.com>"
msg['Subject'] = Header('python发送邮件', 'utf-8')


# 输入Email地址和口令:
# from_addr = raw_input('From: ')
# password = raw_input('Password: '
# 输入SMTP服务器地址:
# smtp_server = raw_input('SMTP server: ')
# 输入收件人地址:

server = smtplib.SMTP()
server.connect("smtp.yeah.net", "25")
server.login('wangjinkuan333@yeah.net', 'sunwang195145!@#')
server.set_debuglevel(1)
# server.login(from_addr, password)
server.sendmail("wangjinkuan333@yeah.net", ['wangjinkuan@qqqg.com'], msg.as_string())
server.quit()

if __name__ == "__main__":
    pass