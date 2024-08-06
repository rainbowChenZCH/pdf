# 1.批量获取pdf标题、图片和详情页链接
# 2.获取pdf详情页的简介、加密密码页面链接、下载链接
# 3.下载pdf文件并解压

from config import *
from loguru import logger
from DrissionPage import ChromiumPage

def get_book_index(n:int=1):
    for i in range(1,n):
        origin_url = f"https://homeofpdf.com/page-{i}.html"
        page=ChromiumPage()
        page.get(origin_url)
        book_index={
            "imgs":page.eles(img),
        }
        
        
        
        
        