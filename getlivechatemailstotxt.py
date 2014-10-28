#! /usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'konakona'
__VERSION__ = "v1.0"


import os,sys,os.path,pycurl,cStringIO,json

python_version = sys.version_info[0]
if(python_version !=2):
    print("本系统依赖于python2.7，您的系统不兼容， goodbye！")
    exit()

start_date = raw_input("1.请输入开始日期（YYYY-MM-DD）：")
end_date = raw_input("2.请输入结束日期（YYYY-MM-DD）：")

start_page = raw_input("3.请输入需要从第几页开始（可以不填）：")
end_page = raw_input("4.请输入需要结束页（可以不填）：")

echo_flag = raw_input("5.输入'Y'代表保存文件，输入'N'代表打印结果：")

if(echo_flag!='Y' and echo_flag!='N'):
    print("您的输入有误")
    exit()

if(start_date=="" or end_date == ""):
    print("请输入开始和结束日期")
    exit()

if (start_date > end_date):
    print("开始日期不能大于结束日期!")
    exit()

if(type(start_page)!=int):
    start_page = 2;
else:
    if(start_page > 2):
        pass
    else:
        start_page = 2

print("程序初始化...")

content = cStringIO.StringIO()
buf = cStringIO.StringIO()
file = open('emails.txt','wa')

#请修改为你的email和key
config = ['input your email','input your key']

def runCurl(start_date,end_date,page = 1):

    api_url = 'https://api.livechatinc.com/chats?date_from='+start_date+"&date_to="+end_date+"&page="+bytes(page)+"&has_goal=1"

    c = pycurl.Curl()
    c.setopt(c.URL, api_url)
    c.setopt(c.WRITEFUNCTION, buf.write)
    c.setopt(c.USERPWD, config[0]+":"+config[1])
    c.setopt(c.CONNECTTIMEOUT, 0)
    c.setopt(c.TIMEOUT, 0)
    # c.setopt(c.PROXY, 'http://www.crazyphper.com')  #如果你需要设置代理访问
    c.perform()

    if(c.getinfo(c.RESPONSE_CODE) != 200):
        print("[Warring] 在请求第"+page+"页时，失败了！")
        # return
    c.close()

# HTTP response code, e.g. 200.
# print('Status: %d' % c.getinfo(c.RESPONSE_CODE))
# Elapsed time for the transfer.
# print('Status: %f' % c.getinfo(c.TOTAL_TIME))



def saveContent(email):
    if(email != ""):
        content.write(email+"\n")

def saveFile(email):
    if(email != ""):
        file.write(email+"\n")

#-----------------程序正式开始-----------------
runCurl(start_date,end_date)
json_val = json.loads(buf.getvalue())
buf.seek(0)
buf.truncate()

if(type(end_page)!=int):
    totalPage = json_val["pages"]
else:
    if(end_page > 2):
        if(end_page > json_val["pages"]):
            totalPage = json_val["pages"]
        else:
            totalPage = end_page
    else:
        totalPage = json_val["pages"]

if(start_page >2):
    pass
else:
    for kk in json_val["chats"]:
        if(echo_flag == 'Y'):
            saveFile(kk["prechat_survey"][1]["value"])
        else:
            saveContent(kk["prechat_survey"][1]["value"])


for page in range(start_page,totalPage):
    runCurl(start_date,end_date,page)
    json_val = json.loads(buf.getvalue())
    buf.seek(0)
    buf.truncate()

    for kk in json_val["chats"]:
        if(echo_flag == 'Y'):
            saveFile(kk["prechat_survey"][1]["value"])
        else:
            saveContent(kk["prechat_survey"][1]["value"])


if(echo_flag == 'Y'):
    file.close()
else:
    print(content.getvalue())
    content.close()

if(raw_input("程序执行完毕，请按任意键结束...")):
    exit()
