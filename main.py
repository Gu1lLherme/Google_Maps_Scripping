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
            estabelecimento.click()
            time.sleep(8)

            ## AGORA COLETA OS DADOS DA NOVA JANELA ABERTA - ENDEREÇO COM CEP PRIORIDADE!!
            try:
                # Nome do estabelecimento
                nome = estabelecimento.find_element(By.CLASS_NAME, "qBF1Pd").text
            except:
                nome = "Nome não encontrado"
            
            try:
                # Média de avaliações
                media_avaliacoes = estabelecimento.find_element(By.XPATH, ".//div[contains(@class, 'F7nice ')]/span/span").text
            except:
                media_avaliacoes = "Média de avaliações não disponível"
            
            try:
                # Quantidade de avaliações
                qtd_avaliacoes = estabelecimento.find_element(By.CLASS_NAME, "UY7F9").text
            except:
                qtd_avaliacoes = "Quantidade de avaliações não disponível"
            
            try:
                # Endereço - Pegando o segundo spand do terceiro span da classe W4Efsd 
                endereco = estabelecimento.find_element(By.XPATH, './/div[contains(@class,"W4Efsd")]/span[3]/span[2]').text
            except:
                endereco = "Endereço não disponível"
            
            try:
                # Informações adicionais, como status de funcionamento
                tipo_estabelecimento = estabelecimento.find_element(By.XPATH, './/div[contains(@class, "W4Efsd")][2]/div[contains(@class,"W4Efsd")]/span/span').text
            except:
                tipo_estabelecimento = "Informação adicional não disponível"
            try:
                contato = estabelecimento.find_element(By.CLASS_NAME, "UsdlK").text
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
# preciso coletar o CEP
# Classe de resultados class="m6QErb DxyBCb kA9KIf dS8AEf XiKgde ecceSd" campo 
# a qual exibe os resultados de estabelecimentos encontrados

# local dos textos class="UaQhfb fontBodyMedium"

# Classe do nome dos Estabelecimentos Titulo class="qBF1Pd fontHeadlineSmall "
# Classe da Media das avaliações class="MW4etd"
# Classe quantidade de avaliações class="UY7F9"
#class="W4Efsd" 

#<div class="W4Efsd"><span><span>Concessionária</span></span><span> <span aria-hidden="true">·</span> <span class="google-symbols" aria-label="Entrada acessível para pessoas em cadeira de rodas" role="img" data-tooltip="Entrada acessível para pessoas em cadeira de rodas" jsaction="focus:pane.focusTooltip; blur:pane.blurTooltip" style="font-size: 15px;"><span class="doJOZc"></span></span></span><span> <span aria-hidden="true">·</span> <span>Av. Maranhão, 12</span></span></div>