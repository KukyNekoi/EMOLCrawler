#%%
from selenium import webdriver
import time
import pandas

def extract_news_from_url(url, crawl_level, driver, sleep_interval):
    # return structurpage_indexe
    title = []
    description = []
    content = []
    news_link = []
    parent_link = []
    page_index = []

    def extract_concatenated_content(driver, selector, print_afterwards=False):
        body_elements = driver.find_elements_by_css_selector(selector)
        body_content = [content.text for content in body_elements]
        body = " ".join(body_content)
        if print_afterwards:
            print(body)
        return body


    for page_idx in range(0, crawl_level + 1):
        driver.get(url)
        time.sleep(sleep_interval)

        if (page_idx > 0):
            nextpage_js = "SelectPage(" + str(page_idx) + ")"
            driver.execute_script(nextpage_js)
            time.sleep(sleep_interval)

        links_noticias = driver.find_elements_by_id("LinkNoticia")
        links = [el.get_attribute("href") for el in links_noticias]
        for current_link  in links:
            print("link: " + str(current_link))
            print("page: " + str(page_idx))
            print("base_href: " + str(url))
        
            driver.get(current_link)
            time.sleep(sleep_interval)

            title_cont = extract_concatenated_content(driver, "#cuDetalle_cuTitular_tituloNoticia", True)
            desc_cont = extract_concatenated_content(driver, "#cuDetalle_cuTitular_bajadaNoticia", True)
            cont_cont = extract_concatenated_content(driver, "#cuDetalle_cuTexto_textoNoticia > div", True)

            # save into structure
            title.append(title_cont)
            description.append(desc_cont)
            content.append(cont_cont)
            news_link.append(current_link)
            parent_link.append(url)
            page_index.append(page_idx)

    return {
        "title": title,
        "description": description,
        "content": content,
        "news_link": news_link,
        "parent_link": parent_link,
        "page_index": page_index
    }

def crawl_and_pandaize(main_pages_to_crawl, MAX_PAGES_TO_CRAWL = 1, driver = webdriver.Firefox(), sleep_interval=1):
    target_dataframe = None

    for target_url in main_pages_to_crawl:
        current_df = pandas.DataFrame.from_dict(extract_news_from_url(
            main_pages_to_crawl = target_url,
            MAX_PAGES_TO_CRAWL = MAX_PAGES_TO_CRAWL, 
            driver=driver, 
            sleep_interval=sleep_interval))
            
        if target_dataframe is None:
            target_dataframe = current_df
        else:
            target_dataframe = pandas.concat([target_dataframe, current_df])

    return target_dataframe

#%%
