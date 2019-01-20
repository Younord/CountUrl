# -*- coding: utf-8 -*-
import requests
from lxml import etree
from BaiduNewSpider import *
import time

class CountBaiduUrls(object):
    def __init__(self, baiduNewSpiderObject):
        self.headers = headers
        self.baiduNewSpider = baiduNewSpiderObject

    def getData(self,crawl_url):
        try:
            data = requests.get(crawl_url, headers=self.baiduNewSpider.header)
            time.sleep(0.1)
            html = data.text
            return html
        except Exception as t:
            with open('log.txt', 'a') as f:
                f.write(str(t) + '\n')

    def hasNextPage(self, html):
        try:
            tree = etree.HTML(html)
            next_page = tree.xpath('//div[@id="wrapper"]/p[@id="page"]/a[contains(string(), "下一页")]/@href')
            if next_page != []:
                next_page_url = "http://news.baidu.com" + next_page[0]
            else:
                next_page_url = None
            return next_page_url
        except Exception as t:
            with open('log.txt', 'a') as f:
                f.write(str(t) + '\n')
            print("======================\n\n出现异常\n\n=====================")


    def getResult(self, html):
        result = []
        try:
            tree = etree.HTML(html)
            temp_result = tree.xpath('//div[@id="content_left"]/div[3]//div[@class="result"]')
            for div in temp_result:
                temp = {
                    'url' : None,
                }
                link = div.xpath('h3/a/@href')[0]
                temp['url'] = link
                result.append(temp)
        except Exception as t:
                with open('log.txt', 'a') as f:
                    f.write(str(t) + '\n')
                print("======================出现异常=====================")
        return result

    def run(self):
        totalurlnum = 0
        for crawl_url in self.baiduNewSpider.urls:
            print("[正在计算URL条数]%s" % crawl_url)
            i = 1
            totalurlnums = 0
            while crawl_url != None:
                html = self.getData(crawl_url)
                try:
                    if i == 1:
                        print("该页显示共有数据:\t%d" % BaiduNewSpider.searchSize(html))
                    result = self.getResult(html)
                    #print(result)
                    print("第%d页:\t%d" % (i,len(result)))
                    i += 1
                    totalurlnums  += len(result)
                    totalurlnum += len(result)
                    crawl_url = self.hasNextPage(html)
                except Exception as t:
                    with open('log.txt', 'a') as f:
                        f.write(str(t) + '\n')
            print("新闻实际条数为%d条" % totalurlnums)
            print("+" * 100)
        print("新闻总数为%d条" % totalurlnum)


if __name__ == "__main__":
    headers = {
        'Host': 'news.baidu.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36'
    }
    keyWord = u"权健"

    search1 = BaiduNewSpider(
        keyWord,
        headers,
        "2018-01-08 00:00:00",
        "2019-01-08 00:00:00",
        1
    )
    search1.urls = BaiduNewSpider.makeUrls(search1.keyWord, search1.startTime, search1.stopTime, search1.timeStep)

    search2 = CountBaiduUrls(search1)
    search2.run()
