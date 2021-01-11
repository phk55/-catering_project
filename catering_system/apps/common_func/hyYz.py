"""
改写互亿无线官方发短信代码类实现
输出结果:
<?xml version="1.0" encoding="utf-8"?>
<SubmitResult xmlns="http://106.ihuyi.com/">
<code>2</code>
<msg>提交成功</msg>
<smsid>15758634658378124643</smsid>
</SubmitResult>
"""

import requests


class SMS(object):
    """
    短信类,提供功能:发短信
    """

    def __init__(self, account, password):
        self.url = "http://106.ihuyi.com/webservice/sms.php?method=Submit"  # 接口地址
        self.account = account  # APIID
        self.password = password  # APIkey

    def send_sms(self, mobiles, content):
        """
        发短信
        :param mobiles: 手机号列表
        :param content: 短信内容
        :return:None
        """
        for mobile in mobiles:
            # 定义请求的头部
            headers = {
                "Content-type": "application/x-www-form-urlencoded",
                "Accept": "text/plain"
            }
            # 定义请求的数据
            data = {
                "account": self.account,
                "password": self.password,
                "mobile": mobile,
                "content": content,
            }
            # 发起数据
            response = requests.post(self.url, headers=headers, data=data)
            print(response.content.decode())


if __name__ == '__main__':
    sms = SMS('C10530451', '7e1ce8c774836315b443ebfb32052d8f')
    sms.send_sms(['13347651901'], '您的验证码是：888888。请不要把验证码泄露给其他人。')