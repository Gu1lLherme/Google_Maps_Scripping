import pandas as pd
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (NoSuchElementException, 
                                        StaleElementReferenceException, 
                                        TimeoutException)

# Configuração do logging para registro de erros
logging.basicConfig(
    filename='scraping_errors.log',
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class GoogleMapsScraper:
    def __init__(self):
        self.driver = None
        self.dados = []
        self.ignored_exceptions = (NoSuchElementException, 
                                 StaleElementReferenceException, 
                                 TimeoutException)
        
    def initialize_driver(self):
        """Inicializa o WebDriver do Chrome com opções configuradas"""
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument("--disable-notifications")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.implicitly_wait(5)

    def accept_cookies(self):
        """Aceita os cookies se o pop-up aparecer"""
        try:
            cookie_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Aceitar todos os cookies"]'))
            )
            cookie_button.click()
        except Exception as e:
            logging.warning("Pop-up de cookies não encontrado")

    def perform_search(self, query):
        """Realiza a pesquisa no Google Maps"""
        search_box = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, "searchboxinput"))
        )
        search_box.clear()
        search_box.send_keys(query)
        search_box.send_keys(Keys.RETURN)

    def scroll_to_load_results(self):
        """Rolagem dinâmica para carregar todos os resultados"""
        scrollable_div = WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//div[@role="feed"]'))
        )
        
        last_height = self.driver.execute_script(
            "return arguments[0].scrollHeight", scrollable_div
        )
        
        while True:
            self.driver.execute_script(
                "arguments[0].scrollBy(0, 1500);", scrollable_div
            )
            time.sleep(2)
            
            new_height = self.driver.execute_script(
                "return arguments[0].scrollHeight", scrollable_div
            )
            
            if new_height == last_height:
                break
            last_height = new_height

    def extract_contact_info(self):
        """Extrai informações de contato de maneira robusta"""
        try:
            contact_section = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Telefone")]/ancestor::div[@class="Io6YTe"]'))
            )
            return contact_section.text
        except Exception:
            return "Contato não disponível"

    def process_listing(self, element):
        """Processa cada listing individualmente"""
        try:
            ActionChains(self.driver).move_to_element(element).perform()
            element.click()
            
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "m6QErb"))
            )
            
            listing_data = {
                "NOME": self.get_text('//h1[@class="DUwDvf lfPIob"]'),
                "MED.AVALIACOES": self.get_text('//div[@class="F7nice "]/span[1]/span'),
                "QNT.AVALIACOES": self.get_text('//div[@class="F7nice "]/span[2]/span'),
                "ENDERECO": self.get_text('//div[@data-item-id="address"]//div[@class="Io6YTe"]'),
                "INF.ADICIONAIS": self.get_text('//div[@class="skqShb"]'),
                "CONTATO": self.extract_contact_info()
            }
            
            self.dados.append(listing_data)
            
        except Exception as e:
            logging.error(f"Erro ao processar listing: {str(e)}")

    def get_text(self, xpath):
        """Método auxiliar para extração segura de texto"""
        try:
            return WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            ).text
        except Exception:
            return "N/A"

    def run(self, query, output_file):
        """Método principal para execução do scraper"""
        try:
            self.initialize_driver()
            self.driver.get("https://www.google.com/maps")
            self.accept_cookies()
            self.perform_search(query)
            self.scroll_to_load_results()
            
            listings = WebDriverWait(self.driver, 20).until(
                EC.presence_of_all_elements_located((By.XPATH, '//a[contains(@class, "hfpxzc")]'))
            )
            
            for index, listing in enumerate(listings[:10]):  # Teste com 10 resultados
                try:
                    self.process_listing(listing)
                except Exception as e:
                    logging.error(f"Erro no item {index}: {str(e)}")
                    continue
            
            df = pd.DataFrame(self.dados)
            df.to_csv(output_file, index=False)
            print(f"Dados salvos com sucesso em {output_file}")
            
        finally:
            if self.driver:
                self.driver.quit()

if __name__ == "__main__":
    scraper = GoogleMapsScraper()
    scraper.run(
        query="Veículos em Aracaju, SE",
        output_file="leads_veiculos_aracaju.csv"
    )