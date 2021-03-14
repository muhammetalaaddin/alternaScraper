import requests as rq
from bs4 import BeautifulSoup
import json

class EksiSozluk():

    def __init__(self):

        self.base_url = 'https://eksisozluk.com/'
        self.headers= {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}

    def makeSoup(self, url):

        return BeautifulSoup(rq.get(url, headers=self.headers).text, 'html.parser')

    
    
    # Kanal isimlerini ve linklerini return eder

    def find_Channels(self):

        soup = self.makeSoup(self.base_url + '/kanallar')

        channel_list = soup.find('ul', id='channel-follow-list').find_all('a')

        return {item.text : self.base_url + item.get('href') for item in channel_list}

    # Bir Kanalın altında bulunan konu başlıklarının isimlerini ve linklerini return eder

    def find_TopicInfoForChannel(self, channel_url):

        soup = self.makeSoup(channel_url)

        topic_list = soup.find('ul', class_='topic-list').find_all('a')

        return {item.text : self.base_url +  item.get('href').split('?')[0] for item in topic_list}
    
    # bir başlık altında bulunan yorumların istenilen sayfa sayısı kadar miktarını return eder.

    def find_commentsOnMultiplePages(self, titleurl, pagecount):

        data = {}

        commentNumber = 1
        
        soup = self.makeSoup(titleurl)

        lastPageNumber = soup.find('div', class_='pager').get('data-pagecount')

        desiredPageCount = pagecount

        if( pagecount > int(lastPageNumber)):

            desiredPageCount = lastPageNumber
        
        #birinci sayfa
        
        commentList = soup.find('ul', id='entry-item-list').findAll('div', class_='content')

        for item in commentList:

            data['comment_' + str(commentNumber)] = item.text.split('\n')[1]

            commentNumber = commentNumber + 1
        
        for i in range(2, desiredPageCount + 1):

            soup = self.makeSoup(titleurl + '?p=' + str(i))

            commentList = soup.find('ul', id='entry-item-list').findAll('div', class_='content')

            for item in commentList:

                data['comment_' + str(commentNumber)] = item.text.split('\n')[1]

                commentNumber = commentNumber + 1
        

        return data
