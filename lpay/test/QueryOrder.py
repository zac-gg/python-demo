import sys
import time
import json
from configparser import ConfigParser
sys.path.append("..")
from urllib.parse import quote,unquote
from library import const,tool,aes
from library.RSACipher import RSACipher

ini_file = "../config.ini"
cfg = ConfigParser()
cfg.read(ini_file)
const.QUERY_PARAMETER = '/bidPriceApi/currentBidPrice'

class QueryOrder():
	def query(self):
		api_url = cfg['config']['REQUEST_URL']+const.QUERY_PARAMETER
		#Get timestamp
		now = str(round(time.time() * 1000))
		#1.Get Sign Data
		sign_data = self.__get_sign_data(now)
		#2.The parameters are sorted from small to large using ASCII code
		sign_data = tool.ksort(sign_data)
		#sign_data = 'address=NY 1058&callbackUrl=www.baidu.com&cardCcv=355&cardExpMonth=01&cardExpYear=2020&cardNo=5105105105105100&cardType=MASTERCARD&city=NY&country=US&currency=USD&email=12345@qq.com&firstName=test&lastName=test&merchantNo=XP00824&merchantOrderNo=1626345205007&orderAmount=1000&payModel=CREDIT_CARD&phone=13700000000&productDetail=Test Goods&timeStamp=1626760723158'
		#3.Sign data
		cipher = RSACipher()
		sign =  cipher.sign(cfg['config']['PRIVATE_KEY'],sign_data)
		print(sign,'sign')
		#4.AES encryption and URLEncode for specified characters
		post_data = tool.url_encoder(self.__get_post_data(sign,now))
		print(post_data,'post data')
		#5.Curl post request
		res = tool.curl_post(api_url,post_data)
		return res.status_code,res.text

	#Check sign
	def checkSign(self,status_code,text):
		if status_code == 200:
			text_dic = json.loads(text)
			if text_dic['meta']['code'] == '0000':
				sign_data  =  text_dic['data']['sign']
				cipher = RSACipher()
				sign = cipher.long_decrypt(cfg['config']['PRIVATE_KEY'],sign_data)
				print(sign)

	#Sign data
	def __get_post_data(self,sign,now):
		post_dict = {
			'merchantNo':cfg['config']['HMERCHANT_ID'],
			'timeStamp': now,
			'language' : 'en',
			'buyingCurrency':"USD",
			"sellingCurrency":"HKD"
		}
		post_dict['sign'] = sign.decode('utf-8')
		return post_dict

	#Sign data
	def __get_sign_data(self,now):
		dict = {
			'merchantNo':cfg['config']['HMERCHANT_ID'],
			'timeStamp': now,
			'buyingCurrency':"USD",
			"sellingCurrency":"HKD"
		}
		return dict
t = QueryOrder()
status_code,text=t.query()
print(status_code,text)
#status_code = 200
#text = '{"meta":{"success":true,"code":"0000","message":"Request Success"},"data":{"merchantNo":"XP00824","merchantOrderNo":"1626345205008","orderNo":"XP01OC0210720172527092760313946","currency":"USD","orderAmount":1000,"orderFee":440,"payModel":"CREDIT_CARD","orderStatus":"SUCCESS","webUrl":null,"page":null,"orderTime":1626744327139,"finishTime":1626744327402,"sign":"V5wgzKfpAZotmz51gR5Oy/irxqOtIjfMQJVs8F5p4sF74Cu7k6lOYmcOF4AAjkQek8hNjbzN5zcN1nKi6HLjaGUQFEYTm3i+plftlCgL9j52LYre6GgX25FHZmX+02dS4b119LIzDDAODHerG+I+MW1hmpRRFYELjrgKPCI+u7lFcjijE3Zk86fMFQW4AqX0tvA44k2KhhOa30EVcC/l2mEsWGUqXWsZGnEs1aP2J/0CtxEl6KUnttnMIP5FsWkUq2i7WvFWDfUkDurBnde4HoKVeusnta4W/3JiWpbw9Ks3yQne7FMoQoOghoFqNsW7mPK6quZEfrlDLGAHd63T6g==","remark":""}}'
t.checkSign(status_code,text)