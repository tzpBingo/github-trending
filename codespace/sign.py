# -*- coding: utf-8 -*
import warnings
import os
import argparse
import time
import subprocess
import fcntl
import csv
import requests
import random
import pandas as pd
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from fake_useragent import UserAgent
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from collections import namedtuple
warnings.filterwarnings("ignore")

API_KEY = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

def go_sign(driver,cityid,city,email,school,fname,lname,bm,by,gm,gy,url):
    
    driver.get(url)
    # print(driver.find_element_by_tag_name("body").text)
    time.sleep(5)
    print_white(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\tRunning")

    driver.execute_script('document.getElementById("j_id0:theForm:cntryCd").value="'+cityid+'"')
    driver.execute_script('document.getElementById("j_id0:theForm:eltFirstName").value="'+fname+'"')
    driver.execute_script('document.getElementById("j_id0:theForm:eltLastName").value="'+lname+'"')
    driver.execute_script('document.getElementById("j_id0:theForm:gradMonth").value="'+gm+'"')
    driver.execute_script('document.getElementById("j_id0:theForm:gradYear").value="'+gy+'"')
    driver.execute_script('document.getElementById("j_id0:theForm:student-bm-date").value="'+bm+'"')
    driver.execute_script('document.getElementById("j_id0:theForm:student-by-date").value="'+by+'"')

    data_sitekey_div = driver.find_element_by_class_name("g-recaptcha")
    data_sitekey = data_sitekey_div.get_attribute("data-sitekey")
    print_white(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\tData Site Key: "+data_sitekey )
 
    s = requests.Session()
    captcha_id = s.post("http://2captcha.com/in.php?key={}&method=userrecaptcha&googlekey={}&pageurl={}".format(API_KEY, data_sitekey, url)).text.split('|')[1]
    recaptcha_answer = s.get("http://2captcha.com/res.php?key={}&action=get&id={}".format(API_KEY, captcha_id)).text
    print_white(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\tSolving Ref Captcha...")
    start_time = time.time()
    while 'CAPCHA_NOT_READY' in recaptcha_answer:
        t = time.time()-start_time
        if t>=60:
            print_red(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\t获取验证码超过1分钟，跳过")
            return
        time.sleep(5)
        recaptcha_answer = s.get("http://2captcha.com/res.php?key={}&action=get&id={}".format(API_KEY, captcha_id)).text
    recaptcha_answer = recaptcha_answer.split('|')[1]
    print_white(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\tCaptcha Res: "+recaptcha_answer)
    driver.execute_script('$("#g-recaptcha-response").val("{}")'.format(recaptcha_answer)) 
    time.sleep(3)
    driver.find_element_by_id("j_id0:CommunitiesTemplateEngage:appFrm:btnNext").click()
    time.sleep(10)
    print_white(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\tGo Next...")
    time.sleep(6)

    if not "Promotion Signup" in driver.find_element_by_tag_name("body").text:
        print_white(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\tSuccess...")
    else:
        print_white(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\tFail...")


def arg_parser():
    parser = argparse.ArgumentParser(description='For AWS')
    parser.add_argument('--profile', '-profile', metavar="字段文件", required=True)
    parser.add_argument('--proxyfile', '-proxyfile', metavar="代理文件", required=True)
    args = parser.parse_args()
    return args
       

def print_red(msg):
    print("\033[1;31m "+msg+"\033[0m")

def print_yellow(msg):
    print("\033[1;32m "+msg+"\033[0m")

def print_blue(msg):
    print("\033[1;36m "+msg+"\033[0m")

def print_white(msg):
    print("\033[0;38m "+msg+"\033[0m")

def main():
    args = arg_parser()
    profilepath = args.profile
    proxyfilepath = args.proxyfile

    with open(profilepath) as f:
        i = 0
        csv_rows = csv.reader(f)
        headings = next(csv_rows)
        Row = namedtuple('Row', headings)
        for r in csv_rows:
            i = i+1
            print_yellow(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\tIndex: "+str(i))

            ua = UserAgent()
            user_agent = ua.random
            opts = FirefoxOptions()
            opts.add_argument("--headless")
            opts.add_argument('user-agent=%s'%user_agent)

            proxy=pd.read_csv(proxyfilepath,header=None).values.tolist()
            size = len(proxy)-1
            idx = random.randint(1,size)
            p = proxy[idx]
            ip = proxy[idx][0]
            port = proxy[idx][1]

            firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
            firefox_capabilities['marionette'] = True
            PROXY = ip+":"+port
            firefox_capabilities['proxy'] = {
                "proxyType": "MANUAL",
                "httpProxy": PROXY,
                "ftpProxy": PROXY,
                "sslProxy": PROXY
            }
            # pf = FirefoxProfile()
            # pf.set_preference("network.proxy.type", 1)
            # pf.set_preference("network.proxy.http", ip)
            # pf.set_preference("network.proxy.http_port", port)
            # pf.set_preference("network.proxy.http", ip)
            # pf.set_preference("network.proxy.http_port", port)
            # pf.set_preference("network.proxy.share_proxy_settings", True)
            driver = Firefox(capabilities=firefox_capabilities,firefox_options=opts)

            counrty = r[0]
            city = r[1]
            school = r[2]
            email = r[3]
            fn = r[4]
            ln = r[5]
            bm = r[6]
            by = r[7]
            cm = r[8]
            cy = r[9]
            url = r[10]
            
            # go_sign(driver,counrty,city,email,school,fn,ln,bm,by,cm,cy)

            try:
                go_sign(driver,counrty,city,email,school,fn,ln,bm,by,cm,cy,url)
                driver.close()
                driver.quit()
                
            except Exception as e:
                # print(e)
                print_red(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())+"\t报错,跳过")
                driver.close()
                driver.quit()
                continue
            # finally:
            #     driver.close()
            #     driver.quit()


if __name__ == "__main__":
    main()