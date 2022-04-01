site_names = {
    "idefix" : "idefix",
    "eganba" : "eganba",
    "dr" : "D&R",
    "istanbulkitapcisi" : "İSTANBUL KİTAPÇISI",
    "halk": "Halk Kitabevi",
}

search_urls = {
    "idefix" : "https://www.idefix.com/search?q=",
    "eganba" : "https://www.eganba.com/arama?q=",
    "dr" : "https://www.dr.com.tr/search?q=",
    "istanbulkitapcisi" : "https://www.istanbulkitapcisi.com/arama?q=",
    "halk": "https://www.halkkitabevi.com/index.php?p=Products&q_field_active=0&q=",
}

price_queries = {
    "idefix" : "#prices",
    "eganba" : "div.product-info > div.product-price",
    "dr" : "div.prd-price-wrapper.dr-flex-start.flex-wrap > div > div",
    "istanbulkitapcisi" : "div.product-info > div.product-price",
    "halk": "#prd_final_price_display",
}

no_stock_queries = {
    "idefix" : "div.box-line-4 > span",
    "eganba" : "div.product-info > div.status > a",
    "dr" : "div.prd-buttons > div > span",
    "istanbulkitapcisi" : "div.product-info > div.status > a",
    "halk": "div.prd_no_sell",
}

not_found_queries = {
    "idefix" : "div.container.PageNotFoundCont > div > div > h3",
    "eganba" : "#main > div > div > h4",
    "dr" : "div > div > div > h3",
    "istanbulkitapcisi" : "#main > div > div",
    "halk": "div.no_product_found",
}

no_stock_phrases = {
    "idefix" : "Stokta Yok",
    "eganba" : "Stokta yok",
    "dr" : "Stokta Yok",
    "istanbulkitapcisi" : "Stokta yok",
    "halk": "Stokta yok",
}

not_found_phrases = {
    "idefix" : "bulunamadı",
    "eganba" : "bulunamadı",
    "dr" : "bulunamadı",
    "istanbulkitapcisi" : "bulunamadı",
    "halk": "bulunamadı",
}

