from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
import json 


class YoutubeScraper:

    def __init__(self, scrapePageUrl):

        self.driver = webdriver.Chrome(ChromeDriverManager().install())

        self.pageUrl = scrapePageUrl
    
    def openPage(self):

        self.driver.get(self.pageUrl)

        time.sleep(3)

    def clickSortingButton(self):

        while(True):
            self.driver.execute_script(("window.scrollBy(0,500)"))

            try:
                btn = self.driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/ytd-comments/ytd-item-section-renderer/div[1]/ytd-comments-header-renderer/div[1]/span/yt-sort-filter-sub-menu-renderer/yt-dropdown-menu/tp-yt-paper-menu-button/div/tp-yt-paper-button')
                btn.click()
                time.sleep(1)
                break
            except:
                print('no element')
        time.sleep(3)
    
    def clickBestComment(self):

        btn = self.driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/ytd-comments/ytd-item-section-renderer/div[1]/ytd-comments-header-renderer/div[1]/span/yt-sort-filter-sub-menu-renderer/yt-dropdown-menu/tp-yt-paper-menu-button/tp-yt-iron-dropdown/div/div/tp-yt-paper-listbox/a[1]')
        btn.click()

        time.sleep(3)
    
    def clicknewestComment(self):

        btn = self.driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/ytd-comments/ytd-item-section-renderer/div[1]/ytd-comments-header-renderer/div[1]/span/yt-sort-filter-sub-menu-renderer/yt-dropdown-menu/tp-yt-paper-menu-button/tp-yt-iron-dropdown/div/div/tp-yt-paper-listbox/a[2]')
        btn.click()

        time.sleep(3)

    def clickReply(self, item):

        try:
            btn = item.find_element_by_id('more-replies')
            btn.click()
        except:
            return False

        time.sleep(1)

        try:
            btn = item.find_element_by_xpath('//*[@id="continuation"]/yt-next-continuation/tp-yt-paper-button/yt-formatted-string')
            btn.click()
        except:
            print('there is no read more')

        time.sleep(1)
        
    def createCommentInfo(self, item):

        data = {}

        mainComment = item.find_element_by_id('content-text')

        data['comment'] = mainComment.text

        if(self.clickReply(item) != False):

            rs = item.find_elements_by_id('content-text')

            replies = {'reply_' + str(i) : rs[i].text for i in range(1, len(rs))}

            data['replies'] = replies
        
        else:
            data['replies'] = False
        
        return data

    def goToBottomPage(self):

        lastCount = 0
        newCount = 0

        while(True):

            length = self.driver.execute_script('return document.documentElement.scrollHeight')
            time.sleep(3)
            self.driver.execute_script("window.scrollBy(0," + str(length) +  ")")
            time.sleep(3)

            try:
                commentSection = self.driver.find_element_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/ytd-comments/ytd-item-section-renderer')
                lastCount = newCount
                items = commentSection.find_elements_by_id('content-text')
                newCount = len(items)
            except:
                print('no data')
            
            if(lastCount == newCount):

                break

    def collectComments(self, maxNumberComments, FileName , folderName ,sortingType = 'Best'):

        self.openPage()

        self.clickSortingButton()

        if(sortingType == 'Best'):

            self.clickBestComment()
        
        if(sortingType == 'Newest'):

            self.clicknewestComment()
        
        self.goToBottomPage()

        items = self.driver.find_elements_by_tag_name('ytd-comment-thread-renderer')

        if(len(items) > maxNumberComments):

            items = items[:maxNumberComments]
        
        data = {'comment_' + str(i) : self.createCommentInfo(items[i]) for i in range(len(items))}

        with open( './' + folderName + '/' + FileName + '.json' , mode='w') as f:

            json.dump(data, f)
