import pandas as pd
import openpyxl 
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

# Configuração do logging
logging.basicConfig(filename='scraping.log', level=logging.ERROR, format='%(asctime)s - %(message)s')

# Pesquisa a ser realizada
pesquisa = "Veiculos em Aracaju, SE"

# Determina o Navegador a ser usado
driver = webdriver.Chrome()

# Site de coleta dos dados
driver.get("https://www.google.com/maps/")

# Verificar se a página é a correta
assert "Google Maps" in driver.title

# Encontra a caixa de pesquisa
search_box = driver.find_element(by=By.ID, value="searchboxinput")

# Digita o conteúdo na caixa de pesquisa e clicar em Enter
search_box.send_keys(pesquisa)
search_box.send_keys(Keys.RETURN)

# Maximiza o tamanho da janela
driver.maximize_window()

# Aguardar os resultados carregarem
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "hfpxzc")))

# Rolagem da página
scrollable_div = driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')
driver.execute_script("""
    var scrollableDiv = arguments[0];
    function scrollWithinElement(scrollableDiv) {
        return new Promise((resolve, reject) => {
            var totalHeight = 0;
            var distance = 1000;
            var scrollDelay = 3000;
            
            var timer = setInterval(() => {
                var scrollHeightBefore = scrollableDiv.scrollHeight;
                scrollableDiv.scrollBy(0, distance);
                totalHeight += distance;

                if (totalHeight >= scrollHeightBefore) {
                    totalHeight = 0;
                    setTimeout(() => {
                        var scrollHeightAfter = scrollableDiv.scrollHeight;
                        if (scrollHeightAfter > scrollHeightBefore) {
                            return;
                        } else {
                            clearInterval(timer);
                            resolve();
                        }
                    }, scrollDelay);
                }
            }, 200);
        });
    }
    return scrollWithinElement(scrollableDiv);
""", scrollable_div)

try:
    # Armazena temporariamente os dados de cada estabelecimento
    dados = []

    # Localizar todos os resultados dos estabelecimentos
    estabelecimentos = driver.find_elements(By.CLASS_NAME, "hfpxzc")
    
    # Iterar sobre os resultados e coletar as informações desejadas
    for index, estabelecimento in enumerate(estabelecimentos):
        try:
             # Certificar que o elemento está visível antes de clicar
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "hfpxzc"))
            )

            # Move para o elemento antes de clicar
            actions = ActionChains(driver)
            actions.move_to_element(estabelecimento).perform()

            # Clica no estabelecimento
            estabelecimento.click()
            time.sleep(3)  # Pequena espera para carregar os detalhes

            # Espera o sidebar abrir
            sidebar = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, "m6QErb"))
            )

            '''# Clicar no estabelecimento 
            estabelecimento.click()
            time.sleep(2)
            
            # Guarda o conteudo da nova janela 
            card_elements =  driver.find_elements(By.CLASS_NAME, 'm6QErb')
            
            # Clicar no estabelecimento 
            WebDriverWait(driver, 20, 2).until(EC.presence_of_element_located((By.XPATH, '//div[@role="feed"]//a[contains(@href, "maps/place")]')))
            
            # Guarda o conteúdo da nova janela aberta  
            for elemento in card_elements:'''
                
            # Coleta de Dados
            try: 
                # Nome do estabelecimento
                nome = estabelecimento.find_element(By.XPATH, "//h1[@class='DUwDvf lfPIob']").text
            except:
                nome = "Nome não encontrado"
            
            try:
                # Média de avaliações
                media_avaliacoes = estabelecimento.find_element(By.XPATH, "//div[@class='F7nice ']//span[@aria-hidden='true']").text
            except:
                media_avaliacoes = "Média de avaliações não disponível"
            
            try:
                # Quantidade de avaliações
                qtd_avaliacoes = estabelecimento.find_element(By.XPATH, '//div[@class="F7nice "]/span[2]/span').text
            except:
                qtd_avaliacoes = "Quantidade de avaliações não disponível"
            
            try:
                # Endereço com CEP
                endereco = estabelecimento.find_element(By.XPATH, '//div[@class="rogA2c "]/div').text    
            except:
                endereco = "Endereço não disponível"
            
            try:
                # Informações adicionais, como status de funcionamento
                tipo_estabelecimento = estabelecimento.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[8]/div[9]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/div[2]/span[1]/span').text
            except:
                tipo_estabelecimento = "Informação adicional não disponível"
            
            try:
                contato = estabelecimento.find_element(By.CSS_SELECTOR, 'div.RcCsl:nth-child(8) > button:nth-child(2) > div:nth-child(1) > div:nth-child(2) > div:nth-child(1)').text
                
            except:
                contato = "Contato não disponível"

            # Adicionar os dados à lista
            dados.append([nome, media_avaliacoes, qtd_avaliacoes, endereco, tipo_estabelecimento, contato])
        
        
        except Exception as e:
            
            logging.error(f"Erro no item {index}: {str(e)}")
            continue

    # Cria o DataFrame com os dados coletados
    df = pd.DataFrame(dados, columns=["NOME", "MED.AVALIACOES", "QNT.AVALIACOES", "ENDERECO", "INF.ADICIONAIS", "CONTATO"])

    # Tratamento de dados
    df["NOME"] = df["NOME"].str.upper()
    df['ENDERECO'] = df['ENDERECO'].str.upper()

    # Salvar o DataFrame em um arquivo .xlsx e .csv
    df.to_excel("C:\\Users\\gesbarreto\\Downloads\\SCRIPPING\\Resultados\\estabelecimentos.xlsx", index=False)
    df.to_csv("C:\\Users\\gesbarreto\\Downloads\\SCRIPPING\\Resultados\\estabelecimentos.csv", index=False)

    # Fechar o driver
    print("Dados salvos com sucesso em CSV e XLSX!")


finally:
    driver.quit()