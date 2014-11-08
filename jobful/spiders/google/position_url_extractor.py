from selenium import webdriver


def get_urls_from(base_page):
    driver = webdriver.PhantomJS()
    driver.get(base_page)

    elems = driver.find_elements_by_xpath("//a[@itemprop='url']")
    urls = [str(i.get_attribute("href")).replace("https", "http") for i in elems]
    driver.quit()

    return urls
