
# @ pdf之家
origin_url = ("visit","index",'https://homeofpdf.com/page-num.html"')

# index page

# 获取书的封面
img=("download-img","Xpath",'//figure[@class="effect-ming tm-video-item"]/img')
# 获取书的标题
title=("text-list","Xpath",'//div[@class="d-flex justify-content-between tm-text-gray"]/span')

# 获取详情页链接
detail_url=("url","Xpath",'//figcaption[@class="d-flex align-items-center justify-content-center"]/a')

# detail page
# 书的简介
book_brief=("text-list","Xpath",'//*[@id="detail-content"]/p')

# 书的解压下载界面
psd_url=("url","Xpath",'//a[@class="btn btn-primary tm-btn-big"][1]')

# psd page

# 获取访问密码
visit_psd=("text","ID",'down-pass')
# 获取解压密码
tar_psd=("text","ID",'zip-pass')
# 获取下载页面
download_url=("url","Xpath",'//div[@class="mb-5"]/a')
x_donate=("click","ID",'x-donate')

# download page

# (操作函数名称，元素定位方式，元素定位的值)

# 输入访问密码
passcode=("input","ID","passcode")
# 去下载
to_down=("click-verify","Xpath",'//button[@class="btn btn-primary btn-lg btn-block mt-3"]')
# 普通下载按钮
download=("click-verify","Xpath",'//div[@class="card-body position-relative"]/button[@class="btn btn-outline-secondary fs--1"]')
# 下载时间
download_time=("text","Xpath",'//*[@id="main-content"]/div/div[1]/div/div/div/div[2]/div[2]/button')
