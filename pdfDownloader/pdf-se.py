
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

    
class webDriver():
    def __init__(self):
        options = webdriver.ChromeOptions()
        self.download_path="/Users/pro/Documents/practice/pdf/temp"
        if not os.path.exists(self.download_path):
            os.makedirs(self.download_path)
        prefs={"download.default_directory":self.download_path}
        options.add_experimental_option("detach", True)
        options.add_experimental_option("prefs",prefs)
        self.driver=webdriver.Chrome(options=options)
        self.driver.implicitly_wait(10)
        self.driver.maximize_window() 
        
    def deal_operation(self,el,page_num=1,send_keys=None):
        print(el)
        if el[0]=="visit" and el[1]=="index":
            self.driver.get(el[2].replace("num",str(page_num)))
        if el[0]=="visit" and el[1]=="get":
            self.driver.get(el[2])
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
            print(element[0].text)
            element[0].click()
        if el[0]=="input":
            element.send_keys(send_keys)
        if el[0]=="download-img":
            return [e.get_attribute("src") for e in element]
        time.sleep(1)
        return True

    
if __name__ == "__main__":
    
    driver=webDriver()
    for n in range(1,10):
        driver.deal_operation(origin_url,page_num=n)
        time.sleep(2)
        imgs=driver.deal_operation(img)
        titles=driver.deal_operation(title)
        detail_urls=driver.deal_operation(detail_url)
        
        book_info_list=[]

        for i in range(len(titles)):
            driver.deal_operation(["visit","get",detail_urls[i]])
            bookBrief=driver.deal_operation(book_brief)
            psdUrl=driver.deal_operation(psd_url)[1]
            driver.deal_operation(["visit","get",psdUrl])
            try:
                visitPsd=driver.deal_operation(visit_psd)
            except:
                # time.sleep(200)
                # driver.deal_operation(["visit","get",psdUrl])
                # visitPsd=driver.deal_operation(visit_psd)
                continue
            tarPsd=driver.deal_operation(tar_psd)
            downloadUrl=driver.deal_operation(download_url)[0]
            print("*"*20,downloadUrl)
            
            book_info={
                "img":imgs[i],
                "title":titles[i],
                "bookBrief":bookBrief,
                "visitPsd":visitPsd,
                "tarPsd":tarPsd,
                "downloadUrl":downloadUrl,
            }
            
            # 下载操作
            # try:
            #     driver.deal_operation(["visit","get",downloadUrl])
            # except:
            #     try:
            #         driver.deal_operation(x_donate)
            #         driver.deal_operation(["visit","get",downloadUrl])
            #     except:
            #         continue
            # driver.deal_operation(passcode,send_keys=downloadUrl.split("=")[-1].replace("//n",""))
            # driver.deal_operation(to_down)
            # driver.deal_operation(download)
            
            # time.sleep(60)
            # if os.listdir(driver.download_path):
            #     file_name=os.listdir(driver.download_path)[0]
            #     file_path=os.path.join(driver.download_path,file_name)
            #     save_path=file_path.replace("temp","upzip").replace(".zip","")
            #     upzip(file_path,save_path,tarPsd.strip())
            #     os.remove(file_path)
            
            book_info_list.append(book_info)
    
    data=pd.DataFrame(book_info_list)
    data.to_excel("pdf_to_download.xlsx",index=False)
        
        
    

    

