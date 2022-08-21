from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
import time

urlpag = 0
blk = []
prc =[]
lnk =[]
pag = []

def pagin ():
    global urlpag
    urlpag += 1
    URL = 'https://www.dns-shop.ru/catalog/17a89aab16404e77/videokarty/?f[mv]=udtf8&p='
    URL = URL + str(urlpag)     # Увеличиваем значение URL на 1
    return URL

def write():
    Value = zip(blk,prc,lnk)
    Value_list = list(Value)

    with open("Pars.csv", "w", encoding="utf8") as file:
        file.write(",\n".join(map(str, Value_list)).replace('(','').replace(')','').replace('[','').replace(']','').replace('"','').replace("'",""))

def option ():
    global bloks, price, link
    options = webdriver.ChromeOptions()
    options.add_argument("start-maximized")

    # options.add_argument("--headless")

    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    driver = webdriver.Chrome(options=options)

    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    url = pagin()
    driver.get(url)
    time.sleep(1)
    bloks = driver.find_element(By.CLASS_NAME, "products-list__content").find_elements(By.TAG_NAME, 'a')
    price = driver.find_elements(By.CLASS_NAME, "product-buy__price")
    link = driver.find_elements(By.CLASS_NAME, "catalog-product__image-link")

    for i in link:
        lnk.append(i.get_attribute('href'))
    for i in price:
        prc.append(i.text)
    for i in bloks:
        if i.find_elements(By.TAG_NAME, "span"):
            res = str(i.text.split('\n'))
            if res.find('3080') != -1:
                blk.append(res)

    for i in price:
        pag.append(i.text)
    if pag != []:
        pag.clear()
        driver.quit()
        option()
    else:
        write()
        driver.quit()

option ()






