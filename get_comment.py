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
import pandas as pd

sys.path.append("..")
from mysql_function import Connet_mysql
# 配置utf-8输出环境
reload(sys)
sys.setdefaultencoding('utf-8')

path=r'C:\Users\wds\Desktop\pinglun\save\project_0\output\comment'
def Check_exist_txt(path):
    dir_list = os.listdir(path)
    if dir_list:
        sortedlist=[]
        for item in dir_list:
            sortedlist.append(int(item[4:-4]))
        print sortedlist
        last=int(sortedlist[0])
        for item in sortedlist:
            if int(item)>last:
                last=int(item)
            else:
                pass
        lastnu=last+1
        newfile=path+"\\need"+str(lastnu)+".txt"
        f=open(newfile,'w')#a
    else:
        newfile=path+"\\need0.txt"
        f=open(newfile,'w')#a
    f.close()
    return newfile
newfile=Check_exist_txt(path)

def Write_Txt(path,content):
        f=open(path,'a')#a
        f.write(content)
        f.write('\n')
        f.close()

#def Open_Url(url):
#    page= urllib2.urlopen(url).read()
#    print page
#Open_Url(url)
need_item_list=["nid","raw_title","nick","item_loc","user_id","view_price","view_sales","comment_count"]
#need_comment_list=["id","picNum","total","used","tamllSweetLevel","displayUserNick","rateContent","rateDate","auctionSku"]
need_comment_list=["id","displayUserNick","tamllSweetLevel","rateContent","rateDate"]

url='https://rate.tmall.com/list_detail_rate.htm?itemId=42466032716&spuId=313233987&sellerId=705069785&order=1&currentPage=2&append=0&content=0&tagId=&posi=&picture=&callback=jsonp2073'
#tm='https://rate.tmall.com/list_detail_rate.htm?itemId='+str(itemId)+'&sellerId='+str(sellerId)+'&order=1&currentPage='+str(pageNu)+'&append=0&content=0&tagId=&posi=&picture=&callback=jsonp2073'
#tb='https://rate.taobao.com/feedRateList.htm?auctionNumId='+str(itemId)+'&userNumId='+str(sellerId)+'&currentPageNum='+str(pageNu)+'&pageSize=20&rateType=&orderType=feedbackdate&showContent=&attribute=&folded=0&callback=jsonp_tbcrate_reviews_list'
def Open_Comment_Url(itemId,sellerId,tm_or_tb,pageNu):
    if tm_or_tb==1:#tianmao
        link='https://rate.tmall.com/list_detail_rate.htm?itemId='+str(itemId)+'&sellerId='+str(sellerId)+'&order=1&currentPage='+str(pageNu)+'&append=0&content=1&tagId=&posi=&picture=&callback=jsonp2073'
    else:
        link='https://rate.taobao.com/feedRateList.htm?auctionNumId='+str(itemId)+'&userNumId='+str(sellerId)+'&currentPageNum='+str(pageNu)+'&pageSize=20&rateType=&orderType=feedbackdate&showContent=1&attribute=&folded=0&callback=jsonp_tbcrate_reviews_list'
#             'https://rate.taobao.com/feedRateList.htm?auctionNumId=521026620896&userNumId=2609505071&currentPageNum=1&pageSize=20&rateType=&orderType=feedbackdate&showContent=1&attribute=&folded=0&callback=jsonp_tbcrate_reviews_list
    print link
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

def Check_Json_Key(s,key):
    if type(s)==dict:
        for (k,v) in s.items():
#            print type(k),type(v)
#            print k,key
            if k in key:
                if k in need_comment_list:
                    print k,s[k]
#                    Write_Txt(newfile,s[k].encode("gbk"))
#                    Write_Txt(newfile,s[k])
            else:
                Check_Json_Key(k,key)
                Check_Json_Key(v,key)
    elif type(s)==list:#或者 if isinstance(jdict, list):
        for item in s:
            Check_Json_Key(item,key)
    else :
        pass

nu=1
while nu<2:#44413300557,768773870#520227142245,2228333954
    soup=Open_Comment_Url(44413300557,768773870,1,nu)
    n=1
    while len(soup)<1000 and n<100:
        print "---------------",n
        soup=Open_Comment_Url(44413300557,768773870,1,nu)
        n+=1
#        print soup
    s=json.loads(soup[15:-1])
#    print s
    ss=pd.DataFrame(s)
#    ss1=pd.DataFrame(ss['rateDetail']['rateCount'])
    ss2=pd.DataFrame(ss['rateDetail']['rateList'])
#    print ss1[['position','rateContent','serviceRateContent','rateDate','tradeEndTime','buyCount','displayRateSum','tamllSweetLevel']]
#    print ss1["total"]
    print ss2[["id","sellerId","auctionSku","cmsSource","displayUserNick","rateContent","rateDate","reply","tamllSweetLevel"]]
#    os.system('pause')
#    output=Check_Json_Key(s,need_comment_list)
    print "=======================================",nu
    nu+=1
