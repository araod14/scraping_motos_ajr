from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

import pandas as pd

import time
import requests


service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)


#Iniciar el navegador
driver.get('https://www.nilmoto.com/')

moto='Honda CRF 1100L AFRICA TWIN'

buscarmoto = WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.XPATH,'//*[@id="search"]')))
buscarmoto.send_keys(moto)

buscadorboton = WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.XPATH,'//*[@id="search-form"]/button')))
buscadorboton.click()

time.sleep(3)

result = []
# Añadir los valores a la lista de resultados
def scrape_page():
    ## Datos a guardar
    links = driver.find_elements(By.XPATH, '//div[@class="product-info"]//h4/a')
    titles = driver.find_elements(By.XPATH, '//div[@class="product-info"]//h4/a')
    prices = driver.find_elements(By.XPATH, '//div[@class="product-info"]/h5')
    image_urls = driver.find_elements(By.XPATH, '//div[@class="single-product"]/a/img')
    #count = 0

    for i in range(len(links)):
        image_url = image_urls[i].get_attribute("src")
        link = links[i].get_attribute("href")
        alt = image_urls[i].get_attribute("alt")
        result.append({
            "Title": titles[i].text,
            "Price": prices[i].text,
            "Image": image_urls[i].get_attribute("src"),
            "Link": links[i].get_attribute("href")
        })

        # Descargar la imagen
        response = requests.get(image_url)
        if response.status_code == 200:
            try:
                #count += 1
                # Guardar la imagen en un archivo
                image_file = open(f"{alt}.jpg", "wb")
                image_file.write(response.content)
                image_file.close()
            except FileNotFoundError:
                print("No se encontró el archivo:", alt)
            continue

scrape_page()

nextpage = driver.find_elements(By.XPATH, '//div[@class="col-lg-9 col-md-9 col-sm-12 col-xs-12"]/div[@class="shop-item-filter"]/div[@class="shop-tab clearfix"]/div[@class="pagination-container"]/ul/li[2]/a')

if nextpage:
    nextpage1 = WebDriverWait(driver, 60).until(ec.element_to_be_clickable(nextpage[0]))
    nextpage1.click()
    scrape_page()

nextpage3 = driver.find_elements(By.XPATH, '//div[@class="col-lg-9 col-md-9 col-sm-12 col-xs-12"]/div[@class="shop-item-filter"]/div[@class="shop-tab clearfix"]/div[@class="pagination-container"]/ul/li[4]/a')
if nextpage3:
    nextpage3b = WebDriverWait(driver, 60).until(ec.element_to_be_clickable(nextpage3[0]))
    nextpage3b.click()
    scrape_page()

nextpage4 = driver.find_elements(By.XPATH, '//div[@class="col-lg-9 col-md-9 col-sm-12 col-xs-12"]/div[@class="shop-item-filter"]/div[@class="shop-tab clearfix"]/div[@class="pagination-container"]/ul/li[5]/a')
if nextpage4:
    nextpage4b = WebDriverWait(driver, 60).until(ec.element_to_be_clickable(nextpage4[0]))
    nextpage4b.click()
    scrape_page()

nextpage5 = driver.find_elements(By.XPATH, '//div[@class="col-lg-9 col-md-9 col-sm-12 col-xs-12"]/div[@class="shop-item-filter"]/div[@class="shop-tab clearfix"]/div[@class="pagination-container"]/ul/li[6]/a')
if nextpage5:
    nextpage5b = WebDriverWait(driver, 60).until(ec.element_to_be_clickable(nextpage5[0]))
    nextpage5b.click()
    scrape_page()

nextpage6 = driver.find_elements(By.XPATH, '//div[@class="col-lg-9 col-md-9 col-sm-12 col-xs-12"]/div[@class="shop-item-filter"]/div[@class="shop-tab clearfix"]/div[@class="pagination-container"]/ul/li[7]/a')
if nextpage6:
    nextpage6b = WebDriverWait(driver, 60).until(ec.element_to_be_clickable(nextpage6[0]))
    nextpage6b.click()
    scrape_page()

#Crear el dataframe y guardarlo en un archivo CSV
df = pd.DataFrame(result)
df.to_csv(f'{moto}.csv', index=False)
