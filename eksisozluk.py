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

            desiredPageCount = int(lastPageNumber)
        
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


    # bir konu başlığının sondan istenilen sayfa sayısı kadar return etmeli

    def find_commentsOnLastPages(self, titleurl, pagecount):

        data = {}

        commentNumber = 1

        soup = self.makeSoup(titleurl)

        lastPageNumber = int(soup.find('div', class_='pager').get('data-pagecount'))

        desiredPageCount = pagecount

        if( pagecount > int(lastPageNumber)):

            desiredPageCount = lastPageNumber

        for i in range(desiredPageCount):

            print(titleurl + '?p=' + str(lastPageNumber - i))

            soup = self.makeSoup(titleurl + '?p=' + str(lastPageNumber - i))

            commentList = soup.find('ul', id='entry-item-list').findAll('div', class_='content')

            for item in commentList:

                data['comment_' + str(commentNumber)] = item.text.split('\n')[1]

                commentNumber = commentNumber + 1
        
        return data







e = EksiSozluk()



data = {
    '15 temmuz kontrollü darbe girişimiydi' : 'https://eksisozluk.com/15-temmuz-kontrollu-darbe-girisimiydi--5272942',
    'gece vakti korna çalan çomar' : 'https://eksisozluk.com/gece-vakti-korna-calan-comar--5151104',
    'negatif insanları hayatınızdan çıkarın' : 'https://eksisozluk.com/negatif-insanlari-hayatinizdan-cikarin--5228537',
    'türkiyenin italyadan beter olacağı gerçeği' : 'https://eksisozluk.com/turkiyenin-italyadan-beter-olacagi-gercegi--6417432',
    '7.9 milyon $ kızılay bağışının ensara verilmesi' : 'https://eksisozluk.com/7-9-milyon-kizilay-bagisinin-ensara-verilmesi--6342305',
    '29 ocak 2020 vodafone cts bayi rezaleti' : 'https://eksisozluk.com/29-ocak-2020-vodafone-cts-bayi-rezaleti--6343955',
    'küfür etkisi yaratan ama küfür olmayan cümleler' : 'https://eksisozluk.com/kufur-etkisi-yaratan-ama-kufur-olmayan-cumleler--151263',
    'yok artık daha neler' : 'https://eksisozluk.com/yok-artik-daha-neler--230308',
    'cristiano ronaldo' : 'https://eksisozluk.com/cristiano-ronaldo--1337211',
    '1 mayıs 2021 corona aşısı yolsuzluğu iddiası' : 'https://eksisozluk.com/1-mayis-2021-corona-asisi-yolsuzlugu-iddiasi--6903154?day=2021-05-03',
    'messi' : 'https://eksisozluk.com/messi--1296095',
    '16 ocak 2021 mesut özilin fenerbahçeye transferi' : 'https://eksisozluk.com/16-ocak-2021-mesut-ozilin-fenerbahceye-transferi--6800751',
    'anıtkabirde rte sloganları atmak' : 'https://eksisozluk.com/anitkabirde-rte-sloganlari-atmak--6242225',
    'finlandiya başbakanının instagram paylaşımı' : 'https://eksisozluk.com/finlandiya-basbakaninin-instagram-paylasimi--6903106?a=popular'

}

pagecount = 20

'''
for item in list(data.keys()):

    comment_url = data[item]

    comments = e.find_commentsOnMultiplePages(comment_url, pagecount= pagecount)

    with open( 'data/' + item + '.json', 'w') as outfile:

        json.dump(comments, outfile)

    print(item)
'''


comment_url = 'https://eksisozluk.com/finlandiya-basbakaninin-instagram-paylasimi--6903106'

comments = e.find_commentsOnMultiplePages(comment_url, pagecount= pagecount)

with open( 'finlandiya_basbakanının_instagram_paylasımı.json', 'w') as outfile:

    json.dump(comments, outfile)
