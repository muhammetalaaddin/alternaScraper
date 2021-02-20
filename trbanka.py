import requests as rq
from bs4 import BeautifulSoup


class Trbanka():

    def __init__(self):

        self.baseurl = 'https://www.trbanka.com/'
        self.headers= {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
    
    def makeSoup(self, url):

        return BeautifulSoup(rq.get(url, headers=self.headers).text, 'html.parser')

    #
    # varalon bütün bankaların isim ve linklerini return eder.
    #

    def findBankNamesandUrls(self):

        soup = self.makeSoup(self.baseurl)

        div = soup.find('div', class_='leftdiv')

        lis = soup.find('ul', class_='banks').find_all('li')

        banks = {}

        for li in lis:

            try:
                title = li.find('a').get('title')

                href = li.find('a').get('href')

                banks[title] = href
            except :

                print('')


        return banks


        #
        # bir bankanın var olduğu bütün şehirlerin linklerini ve isimlerini return eder
        #

    def findBankCitiesAndUrls(self, bankUrl):

        soup = self.makeSoup(bankUrl)

        lis = soup.find('ul', class_='banks').find_all('li')

        cities = {}

        for li in lis:

            try:

                cityname = li.find('a').text

                link = li.find('a').get('href')

                cities[cityname] = link
            except :

                print('') 

        return(cities)      
    
    #
    # bir bankanın bir şehrinde bulunan bütün şubelerin isim ve linkleri return eder
    #


    def findBankBranchNameAndUrlForCity(self, cityurl):

        soup = self.makeSoup(cityurl)

        div = soup.find('div', class_='content').find_all('div', class_='near_title')

        branchies = {}

        for d in div:

            try:

                name = d.find('a').text

                href = d.find('a').get('href')

                branchies[name] = href

            except :

                print('')

        return branchies
    
    #
    # bir şube sayfasında yer alan yorumları bir liste olarak return eder.
    #

    def findReviewsforBranch(self, branchUrl):

        soup = self.makeSoup(branchUrl)

        div = soup.find_all('div', class_='comment')

        comments = []

        for d in div:

            try:

                text = d.find('p', class_='ctext').text

                comments.append(text)
            
            except :

                print('')
            

        return comments