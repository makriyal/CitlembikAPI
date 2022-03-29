from asyncio.windows_events import NULL
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from requests_html import HTMLSession
from halk_linkler import allLinksHalk, allSubCategoriesHalk
from kitapsec_linkler import allLinksKitapsec, allSubCategoriesKitapsec

class Scraper():
    def scrapedata(self, site, kategori, altkategori, link, sorgu, sayfa):
        
        s = HTMLSession()

        results_list = []

        if site == "kitapsec":
            r = s.get(link)
            results = r.html.find('div.Ks_UrunSatir')
            for res in results :
                item = {
                    'title' : res.find('a.img > img', first=True).attrs['title'],
                    'img' : res.find('a.img > img', first=True).attrs['src'],
                    'img_alt' : res.find('a.img > img', first=True).attrs['data-src'],
                    'link' : res.find('a.text', first=True).attrs['href'],
                    'publisher' : res.find('span.yynImg > div > a', first=True).text.strip(),
                    'author' : res.find('span[itemprop=author]', first=True).text.strip(),
                }
                results_list.append(item)
        elif site == "halk":
            if sorgu.isdigit():
                print("sorgu.isdigit()")
                r = s.get("https://www.halkkitabevi.com/index.php?p=Products&q_field_active=0&q="+sorgu)
                try:
                    title = r.html.find('div > div.col2.__col2 > h1', first=True).text.strip()
                except:
                    title = ''
                try:
                    img = r.html.find('#main_img', first=True).attrs['src']
                except:
                    img = ''
                try:
                    img_alt = r.html.find('#main_img', first=True).attrs['data-zoom-image']
                except:
                    img_alt = ''
                try:
                    publisher = r.html.find('div.prd_brand_box > a.publisher', first=True).text.strip()
                except:
                    publisher = ''
                try:
                    author = r.html.find('div.prd_info > div.writer > a', first=True).text.strip()
                except:
                    author = ''
                item = {
                        'title' : title,
                        'img' : img,
                        'img_alt' : img_alt,
                        'link' : sorgu,
                        'publisher' : publisher,
                        'author' : author,
                    }
                results_list.append(item)
            else :
                print("sorgu.isNotdigit()")
                if sorgu == "null":
                    link = allLinksHalk[int(kategori)][int(altkategori)]
                else :
                    link = "https://www.halkkitabevi.com/index.php?p=Products&q_field_active=0&q=" + sorgu + "&page=" + sayfa
                r = s.get(link)
                results = r.html.find('div.prd_list_container_box > div > ul > li > div')
                for res in results :
                    try:
                        title = res.find('a>img', first=True).attrs['title']
                    except:
                        title = ''
                    try:
                        img = res.find('a>img', first=True).attrs['data-src']
                        img_alt = res.find('a>img', first=True).attrs['data-src']
                    except:
                        img = ''
                        img_alt = ''
                    try:
                        link = res.find('a', first=True).attrs['href']
                    except:
                        link = ''
                    try:
                        publisher = res.find('div.prd_info > div.publisher', first=True).text.strip()
                    except:
                        publisher = ''
                    try:
                        author = res.find('div.prd_info > div.writer > a', first=True).text.strip()
                    except:
                        author = ''
                    item = {
                        'title' : title,
                        'img' : img,
                        'img_alt' : img_alt,
                        'link' : link,
                        'publisher' : publisher,
                        'author' : author,
                    }
                    results_list.append(item)
                
        return results_list
    
    def getPrice(self, site, isbn, name, author, publisher):
        s = HTMLSession()

        price_list = []

        if site == "amazon":
            url = "https://www.amazon.com.tr/s?k="+isbn
            r = s.get(url)
            try :
                noStock = r.html.find('span.a-size-small', first=True).text.strip()
                if noStock != NULL & "mevcut değil" in noStock :
                    raise Exception("fetchPriceAmazon noStock raised an exception")
                cantFind = r.html.find('span > div > div > div:nth-child(1) > span:nth-child(2)', first=True).text.strip()
                if cantFind != NULL & "sonuç yok" in cantFind :
                    raise Exception("fetchPriceAmazon cantFind raised an exception")
            except :
                print("fetchPriceAmazon exception")

            imgUrl = "https://m.media-amazon.com/images/G/41/logo/Amazon_com_tr_Logo._CB1198675309_.jpg"

            price = r.html.find('span.a-price', first=True).text.strip()
            tlIx = price.index("TL")
            price_ = price[:tlIx];
            return {
                'site' : "amazon.com.tr",
                'price' : float(price_.replace(",", ".").replace(" TL", "")),
                'imgUrl' : imgUrl,
                'link' : url,
            }
        elif site == "halk":
            url = "https://www.halkkitabevi.com/index.php?p=Products&q_field_active=0&q="+isbn
            r = s.get(url)
            try :
                noStock = r.html.find('div.prd_no_sell', first=True).text.strip()
                if noStock != NULL & "Stokta yok" in noStock :
                    raise Exception
                cantFind = r.html.find('div.no_product_found', first=True).text.strip()
                if cantFind != NULL & "bulunamadı" in cantFind :
                    raise Exception
            except :
                print("fetchHalk exception")

            imgUrl = "https://www.halkkitabevi.com" + r.html.find('div > div > div.logo > a > img', first=True).attrs['src']

            price = r.html.find('#prd_final_price_display', first=True).text.strip()
            tlIx = price.index("TL")
            price_ = price[:tlIx];
            return {
                'site' : "Halk Kitabevi",
                'price' : float(price_.replace(",", ".").replace(" TL", "").replace("TL", "")),
                'imgUrl' : imgUrl,
                'link' : url,
            }
        elif site == "kitapsec":
            url = "https://www.kitapsec.com/Arama/index.php?a="+isbn
            r = s.get(url)
            try :
                cantFind = r.html.find('div.Ks_BodyBack > div > div > div > div:nth-child(2) > div', first=True).text.strip()
                if cantFind != NULL & "bulunamadı" in cantFind :
                    raise Exception
            except :
                print("fetchKitapsec exception")

            imgUrl = "https:" + r.html.find('div.fullBack.Ks_HeaderColor > div > div > table > tbody > tr > td:nth-child(1) > a > img', first=True).attrs['src']

            price = r.html.find('#prd_final_price_display', first=True).text.strip()
            tlIx = price.index("TL")
            price_ = price[:tlIx];
            return {
                'site' : "Kitapseç",
                'price' : float(price_.replace(",", ".").replace(" TL", "").replace("TL", "")),
                'imgUrl' : imgUrl,
                'link' : url,
            }

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

results = Scraper()


# print("amazon : "+results.getPrice("amazon", "9750803736","835 Satır","Nazım Hikmet","Yapı Kredi Yayınları") + "\n")
print("halk : "+results.getPrice("halk", "9750803736","835 Satır","Nazım Hikmet","Yapı Kredi Yayınları") + "\n")
print("kitapsec : "+results.getPrice("kitapsec", "9750803736","835 Satır","Nazım Hikmet","Yapı Kredi Yayınları") + "\n")


@app.get("/{site}/{kategori}/{altkategori}/{link}/{sorgu}/{sayfa}")
async def get_results(site, kategori, altkategori, link, sorgu, sayfa):
    return results.scrapedata(site, kategori, altkategori, link, sorgu, sayfa)


@app.get("/{site}/{index}")
async def get_subcategories(site, index):
    if site == "kitapsec":
        return allSubCategoriesKitapsec[int(index)]
    elif site == "halk":
        return allSubCategoriesHalk[int(index)]

@app.get("/{site}/{isbn}/{name}/{author}/{publisher}")
async def get_results(site, isbn, name, author, publisher):
    return results.getPrice(site, isbn, name, author, publisher)
    
