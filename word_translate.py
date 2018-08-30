#/usr/bin/env python
#coding=utf8
 
import httplib
import md5
import urllib
import random
import json
import asyncio

appid = '' #你的appid
secretKey = '' #你的密钥

@asyncio.coroutine
def get_translate(word):
	translater = ''
	httpClient = None
	myurl = '/api/trans/vip/translate'
	q = word
	fromLang = 'en'
	toLang = 'zh'
	salt = random.randint(32768, 65536)

	sign = appid+q+str(salt)+secretKey
	m1 = md5.new()
	m1.update(sign)
	sign = m1.hexdigest()
	myurl = myurl+'?appid='+appid+'&q='+urllib.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
	 
	try:
	    httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')
	    httpClient.request('GET', myurl)
	 
	    #response是HTTPResponse对象
	    response = httpClient.getresponse()
	    res = response.read()
	    return json.loads(res)["trans_result"][0]["dst"]
# 返回格式{
#   "from": "en",
#   "to": "zh",
#   "trans_result": [
#     {
#       "src": "apple",
#       "dst": "苹果"
#     }
#   ]
# }
	except Exception, e:
	    print e
	finally:
	    if httpClient:
	        httpClient.close()
	return translater

#### main	若当月翻译字符数≤2百万，当月免费；若超过2百万字符，按照49元/百万字符支付当月全部翻译字符数费用
count = 0
with open('./translate.txt', 'w') as wf:
	with open('./words.txt', 'r') as rf:
	    for line in rf.readlines():
	    	count+=1
	    	w = line.strip()[1:-2] # 把末尾的'\n'删掉
	    	if count > 100:
	    		break
    		trans = get_translate(w)
    		print w, ':', trans
    		wf.write("%s : %s\n" % (w, trans.encode('utf-8')))
    		# 不能超过5万个词
    		if count > 50000:
	    		break

print 'translate done!====words count:', count
