import selenium
import os
from selenium import webdriver
from lxml import etree
from time import sleep
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
file_path='./crawl_openlaw/'
from selenium.webdriver import ChromeOptions
option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])#开启实验性功能
def fetch_text_pages(i):

    title_name = driver.find_element_by_xpath(
        "//main[@id='content']/div[@id='ht-kb']/article[@class='ht_kb type-ht_kb status-publish format-standard hentry'][{}]/h3[@class='entry-title']/a".format(
            i)).text
    driver.find_element_by_xpath(
        "//main[@id='content']/div[@id='ht-kb']/article[@class='ht_kb type-ht_kb status-publish format-standard hentry'][{}]/h3[@class='entry-title']/a".format(
            i)).click()
    current_windows = driver.window_handles
    driver.switch_to.window(current_windows[1])
    html = etree.HTML(driver.page_source)
    title = html.xpath("///div[@id='entry-cont']/div[@class='annotator-wrapper']//text()")
    frame = html.xpath("//div[@class='ht-container']/aside[@id='sidebar']/section[@class='widget HT_KB_Authors_Widget clearfix'][1]/ul[@class='clearfix']/li[@class='clearfix ht-kb-pf-standard']//text()")
    print(title_name+'已完成')

    file_path = './crawl_openlaw/' + title_name + '.txt'
    file_path_base_info = './crawl_openlaw_base_info/' + title_name + '.txt'
    with open(file_path, 'w', encoding='utf-8') as f:
        for text in title:
            f.write(text)
    with open(file_path_base_info, 'w', encoding='utf-8') as f:
        for text in frame:
            f.write(text)
            f.write('\n')
    driver.close()
    driver.switch_to.window(current_windows[0])
    sleep(random.random()*2)
if __name__ == '__main__':
    if not os.path.exists('crawl_openlaw'):
        os.mkdir('crawl_openlaw')
    if not os.path.exists('crawl_openlaw_base_info'):
        os.mkdir('crawl_openlaw_base_info')
    root_url = "https://openlaw.cn/search/judgement/type?courtId=&lawFirmId=&docType=Verdict&causeId=06cf4c5dc13949e39b7a679ebaf7cfc9&judgeDateYear=&lawSearch=&litigationType_c=&judgeId=&zoneId=&procedureType=&sideType=&keyword=行政复议&page={}"
    #选定爬取的url,实例代码中的分别是：1、北京中院2、北京第二中院3、河北郑州中院4、山东济南中院
    url_list = ['https://openlaw.cn/search/judgement/type?courtId=789a41bf0fd74e07a2a642d9aaba6520&lawFirmId=&docType=Verdict&causeId=06cf4c5dc13949e39b7a679ebaf7cfc9&judgeDateYear=&lawSearch=&litigationType_c=&judgeId=&zoneId=&procedureType=&sideType=&keyword=行政复议&page={}',
                'https://openlaw.cn/search/judgement/type?courtId=8d166c5739394a6db7f79a84bc2d624a&lawFirmId=&docType=Verdict&causeId=06cf4c5dc13949e39b7a679ebaf7cfc9&judgeDateYear=&lawSearch=&litigationType_c=&judgeId=&zoneId=&procedureType=&sideType=&keyword=行政复议&page={}',
                'https://openlaw.cn/search/judgement/type?courtId=99db8cf5f8594b42abb97150e7904844&lawFirmId=&docType=Verdict&causeId=06cf4c5dc13949e39b7a679ebaf7cfc9&judgeDateYear=&lawSearch=&litigationType_c=&judgeId=&zoneId=&procedureType=&sideType=&keyword=行政复议&page={}',
                'https://openlaw.cn/search/judgement/type?courtId=b99edfb9e66c4783b61b44e5825ba0f6&lawFirmId=&docType=Verdict&causeId=06cf4c5dc13949e39b7a679ebaf7cfc9&judgeDateYear=&lawSearch=&litigationType_c=&judgeId=&zoneId=&procedureType=&sideType=&keyword=行政复议&page={}']
    driver = webdriver.Chrome(options=option)
    driver.implicitly_wait(4)
    driver.get(root_url)
    driver.find_element_by_xpath("//*[@id='username']").send_keys('847405040@qq.com')
    driver.find_element_by_xpath("//*[@id='password']").send_keys('*****')
    driver.find_element_by_xpath("//*[@id='submit']").click()
    for page in range(1,21):
        driver.get(url_list[0].format(page))
        for i in range(1,21):
            fetch_text_pages(i)
