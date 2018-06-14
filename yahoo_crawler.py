
# coding: utf-8

# In[ ]:


#please set how many category you want to crawl

category = 5

import requests
import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import sqlite3 as lite
engine = lite.connect('db.sqlite3')


# In[ ]:


def check_contain_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fa5':
            return True
    return False


# In[ ]:


def crawl_category_list():
    HOST = 'https://tw.buy.yahoo.com'
    res = requests.get(HOST+'/help/helper.asp?p=sitemap')
    res.encoding = 'big5'
    soup = BeautifulSoup(res.text,'lxml')
    a_tag = soup.select('#cl-sitemap a')
    category = []
    href = []
    for a in a_tag:
        category.append(a.text)
        href.append(HOST+a['href'])
    df_category = pd.DataFrame(columns=['category','url'])
    df_category['category'] = category
    df_category['url'] = href
    df_category = df_category[df_category['url'].str.contains('sub')]
    return df_category


# In[ ]:


df_category = crawl_category_list()
print('測試 category crawler')


# In[ ]:


df_category.to_sql('yahoo_category', con=engine, if_exists='append', index=False)
cur = engine.cursor()
cur.execute('SELECT * FROM yahoo_category;').fetchall()
print('產品類別清單已爬取')

# In[ ]:


def crawl_product_list(category_url):
    res = requests.get(category_url)
    soup = BeautifulSoup(res.text,'lxml')
    a_tag = soup.select("a")
    href = []
    for a in a_tag:
        try:
            test = a['href']
            href.append(a['href'])
        except KeyError as e:
            pass
    df_products = pd.DataFrame(columns=['product_title','url'])
    df_products['url'] = href

    #取出為商品頁的連結
    chinese = []
    for i in range(0,len(df_products)):
        chinese.append(check_contain_chinese(df_products.loc[i]['url']))
    product_list = df_products[chinese].url.unique()
    return product_list


# In[ ]:


product_list = crawl_product_list(df_category.loc[1]['url'])
print('測試單一類別產品清單crawler')


# In[ ]:


def crawl_product(product_url,category,position):
    try:
        res = requests.get(product_url)
        soup = BeautifulSoup(res.text,'lxml')
        price = soup.select('.price')
        real_price = -1
        try:
            title = soup.select('h1')[0].text
        except:
            title = '產品名稱無法抓取'
        for p in price:
            try:
                real_price = int(p['content'])
            except KeyError as e:
                pass
        product = [title,category,real_price,position,product_url]
        return product
    except:
        pass


# In[ ]:


product = crawl_product(product_list[0],df_category.loc[1]['category'],0)
print('測試產品crawler')


# In[ ]:


def get_all_category_product(category_title, category_url):
    df_category_products = pd.DataFrame(columns=['product','category','price','position','url'])
    product_list = crawl_product_list(category_url)
    for idx, product_url in enumerate(product_list):
        df_category_products.loc[idx] = crawl_product(product_url,category_title,idx)
    return df_category_products


# In[ ]:


category_list = crawl_category_list()


# In[ ]:


for i in range(0,category):
    df_category_products = get_all_category_product(category_list.loc[i+1]['category'],category_list.loc[i+1]['url'])
    df_category_products.to_sql('yahoo_product', con=engine, if_exists='append', index=False)
    print(category_list.loc[i+1]['category'])
    print('-------------此類別爬取完畢---------------')
