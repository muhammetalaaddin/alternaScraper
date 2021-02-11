from sikayetvar import SikayetVar
import json

#instance oluşturma

s = SikayetVar()

# ilk 2 sayfa için markalar bölümünden marka isimlerini ve linklerini bulma

pagecount = 2

brandnamesUrls = s.findBrandsNamesAndUrls(pagecount)

# Ziraat Bankası için yorum başlıklarını ve yorum linklerini bulma

ziraatUrl = brandnamesUrls['Ziraat Bankası']

reviewlinks = s.findBrandReviewsUrlAndTitles(ziraatUrl, pagecount)

#review linkleri kullanarak reviewleri elde etme

reviews = s.findReviewsForBrand(reviewlinks)

with open('reviews.json', 'w') as outfile:

    json.dump(reviews, outfile)


