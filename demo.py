import crawler

main_pages_to_crawl = [
    "https://www.emol.com/noticias/Nacional"
]

#using firefox driver as default
dataframe = crawler.crawl_and_pandaize(main_pages_to_crawl, MAX_PAGES_TO_CRAWL=20)
display(dataframe)