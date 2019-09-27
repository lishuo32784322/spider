import os
import re
import time
import shutil
import requests
import hashlib
import urllib.request
from requests.adapters import HTTPAdapter
from xml.dom.minidom import parseString
from moviepy.editor import *

def clean_txt(title):#清洗标题中不能用于命名文件的字符
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    title = re.sub(rstr, "_", title)  # 替换为下划线
    return title

def create_folder(name):#创建文件夹
    try:
        if '{}'.format(name) not in os.listdir():#如果不存在
            os.makedirs('{}'.format(name))#则创建
    except:
        return ''

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
def get_one_page_text(url,headers=headers,code='utf-8'):#访问一个页面 返回页面信息
    try:
        s = requests.Session()#保持会话
        s.mount('http://', HTTPAdapter(max_retries=3))#最大重试
        s.mount('https://', HTTPAdapter(max_retries=3))
        r=s.get(url,headers=headers,timeout=15)#超时设置
        r.raise_for_status()#状态码 如果不是200则报错
        r.encoding=code#r.apparent_encoding#字符类型
        return  r.text#返回页面
    except Exception as e:
        t=time.strftime('%Y/%m/%d %H:%M:%S %a')#时间格式化
        with open(r'/Users/lishuo/spider/workspace/selenium_bilibili/1/Exception.txt','a+',encoding='utf-8') as f:
            f.write('time:{}\n\nurl:{}\n\n{}\n\n'.format(t,url,e))

def get_params(start_url,quality,p):
    print(start_url)
    html = get_one_page_text(start_url)
    print(html)
    cid = re.search(r'cid=(\d+)&',html).group(1)
    title = clean_txt(re.search(r'<h1 title="(.*?)">',html).group(1))+'第%sP'%p

    path = '/Users/lishuo/spider/workspace/selenium_bilibili/1/'


    create_folder(path)
    SEC1 = '94aba54af9065f71de72f5508f1cd42e' #上面的SEC已经失效了
    params = 'appkey=84956560bc028eb7&cid={}&otype=xml&qn={}&quality={}&type='.format(cid, quality, quality) #otype=json也行!!
    encrypt = hashlib.md5(bytes(params+SEC1,'utf-8')).hexdigest()
    video_list=get_down_load_url(params, encrypt, start_url)
    print('视频cid : %s 共 %s 段' % (cid, len(video_list)))
    down_load(video_list, start_url, path,title)
    splice_mp4(path,title)

def get_down_load_url(params,encrypt,start_url):
    url_api = 'https://interface.bilibili.com/v2/playurl?' + params + '&sign=' + encrypt
    headers = {'Referer':start_url,'User-Agent':'Mozilla/5.0'}
    html = get_one_page_text(url_api,headers=headers)
    doc = parseString(html.encode('utf8'))
    durl = doc.getElementsByTagName('durl')
    video_list = []
    for i in durl:
        video = i.getElementsByTagName('url')[0]
        url_video = video.childNodes[0].data
        video_list.append(url_video)
    return video_list

def down_load(video_list,start_url,path,title):
    num = 1
    for i in video_list:
        opener = urllib.request.build_opener()
        opener.addheaders = [
            # ('Host', 'upos-hz-mirrorks3.acgvideo.com'),  #注意修改host,不用也行
            ('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:56.0) Gecko/20100101 Firefox/56.0'),
            ('Accept', '*/*'),
            ('Accept-Language', 'en-US,en;q=0.5'),
            ('Accept-Encoding', 'gzip, deflate, br'),
            ('Range', 'bytes=0-'),  # Range 的值要为 bytes=0- 才能下载完整视频
            ('Referer', start_url),  # 注意修改referer,必须要加的!
            ('Origin', 'https://www.bilibili.com'),
            ('Connection', 'keep-alive')
        ]
        print('视频标题 : %s ,第%s段正在下载' % (title, num))
        urllib.request.install_opener(opener)
        urllib.request.urlretrieve(url=i, filename=path+'1.mp4')
        print('视频标题 : %s ,第%s段下载完成' % (title,  num))
        num += 1

def splice_mp4(path,title):
    print('合并视频 : %s ' % (title))
    LL = sorted(os.listdir(path))
    if len(LL)>=2:
        ll=[]
        for file in LL:
            if os.path.splitext(file)[1] == '.flv':
                filepath = os.path.join(path, file)
                video = VideoFileClip(filepath)
                ll.append(video)
        final_clip = concatenate_videoclips(ll)
        final_clip.write_videofile(path+'\\{}.mp4'.format(title), fps=24, remove_temp=False)
        print('视频 : %s 合并完成' % (title))
        os.remove('./{}TEMP_MPY_wvf_snd.mp3'.format(title))  # 删文件
    elif len(LL)==1:
        os.rename(os.path.join(path, LL[0]), os.path.join(path, title + ".mp4"))
        print('视频 : %s 合并完成' % (title))
    new_path = '/Users/lishuo/spider/workspace/selenium_bilibili/2/'
    shutil.move(path + '\\{}.mp4'.format(1), new_path + '\\{}.mp4'.format(1))

def datas():
    quality = 80
    # start = input('请输入您要下载的B站av号或者视频链接地址如：av19956343，或 19956343，或https://www.bilibili.com/video/av19956343:')
    start = str(8846589)
    p = 1
    if start.replace('av','').isdigit() == True:
        av_url = 'https://www.bilibili.com/video/av'+start.replace('av','')
    else:
        av_url=start
    start_url_list=[]
    if p==''or str(p).isdigit()==True:
        start_url = av_url + '/?p=%s' % p
        start_url_list.append([start_url,int(p)])
    elif ','in p:
        for p in p.split(','):
            start_url=av_url+'/?p=%s'%p
            start_url_list.append([start_url,p])
    elif '-'in p:
        for p in range(int(p.split('-')[0]),int(p.split('-')[1])+1):
            start_url=av_url+'/?p=%s'%p
            start_url_list.append([start_url,p])
    else:
        print('输入有误,程序退出')
    return quality, start_url_list

def main ():
    quality,start_url_list=datas()[0],datas()[1]
    for start_url in start_url_list:
        get_params(start_url[0],quality,start_url[1])

if __name__=='__main__':
    main()
