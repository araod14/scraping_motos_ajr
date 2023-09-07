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
driver.get('https://www.ubricarmotos.com/')

moto='Honda CRF 1100L AFRICA TWIN'
time.sleep(3)
buscarmoto = WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.XPATH,'//*[@id="search_widget"]/div/form/input[2]')))
buscarmoto.send_keys(moto)
time.sleep(4)
driver.maximize_window()
buscador = WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.XPATH,'//*[@id="search_widget"]/div/form/button')))
buscador.click()#send_keys(moto)

time.sleep(50)

## Datos a guardar
result = []

def scrape_page():
    links = driver.find_elements(By.XPATH, '//a[@class="dfd-card-link"]')
    titles = driver.find_elements(By.XPATH, '//div[@class="dfd-card-title"]')
    prices = driver.find_elements(By.XPATH, '//div[@class="dfd-card-pricing"]/span[1]')
    image_urls = driver.find_elements(By.XPATH, '//div[@class="dfd-card-media"]/div/img')

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
