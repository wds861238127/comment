# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 22:34:59 2015
@author: wds
"""
import sys
import os
import urllib2
from bs4 import BeautifulSoup
import json
sys.path.append("..")
from mysql_function import Connet_mysql

  
def Write_Txt(path,content):
        f=open(path,'a')#a
        f.write(content)
        f.write('\n')
        f.close()
        
need_item_list=["nid","raw_title","nick","item_loc","user_id","view_price","view_sales","comment_count"]
need_comment_list=["id","tamllSweetLevel","displayUserNick","rateContent","rateDate","auctionSku"]
#need_comment_list=["displayUserNick","rateContent","rateDate"]

url='https://rate.tmall.com/list_detail_rate.htm?itemId=42466032716&spuId=313233987&sellerId=705069785&order=1&currentPage=2&append=0&content=0&tagId=&posi=&picture=&callback=jsonp2073'
#tm='https://rate.tmall.com/list_detail_rate.htm?itemId='+str(itemId)+'&sellerId='+str(sellerId)+'&order=1&currentPage='+str(pageNu)+'&append=0&content=0&tagId=&posi=&picture=&callback=jsonp2073'
#tb='https://rate.taobao.com/feedRateList.htm?auctionNumId='+str(itemId)+'&userNumId='+str(sellerId)+'&currentPageNum='+str(pageNu)+'&pageSize=20&rateType=&orderType=feedbackdate&showContent=&attribute=&folded=0&callback=jsonp_tbcrate_reviews_list'
def Open_Comment_Url(itemId,sellerId,tm_or_tb,pageNu):
    if tm_or_tb==1:#tianmao
        link='https://rate.tmall.com/list_detail_rate.htm?itemId='+str(itemId)+'&sellerId='+str(sellerId)+'&order=1&currentPage='+str(pageNu)+'&append=0&content=1&tagId=&posi=&picture=&callback=jsonp2073'
    else:
        link='https://rate.taobao.com/feedRateList.htm?auctionNumId='+str(itemId)+'&userNumId='+str(sellerId)+'&currentPageNum='+str(pageNu)+'&pageSize=20&rateType=&orderType=feedbackdate&showContent=1&attribute=&folded=0&callback=jsonp_tbcrate_reviews_list'
#             'https://rate.taobao.com/feedRateList.htm?auctionNumId=521026620896&userNumId=2609505071&currentPageNum=1&pageSize=20&rateType=&orderType=feedbackdate&showContent=1&attribute=&folded=0&callback=jsonp_tbcrate_reviews_list
    page= urllib2.urlopen(link).read().decode('gbk')
    return page

def Search_Taobao_Sorted(key,number):
#    search_key_url='https://s.taobao.com/search?data-key=sort&data-value='+str(number)+'&ajax=true&_ksTS=1447937523209_913&callback=jsonp914&q='+key+'&imgfile=&ie=utf8'
    search_key_url='https://s.taobao.com/search?q='+key+'&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.7724922.8452-taobao-item.2&ie=utf8&initiative_id=tbindexz_20151119&sort=sale-desc&bcoffset=0&data-key=s&data-value='+str(number)   
    page= urllib2.urlopen(search_key_url).read()
    return page

def Explian_Page_Taobao(page):
    soup=BeautifulSoup(page)
    find_script=soup.findAll("script")
#    print type(find_script[4].string)
    tmp=find_script[4].string
    return tmp.split('\n')[2][20:-1]

def Insert_mysql(s,cur):
    rateList=s['rateDetail']['rateList']
    for item in rateList:
        insert_list=[item['id'],item['displayUserNick'].encode('utf-8'),item['rateContent'].encode('utf-8'),item['rateDate'],item['tamllSweetLevel'],item['auctionSku']]
#        insert_list=[item['id'],'wda','dawd','dawda',2,'dsad']
#        print insert_list
        cur.execute("insert into two values(%s,%s,%s,%s,%s,%s)",insert_list)
#        print "--------------------------insert one"
def wds():
    creat_table="create table if not exists two (id varchar(100),displayUserNick varchar(100),rateContent varchar(1000),rateDate varchar(100),tamllSweetLevel int,auctionSku varchar(100))"
    conn,cur=Connet_mysql()
    cur.execute("create database if not exists taobao")
    cur.execute("use taobao")
    cur.execute(creat_table)
    nu=1
    while nu<100:
        soup=Open_Comment_Url(522207064310,2162402754,1,nu)
        n=1
        while len(soup)<1000 and n<100:
            print "---------------",n
            soup=Open_Comment_Url(522207064310,2162402754,1,nu)
            n+=1   
        s=json.loads(soup[15:-1]) 
        Insert_mysql(s,cur)
        print "=======================================",nu
        nu+=1
    conn.commit()
    cur.close()
    conn.close() 
wds()
    
    
    
    
    
    