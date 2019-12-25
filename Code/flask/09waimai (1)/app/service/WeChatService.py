# -*- coding: utf-8 -*-
import hashlib, requests, uuid, json, datetime
import xml.etree.ElementTree as ET
from app import db


class WeChatService():

    def __init__(self, merchant_key=None):
        self.merchant_key = merchant_key  # 密钥

    def create_sign(self, pay_data):
        '''
		生成签名
		:return:
		'''
        stringA = '&'.join(["{0}={1}".format(k, pay_data.get(k)) for k in sorted(pay_data)])
        stringSignTemp = '{0}&key={1}'.format(stringA, self.merchant_key)
        sign = hashlib.md5(stringSignTemp.encode("utf-8")).hexdigest()
        return sign.upper()

    def get_pay_info(self, pay_data=None):
        '''
		获取支付信息
		:param xml_data:
		:return:
		'''

        '''
            data = {
        'appid': config_mina['appid'],
        'mch_id': config_mina['mch_id'], #目前没有
        'nonce_str': target_wechat.get_nonce_str(),
        'body': '订餐',  # 商品描述
        'out_trade_no': pay_order_info.order_sn,  # 商户订单号
        'total_fee': int(pay_order_info.total_price * 100),
        'notify_url': notify_url,
        'trade_type': "JSAPI",
        'openid': oauth_bind_info.openid,
        'spbill_create_ip':'127.0.0.1'
    }
        
        '''

        sign = self.create_sign(pay_data) #生成sign
        pay_data['sign'] = sign

        '''
            data = {
        'appid': config_mina['appid'],
        'mch_id': config_mina['mch_id'], #目前没有
        'nonce_str': target_wechat.get_nonce_str(),
        'body': '订餐',  # 商品描述
        'out_trade_no': pay_order_info.order_sn,  # 商户订单号
        'total_fee': int(pay_order_info.total_price * 100),
        'notify_url': notify_url,
        'trade_type': "JSAPI",
        'openid': oauth_bind_info.openid,
        'spbill_create_ip':'127.0.0.1'
        'sign':"AADSJKHKH1233312312DASDAS"
    }

        '''
        xml_data = self.dict_to_xml(pay_data)
        headers = {'Content-Type': 'application/xml'}
        url = "https://api.mch.weixin.qq.com/pay/unifiedorder"
        r = requests.post(url=url, data=xml_data.encode('utf-8'), headers=headers)
        r.encoding = "utf-8"

        '''
        1、统一下单就是为了prepay_id
        
        '''
        if r.status_code == 200:
            prepay_id = self.xml_to_dict(r.text).get('prepay_id')
            #------
            pay_sign_data = {
                'appId': pay_data.get('appid'),# 小程序id
                'timeStamp': pay_data.get('out_trade_no'),# 时间戳
                'nonceStr': pay_data.get('nonce_str'),# 随机字符串
                'package': 'prepay_id={0}'.format(prepay_id),# 数据包
                'signType': 'MD5'
            }
            pay_sign = self.create_sign(pay_sign_data) #在签名
            pay_sign_data.pop('appId')#小程序支付的时候不需要appid
            pay_sign_data['paySign'] = pay_sign
            pay_sign_data['prepay_id'] = prepay_id


            return pay_sign_data

        return False

    def dict_to_xml(self, dict_data):
        '''
        dict to xml
        :param dict_data:
        :return:
        '''
        xml = ["<xml>"]
        for k, v in dict_data.items():
            xml.append("<{0}>{1}</{0}>".format(k, v))
        xml.append("</xml>")
        return "".join(xml)

    def xml_to_dict(self, xml_data):
        '''
        xml to dict
        :param xml_data:
        :return:
        '''
        xml_dict = {}
        root = ET.fromstring(xml_data)
        for child in root:
            xml_dict[child.tag] = child.text
        return xml_dict

    def get_nonce_str(self):
        '''
        获取随机字符串
        :return:
        '''
        return str(uuid.uuid4()).replace('-', '')
