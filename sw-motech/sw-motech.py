from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

import pandas as pd

import time
import requests
"""
falta loop de paginas y resolver tema availity
"""

service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

#Iniciar el navegador
driver.get('https://sw-motech.com/es/')

moto='Honda CRF 1100L AFRICA TWIN'

permitircookie = WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.XPATH,'//*[@id="klaro"]/div/div/div/div[2]/button[1]')))
permitircookie.click()#send_keys(moto)

selectcountry = WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.XPATH,'//*[@id="geo_country"]')))
selectcountry.click()#send_keys(moto)

espana =driver.find_element(By.XPATH,'//*[@id="geo_country"]/option[27]')
driver.execute_script("window.scrollTo(0,document.body.scrollHeight)",espana)
espana.click()

selectlang = WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.XPATH,'//*[@id="geo_language"]')))
selectlang.click()#send_keys(moto)

spanish =driver.find_element(By.XPATH,'//*[@id="geo_language"]/option[1]')
spanish.click()

continueto = WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.XPATH,'/html/body/div[10]/div/div/div[4]/div[2]')))
continueto.click()#send_keys(moto)


buscarmoto = WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.XPATH,'//*[@id="suchbegriff"]')))
buscarmoto.send_keys(moto)

buscador = WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.XPATH,'//*[@id="sPlusForm"]/div[2]')))
buscador.click()#send_keys(moto)

numerodepag = WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.XPATH,'//*[@id="searchResults"]/div[2]/form/div[2]/select')))
numerodepag.click()#send_keys(moto)

pag192 = driver.find_element(By.XPATH,'//*[@id="searchResults"]/div[2]/form/div[2]/select/option[4]')
pag192.click()#send_keys(moto)

time.sleep(3)


    ## Datos a guardar
result = []
links = driver.find_elements(By.XPATH, '//div[@class="descriptionBox"]/a')
titles = driver.find_elements(By.XPATH, '//div[@class="descriptionBox"]/a/span')
#availitys = driver.find_elements(By.XPATH, '//div[@class="lieferzeit"]/span[2]/text()')
prices = driver.find_elements(By.XPATH, '//article/div[@class="priceBox"]/div[@class="preisformat"]/div[@class="priceRow"]/span[@class="price font-7 color-3"]/span')
image_urls = driver.find_elements(By.XPATH, '//div[@class="pictureContainer"]/a/img')

    # Añadir los valores a la lista de resultados
def scrape_page():
    for i in range(len(links)):
        image_url = f'https://sw-motech.com/cosmoshop/default/pix/{image_urls[i].get_attribute("data-src")}'
        link = links[i].get_attribute("href")
        alt = image_urls[i].get_attribute("alt")
        result.append({
            "Title": titles[i].text,
            "Price": prices[i].text,
            "Image": image_urls[i].get_attribute("data-src"),
            "Link": links[i].get_attribute("href")
        })
        # Descargar la imagen
        response = requests.get(image_url)
        if response.status_code == 200:
            try:
                # Guardar la imagen en un archivo
                image_file = open(f"{alt}.jpg", "wb")
                image_file.write(response.content)
                image_file.close()

            except FileNotFoundError:
                    print("No se encontró el archivo:", alt)
            continue

scrape_page()

# Crear el dataframe
df = pd.DataFrame(result)
df.to_csv(f'{moto}.csv', index=False)
print(df)
