import requests
from lxml import etree
import os

basedir = os.path.dirname(__file__) + '/emoji'

headers = {
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
}
base_url = 'https://www.doutula.com/article/list/?page='

j = int(input('输入要爬取的页数：'))

for i in range(1,j+1):


	url = base_url + str(i)

	req = requests.get(url, headers=headers)


	html = etree.HTML(req.text)

	a_list = html.xpath('//div[@id="home"]//div[@class="col-sm-9"]/a')

	for a in a_list:

		detail_url = a.xpath('@href')[0]
		detail_req = requests.get(detail_url, headers=headers)
		detail_html = etree.HTML(detail_req.text)
		li = detail_html.xpath('//div[@class="container_"]/div[@class="container"]//li[@class="list-group-item"]')[0]
		dir_name = li.xpath('./div[@class="pic-title"]/h1/a/text()')[0]
		img_list = li.xpath('./div[@class="pic-content"]/div[@class="artile_des"]/table//a/img')

		file_dir = basedir + '/' + dir_name
		print('正在爬取第{}页的{}'.format(i, dir_name))
		if not os.path.exists(file_dir):
			os.makedirs(file_dir)
		for img in img_list:
			url = img.xpath('./@onerror')[0]

			file_name = img.xpath('./@alt')[0]
			new_url = url.split('=')[1]
			new_url = new_url[1:-1]
			ext = new_url.rsplit('.', 1)[1]
			file_path = file_dir + '/' + file_name + '.' + ext
			with open(file_path, 'wb') as f:
				f.write(requests.get(new_url, headers=headers).content)
			f.close()

print('爬取完成。。。')


