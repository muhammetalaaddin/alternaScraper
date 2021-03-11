import requests as rq
from bs4 import BeautifulSoup

class BeyazPerde():

    def __init__(self):

        self.baseUrl = 'http://www.beyazperde.com'
        self.basefilmurl = 'http://www.beyazperde.com/filmler/tum-filmleri/kullanici-puani/'
        self.headers= {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
    
    
    def makeSoup(self, url):

        return BeautifulSoup(rq.get(url, headers=self.headers).text, 'html.parser')


    #
    ## bütün filmlerin olduğu sayfaya giderek film kategorilerinin adlarını ve linklerini toplar
    #

    def find_filmCategories(self):

        soup = self.makeSoup(self.basefilmurl)

        categoryList = soup.find('div', class_='left_col_menu_item')

        categoryInfo = {item.find('a').text : self.baseUrl + item.find('a').get('href') for item in categoryList.find_all('li')[1:]}

        return categoryInfo
    
    
    #
    ## Kategori sayfasında istenilen sayfa sayısı kadar film ismi ve linki toplar
    #

    
    def find_filmNamesAndUrlForPages(self, categoryurl, pagecount):

        filmInfo = {}
        
        # birinci sayfa

        soup = self.makeSoup(categoryurl)

        for item in soup.find_all('div', class_='data_box'):

            filmname = item.find('h2').find('a').text.split('\n')[1]

            filmUrl = self.baseUrl +  item.find('h2').find('a').get('href')

            filmInfo[filmname] = filmUrl
        
        # birden fazla sayfa için

        for i in range(2, int(pagecount) + 1):

            categoryurl = categoryurl + '?page=' + str(pagecount)

            soup = self.makeSoup(categoryurl)

            for item in soup.find_all('div', class_='data_box'):

                filmname = item.find('h2').find('a').text.split('\n')[1]

                filmUrl = self.baseUrl +  item.find('h2').find('a').get('href')

                filmInfo[filmname] = filmUrl

        return filmInfo

    
    #
    ## filmin olduğu sayfaya giderek istenilen sayfa sayısı kadar yorum toplar. 
    #  beyazperde sitesi içinde film linkini direkt olarak filme gidip almak yerine kategori üzerinden almak gerekli. 
    #  Aksi halde üye eleştirileri kısmı kapalı oluyor. 
    #

    def find_commentsForFilm(self, filmUrl, pagecount):

        commentInfo = []
        
        commentUrl = filmUrl + 'kullanici-elestirileri/'

        # birinci sayfa

        soup = self.makeSoup(commentUrl)

        for item in soup.find_all('div', class_='content-txt review-card-content'):

            commentInfo.append(item.text.split('\n')[1])

        
        # birden fazla sayfa için

        for i in range(2, int(pagecount) + 1):

            commentUrl = filmUrl + 'kullanici-elestirileri/' + '?page=' + str(pagecount)

            soup = self.makeSoup(commentUrl)

            for item in soup.find_all('div', class_='content-txt review-card-content'):

                commentInfo.append(item.text.split('\n')[1])
        


        
        return commentInfo

