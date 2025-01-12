from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import json

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 3)

munis = []

results = {}

with open("municipios.txt", "r", encoding="utf-8") as file:
    for line in file:
        munis.append(line.strip())

driver.get('https://www.google.com.br/maps')

for municipio in munis:
    search_bar = wait.until(EC.presence_of_element_located((By.ID, 'searchboxinput')))
    search_bar.clear()
    search_bar.send_keys(f'Bairros de {municipio}')
    
    search_icon = wait.until(EC.presence_of_element_located((By.ID, 'searchbox-searchbutton')))
    search_icon.click()

    try:
        divSideBar = wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, f"div[aria-label='Resultados para Bairros de {municipio}']")
        ))

        keepScrolling = True
        while keepScrolling:
            divSideBar.send_keys(Keys.PAGE_DOWN)
            time.sleep(0.5)

            html = driver.find_element(By.TAG_NAME, "html").get_attribute('outerHTML')
            if "Você chegou ao final da lista." in html:
                keepScrolling = False

        neighborhoods = []
        i = 1
        while True:
            try:
                bairro = wait.until(EC.presence_of_element_located(
                    (By.XPATH, f'//*[@id="QA0Szd"]/div/div/div[1]/div[2]/div/div[1]/div/div/div[1]/div[1]/div[{i}]/div/div[2]/div[4]/div[1]/div/div/div[2]/div[1]')
                ))
                ActionChains(driver).scroll_to_element(bairro).perform()
                
                neighborhoods.append(bairro.text)
                i += 2
            except:
                break
        
        results[municipio] = neighborhoods
    except:
        print(f'No results found for {municipio}.')
        results[municipio] = municipio
        continue

driver.quit()

with open("results.json", "w", encoding="utf-8") as json_file:
    json.dump(results, json_file, ensure_ascii=False, indent=4)

print("Results saved to results.json")