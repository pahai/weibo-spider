from urllib.parse import urlencode
from pyquery import PyQuery as pq
import requests
import time
import csv

uids =[ '6766326144','1460381662','3982803458','2219915922','6096345524','1670659923','1902737731','3312170677','1614282004','1653567397']
#btc狙击手、火星人、江卓尔、邪恶猫、crypto_investor、月风_投资笔记、子修、塔特、蔡学镛、Horacex
base_url = 'https://m.weibo.cn/api/container/getIndex?'

#获取m端微博页面
def get_page(page):
	params = {
		'type':'uid',
		'value':uid,
		'containerid':'107603'+uid,
		'page':page
		}
	url = base_url + urlencode(params)
	try:
		response = requests.get(url,headers = headers)
		if response.status_code == 200:
			return response.json()
	except requests.ConnectionError as e:
		print('Error',e.args)
#页面解析
def parse_page(json):
	if json:
		items = json.get('data').get('cards')
		for item in items:
			item = item.get('mblog')
			if item == None:
				continue				
			weibo = {}
			weibo['name'] = item.get('user').get('screen_name')
			weibo['created_at'] = item.get('created_at')
				
			if item.get('isLongText') == True:
				longid = item.get('id')
				weibo['text'] = get_long_weibo(longid)
			else:
				weibo['text'] = pq(item.get('text')).text()
			yield weibo
#获取长微博功能		
def get_long_weibo(longid):             
	long_url = 'https://m.weibo.cn/statuses/extend?id=' + longid
	response = requests.get(long_url,headers = headers)
	try:
		a = response.json().get('data').get('longTextContent')
		long_weibo = pq(a).text()		
	except AttributeError:
		long_weibo = '获取失败'
	return long_weibo
		
if __name__ == '__main__':
	for uid in uids:
		headers = {
		'Host':'m.weibo.cn',
		'Referer':'https://m.weibo.cn/u/'+uid,
		'User-Agent':'Mozilla/5.0(Macintosh;Intel Mac OS X 10_13_3)AppleWebKit/537.36(KHTM,like Gecko) Chrome/65.0.3325.162 Safari/537.36',
		'X-Requested-With':'XMLHttpRequest'
		}
		weibo_num = get_page(1).get('data').get('cardlistInfo').get('total')
		counter = 0
		for page in range(1,int(weibo_num/10)+2):    
			time.sleep(1) 
			json = get_page(page)
			results = parse_page(json)

			for result in results:
				print(result)
				counter += 1
				name = result['name']
				file_path = 'X:\weibo_spider\id-' + name +'.txt'
				with open(file_path,'a',encoding = 'utf-8') as f:
					f.write('\n'.join(list(result.values())))#把换行符加入到weibo字典value生成的列表间
					f.write('\n' + '='*50 + str(counter)+'\n')
						
		print(str(weibo_num) + u'条爬取完毕')
		f.close()	
