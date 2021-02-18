import requests as rq
from bs4 import BeautifulSoup
import json


class SikayetVar():

    def __init__(self):

        self.name = 'şikayet hello'
        self.headers= {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
        self.baseurl = 'https://www.sikayetvar.com'

    def makeSoup(self, url):

        return BeautifulSoup(rq.get(url, headers=self.headers).text, 'html.parser')

    
    #
    # verilen başlık link çiftlerinden yola çıkarak her bir başlığa karşılık gelen yorumları toplar.
    #

    def findReviewsForBrand(self,titleUrlpair):

        data = {}

        for title in titleUrlpair:

            data[title] = self.findReviewForUrl(titleUrlpair[title])

        return data


    #
    # verilen yorum linkine giderek yorumun tamamını alma işlemini yapar.
    #

    def findReviewForUrl(self, url):

        complaintPage = self.makeSoup(url).find('div', class_='card-text')

        return complaintPage.text

    
    #
    # verilen marka linkine giderek girilen sayfa sayısına karşılık gelen yorumların başlıklarını ve linklerini toplar. 
    #

    def findBrandReviewsUrlAndTitles(self, brandurl, pagecount):

        data = {}

        soup = self.makeSoup(brandurl)

        complaintTitle = soup.find_all('h2', class_='complaint-title')   

        # birinci sayfa

        for item in complaintTitle:

            title = item.find('a').get('title')

            reviewurl = self.baseurl +  item.find('a').get('href')

            data[title] = reviewurl
        
        for i in range(2, int(pagecount) + 1):

            soup = self.makeSoup(brandurl + '?page=' + str(i))

            complaintTitle = soup.find_all('h2', class_='complaint-title')   

            for item in complaintTitle:

                title = item.find('a').get('title')

                reviewurl = self.baseurl +  item.find('a').get('href')

                data[title] = reviewurl
        
        return data




    #
    # markalar bölümündeki girilen sayfa linkinden giderek marka isimlerini ve linklerini toplar.
    #

    def findBrandNamesAndUrlsPerPage(self, pageUrl):

        soup = self.makeSoup(pageUrl)

        brandlist = soup.find('ul', class_='brand-list').find_all('li')

        data = {item.find('a', class_='brand-logo').get('title') : self.baseurl +  item.find('a', class_='brand-logo').get('href') for item in brandlist}        

        return data


    

    #
    # girilen sayfa sayısı kadar markalar bölümünden marka adı ve linki toplar.
    #

    def findBrandsNamesAndUrls(self, pagecount):

        query = '/tum-markalar'

        url = self.baseurl + query

        soup = self.makeSoup(url)

        data = {}

        #birinci sayfa
        pageData = self.findBrandNamesAndUrlsPerPage(url)
        
        for brandname in pageData:

            data[brandname] = pageData[brandname]

        for i in range(2,pagecount + 1):


            query = '/tum-markalar?page=' + str(i)

            url = self.baseurl + query

            pageData = self.findBrandNamesAndUrlsPerPage(url)
        
            for brandname in pageData:

                data[brandname] = pageData[brandname]
 
        return data

    #
    # girilen banka linkinin alt kategorilerini tespit eder. Başlık ve link çitleri şeklinde return eder
    #

    def findSubCategoryNamesforBrand(self, brandurl):

        soup = self.makeSoup(brandurl)

        hashtags = soup.find('div', class_='hashtags').find_all('div')

        data = {}

        for hashtag in hashtags:

            try:
                title = hashtag.find('a').get('title')
                href = self.baseurl + hashtag.find('a').get('href')

                data[title] = href
            except:

                print('')

        return data

 
    # girilen markanın istenilen alt kategorisi varsa ilgili alt kategori'nin istenilen sayfa sayısı kadar yorumunu toplar.

    def findSubCategoryReviews(self, subcategory, brandurl, pagecount):

        subcategories = self.findSubCategoryNamesforBrand(brandurl)

        if(subcategory in list(subcategories.keys())):

            reviewslinks = self.findBrandReviewsUrlAndTitles(subcategories[subcategory], pagecount)

            return self.findReviewsForBrand(reviewslinks)
        
        else:

            print('subcategory does not exist')

