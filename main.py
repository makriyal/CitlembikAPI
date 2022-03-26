from asyncio.windows_events import NULL
from tokenize import Double
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from requests_html import HTMLSession

class Scraper():
    def scrapedata(self, site, sorgu):
        # url = 'https://www.kitapsec.com/Arama/index.php?a=Astronomi&AnaKat=Bilim-Kitaplari'
        s = HTMLSession()
        # r = s.get(url)
        r = s.get(sorgu)
        # print(r.status_code)

        qlist = []
        if site == "kitapsec":
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
                qlist.append(item)
        elif site == "halk":
            if "index.php?" in sorgu:
                results = r.html.find('div.prd_list_container_box > div > ul > li > div')
                for res in results :
                    item = {
                        'title' : res.find('a>img', first=True).attrs['title'],
                        'img' : res.find('a>img', first=True).attrs['data-src'],
                        'img_alt' : res.find('a.img > img', first=True).attrs['data-src'],
                        'link' : res.find('a', first=True).attrs['href'],
                        'publisher' : res.find('div.prd_info > div.publisher', first=True).text.strip(),
                        'author' : res.find('div.prd_info > div.writer > a', first=True).text.strip(),
                    }
                    qlist.append(item)
            else :
                item = {
                        'title' : r.html.find('div > div.col2.__col2 > h1', first=True).text.strip(),
                        'img' : r.html.find('#main_img', first=True).attrs['src'],
                        'img_alt' : r.html.find('#main_img', first=True).attrs['data-zoom-image'],
                        'link' : sorgu,
                        'publisher' : r.html.find('div.prd_brand_box > a.publisher', first=True).text.strip(),
                        'author' : r.html.find('div.prd_info > div.writer > a', first=True).text.strip(),
                    }
                qlist.append(item)
                
        return qlist

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

quotes = Scraper()

@app.get("/{site}/{sorgu}")
async def get_results():
    return quotes.scrapedata()