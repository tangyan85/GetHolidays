# coding:utf-8
import urllib.request
import re
import time
import logging
import json
#import requests
from bs4 import BeautifulSoup

language = "zh_cn"

logging.basicConfig(
    filename='app.log',
    format='%(asctime)s - %(module)s - %(levelname)s :  %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S %p',
    level=logging.ERROR
)


def getHtmlTxt(year=time.strftime("%Y"), lan="zh_cn"):
    url_year = "%s/" % year if time.strftime("%Y") != year else ""
    page_url = "http://holidays-calendar.net/%scalendar_%s/china_%s.html" % (url_year, lan, lan)
    #page_url="https://holidays-calendar.net/2019/calendar_zh_cn/china_zh_cn.html"
    logging.debug("爬取地址: %s" % page_url)
    try:
        response = urllib.request.urlopen(page_url, timeout=10)
        html = response.read()
    except Exception as e:
        logging.error(e)
        return
    if len(html) > 5000:
        return html.decode('utf-8')

    return


def getYearHolidays(year=time.strftime("%Y"), lan="zh_cn"):
    data = {}
    html = getHtmlTxt(year, lan)
    if html is None:
        return
    
   

    soup = BeautifulSoup(html)
    #获取调休上班的日期
    noNeeddays=getWorkDay4Break(soup.find_all('div',class_="list-mark"),year)

    for table in soup.find_all('table'):
        #<tr><td class="month" colspan="7">Jan（1月）</td></tr>
        #Jan（1月）
        title_str=table.contents[0].get_text()
         #最小匹配
        p1 = re.compile('（(.+)月）', re.S) 
        momth_str="".join(re.findall(p1, title_str))
        month = "%s%s" % (year, momth_str.zfill(2))
        #过滤头
        head_str=table.contents[1].extract()

        #抓取当月所有的天
        day_list = [ row.get_text(strip=True) for row in table.select('.day') if not row.text is None ]
        #抓取当月所有的节假日，bs4好像不支持同时获取多个css，只能分开处理了
        hol_list = [ row.get_text(strip=True) for row in table.select('.hol') if not row.text is None ]
        #抓取当月所有的星期六
        sat_list = [ row.get_text(strip=True) for row in table.select('.sat') if not row.text is None ]
         #抓取当月所有的星期日
        sun_list = [ row.get_text(strip=True) for row in table.select('.sun') if not row.text is None ]
        months = {}
        
        #1--workday  0---节假日   2---周末    
        for day in day_list:
            if day!= '':
                day_type = 1
                if day in hol_list:
                   day_type = 0
                elif day in sat_list:
                   day_type = 2
                elif day in sun_list:
                   day_type = 2
                day = "%s%s" % (month, day.zfill(2))

                if day in noNeeddays:
                    day_type = 2

                months[day] = day_type
        data[month] = months
    
    with open('data.json', 'w') as f:
         json.dump(data, f)
    return data

#解析调休上班的日期
    # []['2月7日（星期日）、2月20日（星期六）'] []
    # ['4月25日（星期日）、5月8日（星期六）'][]
    # ['9月18日（星期六）']['9月26日（星期日）、10月9日（星期六）']
def getWorkDay4Break(htmlData,year=time.strftime("%Y")):
    noWorkDays=[]
    p0 = re.compile('【调休上班】(.+)上班。', re.S) 
    for div in htmlData:
        days_str=re.findall(p0, div.text)

        if len(days_str)>0:
            for word in days_str:
                for tmp in word.split('、'):
                    if len(tmp)>0:
                       noWorkDays.append(getDay4Word(tmp,year))
    return noWorkDays


#input:4月25日（星期日）
#output:"0425"
def getDay4Word(word,year=time.strftime("%Y")):
    if len(word)==0:return
    #firstHalf=word[0:word.index('（')]
    # endHalf=word[word.index('（')+1:word.index('）')]
    # print(firstHalf)
    # print(endHalf)
    month=word[0:word.index('月')]
    day=word[word.index('月')+1:word.index('日')]
    # print(mouth)
    # print(day)
    return "%s%s%s" % (year,month.zfill(2), day.zfill(2))

def getMonthHolidays(month=time.strftime("%Y%m"), lan="zh_cn"):
    year = month[0:4]
    days = getYearHolidays(year, lan)



# def getDayHoliday(day=time.strftime("%Y%m%d"), lan="zh_cn"):
#     month = day[0:6]
#     data = getMonthHolidays(month, lan)
#     if data is None:
#         return
#     return data[day]
