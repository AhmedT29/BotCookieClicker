from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import threading

# Variável de controle para parar as threads
running = True

def click_cookie():
    #Função para clicar repetidamente no cookie.
    while running:
        cookie.click()
        time.sleep(0.0001)

def check_upgrades():

    #Função para verificar upgrades de caixa disponíveis periodicamente.
    while running:
        try:
            crate_upgrades_unable = driver.find_element(By.CLASS_NAME, "crate.upgrade")
            crate_ID_unable = crate_upgrades_unable.get_attribute("data-id")
            price = driver.execute_script(f"return Game.UpgradesById[{crate_ID_unable}].basePrice;")
            cookies = driver.execute_script("return Game.cookies;")
            if price*0.2 < cookies:
                WebDriverWait(driver,90).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "crate.upgrade.enabled"))
                )
        except:
            pass
                

        try:
            crate_upgrades = driver.find_elements(By.CLASS_NAME, "crate.upgrade.enabled")
            if crate_upgrades:
                crate_upgrades[0].click()
        except Exception:
            pass
    
        #Função para verificar upgrades disponíveis periodicamente.
        try:
            upgrades = driver.find_elements(By.CLASS_NAME, "product.unlocked.enabled")
            if upgrades:
                upgrades[-1].click()
        except Exception:
            pass
        time.sleep(0.05)  # Verifica upgrades a cada 0.5 segundo



# Configuração do Selenium
driver = webdriver.Chrome()
driver.get("https://orteil.dashnet.org/cookieclicker/")

# Espera até que o botão de idioma esteja presente e clicável
WebDriverWait(driver, 15).until(
    EC.element_to_be_clickable((By.ID, "langSelect-PT-BR"))
).click()

# Espera até que o cookie principal esteja presente
WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.ID, "bigCookie"))
)

# Espera até ser possível nomear padaria
WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.ID, "bakeryName"))
)

#Nomear Padaria
driver.find_element(By.ID, "bakeryName").click()
inputPadaria = driver.find_element(By.ID,"bakeryNameInput")
inputPadaria.clear()
inputPadaria.send_keys("Jalim Habey's")
inputPadaria.send_keys(Keys.ENTER)


#Icone do cookie
cookie = driver.find_element(By.ID,"bigCookie")

# Cria threads para executar as funções simultaneamente
thread1 = threading.Thread(target=click_cookie)
thread2 = threading.Thread(target=check_upgrades)

# Inicia as threads
thread1.start()
thread2.start()

input()

# Para as threads
running = False

# Aguarda as threads terminarem
thread1.join()
thread2.join()

# Fecha o navegador
driver.quit()
