from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from requests_html import HTMLSession
import math
from halk_linkler import allLinksHalk, allSubCategoriesHalk
from kitapsec_linkler import allLinksKitapsec, allSubCategoriesKitapsec
from queries import *


class Scraper:

    @staticmethod
    def scrapedata(site, kategori, altkategori, sorgu, sayfa):

        s = HTMLSession()
        all_list = []
        results_list = []

        if sorgu.isdigit():
            print("sorgu is digit")
            if site == "halk":
                r = s.get("https://www.halkkitabevi.com/index.php?p=Products&q_field_active=0&q=" + sorgu)
            else:
                r = s.get("https://www.kitapsec.com/Arama/index.php?a=" + sorgu)

            try:
                title = r.html.find(title_queries_d[site], first=True).text.strip()
            except AttributeError:
                title = ''
            try:
                img = r.html.find(img_queries_d[site], first=True).attrs[img_attrs_d[site]]
            except AttributeError:
                img = ''
            try:
                img_alt = r.html.find(img_alt_queries_d[site], first=True).attrs[img_alt_attrs_d[site]]
            except AttributeError:
                img_alt = ''
            try:
                publisher = r.html.find(publisher_queries_d[site], first=True).text.strip()
            except AttributeError:
                publisher = ''
            try:
                author = r.html.find(author_queries_d[site], first=True).text.strip()
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
            all_list.append(results_list)
            all_list.append([
                {
                    "lastPage": 0,
                },
            ])
        else:
            print("sorgu is not digit")
            if sorgu == "null":
                print("sorgu is null")
                if site == "halk":
                    link = allLinksHalk[int(kategori)][int(altkategori)]
                else:
                    link = allLinksKitapsec[int(kategori)][int(altkategori)]
                print(link)
            else:
                print("sorgu is not null")
                if site == "halk":
                    link = "https://www.halkkitabevi.com/index.php?p=Products&q_field_active=0&q=" \
                           + sorgu + "&page=" + sayfa
                else:
                    link = "https://www.kitapsec.com/Arama/index.php?a=" \
                           + to_ascii(sorgu) + "&arama=" + sayfa
                print(link)
            r = s.get(link)
            results_ = r.html.find(main_queries_nd[site])
            for res in results_:
                try:
                    title = res.find(title_queries_nd[site], first=True).attrs[title_attrs_nd[site]]
                except AttributeError:
                    title = ''
                try:
                    img = res.find(img_queries_nd[site], first=True).attrs[img_attrs_nd[site]]
                except AttributeError:
                    img = ''
                try:
                    img_alt = res.find(img_alt_queries_nd[site], first=True).attrs[img_alt_attrs_nd[site]]
                except AttributeError:
                    img_alt = ''
                try:
                    link = res.find(ind_link_queries_nd[site], first=True).attrs[ind_link_attrs_nd[site]]
                except AttributeError:
                    link = ''
                try:
                    publisher = res.find(publisher_queries_nd[site], first=True).text.strip()
                except AttributeError:
                    publisher = ''
                try:
                    author = res.find(author_queries_nd[site], first=True).text.strip()
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
            all_list.append(results_list)
            last_page = 0
            try:
                lp0 = r.html.find(last_page_queries[site], first=True)
                if site == "halk":
                    lp1 = lp0.attrs['href']
                    page_index = lp1.index("page=")
                    lp2 = lp1[page_index:]
                    last_page = int(lp2.replace("page=", ""))
                else:
                    lp1 = lp0.text.strip()
                    page_index = lp1.index(": ")
                    lp2 = lp1[page_index:]
                    lp3 = lp2.replace(": ", "")
                    last_page = math.ceil(int(lp3) / len(results_))
            except AttributeError:
                pass
            all_list.append([
                {
                    "lastPage": last_page,
                },
            ])
        return all_list

    @staticmethod
    def get_price(site, isbn, name, author, publisher):

        s = HTMLSession()

        url = search_urls[site] + " " + name + " " + author + " " + publisher \
            if site == "kitapyurdu" else search_urls[site] + isbn

        # print(url)

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
            return return_(site, price.replace(",", ".").replace(" TL", "").replace("TL", "")
                           .replace("Site Fiyatı: ", ""), url)
        except AttributeError:
            # print(f"{site} main raised an exception")
            return return_(site, "Hata", url)


def return_(site, price, url):
    return {
        'site': site_names[site],
        'price': price,
        'link': url,
    }


def to_ascii(mystring):
    return mystring.replace("ü", "%FC").replace("Ü", "%DC") \
        .replace("ı", "%FD").replace("ö", "%F6").replace("Ö", "%D6") \
        .replace("Ç", "%C7").replace("ç", "%E7").replace("Ğ", "%D0") \
        .replace("ğ", "%F0").replace("Ş", "%DE").replace("ş", "%FE").replace("İ", "%DD")


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

# print(results.scrapedata("halk", "2", "0", "null", "1"))
print(results.scrapedata("kitapsec", "2", "0", "null", "1"))


# print(results.get_price("kitapyurdu", "9786257303576", "Pençe", "Elif Sofya", "EVEREST YAYINLARI"))
# print(results.get_price("kitapsepeti", "9786257303576", "Pençe", "Elif Sofya", "EVEREST YAYINLARI"))
# print(results.get_price("babil", "9786257303576", "Pençe", "Elif Sofya", "EVEREST YAYINLARI"))
# print(results.get_price("tele1", "9786257303576", "Pençe", "Elif Sofya", "EVEREST YAYINLARI"))
# print(results.get_price("kitapsec", "9786257303576", "Pençe", "Elif Sofya", "EVEREST YAYINLARI"))
# print(results.get_price("pandora", "9786257303576", "Pençe", "Elif Sofya", "EVEREST YAYINLARI"))
# print(results.get_price("amazon", "9786257303576", "Pençe", "Elif Sofya", "EVEREST YAYINLARI"))
# # 9750803734 hata veriyor
# print(results.get_price("eganba", "9786257303576", "Pençe", "Elif Sofya", "EVEREST YAYINLARI"))
# print(results.get_price("idefix", "9786257303576", "Pençe", "Elif Sofya", "EVEREST YAYINLARI"))
# print(results.get_price("eganba", "9786257303576", "Pençe", "Elif Sofya", "EVEREST YAYINLARI"))
# print(results.get_price("dr", "9786257303576", "Pençe", "Elif Sofya", "EVEREST YAYINLARI"))
# print(results.get_price("istanbulkitapcisi", "9786257303576", "Pençe", "Elif Sofya", "EVEREST YAYINLARI"))
# print(results.get_price("halk", "9786257303576", "Pençe", "Elif Sofya", "EVEREST YAYINLARI"))


# 9750803734 hata veriyor


# print(results.getPrice("kitapsec", "9789750803734","835 Satır","Nazım Hikmet","Yapı Kredi Yayınları"))#
# 9789750803734 hata veriyor


@app.get("/0/{site}/{kategori}/{altkategori}/{sorgu}/{sayfa}")
async def get_results(site, kategori, altkategori, sorgu, sayfa):
    return results.scrapedata(site, kategori, altkategori, sorgu, sayfa)


@app.get("/{site}/{index}")
async def get_subcategories(site, index):
    if site == "kitapsec":
        return allSubCategoriesKitapsec[int(index)]
    elif site == "halk":
        return allSubCategoriesHalk[int(index)]


@app.get("/1/{site}/{isbn}/{name}/{author}/{publisher}")
async def get_results(site, isbn, name, author, publisher):
    return results.get_price(site, isbn, name, author, publisher)
