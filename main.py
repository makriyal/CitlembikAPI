from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from requests_html import HTMLSession
from halk_linkler import allLinksHalk, allSubCategoriesHalk
from kitapsec_linkler import allSubCategoriesKitapsec
from queries import *


class Scraper:
    @staticmethod
    def scrapedata(site, kategori, altkategori, link, sorgu, sayfa):

        s = HTMLSession()

        results_list = []

        if site == "kitapsec":
            r = s.get(link)
            results_ = r.html.find('div.Ks_UrunSatir')
            for res in results_:
                item = {
                    'title': res.find('a.img > img', first=True).attrs['title'],
                    'img': res.find('a.img > img', first=True).attrs['src'],
                    'img_alt': res.find('a.img > img', first=True).attrs['data-src'],
                    'link': res.find('a.text', first=True).attrs['href'],
                    'publisher': res.find('span.yynImg > div > a', first=True).text.strip(),
                    'author': res.find('span[itemprop=author]', first=True).text.strip(),
                }
                results_list.append(item)
        elif site == "halk":
            if sorgu.isdigit():
                print("sorgu.isdigit()")
                r = s.get("https://www.halkkitabevi.com/index.php?p=Products&q_field_active=0&q=" + sorgu)
                try:
                    title = r.html.find('div > div.col2.__col2 > h1', first=True).text.strip()
                except AttributeError:
                    title = ''
                try:
                    img = r.html.find('#main_img', first=True).attrs['src']
                except AttributeError:
                    img = ''
                try:
                    img_alt = r.html.find('#main_img', first=True).attrs['data-zoom-image']
                except AttributeError:
                    img_alt = ''
                try:
                    publisher = r.html.find('div.prd_brand_box > a.publisher', first=True).text.strip()
                except AttributeError:
                    publisher = ''
                try:
                    author = r.html.find('div.prd_info > div.writer > a', first=True).text.strip()
                except AttributeError:
                    author = ''
                item = {
                    'title': title,
                    'img': img,
                    'img_alt': img_alt,
                    'link': sorgu,
                    'publisher': publisher,
                    'author': author,
                }
                results_list.append(item)
            else:
                print("sorgu.isNotdigit()")
                if sorgu == "null":
                    link = allLinksHalk[int(kategori)][int(altkategori)]
                else:
                    link = "https://www.halkkitabevi.com/index.php?p=Products&q_field_active=0&q=" \
                           + sorgu + "&page=" + sayfa
                r = s.get(link)
                results_ = r.html.find('div.prd_list_container_box > div > ul > li > div')
                for res in results_:
                    try:
                        title = res.find('a>img', first=True).attrs['title']
                    except AttributeError:
                        title = ''
                    try:
                        img = res.find('a>img', first=True).attrs['data-src']
                        img_alt = res.find('a>img', first=True).attrs['data-src']
                    except AttributeError:
                        img = ''
                        img_alt = ''
                    try:
                        link = res.find('a', first=True).attrs['href']
                    except AttributeError:
                        link = ''
                    try:
                        publisher = res.find('div.prd_info > div.publisher', first=True).text.strip()
                    except AttributeError:
                        publisher = ''
                    try:
                        author = res.find('div.prd_info > div.writer > a', first=True).text.strip()
                    except AttributeError:
                        author = ''
                    item = {
                        'title': title,
                        'img': img,
                        'img_alt': img_alt,
                        'link': link,
                        'publisher': publisher,
                        'author': author,
                    }
                    results_list.append(item)

        return results_list
    
    @staticmethod
    def get_price(site, isbn):

        s = HTMLSession()

        url = search_urls[site] + isbn
        
        #print(url)

        r = s.get(url)

        try:
            no_stock = r.html.find(no_stock_queries[site], first=True).text.strip()
            if no_stock_phrases[site] in no_stock:
                return return_(site, "Stokta yok", url)
        except AttributeError:
            pass
            # print(f"{site} noStock raised an exception")

        try:
            not_found = r.html.find(not_found_queries[site], first=True).text.strip()
            if not_found_phrases[site] in not_found:
                return return_(site, "Bulunamadı", url)
        except AttributeError:
            pass
            # print(f"{site} notFound raised an exception")

        try:
            price = r.html.find(price_queries[site], first=True).text.strip()
            return return_(site, price.replace(",", ".").replace(" TL", "").replace("TL", ""), url)
        except AttributeError:
            # print(f"{site} main raised an exception")
            return return_(site, "Hata", url)

def return_(site, price, url):
    return {
        'site': site_names[site],
        'price': price,
        'link': url,
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
print(results.get_price("kitapsepeti", "9786051856810"))
print(results.get_price("babil", "9786051856810"))
print(results.get_price("tele1", "9786051856810"))
print(results.get_price("kitapsec", "9786051856810"))
print(results.get_price("pandora", "9786051856810"))
print(results.get_price("amazon", "9786051856810"))  # 9750803734 hata veriyor
print(results.get_price("eganba", "9786051856810"))
print(results.get_price("idefix", "9786051856810"))
print(results.get_price("eganba", "9786051856810"))
print(results.get_price("dr", "9786051856810"))
print(results.get_price("istanbulkitapcisi", "9786051856810"))
print(results.get_price("halk", "9786051856810"))  # 9750803734 hata veriyor


# print(results.getPrice("kitapsec", "9789750803734","835 Satır","Nazım Hikmet","Yapı Kredi Yayınları"))#
# 9789750803734 hata veriyor


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
    return results.getprice(site, isbn, name, author, publisher)