from youtube import YoutubeScraper






links = ['https://www.youtube.com/watch?v=BVZc7CEBe3g',
'https://www.youtube.com/watch?v=-mq28FE-ooA',
'https://www.youtube.com/watch?v=ygfZAjN-gzI',
'https://www.youtube.com/watch?v=pd0UzDMFyE8',
'https://www.youtube.com/watch?v=MSqWg_lKn9k']

index = 1

'''
for l in links[1:]:

    ys = YoutubeScraper(l)

    index = index + 1

    ys.collectComments(maxNumberComments=1000, FileName = str(index), folderName = 'newest' ,sortingType='Newest')
    ys.driver.close()
'''


url = 'https://www.youtube.com/watch?v=vEGSxd8uPr8'

ys = YoutubeScraper(url)
ys.collectComments(maxNumberComments=1000, FileName = str(index), folderName = 'newest' ,sortingType='Newest')
ys.driver.close()
