
import requests
from  lxml import etree
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
import time,os
from utils import upzip
from config import *
from concurrent.futures import ThreadPoolExecutor
from loguru import logger

    
class webDriver():
    def __init__(self,diy_options=None):
        options = webdriver.ChromeOptions()
        options.add_experimental_option("detach", True)
        if diy_options:
            options.add_experimental_option("prefs",diy_options)
        self.driver=webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)
        self.driver.maximize_window() 
        
    # elemnt data structure: 
        # page visit ("visit","get","https://www.baidu.com")
        # get by ID ("text","ID","kw")  
        # get by Xpath ("text","Xpath",'//*[@id="su"]')
        # get url ("url","Xpath",'//*[@id="su"]')
        # get text list ("text-list","Xpath",'//*[@id="su"]')
        # click ("click","ID","su")

    def run(self,el,value=None):
        if el[0]=="visit" and el[1]=="get":
            return self.driver.get(el[2])
        if el[1]=="Xpath":
            element=self.driver.find_elements(By.XPATH,el[2])
        if el[1]=="ID":
            element=self.driver.find_element(By.ID,el[2])
        if el[0]=="text":
            return element.text
        if el[0]=="url":
            return [e.get_attribute("href") for e in element]
        if el[0]=="text-list":
            return [e.text for e in element]
        if el[0]=="click":
            element.click()
        if el[0]=="click-verify":
            logger.info(element[0].text)
            element[0].click()
        if el[0]=="input":
            element.send_keys(value)
        if el[0]=="download-img":
            return [e.get_attribute("src") for e in element]
        return True

        
def get_book_name(x):
    if "《" not in x:
        return x
    first=x.index("《")
    last=x.index("》")
    return x[first+1:last]

def get_book_author(x):
    if "《" not in x:
        return None
    first=x.index("》")
    if "版" in x:
        x=x[first+1:].strip()[:-3]
    else:
        x=x[first+1:].strip()
    return x

def get_book_version(x):
    if "版" not in x:
        return None
    last=x.index("版")+1
    return x.strip()[last-3:last]


def get_book_index(nth:int=1):
    origin_url = f"https://homeofpdf.com/page-{nth}.html"
    logger.info(f"visiting {nth} page...")
    driver=webDriver(diy_options=prefs)
    driver.run(("visit","get",origin_url))
    time.sleep(5)
    book_index={
        # "image_url":driver.run(img),
        "title":driver.run(title),
        "detail_url":driver.run(detail_url),   
    }
    driver.driver.close()
    book_index_info_pd=pd.DataFrame(book_index)
    book_index_info_pd.to_csv(temp+"%s.csv"%str(nth),encoding="utf-8",index=False)
    return True

def batch_get_book_index(MAX_PAGE_NUM:int=30):
    try:
        with ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(get_book_index, [i for i in range(MAX_PAGE_NUM)])
    except Exception as e:
        logger.info(e)
        
def check_finished():
    if len(os.listdir(temp))>=MAX_PAGE_NUM:
        return True 
    else:
        check_finished()
        
def get_book_index_all():
    
    if os.path.exists("./all/res_book_index.xlsx"):
        return True
    try: 
        batch_get_book_index(MAX_PAGE_NUM)
        book_index_info=[]     
        if check_finished():
            for f in os.listdir(temp):
                book_index_info.append(pd.read_csv(temp+f,encoding="utf-8"))
                
            book_index_info_res=pd.concat(book_index_info)
            
            book_index_info_res["name"]=book_index_info_res["title"].apply(get_book_name)
            book_index_info_res["author"]=book_index_info_res["title"].apply(get_book_author)
            book_index_info_res["version"]=book_index_info_res["title"].apply(get_book_version)
            
            res_path="./all/"
            if not os.path.exists(res_path):
                os.makedirs(res_path)
                
            book_index_info_res.to_excel(res_path+"/res_book_index.xlsx",sheet_name="books",index=True)
    
        return True
    except:
        return False
    
def get_book_detail(detail_url:str):
    logger.info(f"visiting detail {detail_url} page...")
    driver=webDriver(diy_options=prefs)
    driver.run(("visit","get",detail_url))
    bookBrief=driver.run(book_brief)
    logger.info(bookBrief)
    driver.driver.close()
    return bookBrief

