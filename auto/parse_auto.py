#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 11:23:54 2022

@author: honepa
"""

import requests as req
from time import sleep
from random import random
from user_agent import generate_user_agent
from bs4 import BeautifulSoup
from PIL import Image
import json
import os
import csv
from datetime import datetime 
import re

start_time = datetime.now()

data_auto = []
auto_first_line = ["auto_id", "auto_url", "phone_num", "city", "auto name",  "auto description", "foto"]
data_auto.append(auto_first_line)

second = []
auto_id_list = []
"""
r = req.get("https://autosakhcom.ru/sales/auto/?page=1", headers = {'User_Agent' : generate_user_agent()})
second.append(r.elapsed.total_seconds())
soup = BeautifulSoup(r.text, 'html.parser')
page = soup.find_all('a', {"class" : "pager-widget__page"})
page_count = int(page[6].text)
auto_url = soup.find_all('div',{"property" : "itemListElement"})
del soup

for i in range(len(auto_url)):
    auto_id = auto_url[i].div.get("data-id")
    auto_id_list.append(auto_id)
sleep(random())

for i in range(2, page_count + 1):
    r = req.get(f"https://autosakhcom.ru/sales/auto/?page={i}", headers = {'User_Agent' : generate_user_agent()})
    soup = BeautifulSoup(r.text, 'html.parser')
    auto_url = soup.find_all('div',{"property" : "itemListElement"})
    for i in range(len(auto_url)):
        auto_id = auto_url[i].div.get("data-id")
        auto_id_list.append(auto_id)
    sleep(random())
    second.append(r.elapsed.total_seconds())
    del soup
print(sum(second))
print(len(auto_id_list))
"""
"""
r = req.get("https://autosakhcom.ru/sales/auto/?page=1", headers = {'User_Agent' : generate_user_agent()})
with open('test_auto.html', 'w', encoding='utf-8') as f:
    f.write(r.text)
print(r.elapsed.total_seconds())

"""
r = req.get("https://autosakhcom.ru/sales/auto/?page=1", headers = {'User_Agent' : generate_user_agent()})
#file = open('test_auto.html', 'r')
#text = file.read()
#file.close()
soup = BeautifulSoup(r.text, 'html.parser')
auto_url = soup.find_all('div',{"property" : "itemListElement"})

auto_id_list = []
auto_url_list = []
page = soup.find_all('a', {"class" : "pager-widget__page"})
page_count = int(page[6].text)

for i in range(len(auto_url)):
    auto_id = auto_url[i].meta.get("content")
    auto_url_list.append(auto_id)
    auto_id = auto_url[i].div.get("data-id")
    auto_id_list.append(auto_id)
"""
r = req.get(f"https://autosakhcom.ru/sale/{auto_id_list[0]}/?index=0")
with open('auto_index.html', 'w', encoding='utf-8') as f:
    f.write(r.text)
