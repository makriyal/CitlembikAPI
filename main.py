from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from requests_html import HTMLSession

class Scraper():
    def scrapedata(self):
        url = 'https://www.kitapsec.com/Arama/index.php?a=Astronomi&AnaKat=Bilim-Kitaplari'
        s = HTMLSession()
        r = s.get(url)
        print(r.status_code)

        qlist = []
        quotes = r.html.find('div.Ks_UrunSatir')
        for q in quotes :
            item = {
                'title' : q.find('a.img > img', first=True).attrs['title'],
                'img' : q.find('a.img > img', first=True).attrs['src'],
                'img_alt' : q.find('a.img > img', first=True).attrs['data-src'],
                'link' : q.find('a.text', first=True).attrs['href'],
                'publisher' : q.find('span.yynImg > div > a', first=True).text.strip(),
                'author' : q.find('span[itemprop=author]', first=True).text.strip(),
            }
            print(item)
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

@app.get("/")
async def read_item():
    return quotes.scrapedata()