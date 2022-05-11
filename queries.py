site_names = {
    "idefix": "idefix",
    "eganba": "eganba",
    "dr": "D&R",
    "istanbulkitapcisi": "İSTANBUL KİTAPÇISI",
    "halk": "Halk Kitabevi",
    "kidega": "kidega",
    "amazon": "amazon.com.tr",
    "pandora": "paNdora",
    "kitapsec": "kitapseç",
    "tele1": "TELE1 kitap",
    "babil": "babil",
    "oda": "oda kitap",
    "kitapsepeti": "kitapsepeti",
    "kitapyurdu": "kitapyurdu.com",
}

main_urls = {
    "idefix": "https://www.idefix.com/",
    "eganba": "https://www.eganba.com/",
    "dr": "https://www.dr.com.tr/",
    "istanbulkitapcisi": "https://www.istanbulkitapcisi.com/",
    "halk": "https://www.halkkitabevi.com/",
    "kidega": "https://kidega.com/",
    "amazon": "https://www.amazon.com.tr/",
    "pandora": "https://www.pandora.com.tr/",
    "kitapsec": "https://www.kitapsec.com/",
    "tele1": "https://tele1kitap.com/",
    "babil": "https://www.babil.com/",
    "oda": "https://www.odakitap.com/",
    "kitapsepeti": "https://www.kitapsepeti.com/",
    "kitapyurdu": "https://www.kitapyurdu.com/",
}

search_urls = {
    "idefix": "https://www.idefix.com/search?q=",
    "eganba": "https://www.eganba.com/arama?q=",
    "dr": "https://www.dr.com.tr/search?q=",
    "istanbulkitapcisi": "https://www.istanbulkitapcisi.com/arama?q=",
    "halk": "https://www.halkkitabevi.com/index.php?p=Products&q_field_active=0&q=",
    "kidega": "https://kidega.com/arama/",
    "amazon": "https://www.amazon.com.tr/s?k=",
    "pandora": "https://www.pandora.com.tr/Arama/?type=9&isbn=",
    "kitapsec": "https://www.kitapsec.com/Arama/index.php?a=",
    "tele1": "https://tele1kitap.com/?s=",
    "babil": "https://www.babil.com/search?q=",
    "oda": "https://www.odakitap.com/arama?q=",
    "kitapsepeti": "https://www.kitapsepeti.com/index.php?p=Products&q_field_active=0&ctg_id=&q=",
    "kitapyurdu": "https://www.kitapyurdu.com/index.php?route=product/search&filter_name=",
}

price_queries = {
    "idefix": "#prices",
    "eganba": "div.product-info > div.product-price",
    "dr": "div.prd-price-wrapper.dr-flex-start.flex-wrap > div > div",
    "istanbulkitapcisi": "div.product-info > div.product-price",
    "halk": "#prd_final_price_display",
    "kidega": "#plhUrun_satisFiyat",
    "amazon": "span.a-price",
    "pandora": "p.indirimliFiyat",
    "kitapsec": "span.fiyat > font.satis",
    "tele1": "div.product-item-price > span",
    "babil": "ul.price > li:nth-child(1)",
    "oda": "span.new-price",
    "kitapsepeti": "#prd_final_price_display",
    "kitapyurdu": "div.price-new > span.value",
}

no_stock_queries = {
    "idefix": "div.box-line-4 > span",
    "eganba": "div.product-info > div.status > a",
    "dr": "div.prd-buttons > div > span",
    "istanbulkitapcisi": "div.product-info > div.status > a",
    "halk": "div.prd_no_sell",
    "kidega": "div.noStock",
    "amazon": "div.a-section.a-spacing-none.a-spacing-top-micro>div",
    "pandora": "",
    "kitapsec": "",
    "tele1": "div > div > button > span",
    "babil": "article > small",
    "oda": "div.status",
    "kitapsepeti": "div.actions > div > span > span",
    "kitapyurdu": "",
}

not_found_queries = {
    "idefix": "div.container.PageNotFoundCont > div > div > h3",
    "eganba": "#main > div > div > h4",
    "dr": "div > div > div > h3",
    "istanbulkitapcisi": "#main > div > div",
    "halk": "div.no_product_found",
    "kidega": "#ctl00_u10_ascArama_urun_ascUrunList_lblKayitSayisi > div",
    "amazon": "div.a-section.a-spacing-none.s-result-item.s-flex-full-width.s-border-bottom-none.s-widget.s-widget"
              "-spacing-large > div > div > div",
    "pandora": "p:nth-child(1) > strong",
    "kitapsec": "div.Ks_BodyBack > div > div > div > div:nth-child(2) > div",
    "tele1": "",
    "babil": "section > p",
    "oda": "h4",
    "kitapsepeti": "div.no_product_found",
    "kitapyurdu": "div.product-not-found",
}