f.close()
"""
for i in range(len(auto_id_list)):
    now_auto = []
    now_auto.append(auto_id_list[i])
    now_auto.append(auto_url_list[i])
    try:
        r = req.get(f"https://autosakhcom.ru/ajax/sale/getPhone/?sale_id={auto_id_list[i]}", headers = {'User_Agent' : generate_user_agent()}) 
        data = json.loads(r.text)
        phone_num = data.get('data').get('phone')
        phone_num = "".join([i for i in re.findall(r'\d+', phone_num)]) 
        now_auto.append(phone_num)
        print(phone_num)
        sleep(random())
    except Exception as e:
        print(e)
        if phone_num > 0:
            now_auto.append(phone_num)
        else:
            now_auto.append("не удалось получить номер")
    print(f"{auto_url_list[i]}/?index=0")
    try:
        r = req.get(f"{auto_url_list[i]}", headers = {'User_Agent' : generate_user_agent()})
        sleep(random())
    except Exception as e:
        print(e)
        pass
    soup = BeautifulSoup(r.text, 'html.parser')
    city = soup.find_all('div', {'class' : 'sale-property'})
    city = city[-1].find('span', class_='sale-property-value').text
    now_auto.append(city)
    print(city)
    auto_name = soup.find_all('a', {"href" : f"/sale/{auto_id_list[i]}/"})
    auto_name = auto_name[1].text
    auto_name = " ".join(auto_name.split())
    now_auto.append(auto_name)
    print(auto_name)
    try:
        auto_description = soup.find_all('div', {'class' : "sale-text"})
        auto_description = auto_description[0].find('div', class_ = 'text').text
        now_auto.append(auto_description)
        print(auto_description)
    except Exception as e:
        print(e)
        now_auto.append("not description")
    """
    auto_img = soup.find_all('img', {"alt" : str(auto_name)})
    os.mkdir(f"photo/{auto_id_list[i]}")
    print(f"photo/{auto_id_list[i]}")
    foto_sline = str()
    for j in range(1, len(auto_img)):
        img_url = str(auto_img[j].get("src"))
        img_url = img_url.replace("/sm/", "/md/")
        img = req.get(img_url, headers = {'User_Agent' : generate_user_agent()})
        test_out_img = open("test.webp", 'wb')
        test_out_img.write(img.content)
        test_out_img.close()
        
        im = Image.open("test.webp").convert("RGB")
        im.save(f"photo/{auto_id_list[i]}/car_{auto_id_list[i]}_{j}.jpg", "jpeg")
        foto_sline += f"photo/{auto_id_list[i]}/car_{auto_id_list[i]}_{j}.jpg, "
        sleep(random())
    """
    now_auto.append("phone")        
    #now_auto.append(foto_sline)
    data_auto.append(now_auto)
    del now_auto

with open("parse_auto.csv", "w", newline="") as file: 
    writer = csv.writer(file) 
    writer.writerows(data_auto)
    
print(datetime.now() - start_time)

"""
file = open('/tmp/auto_touota.html', 'r')
text = file.read()
file.close()
soup = BeautifulSoup(text, 'html.parser')
os.mkdir("test")
"""
"""
#get city
city = soup.find_all('div', {'class' : 'sale-property'})
city = city[7].find('span', class_='sale-property-value').text
"""
"""
#get phone number
#can not get ok == true
r = req.get(f"https://autosakhcom.ru/ajax/sale/getPhone/?sale_id={auto_id_list[0]}", headers = {'User_Agent' : generate_user_agent()}) 
data = json.loads(r.text)
phone_num = data.get('data').get('phone')
print(phone_num)
"""
"""
#get auto description
auto_description = soup.find_all('div', {'class' : "sale-text"})
auto_description = auto_description[0].find('div', class_ = 'text').text
print(auto_description)
"""
"""
#get photo
auto_img = soup.find_all('img', {"alt" : "Toyota Granvia, 2001"})
for i in range(1, len(auto_img)):
    img_url = str(auto_img[i].get("src"))
    img_url = img_url.replace("/sm/", "/md/")
    img = req.get(img_url, headers = {'User_Agent' : generate_user_agent()})
    test_out_img = open("test.webp", 'wb')
    test_out_img.write(img.content)
    test_out_img.close()

    im = Image.open("test.webp").convert("RGB")
    im.save(f"test_car_{i}.jpg", "jpeg")
    sleep(random())

del im
"""
"""
#get auto name
auto_name = soup.find_all('a', {"href" : "/sale/1614161/"})
auto_name = auto_name[1].text
auto_name = " ".join(auto_name.split())
print(auto_name)
"""
"""
seconds3= []
r = req.get("https://s.sakh.name/i/lg/auto/sales/16/11/1611803/n1611803_20220929222440_456441fb.webp", 
            headers = {'User_Agent' : generate_user_agent()}) 
if r.status_code == 200: 
    seconds3.append(r.elapsed.total_seconds()) 
else: 
    print('%d ----=----- %d'%(r.status_code)) 
    print('%d ----=----- %d'%(r.elapsed.total_seconds())) 
sleep(random()) 
"""
