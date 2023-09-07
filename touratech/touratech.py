from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service

import pandas as pd

import time
import requests
"""

"""

service = Service()
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

#Iniciar el navegador
driver.get('https://touratech.es/')

time.sleep(6)

moto='Honda CRF 1100L AFRICA TWIN'

#cokie = WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.XPATH,'//*[@id="lgcookieslaw_banner"]/div/div/div[4]/button[2]')))
#cokie.click()
driver.maximize_window()

buscador = WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.XPATH,'//*[@id="search_button"]')))
buscador.click()#send_keys(moto)

#buscador1 = WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.XPATH,'//*[@id="searchbox"]/button')))
#buscador1.click()#send_keys(moto)

#buscarmoto = WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.XPATH,'//*[@id="dfd-searchbox-id-AGk8d-input"]')))
#buscarmoto.send_keys(moto)

time.sleep(30)


## Datos a guardar
result = []

def scrape_page():
    links = driver.find_elements(By.XPATH, '//div[@class="dfd-card-content dfd-card-flex"]/a')
    titles = driver.find_elements(By.XPATH, '//div[@class="dfd-card-title"]')
    prices = driver.find_elements(By.XPATH, '//div[@class="dfd-card-pricing"]/span')
    image_urls = driver.find_elements(By.XPATH, '//div[@class="dfd-card-thumbnail"]/img')

    # Añadir los valores a la lista de resultados
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
