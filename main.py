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

@app.get("/{site}/{kategori}/{altkategori}/{link}/{sorgu}/{sayfa}")
async def get_results(site, kategori, altkategori, link, sorgu, sayfa):
    return results.scrapedata(site, kategori, altkategori, link, sorgu, sayfa)


@app.get("/{site}/{index}")
async def get_subcategories(site, index):
    if site == "kitapsec":
        return allSubCategoriesKitapsec[int(index)]
    elif site == "halk":
        return allSubCategoriesHalk[int(index)]
    
