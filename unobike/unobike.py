from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

import pandas as pd

import time
import requests
"""
falta loop de paginas y resolver tema PRECIO
"""

service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

#Iniciar el navegador
driver.get('https://www.unobike.com/')

moto='Honda CRF 1100L AFRICA TWIN'

driver.maximize_window()

buscarmoto = WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.XPATH,'//*[@id="menu"]/div/div/div[2]/div[1]/app-search/form/div/input')))
buscarmoto.send_keys(moto)

buscador = WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.XPATH,'//*[@id="menu"]/div/div/div[2]/div[1]/app-search/form/div/div/button')))
buscador.click()#send_keys(moto)

time.sleep(3)


    ## Datos a guardar
result = []

def scrape_page():
    links = driver.find_elements(By.XPATH, '//div[@class="ficha-bloque"]/a')
    titles = driver.find_elements(By.XPATH, '//div[@class="bloque-texto no-gutters"]/h3')
    #marcas = driver.find_elements(By.XPATH, '//div[@class="lieferzeit"]/span[2]/text()')
    prices = driver.find_elements(By.XPATH, '//p[@class="pvplistado"]')
    image_urls = driver.find_elements(By.XPATH, '//div[@class="thumb"]/img')

        # Añadir los valores a la lista de resultados
    
    for i in range(len(links)):
        image_url = image_urls[i].get_attribute("src")
        link = links[i].get_attribute("href")
        alt = image_urls[i].get_attribute("alt")
        price = prices[i].text if i < len(prices) else None
        result.append({
            "Title": titles[i].text,
            "Price": prices,
            "Image": image_urls[i].get_attribute("src"),
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

time.sleep(15)
scrape_page()

while True:
    nextpage = driver.find_elements(By.XPATH, '//div[@class="mat-paginator-range-actions"]/button[@class="mat-focus-indicator mat-tooltip-trigger mat-paginator-navigation-next mat-icon-button mat-button-base"]')

    if nextpage:
        nextpage2 = WebDriverWait(driver, 60).until(ec.element_to_be_clickable(nextpage[0]))
        nextpage2.click()
        time.sleep(15)
        scrape_page()
    else:
        break

# Crear el dataframe
df = pd.DataFrame(result)
df.to_csv(f'{moto}.csv', index=False)
print(df)