no_stock_phrases = {
    "idefix": "Stokta Yok",
    "eganba": "Stokta yok",
    "dr": "Stokta Yok",
    "istanbulkitapcisi": "Stokta yok",
    "halk": "Stokta yok",
    "kidega": "Tükendi",
    "amazon": "mevcut değil",
    "pandora": "",
    "kitapsec": "",
    "tele1": "TÜKENDİ",
    "babil": "Tükendi",
    "oda": "Stokta yok",
    "kitapsepeti": "Tükendi",
    "kitapyurdu": "",
}

not_found_phrases = {
    "idefix": "bulunamadı",
    "eganba": "bulunamadı",
    "dr": "bulunamadı",
    "istanbulkitapcisi": "bulunamadı",
    "halk": "bulunamadı",
    "kidega": "0 adet",
    "amazon": "sonuç yok",
    "pandora": "bulunamadı",
    "kitapsec": "bulunamadı",
    "tele1": "",
    "babil": "bulunamamıştır",
    "oda": "bulunamadı",
    "kitapsepeti": "bulunamadı",
    "kitapyurdu": "bulamadık",
}

details_main_queries = {
    "halk": "div.__product_fields > div",
    "kitapsec": "div.detayBilgiDiv > div > div",
    "kitapyurdu": "tr",
}

details_main_urls = {
    "halk": "https://www.halkkitabevi.com/",
    "kitapsec": "https://www.kitapsec.com/Products/",
    "kitapyurdu": "https://www.kitapyurdu.com/kitap/",
}

description_queries = {
    "halk": "div.prd_description > p",
    "kitapsec": "#tab1 > p",
    "kitapyurdu": "#description_text",
}

# nd : not digit
main_queries_nd = {
    "halk": "div.prd_list_container_box > div > ul > li > div",
    "kitapsec": "div.Ks_UrunSatir",
    "kitapyurdu": "div.product-cr",
}

title_queries_nd = {
    "halk": "a>img",
    "kitapsec": "a.img > img",
    "kitapyurdu": "div.image > div.cover > a.pr-img-link > img",
}

title_queries_d = {
    "halk": "div > div.col2.__col2 > h1",
    "kitapsec": "a.text > span",
    "kitapyurdu": "",
}

img_queries_nd = {
    "halk": "a>img",
    "kitapsec": "a.img > img",
    "kitapyurdu": "div.image > div.cover > a.pr-img-link > img",
}

img_queries_d = {
    "halk": "#main_img",
    "kitapsec": "a.img > img",
    "kitapyurdu": "",
}

img_alt_queries_nd = {
    "halk": "a>img",
    "kitapsec": "a.img > img",
    "kitapyurdu": "div.image > div.cover > a.pr-img-link > img",
}

img_alt_queries_d = {
    "halk": "a>img",
    "kitapsec": "a.img > img",
    "kitapyurdu": "",
}

ind_link_queries_nd = {
    "halk": "a",
    "kitapsec": "a.text",
    "kitapyurdu": "div.image > div.cover > a.pr-img-link",
}

publisher_queries_nd = {
    "halk": "div.prd_info > div.publisher",
    "kitapsec": "span.yynImg > div > a",
    "kitapyurdu": "div.publisher",
}

publisher_queries_d = {
    "halk": "div.prd_brand_box > a.publisher",
    "kitapsec": "span.yynImg > div > a > span",
    "kitapyurdu": "",
}

author_queries_nd = {
    "halk": "div.prd_info > div.writer > a",
    "kitapsec": "span[itemprop=author]",
    "kitapyurdu": "div.author.compact.ellipsis",
}

author_queries_d = {
    "halk": "div.prd_info > div.writer > a",
    "kitapsec": "span[itemprop=author]",
    "kitapyurdu": "",
}

title_attrs_nd = {
    "halk": "title",
    "kitapsec": "title",
    "kitapyurdu": "alt",
}

img_attrs_nd = {
    "halk": "data-src",
    "kitapsec": "src",
    "kitapyurdu": "src",
}

img_attrs_d = {
    "halk": "src",
    "kitapsec": "src",
    "kitapyurdu": "",
}

img_alt_attrs_nd = {
    "halk": "data-src",
    "kitapsec": "data-src",
    "kitapyurdu": "src",
}

img_alt_attrs_d = {
    "halk": "data-zoom-image",
    "kitapsec": "src",
    "kitapyurdu": "",
}

ind_link_attrs_nd = {
    "halk": "href",
    "kitapsec": "href",
    "kitapyurdu": "href",
}

last_page_queries = {
    "halk": "a.button.button_pager.button_pager_last",
    "kitapsec": "div.toplam_sonuc",
    "kitapyurdu": "a.last",
}
