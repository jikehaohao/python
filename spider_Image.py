#coding:utf-8

import urllib.parse
import urllib2
import socket
import ssl
import re
import requests
import threading

####设置最大线程锁 一次接收20个线程
thread_lock=threading.BoundedSemaphore(value=20)

###通过url获取数据
def get_page(url):
    page = requests.get(url)
    page=page.content
    ###将bytes转成字符串
    page=page.decode('utf-8')
    return page

## label  '校花'
def pages_from_duitang(label):
    pages=[]
    url='https://www.duitang.com/napi/blog/list/by_search/?kw={}&start={}&limit=1000'
    ###将中文转换呈url编码
    label=urllib.parse.quote(label)
    for index in range(0,3600,100):
        u=url.format(label,index)
        print(u)
        page=get_page(u)
        pages.append(page)
    return pages


def findall_in_page(page,startpart,endpart):
    all_strings=[]
    end=0
    while page.find(startpart,end)!=-1:
        start=page.find(startpart,end)+len(startpart)
        end=page.find(endpart,start)
        string=page[start:end]
        all_strings.append(string)
    return all_strings

def pic_urls_from_pages(pages):
    pic_urls=[]
    for page in pages:
        urls=findall_in_page(page,'path":"','"')
        pic_urls.extend(urls)
    return pic_urls

def download_pics(url):
    r=requests.get(url)
    path='../memory/pics/'+str(n)+'.jpg'
    with open(path,'wb') as f:
        f.write(r.content)
    ##下载完以后解锁
    thread_lock.release()

def main(label):
    pages=pages_from_duitang(label)
    pic_urls=pic_urls_from_pages(pages)
    n=0
    for url in pic_urls:
        n+=1
        print('正在下载第{}张图片'.format(n))
        ###上锁
        thread_lock.acquire()
        t=threading.Thread(target=download_pics,args=(url,n))
        t.start()

main('校花')
