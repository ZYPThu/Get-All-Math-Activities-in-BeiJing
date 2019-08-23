# -*- coding: utf-8 -*-
import urllib.request as rst
import urllib.parse as pse
import datetime as dte
import time
import os
import json
import tunet
import smtplib
import os
import socket
import threading as td
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage





def getconf():
    file=open('./configuration.txt','r')

    con=[]
    for l in file:
        if '##' in l:
            break
        else:
            p=l.find('=')
            q=len(l)
            con.append(l[p+1:q-1])
    return con







def getinfobicmr():
    urls=geturl()
    hd={'Host': 'bicmr.pku.edu.cn',
'Connection': 'keep-alive',
'Cache-Control': 'max-age=0',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
'If-None-Match': "5d4921ed-4434",
}
    isdate=0
    isneed=0
    tit=''
    typ=''
    yr=''
    dt=''
    ymd=''
    spk=''
    website=''
    infonew=''

    fileodd=open('./Interesting Academic Activities in PKU.csv','r',encoding='utf-8')
    infoodd=fileodd.readlines()
    fileodd.close()

    g=open("./Upcoming Activities in PKU.csv",'w',encoding='utf-8')
    h=open('./Interesting Academic Activities in PKU.csv','w',encoding='utf-8')
    g.write('Title,Type,Date(Y/M/D),Speaker,Web Site\n')
    h.write('Title,Type,Date(Y/M/D),Speaker,Web Site\n')


    


    for url in urls:
        
        repd=rst.Request(url,headers=hd)
        cont=rst.urlopen(repd)
        
        
        cont1=cont.read().decode('utf-8')


#原谅我写这么蠢的代码，下面这一段代码的目的是逐行分析上面返回的内容。

        f=open('./Httpres.txt','wb')
        f.write(cont1.encode('utf-8'))
        f.close()

        f=open('./Httpres.txt','rb')
        line=f.readline()

        for line in f:
            line1=line.decode('utf-8')

            if isneed==1:

    #获取年份与日期
                if isdate==1:
                    p=line1.find('<span>')
                    if p>-1:
                        yr=line1[p+6:p+10]
                        print(yr)
                        isdate=isdate+1
                if isdate==2:
                    p=line1.find('<p>')
                    q=line1.find('</p>')
                    if p>-1 and q>-1:
                        dt=line1[p+3:q]
                        print(dt)
                        isdate=0
                        ymd=getymd(yr,dt)

                if '<dt>' in line1:
                    isdate=1
                if '</dt>' in line1:
                    isdate=0
    #获取类型，Conference、MiniCourse、Seminar或者Colloquium
                if '/content/lists/' in line1:
                    p=line1.find('title')
                    q=line1.find('target')
                    if p>-1 and q>-1:
                        p=p+7
                        q=q-2
                        typ=line1[p:q:1]
                        print(typ)
    #获取标题以及网址
                else:
                    p=line1.find('href')
                    q=line1.find('title')
                    r=line1.find('">')
                    if p>-1 and q>-1 and r>-1:
                        website=line1[p+6:q-2]
                        print(website)
                        tit=line1[q+7:r]
                        tit=tit.replace(',',' ')
                        tit=tit.replace('“','"')
                        tit=tit.replace('”','"')
                        print(tit)
                        if '/content/show/' in website:
                            website="http://bicmr.pku.edu.cn"+website

    #获取Speaker  
                if "Speaker(s)" in line1:
                    p=line1.find('Speaker(s)')
                    q=line1.find('</p>')
                    if p>-1 and q>-1:
                        spk=line1[p+12:q]   
                        spk=spk.replace('（','(')
                        spk=spk.replace('）',')')
                        spk=spk.replace('，','&')
                        print(spk)
                    

            
            if '<dl class=\"clearfix event-lst\">'in line1:
                isneed=1
            if '</dd>' in line1:
   #更新信息             
                isneed=0
                updte,intes=Interestingornot(ymd,tit)
                if updte==1:
                    g.write(tit+','+typ+','+ymd+','+spk+','+website+'\n')
                if updte==1 and intes==1:
                    inff=tit+','+typ+','+ymd+','+spk+','+website+'\n'
                    h.write(inff)
                    inff1=inff.replace('\n','<br>')
                    if inff in (infoodd):
                        print(1)
                        infonew=infonew
                    else:
                        print(2)
                        infonew=infonew+inff1
                tit=typ=ymd=spk=website=''
            
        f.close()
    g.close()
    h.close()

    print(str(infoodd))

    #有更新就返回新的信息
    print(str(infonew))
    return infonew
    

def geturl():
    file=open('./PKUweb.txt','r')
    urls=[]
    for l in file:
        if "##" in l:

            break
        llen=len(l)
        if llen==1:
            continue
        l=l[0:llen-1]
        print(l)
    
        urls.append(l)
    print(urls)
    return urls

def getymd(yr,dt):
    month=dt[0:3]
    day=dt[4:]
    fymd=yr+'-'+month+'-'+day


    return fymd

def Interestingornot(ymd,tit):
    #比较日期
    intes=0
    uptodate=0
    nymd=dte.datetime.now().strftime('%Y-%m-%d') 
    fymd=ymd
    fymd=fymd.replace('Jan','01')
    fymd=fymd.replace('Feb','02')
    fymd=fymd.replace('Mar','03')
    fymd=fymd.replace('Apr','04')
    fymd=fymd.replace('May','05')
    fymd=fymd.replace('Jun','06')
    fymd=fymd.replace('Jul','07')
    fymd=fymd.replace('Aut','08')
    fymd=fymd.replace('Sep','09')
    fymd=fymd.replace('Oct','10')
    fymd=fymd.replace('Nov','11')
    fymd=fymd.replace('Dec','12')
    if fymd<nymd:
        uptodate=0

    else:
        uptodate=1
 

    
    print(nymd)

    #比较关键词
    file=open('./KeyWords.txt','r')
    
    for l in file:
        if "##" in l:
            
            break
        lt=len(l)
        l=l[0:lt-1]
        print(l)
        if l in tit:
            intes=1
            break


    return uptodate,intes

def sendEmail(smtpserver,username,password,sender,receiver,subject,msghtml):
    try:
        msgRoot =MIMEMultipart('reklated')
        msgRoot['To']=','.join(receiver)
        msgRoot['Subject']= subject
        msgText = MIMEText(msghtml,'html','utf-8')
        msgRoot.attach(msgText)
        smtp = smtplib.SMTP()
        smtp.connect(smtpserver,"25")
        smtp.login(username,password)
        for re in receiver:

            smtp.sendmail(sender,re,str(msgRoot))
        print ("YES")
        smtp.quit()
    except Exception as e:
        print(e)
        print('Test Failed')
    else:
        print('Test Succeed')


if  __name__ == '__main__' :
    #
    try:
        conf=[]
        conf=getconf()
        print(conf)
        newinfo=getinfobicmr()
        #tunet.net.login(conf[0],conf[1])

        if newinfo!='':
            contss='New Upcoming Activities You Might be Interested:<br>'+newinfo
            sendEmail("mails.tsinghua.edu.cn",conf[2],conf[3],conf[2],[conf[4]],'Updates in Math Activities',contss)

        #tunet.net.logout()
    except Exception as e:
        print(str(e))
        print("!!!")

        

