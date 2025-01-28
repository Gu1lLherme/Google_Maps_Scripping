import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

# Informações de interesse
"""
NOME DO ESTABELECIMENTO
ENDEREÇO COM CEP
TOTAL DE AVALIZAÇÕES
MEDIA DE AVALIAÇÕES
CONTATO
"""

# Determina o Navegador a ser usado
driver = webdriver.Chrome()

# Site de coleta dos dados
driver.get("https://www.google.com/maps/")

assert "Google Maps" in driver.title
search_box  = driver.find_element(by=By.ID, value="searchboxinput" )
search_box.send_keys("Veiculos em Aracaju, SE")
search_box.send_keys(Keys.RETURN)

# Aguardar os resultados carregarem
time.sleep(5)
# Maximiza o tamanho da janela
driver.maximize_window()

# Localizar todos os resultados dos estabelecimentos
estabelecimentos = driver.find_elements(By.CLASS_NAME, "hfpxzc")

# Abrir arquivo para salvar os dados
with open("estabelecimentos.txt", "w", encoding="utf-8") as file:
    # Iterar sobre os resultados e coletar as informações desejadas
    for estabelecimento in estabelecimentos:

        try:
            # Clicar no estabelecimento
            estabelecimento.click()
            time.sleep(4)

            # Guarda o conteudo da nova janela 
            card_elements =  driver.find_elements(By.CLASS_NAME, 'm6QErb')


            for elemento in card_elements:
       
                ## AGORA COLETA OS DADOS DA NOVA JANELA ABERTA - ENDEREÇO COM CEP PRIORIDADE!!
                try:
                    # Nome do estabelecimento
                    nome = elemento.find_element(By.XPATH, "//h1[@class='DUwDvf lfPIob']").text
                except:
                    nome = "Nome não encontrado"
                
                try:
                    # Média de avaliações
                    media_avaliacoes = elemento.find_element(By.XPATH, "//div[@class='F7nice ']//span[@aria-hidden='true']").text
                except:
                    media_avaliacoes = "Média de avaliações não disponível"
                
                try:
                    # Quantidade de avaliações
                    qtd_avaliacoes = elemento.find_element(By.XPATH, '//div[@class="F7nice "]/span[2]/span').text
                except:
                    qtd_avaliacoes = "Quantidade de avaliações não disponível"
                
                try:
                    # Endereço 
                    endereco = elemento.find_element(By.XPATH, '//div[@class="rogA2c "]/div').text
                    
                except:
                    endereco = "Endereço não disponível"
                
                try:
                    # Informações adicionais, como status de funcionamento
                    tipo_estabelecimento = estabelecimento.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[8]/div[9]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/div[2]/span[1]/span/button').text
                except:
                    tipo_estabelecimento = "Informação adicional não disponível"
                
                try:
                    contato = estabelecimento.find_element(By.XPATH, '/html/body/div[1]/div[3]/div[8]/div[9]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[9]/div[8]/button/div/div[2]/div[1]').text
                except:
                    contato = "Contato não disponível"

            # Escrever no arquivo
            file.write(f"Nome: {nome}\n")
            file.write(f"Média de Avaliações: {media_avaliacoes}\n")
            file.write(f"Quantidade de Avaliações: {qtd_avaliacoes}\n")
            file.write(f"Endereço: {endereco}\n")
            file.write(f"Informações Adicionais: {tipo_estabelecimento}\n")
            file.write(f"Contato: {contato}\n")
            file.write("-" * 50 + "\n")
        except:
            print("Erro ao coletar informações")
            continue

print("CONSULTA FINALIZADA!!")
# Fechar o driver
driver.quit()

