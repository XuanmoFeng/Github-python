#!/usr/bin/env python
# coding=utf-8
import re
import urllib
import sys
import os
import cookielib
import requests
import urllib2
import string
from Tkinter import *
import tkMessageBox
reload(sys)
sys.setdefaultencoding('utf-8')
s = requests.Session()#获取会话对象，用于登录时的cookie和session
header = {
    'Host': 'github.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://github.com',
    'Connection': 'keep-alive'
}
def AllList(owner):
    url='https://github.com/'+owner
    pyload={
    'tab':'repositories'
    }
    All=s.get(url,params=pyload)
    str=r'<li class="col-12.*?itemscope(.*?)</li>'
    All=re.findall(str,All.text,re.S)
    x=len(All)
    for i in range(0,x):
        str=r'name codeRepository">([\'\n\'|\' \']*)(.*?)</a>'
        Des=r'description">([\'\n\'|\' \']*)(.*?)</p>'
        datetime=r'datetime="(.*?)".*</relative-time>'
        Mu=re.findall(str,All[i],re.S)
        Des=re.findall(Des,All[i],re.S)
        Date=re.findall(datetime,All[i],re.S)
        if Des !=[]:
            print Mu[0][1],Des[0][1],Date[0]#,Date[0][1]
        else:
            print Mu[0][1],Date[0]#,Date[0][1]
def OONewrepobilty(token,owner,NewRename,DescrText):
    NewrepobiltyUrl='https://github.com/new'
    NewUrl='https://github.com/repositories'
    NewData={
        'utf8':'✓',
        'authenticity_token':token,
        'owner':owner,
        'repository[name]':NewRename,
        'repository[description]':DescrText,
        'repository[public]':'true',
        'repository[auto_init]':0,
        'repository[auto_init]':1
    }
    s.get(NewrepobiltyUrl)
    NewPage = s.post(NewUrl,data=NewData,headers=hea)
    print NewPage.text
def User(indexhtml):
    str=r'css-truncate-target">(.*?)</strong'
    str=re.findall(str,indexhtml.text,re.S)
    return str[0]

def convert_to_cn(text):
    text=re.sub(r'&#x([a-fA-F0-9]{2});',r'&#x00\1;',text)
    return text.replace('&#x','\u').replace(';','')\
    .decode('unicode-escape','replace').encode('utf-8')
#def Test():
def Newrepobilty(token,owner,NewRename,DescrText):
    NewrepobiltyUrl='https://github.com/new'
    kk=s.get(NewrepobiltyUrl)
    tokenRule = 'authenticity_token".*value="(.*?)"'#登录参数里面有一个token参数，是加载到页面中并且是动态的，需要爬出来
    tok=re.findall(tokenRule,kk.text,re.S)
    token=tok[0]
    NewUrl='https://github.com/repositories'
    NewData={
        'utf8':'✓',
        'authenticity_token':token,
        'owner':owner,
        'repository[name]':NewRename,
        'repository[description]':DescrText,
        'repository[public]':'true',
        'repository[auto_init]':0,
        'repository[auto_init]':'1'
    }
    hea={
    	'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Content-Type':'application/x-www-form-urlencoded',
        'Host':'github.com',
        'Origin':'https://github.com',
        'Referer':'https://github.com/new',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0',
    }
    s.get(NewrepobiltyUrl)
    NewPage = s.post(NewUrl,data=NewData,headers=hea)
    print NewPage.text
def MainMap(token,owner):
    MainList=Tk()
    MainList.geometry('+1000+200')
    MainList.title("python版gitHub")
    Label(MainList,text="新仓库名字",font=('微软雅黑',15),fg='yellow').grid()
    newName=Entry(MainList,fg='red',font=('微软雅黑',15))
    newName.grid(row=0,column=1)
    Label(MainList,text='描述',font=('微软雅黑',15),fg='blue').grid(row=1,column=0)
    DescrText=Entry(MainList,fg='red',font=('微软雅黑',15))
    DescrText.grid(row=1,column=1)
    Button(MainList,text='创建',font=('微软雅黑',15),height='1',fg='yellow',command=lambda:Newrepobilty(token,owner,newName.get(),DescrText.get())).grid(row=2,column=2)
    #Label(MainList,text="登陆成功",font=('微软雅黑',15),fg='yellow').grid()
    root.destroy()
def Login(username,password):
    indexUrl = 'https://github.com/'#首页地址
    loginUrl = 'https://github.com/login'#登录页面
    sessionUrl = 'https://github.com/session'#登录页面把表单提交到这个url，然后重定向到首页，把数据提交到这个Url之后可以获取到cookie,用于登录
    tokenRule = 'authenticity_token".*?value="(.*?)"'#登录参数里面有一个token参数，是加载到页面中并且是动态的，需要爬出来
    loginHtml = s.get(loginUrl,headers=header)#得到登录页面
    tokenPattern = re.compile(tokenRule,re.S)
    arraryTolen = re.findall(tokenPattern,loginHtml.text)#得到动态的token,这里返回的事数组，取第一个
    token = arraryTolen[0]
    print token
    loginParams = {
        'login':username,
        'password':password,
        'authenticity_token':token,
        'commit':'Sign in',
        'utf8': "✓"}#配置登录参数
    sessionHtml = s.post(sessionUrl,data=loginParams)#得到登录后的页面，其实被定位到了首页
    use=User(sessionHtml)
    #AllList(use)
    #Test()
    Newrepobilty(token,use,"helllowe","das")
    #MainMap(token,use)
    url=''
    url='https://github.com/phodal'
    indexhtml = s.get(url,headers=header)
    str=r'<li.*?Email.*?href=".*?">(.*?)</a>'
    rek=re.findall(str,indexhtml.text,re.S)
    x=len(rek)
    for i in range(0,x):
        print convert_to_cn(rek[i]) 

username="XXXX"
PassWord="XXXX"
Login(username,PassWord)


#root=Tk()
#root.title("python版gitHub")
#root.geometry('+100+200')
#Label(root,text="输入账号",font=('微软雅黑',15),fg='yellow').grid()
#Username=Entry(root,fg='red',font=('微软雅黑',15))
#Username.grid(row=0,column=1)
#Label(root,text='输入密码',font=('微软雅黑',15),fg='blue').grid(row=1,column=0)
#PassWord=Entry(root,fg='red',font=('微软雅黑',15))
#PassWord.grid(row=1,column=1)
#Button(root,text='登陆',font=('微软雅黑',15),height='1',fg='yellow',command=Login).grid(row=2,column=2)
#mainloop()
