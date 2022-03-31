from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from requests_html import HTMLSession
from halk_linkler import allLinksHalk, allSubCategoriesHalk
from kitapsec_linkler import allSubCategoriesKitapsec


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
    def getprice(site, isbn, name, author, publisher):

        s = HTMLSession()

        if site == "amazon":
            url = "https://www.amazon.com.tr/s?k=" + isbn
            img_url = "https://m.media-amazon.com/images/G/41/logo/Amazon_com_tr_Logo._CB1198675309_.jpg"
            print(url)
            r = s.get(url)
            print(r)

            try:
                no_stock = r.html.find('div.a-section.a-spacing-none.a-spacing-top-micro>div', first=True).text.strip()
                if "mevcut değil" in no_stock:
                    return {
                        'site': "amazon.com.tr",
                        'price': "Mevcut değil",
                        'imgUrl': img_url,
                        'link': url,
                    }
            except AttributeError:
                print("fetchPriceAmazon no_stock exception")

            try:
                cant_find = r.html.find('div.a-section.a-spacing-none.s-result-item.s-flex-full-width.s-border-bottom'
                                        '-none.s-widget.s-widget-spacing-large > div > div > div > div:nth-child(1) >'
                                        ' span:nth-child(2)',
                                        first=True).text.strip()
                if "sonuç yok" in cant_find:
                    return {
                        'site': "amazon.com.tr",
                        'price': "Sonuç yok",
                        'imgUrl': img_url,
                        'link': url,
                    }
            except AttributeError:
                print("fetchPriceAmazon cant_find exception")

            try:
                price = r.html.find('span.a-price', first=True).text.strip()
                tl_ix = price.index("TL")
                price_ = price[:tl_ix]
                return {
                    'site': "amazon.com.tr",
                    'price': float(price_.replace(",", ".").replace(" TL", "")),
                    'imgUrl': img_url,
                    'link': url,
                }
            except AttributeError:
                print("fetchAmazon main raised an exception")
                return {
                    'site': "amazon.com.tr",
                    'price': "Hata",
                    'imgUrl': img_url,
                    'link': url,
                }

        elif site == "halk":
            url = "https://www.halkkitabevi.com/index.php?p=Products&q_field_active=0&q=" + isbn
            print(url)
            r = s.get(url)

            img_url = "https://www.halkkitabevi.com/u/halkkitabevi/halk-kitabevi-1580467677-1582817300-1585232584.png"

            try:
                no_stock = r.html.find('div.prd_no_sell', first=True).text.strip()
                if "Stokta yok" in no_stock:
                    return {
                        'site': "Halk Kitabevi",
                        'price': "Stokta yok",
                        'imgUrl': img_url,
                        'link': url,
                    }
            except AttributeError:
                print("fetchHalk noStock raised an exception")

            try:
                cant_find = r.html.find('div.no_product_found', first=True).text.strip()
                if "bulunamadı" in cant_find:
                    return {
                        'site': "Halk Kitabevi",
                        'price': "Bulunamadı",
                        'imgUrl': img_url,
                        'link': url,
                    }
            except AttributeError:
                print("fetchHalk cantFind raised an exception")

            try:
                price = r.html.find('#prd_final_price_display', first=True).text.strip()
                tl_ix = price.index("TL")
                price_ = price[:tl_ix]
                return {
                    'site': "Halk Kitabevi",
                    'price': float(price_.replace(",", ".").replace(" TL", "").replace("TL", "")),
                    'imgUrl': img_url,
                    'link': url,
                }
            except AttributeError:
                print("fetchHalk main raised an exception")
                return {
                    'site': "Halk Kitabevi",
                    'price': "Hata",
                    'imgUrl': img_url,
                    'link': url,
                }
        elif site == "istanbulkitapcisi":
            url = "https://www.istanbulkitapcisi.com/arama?q=" + isbn
            print(url)
            r = s.get(url)

            img_url = "https://www.istanbulkitapcisi.com/wwwroot/images/istanbulkitapcisi-logo.png"

            try:
                no_stock = r.html.find('div.product-info > div.status > a', first=True).text.strip()
                if "Stokta yok" in no_stock:
                    return {
                        'site': "İSTANBUL KİTAPÇISI",
                        'price': "Stokta yok",
                        'imgUrl': img_url,
                        'link': url,
                    }
            except AttributeError:
                print("fetchİstanbul noStock raised an exception")

            try:
                cant_find = r.html.find('#main > div > div', first=True).text.strip()
                if "bulunamadı" in cant_find:
                    return {
                        'site': "İSTANBUL KİTAPÇISI",
                        'price': "Bulunamadı",
                        'imgUrl': img_url,
                        'link': url,
                    }
            except AttributeError:
                print("fetchİstanbul cantFind raised an exception")

            try:
                price = r.html.find('div.product-info > div.product-price', first=True).text.strip()
                return {
                    'site': "İSTANBUL KİTAPÇISI",
                    'price': float(price.replace(",", ".").replace(" TL", "").replace("TL", "")),
                    'imgUrl': img_url,
                    'link': url,
                }
            except AttributeError:
                print("fetchİstanbul main raised an exception")
                return {
                    'site': "İSTANBUL KİTAPÇISI",
                    'price': "Hata",
                    'imgUrl': img_url,
                    'link': url,
                }
        elif site == "kitapsec":
            url = "https://www.kitapsec.com/Arama/index.php?a=" + isbn
            # print(url)
            r = s.get(url)
            try:
                cant_find = r.html.find('div.Ks_BodyBack > div > div > div > div:nth-child(2) > div',
                                        first=True).text.strip()
                if "bulunamadı" in cant_find:
                    raise Exception
            except AttributeError:
                raise Exception("fetchKitapsec exception")
                # print("fetchKitapsec exception")

            img_url = "https://cdn.kitapsec.com//temalar/KitapSec2017/img/logo.jpg"

            price = r.html.find('#prd_final_price_display', first=True).text.strip()
            tl_ix = price.index("TL")
            price_ = price[:tl_ix]
            return {
                'site': "Kitapseç",
                'price': float(price_.replace(",", ".").replace(" TL", "").replace("TL", "")),
                'imgUrl': img_url,
                'link': url,
            }
        elif site == "tele1":
            url = "https://tele1kitap.com/?s=" + isbn
            print(url)
            r = s.get(url)

            img_url = "https://tele1kitap.com/files/img/tele1kitap-logo.png"

            try:
                no_stock = r.html.find('div > div > button > span', first=True).text.strip()
                if "TÜKENDİ" in no_stock:
                    return {
                        'site': "TELE1 KİTAP",
                        'price': "TÜKENDİ",
                        'imgUrl': img_url,
                        'link': url,
                    }
            except AttributeError:
                print("fetchTele1 noStock raised an exception")
                return {
                    'site': "TELE1 KİTAP",
                    'price': "Bulunamadı",
                    'imgUrl': img_url,
                    'link': url,
                }

            try:
                price = r.html.find('div.product-item-price > span', first=True).text.strip()
                return {
                    'site': "TELE1 KİTAP",
                    'price': float(price.replace(",", ".").replace(" TL", "").replace("TL", "")),
                    'imgUrl': img_url,
                    'link': url,
                }
            except AttributeError:
                print("fetchTele1 main raised an exception")
                return {
                    'site': "TELE1 KİTAP",
                    'price': "Hata",
                    'imgUrl': img_url,
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
print(results.getprice("tele1", "9786254180767", "", "", ""))
print(results.getprice("istanbulkitapcisi", "9786254180767", "", "", ""))
print(results.getprice("amazon", "9786254180767", "", "", ""))  # 9750803734 hata veriyor
print(results.getprice("halk", "9786254180767", "", "", ""))  # 9750803734 hata veriyor


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
