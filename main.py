from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from requests_html import HTMLSession

class Scraper():
    def scrapedata(self, site, sorgu):
        # url = 'https://www.kitapsec.com/Arama/index.php?a=Astronomi&AnaKat=Bilim-Kitaplari'
        s = HTMLSession()
        # r = s.get(url)
        # r = s.get(sorgu)
        # print(r.status_code)

        results_list = []
        if site == "kitapsec":
            r = s.get(sorgu)
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
            if "index.php?" not in sorgu:
                r = s.get("https://www.halkkitabevi.com/index.php?p=Products&" + sorgu)
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
                    results_list.append(item)
            else :
                r = s.get(sorgu)
                item = {
                        'title' : r.html.find('div > div.col2.__col2 > h1', first=True).text.strip(),
                        'img' : r.html.find('#main_img', first=True).attrs['src'],
                        'img_alt' : r.html.find('#main_img', first=True).attrs['data-zoom-image'],
                        'link' : sorgu,
                        'publisher' : r.html.find('div.prd_brand_box > a.publisher', first=True).text.strip(),
                        'author' : r.html.find('div.prd_info > div.writer > a', first=True).text.strip(),
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

@app.get("/site/{site}/sorgu/{sorgu}")
async def get_results(site, sorgu):
    return results.scrapedata(site, sorgu)