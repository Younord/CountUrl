# -*- coding: utf-8 -*-

import requests
from lxml import etree
import time
import datetime

BaseUrl = "http://news.baidu.com/ns?word=%s&bt=%s&et=%s&rn=100&ie=utf-8&ct=2"

MaxSearchSize = 100

class BaiduNewSpider(object):

    def __init__(self, keyWord, header, startTime, stopTime, timeStep, dataBase=None):
        super().__init__()

        self.keyWord = keyWord
        self.header = header
        self.database = dataBase
        self.startTime = datetime.datetime.strptime(startTime, "%Y-%m-%d %H:%M:%S")
        self.stopTime = datetime.datetime.strptime(stopTime, "%Y-%m-%d %H:%M:%S")
        self.timeStep = datetime.timedelta(hours=timeStep)
        self.urls = []

    def searchSize(html):
        try:
            tree = etree.HTML(html)
            tempResult = tree.xpath('//span[@class="nums"]/text()')[0]

            if tempResult[6].isdigit():
                temp = tempResult[6: -1]
                temp = int(temp.replace(",", ""))
            else:
                temp = tempResult[7: -1]
                temp = int(temp.replace(",", ""))
            return temp
        except Exception as e:
            raise e
            
    def makeUrls(keyWord, startTime, stopTime, timeStep):
        searchUrls = []
        # url = BaseUrl % (keyWord, str(startTime), str(stopTime))
        #
        # print(url)
        # html = requests.get(url, headers=headers).text
        # time.sleep(1)
        # if BaiduNewSpider.searchSize(html) > MaxSearchSize:
        #     medainTime = (stopTime + startTime) / 2
        #
        #     searchUrls += BaiduNewSpider.makeUrls(keyWord, startTime, medainTime, headers)
        #     searchUrls += BaiduNewSpider.makeUrls(keyWord, medainTime, stopTime, headers)
        # else:
        #     searchUrls.append(url)
        i = 0
        endTime = 0
        while endTime < time.mktime(stopTime.timetuple()):
            beginTime = time.mktime((startTime + i * timeStep).timetuple())
            endTime = time.mktime((startTime + (i + 1) * timeStep).timetuple())
            url = BaseUrl % (keyWord, str(beginTime), str(endTime))
            i += 1
            searchUrls.append(url)

        return searchUrls


if __name__ == "__main__":
    headers = {
        'Host': 'news.baidu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36\
         (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
    }
    keyWord = u"权健"

    search = BaiduNewSpider(
        keyWord,
        headers,
        "2018-11-06 00:00:00",
        "2018-12-08 00:00:00",
        24
    )
    
    search.urls = BaiduNewSpider.makeUrls(search.keyWord, search.startTime, search.stopTime, search.timeStep)
    print(search.urls)
    print(len(search.urls))

