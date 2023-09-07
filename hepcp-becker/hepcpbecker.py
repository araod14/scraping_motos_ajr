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
driver.get('https://www.hepco-becker.es/')

moto='Honda CRF 1100L AFRICA TWIN'
time.sleep(5)
#buttonbcokie = WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.XPATH,'//*[@id="lgcookieslaw_banner"]/div/div/div[4]/button[2]')))
#buttonbcokie.click()#send_keys(moto)

buscarmoto = WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.XPATH,'//*[@id="search_widget"]/form/input[2]')))
buscarmoto.send_keys(moto)

driver.maximize_window()

time.sleep(5)
buscador = WebDriverWait(driver, 60).until(ec.element_to_be_clickable((By.XPATH,'//*[@id="search_widget"]/form/button')))
buscador.click()#send_keys(moto)

time.sleep(3)
## Datos a guardar
result = []
    # Añadir los valores a la lista de resultados
def scrape_page():
    time.sleep(3)
    links = driver.find_elements(By.XPATH, '//h2[@class="h3 product-title"]/a')
    titles = driver.find_elements(By.XPATH, '//h2[@class="h3 product-title"]/a')
    prices = driver.find_elements(By.XPATH, '//span[@class="price"]')
    image_urls = driver.find_elements(By.XPATH, '//div[@class="thumbnail-container"]/a[@class="thumbnail product-thumbnail"]/img')  

    for i in range(len(links)):
        image_url = image_urls[i].get_attribute("src")
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
time.sleep(6)
scrape_page()

nextpage = driver.find_element(By.XPATH, '//div[@class="col-md-6 offset-md-2 pr-0"]/ul/li[3]/a')
if nextpage:
   nextpage2 = WebDriverWait(driver, 60).until(ec.element_to_be_clickable(nextpage))
   nextpage2.click()
   time.sleep(6)
   scrape_page()

"""
nextpage3 = driver.find_element(By.XPATH, '//div[@class="col-md-6 offset-md-2 pr-0"]/ul/li[7]/a')
if nextpage3:
    nextpage3 = WebDriverWait(driver, 60).until(ec.element_to_be_clickable(nextpage3))
    nextpage3.click()
    time.sleep(6)
    scrape_page()

nextpage4 = driver.find_element(By.XPATH, '//div[@class="col-md-6 offset-md-2 pr-0"]/ul/li[7]/a')
if nextpage4:
    nextpage4 = WebDriverWait(driver, 60).until(ec.element_to_be_clickable(nextpage4))
    nextpage4.click()
    time.sleep(6)
    scrape_page()

nextpage5 = driver.find_element(By.XPATH, '//div[@class="col-md-6 offset-md-2 pr-0"]/ul/li[7]/a')
if nextpage5:
    nextpage5 = WebDriverWait(driver, 60).until(ec.element_to_be_clickable(nextpage5))
    nextpage5.click()
    time.sleep(6)
    scrape_page()

nextpage6 = driver.find_elements(By.XPATH, '//div[@class="col-md-6 offset-md-2 pr-0"]/ul/li[7]/a/@href')
if nextpage6:
    nextpage6 = WebDriverWait(driver, 60).until(ec.element_to_be_clickable(nextpage6))
    nextpage6.click()
    scrape_page()
"""
# Crear el dataframe
df = pd.DataFrame(result)
df.to_csv(f'{moto}.csv', index=False)
print(df)
