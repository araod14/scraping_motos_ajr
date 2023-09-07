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
driver.get('https://buy2race.com/es/')

moto='Honda CRF 1100L AFRICA TWIN'

buscador = WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.XPATH,'//*[@id="search_widget"]/form/input[2]')))
buscador.click()#send_keys(moto)

buscarmoto = WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.XPATH,'//*[@id="df-searchbox__dffullscreen"]')))
buscarmoto.send_keys(moto)

time.sleep(3)

    ## Datos a guardar
result = []
links = driver.find_elements(By.XPATH, '//div[@class="df-card"]/a')
titles = driver.find_elements(By.XPATH, '//div[@class="df-card__title"]')
availitys = driver.find_elements(By.XPATH, '//div[@class="df-card__pricing"]/span/span')
prices = driver.find_elements(By.XPATH, '//span[@class="df-card__price "]')
image_urls = driver.find_elements(By.XPATH, '//figure/img')

    # Añadir los valores a la lista de resultados
for i in range(len(links)):
    image_url = image_urls[i].get_attribute("src")
    link = links[i].get_attribute("href")
    #alt = image_urls[i].get_attribute("src")
    result.append({
        "Title": titles[i].text,
        "Availity": availitys[i].get_attribute("class"),
        "Price": prices[i].text,
        "Image": image_urls[i].get_attribute("src"),
        "Link": links[i].get_attribute("href")
    })
    # Descargar la imagen
    response = requests.get(image_url)
    if response.status_code == 200:
        # Guardar la imagen en un archivo
        image_file = open(f"image_{i}.jpg", "wb")
        image_file.write(response.content)
        image_file.close()

    else:
        print("No se pudo descargar la imagen del enlace:")

# Crear el dataframe
df = pd.DataFrame(result)
df.to_csv(f'{moto}.csv', index=False)
print(df)
