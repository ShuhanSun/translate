#/usr/bin/env python3
#coding=utf8


import hashlib
import random
import json
import time
import asyncio

# 使用百度翻译api
appid = '' #你的appid
secretKey = '' #你的密钥
translate_domain = 'api.fanyi.baidu.com'
translate_path = '/api/trans/vip/translate'
translate_dic = {}

def get_tiem():
	return time.strftime("%Y%m%d-%H:%M:%S", time.localtime())

@asyncio.coroutine
def get_translate(word):
	translate = ''
	# print('GET %s%s' % (host, path))
	connect = asyncio.open_connection(translate_domain, 80)
	reader, writer = yield from connect
	header = 'GET %s HTTP/1.0\r\nHost: %s\r\n\r\n' % (get_translate_request_url(word), translate_domain)
	writer.write(header.encode('utf-8'))
	yield from writer.drain()
	is_body = False
	while True:
		line = yield from reader.readline()
		if line == b'\r\n' :
			is_body = True
			continue
		if is_body :
			trans_result = line.decode('utf-8').rstrip()
			translate = json.loads(trans_result)["trans_result"][0]["dst"]
			break
	writer.close()
	# print('%s : %s' % (word, translate))
	translate_dic[word] = translate
	return translate

def get_translate_request_url(word):
	fromLang = 'en'
	toLang = 'zh'
	salt = random.randint(32768, 65536)
	sign = appid+word+str(salt)+secretKey
	m1 = hashlib.md5()
	m1.update(sign.encode('utf-8'))
	sign = m1.hexdigest()
	return translate_path+'?appid='+appid+'&q='+word+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign

##======main========================================================================##
## 	若当月翻译字符数≤2百万，当月免费；若超过2百万字符，按照49元/百万字符支付当月全部翻译字符数费用
words = []
count = 0
print('%s开始读取单词......' % get_tiem())
with open('./words.txt', 'r') as rf:
	for line in rf.readlines():
		count+=1
		w = line.strip()[1:-2] # 把末尾的'\n'删掉
		words.append(w)
		# 不能超过5万个词
		if count > 50000:
			break
print('读取单词完毕，共有:%d个，开始获取翻译......' % count)

# 每1000个批量翻译一次
n = 200
for wn in [words[i:i + n] for i in range(0, len(words), n)]:
	loop = asyncio.get_event_loop()
	tasks = [get_translate(word) for word in wn]
	loop.run_until_complete(asyncio.wait(tasks))
	print('================done 200=====================')

loop.close()

print('%s获取翻译完毕! ' % get_tiem())

# 写入文件
trans_file = './translate-'+get_tiem()+'.txt';
with open(trans_file, 'w') as wf:
	for k, v in translate_dic.items():
		wf.write("%s : %s\n" % (k, v))
print('写入文件完毕!'+trans_file+', 共有:%d个单词' % count)


