#encoding='utf-8'
import requests
from lxml import etree
from time import sleep
import random
import os
import concurrent
from concurrent.futures import ThreadPoolExecutor
import multiprocessing

User_Agent = [
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
]


class Spider():
    def __init__(self):

        #三表在URL中的名称，基本URL
        self.data_name = ['zcfzb','lrb','xjllb']
        self.year_type = '?type=year'
        self.service_url = 'http://quotes.money.163.com/service/{}_{}.html'

        #各个报表的URL

        #股票列表的URL
        self.url = 'http://www.court.gov.cn/wenshu/gengduo-3.html?page={}'
        self.headers = {'User-Agent': None,
                        'Cookie': 'Hm_lvt_9e03c161142422698f5b0d82bf699727=1591583495,1592050599; '
                                  'COURTID=ftib6edl18sq27dmm8fm5qr3o4; '
                                  'Hm_lpvt_9e03c161142422698f5b0d82bf699727=1592051213',
                        'Host': 'www.court.gov.cn',
                        'Referer': 'http://www.court.gov.cn/wenshu/gengduo-3.html'}
    def initalize(self,get_his_crawl_list = True):
        if not os.path.exists('crawl_txt') :
            os.mkdir('crawl_txt')
        r=[]
        if os.path.exists('finish_list.txt') and (get_his_crawl_list == True):
            with open ('finish_list.txt', 'r') as f:
                r = f.readlines()
            r = [r_num[:-1] for r_num in r]
        return r

    #获取decode()返回值
    def get_url(self,url):
        headers = self.headers
        headers['User-Agent'] = random.choice(User_Agent)
        response = requests.get(url, headers=headers)
        return response.content.decode()

    def get_url_list(self,url):
        div_url_list=[]
        complete_page_list=[]
        for i in range (1,76):
            url_tor = url.format(i)
            html_str=self.get_url(url_tor)
            html = etree.HTML(html_str)
            div_list = html.xpath( "//div[@class='list']/ul/li[@class='wslist']/div[@class='l']/ul/li[@class='list_tit']/a/@href")
            div_list = ['http://www.court.gov.cn' + div for div in div_list]
            div_url_list =  div_url_list+div_list
            complete_page_list.append(i)
            print('第{}页爬取完成，共{}个'.format(i, len(div_list)))
            sleep(random.random() * 2)
        with open('url_list.txt', "w", encoding='utf-8') as f:
            for stname in div_url_list:
                f.write(stname)
                f.write('\n')
        return div_url_list

    def read_url_list(self):

        with open('url_list.txt', 'r') as f:
            div_url_list=f.read()
            div_url=div_url_list.split('\n')

        return div_url

    def fetch_text_pages(self,url):

        html_str = self.get_url(url)
        html = etree.HTML(html_str)
        title = html.xpath("//div[@class='cpws_content']/div[@class='clearfix cpws']/div[@class='title']/text()")[0]
        text_doc = html.xpath("//div[@class='txt big']/div[@id='zoom']/div/text()")
        file_path ='./crawl_txt/'+ title+'.txt'
        with open(file_path, 'w', encoding='utf-8') as f:
            for text in text_doc:
                f.write(text)
                f.write('\n')
        sleep(random.random() * 2)
        print('爬取{} 已完成'.format(title))
        # except:
        #     print('爬取{} 失败'.format(url))

    # 多进程爬取文件
    def download_csv_multprosess(self,stock):
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        pool.map(self.fetch_text_pages, stock)
        pool.close()
        pool.join()
    def run(self):
        crawl_list = self.initalize(get_his_crawl_list=True)
        # url_list = self.get_url_list(self.url)
        url_list = self.read_url_list()
        for url in url_list:
            self.fetch_text_pages(url)
        #更新爬取文书列表
        #多进程爬取文件
        # self.download_csv_multprosess(self, url_list)


if __name__ == '__main__':
    spider = Spider()
    spider.run()
# headers = {'User-Agent': "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
#                         'Cookie': 'Hm_lvt_9e03c161142422698f5b0d82bf699727=1591583495,1592050599; '
#                                   'COURTID=ftib6edl18sq27dmm8fm5qr3o4; '
#                                   'Hm_lpvt_9e03c161142422698f5b0d82bf699727=1592051213',
#                         'Host': 'www.court.gov.cn',
#                         'Referer': 'http://www.court.gov.cn/wenshu/gengduo-3.html'}
# html_str=requests.get('http://www.court.gov.cn/wenshu/xiangqing-11306.html', headers=headers).content.decode()
# html = etree.HTML(html_str)
# div_list = html.xpath( "//div[@class='cpws_content']/div[@class='clearfix cpws']/div[@class='title']/text()")[0]
# print(div_list)