def get_psd_url(psd_url:str):
    logger.info(f"visiting psd {psd_url} page...")
    driver=webDriver(diy_options=prefs)
    try:
        driver.run(["visit","get",psd_url])
        psdUrl=driver.run(psd_url)
        logger.info(psdUrl)
    except Exception as e:
        logger.info(e)

    while True:
        try:
            logger.info("try to get visit psd")
            visitPsd=driver.run(visit_psd)
            logger.info(visitPsd)
            break
        except:
            logger.info("try to get visit psd again")
            try:
                driver.run(x_donate)
            except:
                driver.run(["visit","get",psdUrl])
                visitPsd=driver.run(visit_psd)
                if visitPsd:
                    break
                else:
                    logger.info(driver.run(["visit","get",psdUrl]))
            driver.driver.close()
            return False
            
    from random import randint
    time.sleep(randint(3,5))

        
    tarPsd=driver.run(tar_psd)
    logger.info(tarPsd)
    downloadUrl=driver.run(download_url)[0]
    logger.info(downloadUrl)
    
    # logger.info(visitPsd,tarPsd,downloadUrl)
    driver.driver.close()
        
    return visitPsd,tarPsd,downloadUrl

def download_pdf(downloadUrl:str,tarPsd:str):
    logger.info(f"downloading.... {downloadUrl} ...")
    temp_path="/Users/pro/Documents/pdf/pdf/temp/"+tarPsd+"/"
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)
    logger.info(f"setting temp path as {temp_path}")
    tem={"download.default_directory":temp_path}
    driver_download=webDriver(diy_options=tem)
        # 下载操作
    while True:
        try:
            logger.info("try to get download page")
            driver_download.run(["visit","get",downloadUrl])
            break
        except Exception as e:
            logger.info(e)
            driver_download.run(x_donate)
            driver_download.run(["visit","get",downloadUrl])
            time.sleep(200)
        driver_download.driver.close()
            
    logger.info("try to get passcode")  
    try:
        pass_code=downloadUrl.split("=")[-1].replace("//n","")  
        logger.info(pass_code)
        driver_download.run(passcode,value=pass_code)
    except Exception as e:
        logger.info(e)
        
    logger.info("try to go to download page")
    driver_download.run(to_down)
    logger.info("try to download")
    driver_download.run(download)
    logger.info("downloading...")
    try:
        wait_s=driver_download.run(download_time)[0]
        logger.info(wait_s)
        if "秒" in wait_s:
            s=int(wait_s[wait_s.index("约")+1:wait_s.index("秒")].strip())
        if "分钟" in wait_s:
            s=int(wait_s[wait_s.index("约")+1:wait_s.index("分钟")].strip())*60
    except Exception as e:
        logger.info(e)
    
    time.sleep(s+10)
    logger.info("waiting for %s seconds..."%s)
    
    print(temp_path,os.listdir(temp_path))
    
    if os.listdir(temp_path):
        logger.info("download successfully!")
        file_name=os.listdir(temp_path)[0]
        logger.info("file name:%s"%file_name)
        file_path=os.path.join(temp_path,file_name)
        logger.info("file path:%s"%file_path)
        save_path=file_path.replace("temp"+"/"+tarPsd,"upzip").replace(".zip","")
        logger.info("save path:%s"%save_path)
        upzip(file_path,save_path,tarPsd.strip())
        # os.remove(file_path)
    driver_download.driver.close()
    return True

def get_encry_download(index_book):
    logger.info(dict(index_book))
    book_brief=get_book_detail(index_book["detail_url"])
    finished_book_brief={
        "detail_url":index_book["detail_url"],
        "book_brief":book_brief
    }
    with open(all+"finished_book_detail.txt","a") as f:
        f.write(str(finished_book_brief))
    
    visitPsd,tarPsd,downloadUrl=get_psd_url(index_book["psd_url"])
    if download_pdf(downloadUrl,tarPsd):
        finished_book={
            "detail_url":index_book["detail_url"],
            "book_brief":book_brief,
            "visitPsd":visitPsd,
            "tarPsd":tarPsd,
            "downloadUrl":downloadUrl
        }
        with open(all+"finished_book.txt","a") as f:
            f.write(str(finished_book))
        return True
    
if __name__ == "__main__":
    
    download_path="/Users/pro/Documents/pdf/pdf/temp"
    unzipped_path="/Users/pro/Documents/pdf/pdf/upzip"
    img_download_path="./pdf/img"
    all="./all/"
    temp="./temp/"
    MAX_PAGE_NUM=30
    
    if not os.path.exists(download_path):
        os.makedirs(download_path)
    if not os.path.exists(img_download_path):
        os.makedirs(img_download_path)
    if not os.path.exists(temp):
        os.makedirs(temp)
    if not os.path.exists(all):
        os.makedirs(all)
    if not os.path.exists(unzipped_path):
        os.makedirs(unzipped_path)
    
    prefs={"download.default_directory":download_path}
    
    if get_book_index_all():
        logger.info("get book index successfully!")
        index_all=pd.read_excel(all+"res_book_index.xlsx")
        index_all["psd_url"]=index_all["detail_url"].apply(lambda x: x.replace("detail","download"))
        with ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(get_encry_download, [index_all.iloc[i] for i in range(len(index_all))])
        
        
    

    

