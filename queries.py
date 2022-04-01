site_names = {
    "idefix" : "idefix",
    "eganba" : "eganba",
    "dr" : "D&R",
    "istanbulkitapcisi" : "İSTANBUL KİTAPÇISI",
    "halk": "Halk Kitabevi",
    "kidega" : "kidega",
    "amazon": "amazon.com.tr",
    "pandora" : "paNdora",
    "kitapsec" : "kitapseç",
    "tele1" : "TELE1 kitap",
}

search_urls = {
    "idefix" : "https://www.idefix.com/search?q=",
    "eganba" : "https://www.eganba.com/arama?q=",
    "dr" : "https://www.dr.com.tr/search?q=",
    "istanbulkitapcisi" : "https://www.istanbulkitapcisi.com/arama?q=",
    "halk": "https://www.halkkitabevi.com/index.php?p=Products&q_field_active=0&q=",
    "kidega" : "https://kidega.com/arama/",
    "amazon": "https://www.amazon.com.tr/s?k=",
    "pandora" : "https://www.pandora.com.tr/Arama/?type=9&isbn=",
    "kitapsec" : "https://www.kitapsec.com/Arama/index.php?a=",
    "tele1" : "https://tele1kitap.com/?s=",
}

price_queries = {
    "idefix" : "#prices",
    "eganba" : "div.product-info > div.product-price",
    "dr" : "div.prd-price-wrapper.dr-flex-start.flex-wrap > div > div",
    "istanbulkitapcisi" : "div.product-info > div.product-price",
    "halk": "#prd_final_price_display",
    "kidega" : "#plhUrun_satisFiyat",
    "amazon": "span.a-price",
    "pandora" : "p.indirimliFiyat",
    "kitapsec" : "span.fiyat > font.satis",
    "tele1" : "div.product-item-price > span",
}

no_stock_queries = {
    "idefix" : "div.box-line-4 > span",
    "eganba" : "div.product-info > div.status > a",
    "dr" : "div.prd-buttons > div > span",
    "istanbulkitapcisi" : "div.product-info > div.status > a",
    "halk": "div.prd_no_sell",
    "kidega" : "div.noStock",
    "amazon": "div.a-section.a-spacing-none.a-spacing-top-micro>div",
    "pandora" : "",
    "kitapsec" : "",
    "tele1" : "div > div > button > span",
}

not_found_queries = {
    "idefix" : "div.container.PageNotFoundCont > div > div > h3",
    "eganba" : "#main > div > div > h4",
    "dr" : "div > div > div > h3",
    "istanbulkitapcisi" : "#main > div > div",
    "halk": "div.no_product_found",
    "kidega" : "#ctl00_u10_ascArama_urun_ascUrunList_lblKayitSayisi > div",
    "amazon": "div.a-section.a-spacing-none.s-result-item.s-flex-full-width.s-border-bottom-none.s-widget.s-widget-spacing-large > div > div > div",
    "pandora" : "p:nth-child(1) > strong",
    "kitapsec" : "div.Ks_BodyBack > div > div > div > div:nth-child(2) > div",
    "tele1" : "",
}

no_stock_phrases = {
    "idefix" : "Stokta Yok",
    "eganba" : "Stokta yok",
    "dr" : "Stokta Yok",
    "istanbulkitapcisi" : "Stokta yok",
    "halk": "Stokta yok",
    "kidega" : "Tükendi",
    "amazon": "mevcut değil",
    "pandora" : "",
    "kitapsec" : "",
    "tele1" : "TÜKENDİ",
}

not_found_phrases = {
    "idefix" : "bulunamadı",
    "eganba" : "bulunamadı",
    "dr" : "bulunamadı",
    "istanbulkitapcisi" : "bulunamadı",
    "halk": "bulunamadı",
    "kidega" : "0 adet",
    "amazon": "sonuç yok",
    "pandora" : "bulunamadı",
    "kitapsec" : "bulunamadı",
    "tele1" : "",
}

