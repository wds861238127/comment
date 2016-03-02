# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 10:51:25 2016
@author: wds
"""
import sys
import os
import urllib2
from bs4 import BeautifulSoup
import json
import pandas as pd

# 配置utf-8输出环境
reload(sys)
sys.setdefaultencoding('utf-8')

path=r'C:\Users\wds\Desktop\pinglun\save\project_0\output\comment\\'
path1=r'C:\Users\wds\Desktop\pinglun\save\project_0\output\summarize\\'
path2=r'C:\Users\wds\Desktop\pinglun\save\project_0\output\statistics'

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
        newfile=path+"\\need"+str(lastnu)+".csv"
        f=open(newfile,'w')#a
    else:
        newfile=path+"\\need0.csv"
        f=open(newfile,'w')#a
    f.close()
    return newfile


def Search_Taobao_Sorted(key,number):
#    search_key_url='https://s.taobao.com/search?data-key=sort&data-value='+str(number)+'&ajax=true&_ksTS=1447937523209_913&callback=jsonp914&q='+key+'&imgfile=&ie=utf8'
    search_key_url='https://s.taobao.com/search?q='+key+'&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.7724922.8452-taobao-item.2&ie=utf8&initiative_id=tbindexz_20151119&sort=sale-desc&bcoffset=0&data-key=s&data-value='+str(number)
    page= urllib2.urlopen(search_key_url).read()
    return page

def Explian_Page_Taobao(page):
    soup=BeautifulSoup(page)
    find_script=soup.findAll("script")
    tmp=str(find_script[5])
    a=tmp[37:-11].splitlines()
    # print a[0]
    s=json.loads(a[0][:-1])
    return s

#https://item.taobao.com/item.htm?id=44413300557&ns=1&abbucket=0&on_comment=1

def Open_Comment_Url(itemId,sellerId,tm_or_tb,pageNu):
    if tm_or_tb==1:#tianmao
        link='https://rate.tmall.com/list_detail_rate.htm?itemId='+str(itemId)+'&sellerId='+str(sellerId)+'&order=1&currentPage='+str(pageNu)+'&append=0&content=1&tagId=&posi=&picture=&callback=jsonp2073'
    else:
        link='https://rate.taobao.com/feedRateList.htm?auctionNumId='+str(itemId)+'&userNumId='+str(sellerId)+'&currentPageNum='+str(pageNu)+'&pageSize=20&rateType=&orderType=feedbackdate&showContent=1&attribute=&folded=0&callback=jsonp_tbcrate_reviews_list'
#             'https://rate.taobao.com/feedRateList.htm?auctionNumId=521026620896&userNumId=2609505071&currentPageNum=1&pageSize=20&rateType=&orderType=feedbackdate&showContent=1&attribute=&folded=0&callback=jsonp_tbcrate_reviews_list
    print link
    page= urllib2.urlopen(link).read().decode('gbk')
    return page

def action(nid,seller):
    nu=1
    while nu<100:
        try:
            soup=Open_Comment_Url(nid,seller,1,nu)
            n=1
            while len(soup)<1000 and n<100:
                print "---------------",n
                soup=Open_Comment_Url(nid,seller,1,nu)
                n+=1
            s=json.loads(soup[15:-1])
            s1=pd.DataFrame(s)
            s2=s1.loc['rateCount','rateDetail']
            s3=s2.values()#keys("total","picNum","used")
            ss=pd.DataFrame(s['rateDetail']['rateList'])
        #    ss1=pd.DataFrame(ss['rateDetail']['rateCount'])
        #    ss2=pd.DataFrame(ss['rateDetail']['rateList'])
        #    print ss1[['position','rateContent','serviceRateContent','rateDate','tradeEndTime','buyCount','displayRateSum','tamllSweetLevel']]
        #    print ss1["total"]
            ss[["id","sellerId","reply","tamllSweetLevel","displayUserNick","cmsSource","auctionSku","rateDate","rateContent","appendComment"]].to_csv(path+str(nid)+'.csv',sep='\t',header=False,index=False,mode='a')
        #    os.system('pause')
        #    output=Check_Json_Key(s,need_comment_list)
            print "=======================================",nu
        except:pass
        nu+=1

def main(request):
    print request
    page=Search_Taobao_Sorted(request,str(1))
    s=Explian_Page_Taobao(page)
    ss=pd.DataFrame(s)  
    sss=pd.DataFrame(ss['mods']["itemlist"])
    sss1=pd.DataFrame(sss.loc['auctions','data'])
    itemlist=sss1[['nid','user_id','category','comment_count','raw_title','item_loc','nick','pid','view_price','view_sales']]
    itemlist.to_csv(path1+request+'.csv',sep='\t',header=True,index=True,mode='a')
    for i in itemlist.index:
        print itemlist['raw_title'][i]
        nid=itemlist['nid'][i]
        seller=itemlist['user_id'][i]
        action(nid,seller)
        
main(u'围巾')



