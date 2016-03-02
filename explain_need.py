# -*- coding: utf-8 -*-
import operator
import sys  
import os 
import jieba
import nltk 

# 配置utf-8输出环境
reload(sys)
sys.setdefaultencoding('utf-8')

#从文件导入停用词表
def Open_stopword():
    stpwrdpath = "C:\\Users\\wds\\Desktop\\pinglun\\nlp\\code\\data\\stop_word.txt"
    stpwrd_dic = open(stpwrdpath, 'rb')
    stpwrd_content = stpwrd_dic.read().decode("gbk")
    #将停用词表转换为list  
    stop_word_list = stpwrd_content.splitlines()
    stpwrd_dic.close()
    return stop_word_list

def  Customize_del_word(stop_word_list):
    customize_list_path=r'C:\Users\wds\Desktop\pinglun\save\project_0\custom_del_word\del_word.txt'
    stpwrd_dic = open(customize_list_path, 'rb')
    stpwrd_content = stpwrd_dic.read().decode("gbk")
    customize_list = stpwrd_content.splitlines()
#    print len(stop_word_list)
    stop_word_list.extend(customize_list)
#    for item in customize_list:
#        stop_word_list.append(item)     
#    print len(stop_word_list)
    return stop_word_list

path=r'C:\Users\wds\Desktop\pinglun\save\project_0\output\statistics'
def Check_exist_txt(path):
    dir_list = os.listdir(path)
    if dir_list:
        sortedlist=[]
        for item in dir_list:
            sortedlist.append(int(item) )  
        print sortedlist
        last=int(sortedlist[0])
        for item in sortedlist:
            if int(item)>last:
                last=int(item)
            else:
                pass
        lastnu=last+1 
        newfile=path+"\\"+str(lastnu)
        os.makedirs(newfile)
    else:
        newfile=path+"\\0"
        os.makedirs(newfile)
    return newfile


pos_path=r"C:\Users\wds\Desktop\pinglun\save\project_0\output"
def Data_clean(pos_path):
    dir_list = os.listdir(pos_path)
    # 获取每个目录下所有的文件
    for mydir in dir_list:
            class_path = pos_path+"/"+mydir+"/" # 拼出分类子目录的路径
            file_list = os.listdir(class_path)  # 获取class_path下的所有文件
            for file_path in file_list:   # 遍历所有文件
                    newdir=Check_exist_txt(path)
                    file_name = class_path + file_path  # 拼出文件名全路径
                    file_read = open(file_name, 'rb')   # 打开一个文件
                    raw_corpus = file_read.read()# 读取未分词语料
                    corpus_array = raw_corpus.splitlines()
                    raw_corpus = ""
                    file_write = open (newdir+"\\jieba.txt", 'w' )
                    for line in corpus_array:
                        line=line.strip()
                        seg_corpus = jieba.cut(line)  # 结巴分词操作
                        file_write.write(" ".join(seg_corpus))#用空格将分词结果分开并写入到分词后语料文件中
                        file_write.write("\n")
                    file_read.close()  #关闭打开的文件
                    file_write.close()  #关闭写入的文件
                    print "中文语料分词成功完成！！！"
                    Del_stopword(newdir)
                    word_dict,length=Count_term(newdir)
                    Count_dict_dif(newdir,word_dict,length)
#导入训练集

def Del_stopword(newdir):
    file_read = open(newdir+"\\jieba.txt", 'rb')   # 打开一个文件
    raw_corpus = file_read.read()# 读取未分词语料
    corpus_array = raw_corpus.splitlines()
    raw_corpus = ""
    file_write = open (newdir+"\\stopdel.txt", 'w' )
    for line in corpus_array:
        listword=line.split(" ")
        for word in listword:
            if word in stpwrdlst:
#                print "-------no",word
                pass
            else:
#                print "-------ok",word
                file_write.write(word)
                file_write.write(" ")
        file_write.write("\n")
    file_write.close()
 
def Count_word(newdir):
    file_read = open(newdir+"\\stopdel.txt", 'rb')   # 打开一个文件
    raw_corpus = file_read.read().decode("gbk")
    fredist=nltk.FreqDist(raw_corpus)
#    print fredist
    return fredist


def Count_term(newdir):
    word_lst = []
    word_dict = {}
    output=[]
    with open(newdir+"\\stopdel.txt","r") as f1 ,open(newdir+"\\count_dict.txt",'w') as f2:
        for line in f1:
            word_lst.append(line.split(' '))
        for item in word_lst:
           for item2 in item:
               if item2.strip() not in "，！。“”" :
                   if   item2 not in word_dict:
                       word_dict[item2] = 1
                   else :
                       word_dict[item2] += 1
        sortword_dict = sorted(word_dict.iteritems(), key=operator.itemgetter(1), reverse=True)               
        for item in sortword_dict:
            tmp=list(item)
            output.append(tmp)
        for item in output:
#            print item[0].decode("utf-8"),item[1]
            f2.write(str(item[0].decode("utf-8"))+':'+str(item[1])+"\n")
        print len(output)
        return word_dict,len(output)

def Count_dict_dif(newdir,word_dict,length):
    count={}
    for item in word_dict.values():
        if item not in count.keys():
            count[item]=0
        count[item]+=1
    sortcount = sorted(count.iteritems(), key=operator.itemgetter(0), reverse=True)
    file_write = open (newdir+"\\statistics.txt", 'w' )
    file_write.write("total:"+str(length)+" word !!! ")
    file_write.write("\n")    
    for item in sortcount:
        file_write.write(str(item))
        file_write.write("\n")
    file_write.close()
    print sortcount
    
    
stop_word_list=Open_stopword()
stpwrdlst=Customize_del_word(stop_word_list)  
Data_clean(pos_path)


 