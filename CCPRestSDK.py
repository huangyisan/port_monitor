    #-*- coding: UTF-8 -*-
    #  Copyright (c) 2014 The CCP project authors. All Rights Reserved.
    #
    #  Use of this source code is governed by a Beijing Speedtong Information Technology Co.,Ltd license
    #  that can be found in the LICENSE file in the root of the web site.
    #
    #   http://www.yuntongxun.com
    #
    #  An additional intellectual property rights grant can be found
    #  in the file PATENTS.  All contributing project authors may
    #  be found in the AUTHORS file in the root of the source tree.

import hashlib
import base64
import datetime
import requests

class REST(object):
    
    AccountSid = ''
    AccountToken = ''
    AppId = ''
    SubAccountSid = ''
    SubAccountToken = ''
    ServerIP = ''
    ServerPort = ''
    SoftVersion = ''
    Iflog = True #是否打印日志
    Batch = ''  #时间戳
    BodyType = 'xml'#包体格式，可填值：json 、xml

    def __init__(self, ServerIP, ServerPort, SoftVersion):
        '''

        :param ServerIP: 必选参数    服务器地址
        :param ServerPort: 必选参数    服务器端口
        :param SoftVersion: 必选参数    REST版本号
        '''
        self.ServerIP = ServerIP
        self.ServerPort = ServerPort
        self.SoftVersion = SoftVersion

    def setAccount(self,AccountSid,AccountToken):
        '''
        
        :param AccountSid: 必选参数    主帐号
        :param AccountToken: 必选参数    主帐号Token
        :return: 
        '''
        self.AccountSid = AccountSid
        self.AccountToken = AccountToken

    def setAppId(self, AppId):
        '''

        :param AppId:  application iD
        :return:
        '''
        self.AppId = AppId
    
    def log(self, url, body, data):
        print('这是请求的URL：')
        print(url)
        print('这是请求包体:')
        print(body)
        print('这是响应包体:')
        print(data)
        print('********************************')
    
    # 主帐号鉴权
    def accAuth(self):
        if(self.ServerIP==""):
            print('172004')
            print('IP为空')
        
        if(int(self.ServerPort)<=0):
            print('172005')
            print('端口错误（小于等于0）')
        
        if(self.SoftVersion==""):
            print('172013')
            print('版本号为空')
        
        if(self.AccountSid==""):
            print('172006')
            print('主帐号为空')
        
        if(self.AccountToken==""):
            print('172007')
            print('主帐号令牌为空')
        
        if(self.AppId==""):
            print('172012')
            print('应用ID为空')


    #设置包头
    def setHttpHeader(self, headers):
        if self.BodyType == 'json':
            headers["Accept"] = "application/json"
            headers["Content-Type"] = "application/json;charset=utf-8"
            
        else:
            headers["Accept"] = "application/xml"
            headers["Content-Type"] = "application/xml;charset=utf-8"

    def sendTemplateSMS(self, to, datas, tempId):
        '''

        :param to: 必选参数 短信接收彿手机号码集合,用英文逗号分开
        :param datas: 可选参数 内容数据
        :param tempId: 必选参数 模板Id
        :return:
        '''

        self.accAuth()
        nowdate = datetime.datetime.now()
        self.Batch = nowdate.strftime("%Y%m%d%H%M%S")

        # 生成sig
        signature = self.AccountSid + self.AccountToken + self.Batch
        md5 = hashlib.md5()
        md5.update(signature.encode())
        sig = md5.hexdigest().upper()

        # 拼接URL
        url = "https://"+self.ServerIP + ":" + self.ServerPort + "/" + self.SoftVersion + "/Accounts/" + self.AccountSid + "/SMS/TemplateSMS?sig=" + sig

        # 生成auth
        src = self.AccountSid + ":" + self.Batch
        auth = base64.encodebytes(src.encode()).strip()
        headers = {'Authorization': auth}
        self.setHttpHeader(headers)

        # 创建包体
        b = ''
        for a in datas:
            b += '<data>{0}</data>'.format(a)
        body = '<?xml version="1.0" encoding="utf-8"?><SubAccount><datas>'+b+'</datas><to>%s</to><templateId>%s</templateId><appId>%s</appId>\
            </SubAccount>\
            '%(to, tempId, self.AppId)
        if self.BodyType == 'json':
            # if this model is Json ..then do next code
            b = '['
            for a in datas:
                b += '"{0}",'.format(a)
            b += ']'
            body = '''{"to": "{0}", "datas": {1}, "templateId": "{2}", "appId": "{3}"}'''.format(to, b, tempId, self.AppId)
        data = ''
        try:
            res = requests.post(url, headers=headers, data=body)
            
            if res.status_code != 200:
                print({res.status_code: '发送失败'})
            else:
                print({200: '发送成功'})
        except Exception as e:
            print(e)
            print({'172001': '网络错误'})