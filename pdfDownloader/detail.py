import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

url='https://homeofpdf.com/detail-cdbc615f8602b8ed2cd3b111ddf0b91c.html'
response=requests.get(url)
# print(response.text)
html=etree.HTML(response.text)
# # xz=html.xpath('//*[@id="detail-content')
# # psd_url=html.xpath('//a[@class="btn btn-primary tm-bt-flen-big"]/@href')[1]
# # title=html.xpath('//div[@class="col-xl-8 col-lg-7 col-md-6 col-sm-12"]/p/text()')

psd_url=html.xpath('//a[@class="btn btn-primary tm-btn-big"]/@href')[1]

# visit_psd=html.xpath('//*[@id="down-pass"]/text()')
# tar_psd=html.xpath('//*[@id="zip-pass"]/text()')[0].replace("\\n","")
# download_url=html.xpath('//div[@class="mb-5"]/a/@href')[0]
# d=download_url[1]
# print(visit_psd,tar_psd,download_url)
print(psd_url)
