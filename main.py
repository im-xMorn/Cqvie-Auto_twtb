import random
import requests
import datetime
import re
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
# 邮箱发送
def mail(answer, my_user):
    my_sender = '*************'  # 发件人邮箱账号
    my_pass = '*************'  # 发件人邮箱授权码，第一步得到的
    ret = True
    try:
        if answer[2:-2] == "'体温填报成功!'":
            mail_msg = """
                        <p>体温填报成功!</p>
                        <p>填报时间为:{now.hour}:{now.minute}\t填报体温为:36.{timeper}</p>
                        <p>今天填报次数已完成，勿需再次填报!</p>
                       """
        else:
            mail_msg = f"""
                            <p>{answer[3:-3]}</p>
                       """
        msg = MIMEText(mail_msg, 'html', 'utf-8')
        msg['From'] = formataddr(["********", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
        msg['To'] = formataddr(["*********", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
        msg['Subject'] = "自动体温填报"  # 邮件的主题，也可以说是标题
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是465，固定的，不能更改 使用SSL模式
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱授权码
        server.set_debuglevel(1)
        server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件信息
        server.quit()  # 关闭连接
    except Exception as err:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        ret = False
    return ret
# 程序开始
if __name__ == '__main__':
    # 用户接收邮箱地址
    email = ['*************']
    # 学号
    user = ['**********']
    # 密码 身份证后六位
    psd = ['**********']
    url_1 = 'http://xgn.cqvie.edu.cn:8200/SPCP/Web'
    url_2 = 'http://xgn.cqvie.edu.cn:8200/SPCP/Web/Temperature/StuTemperatureInfo'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36 Edg/99.0.1150.39'
    }
# 获取用户 cookie 值
    cookies_id = []
    for i in range(0, len(email)):
        data_1 = { # 用户登陆数据
            'StuLoginMode': '1',
            'txtUid': user[i],
            'txtPwd': psd[i],
        }
        # 创建 session 对象
        session = requests.Session()
        session.post(url=url_1, data=data_1)
        cookies_id.append(str(session.cookies.get_dict()['CenterSoftWeb']))
    chose = 0
# 填报
    for i in cookies_id:
        timeper = random.randint(1,9)
        now = datetime.datetime.now()
        cookie = {
            'CenterSoftWeb':str(i)
        }
        data_2 = { # 体温信息
            'TimeNowHour':str(now.hour),
            'TimeNowMinute':str(now.minute),
            'Temper1':'36',
            'Temper2':str(timeper)
        }
        response = requests.post(url=url_2,headers=headers,data=data_2,cookies=cookie)
        # 获取填报状态
        answer = re.findall('content: (.*?),',response.text,re.M)
        print(response.text)
        print(answer)
        answer = str(answer)
        # 调用并发送邮箱通知
        ret = mail(answer,email[chose])
        chose+=1
