
# @ 批量下载pdf文件

import requests
from  lxml import etree
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from utils import upzip




headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
}


# @ 1.获取首页的所有pdf链接
# @ 2.获取pdf的title，图书图片，作者版本，详情页的url
# @ 3.进入详情页，获取pdf的下载链接，内容简介和作者简介
# @ 4.点击直接下载，进入下载页面，获取下载密码和解压密码
# @ 5.点击下载，进入下载页面，此时需要确保城通网盘登录，进入下载页面，获取下载链接
# @ 6.下载pdf文件，并保存图书信息到数据库

class BookInfo:
    def __init__(self,name,img,author,version,detail_url,**args):
        self.name=name
        self.img=img
        self.author=author
        self.version=version
        self.detail_url=detail_url
        self.book_brief=None if args.get('book_brief') is None else args.get('book_brief')
        self.psd_url=None if args.get('psd_url') is None else args.get('psd_url')
        self.visit_psd=None if args.get('visit_psd') is None else args.get('visit_psd')
        self.tar_psd=None if args.get('tar_psd') is None else args.get('tar_psd')
        self.download_url=None if args.get('download_url') is None else args.get('download_url')
        

def getIndexPage(num):
    book_info_list=[]
    book_index_page_url="https://homeofpdf.com/page-%s.html"%num
    req=requests.get(book_index_page_url)
    html=etree.HTML(req.text)
    img=html.xpath('//figure[@class="effect-ming tm-video-item"]/img/@src')
    title=html.xpath('//div[@class="d-flex justify-content-between tm-text-gray"]/span/text()')
    detail_url=html.xpath('//figcaption[@class="d-flex align-items-center justify-content-center"]/a/@href')
    for i in range(len(title)):
        book_title=title[i].split('》')
        name=book_title[0].split('《')[1]
        if "版" not in book_title[1]:
            author=book_title[1].replace(" ","")
            version=None
        else:
            author=book_title[1][:-3].replace(" ","")
            version=book_title[1][-3:]
        book_info_list.append(BookInfo(name,img,author,version,detail_url[i]))
    return book_info_list

def getDetailPage(book_info):
    base_url="https://homeofpdf.com/"
    detail_url=base_url+book_info.detail_url
    req=requests.get(detail_url,headers=headers)
    html=etree.HTML(req.text)
    
    
    book_info.book_brief=html.xpath('//*[@id="detail-content"]/p/text()')
    book_info.psd_url=html.xpath('//a[@class="btn btn-primary tm-btn-big"]/@href')
    print(book_info.psd_url)
    book_info.psd_url=html.xpath('//a[@class="btn btn-primary tm-btn-big"]/@href')[1]
    if "javascript" in book_info.psd_url:
        return False
    print(book_info.psd_url)
    return book_info

def getPsdInfo(book_info):
    base_url="https://homeofpdf.com"
    psd_url=base_url+book_info.psd_url
    req=requests.get(psd_url,headers=headers)
    html=etree.HTML(req.text)
    book_info.visit_psd=html.xpath('//*[@id="down-pass"]/text()')
    book_info.tar_psd=html.xpath('//*[@id="zip-pass"]/text()')[0].replace("\\n","")
    book_info.download_url=html.xpath('//div[@class="mb-5"]/a/@href')[0]
    return book_info


   
   
# 调不通
    
# def download_pdf(book_info):
    # f=book_info.download_url.split('/')[-1].split('?')[0]
    # token=book_info.download_url.split("=")[-1]

    # url = "https://webapi.ctfile.com/getfile.php?path=f&f=%s&passcode=%s&token=us952mdrg5f6zbqyd0wj3s&r=0.27557914800748295&ref="%(f,token)
    # # print(url)

    # payload={}
    # headers = {
    # 'Cookie': 'sessionid=1722662383281; ua_checkmutilogin=JCRIpK9IE6; PHPSESSID=vpedd5an1laesuku1eg9vhbmv3',
    # 'User-Agent': 'Apifox/1.0.0 (https://apifox.com)'
    # }

    # response = requests.request("GET", url, headers=headers, data=payload)
    # print(response.json())
    
    # pdf_url=response.json()['downurl']
    # with open("pdf/"+book_info.name+".pdf","wb") as f:
    #     f.write(requests.get(pdf_url).content)
    # f.close()

def downloadPDF(download_url,zip_pass):
    options = webdriver.ChromeOptions()
    download_path="/Users/pro/Documents/practice/pdf/temp"
    unzip_path="/Users/pro/Documents/practice/pdf/unzip"
    prefs={"download.default_directory":download_path}
    options.add_experimental_option("detach", True)
    options.add_experimental_option("prefs",prefs)

    driver=webdriver.Chrome(options=options)
    driver.get(download_url)
    time.sleep(2)
    visit_pass=driver.find_element(By.ID,'passcode')
    to_down=driver.find_element(By.XPATH,"//*[@id='main-content']/div/div[1]/div/div/div/div[2]/div[2]/button")
    visit_pass.send_keys(download_url.split("=")[-1])
    to_down.click()
    time.sleep(2)
    download=driver.find_element(By.XPATH,'//div[@class="card-body position-relative"]/button[@class="btn btn-outline-secondary fs--1"]')
    
    download.click()
    
    import os
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    # if not os.path.exists(unzip_path):
    #     os.makedirs(unzip_path)
        
    if os.listdir(download_path):
        file_name=os.listdir(download_path)[0]
        file_path=os.path.join(download_path,file_name)
        save_path=file_path.replace("temp","upzip").replace(".zip","")
        upzip(file_path,save_path,zip_pass.strip())
        os.remove(file_path)
    
    driver.implicitly_wait(100)
    print("%s 下载成功"%(download_url))
    
    
def downloadPDFs(book_info_list):
    with ThreadPoolExecutor(max_workers=5) as executor:
        for book_info in book_info_list:
            executor.submit(downloadPDF,book_info.download_url,book_info.tar_psd)
            
def save_book_info(book_info_list):
    df=pd.DataFrame(book_info_list)
    df.to_excel("pdf_res.xlsx",index=False)
    
def get_book_info_list(n):
    book_info_list=getIndexPage(n)
    book_infos=[]
    for book_info in book_info_list:
        print("book_info_1",book_info.name)
        book_info=getDetailPage(book_info)
        if book_info==False:
            continue 
        print("book_info_2",book_info.__dict__)
        book_info=getPsdInfo(book_info)
        print("book_info_3",book_info.__dict__)
        book_infos.append(book_info.__dict__)
    save_book_info(book_infos)
    return book_infos
    
def batch_book_info(n):
    pass  
    
    
if __name__ == "__main__":
    get_book_info_list(1)


        
                
        
