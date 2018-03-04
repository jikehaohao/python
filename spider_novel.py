#!/usr/bin/env python
#coding:utf-8

import requests
import re
import io
import time
##模拟浏览器区访问网址
header={
    'User-Agent':'Mozilla/5.0 (Windows NT 6.1;WOW64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/58.0.3029.96 Safari/537.36'
}

###模拟虚拟ip去访问网址，防封ip
def use_proxy(proxy_addr,url):
    proxy=urllib.ProxyHandler({'http':proxy_addr})
    opener=urllib.build_opener(proxy,urllib.request.HTTPHandler)
    urllib.install_opener(opener)
    data=urllib.urlopen(url).read().decode('utf8')
    return data
    proxy_addr='61.163.39.70:9999'
    data=use_proxy(proxy_addr,html)
    print(len(data))


##防止被网站ban掉
def getCode(html):
    error_time = 0
    while True:
        time.sleep(1)
        try:
            firline=urllib.urlopen("http://www.jingcaiyuedu.com/book/15205.html")
            data=firline.read()
            fhandle=open("../Desktop/无上真仙.txt",'wb')
            fhandle.write(data)
            fhandle.close()
        except Exception as ex:
            print ex
            error_time += 1
            if error_time == 100:
                print 'your network is little bad'
                time.sleep(60)
                if error_time == 101:
                    print 'your network is broken'
                    break
                continue
            break

def download_html(url):
    #模拟发送http请求
    response=requests.get(url)
    #字符编码
    response.encoding='utf-8'
    return response.text 

#获取小说的章节数据
def get_chapter_info(url):
    html=download_html(url)
    #获取小说的名称
    title=re.findall(r'<meta property="og:title" content="(.*?)"/>',html)[0]
    #获取小说的数据 章节内容
    dl=re.findall(r'<dl id="list">.*?</dl>',html,re.S)[0]
    chapter_info_list=re.findall(r'hre="(.*?)">(.*?)',dl)
    return title,chapter_info_list


##获取小说的内容
def get_chapter_content(chapter_url):
    html=download_html(chapter_url)
    #提取章节内容
    chapter_content=re.findall(r'<script>a1\(\);</script>(.*?)<script>a2\(\)</script>',html,re.S)[0]
    #清洗数据
    chapter_content=chapter_content.replace(' ','')
    chapter_content=chapter_content.replace('&nbsp','')
    chapter_content=chapter_content.replace('<br/>','')
    chapter_content=chapter_content.replace(';','')
    return chapter_content



##小说内容的主函数入口
def spider(url):
    novel_title,chapter_info_list=get_chapter_info(url)
    f=io.open('%s.txt'%novel_title,'w',encoding='utf-8')
    for chapter_url,chapter_title in chapter_info_list:
        chapter_url='http://www.jingcaiyuedu.com%s'%chapter_url
        chapter_content=get_chapter_content(chapter_url)
        f.write(chapter_title)
        f.write(chapter_content)
        f.write('\n')
        print(chapter_url)
        f.close()

if __name__=='__main__':
    novel_url='http://www.jingcaiyuedu.com/book/15205.html'
    spider(novel_url)


