import pandas as pd
import os
import re
import time
import logging
from src.tratamentoDados import create_data_frame, dados_format, extrair_endereco, save_data
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

# ==================== LOGS DE ERRO ====================

# Criar diretório 'logs' se não existir
log_dir = "C:\\Users\\gesbarreto\\Downloads\\SmartSniffer\\src\\logs"
os.makedirs(log_dir, exist_ok=True)

# Caminho completo do arquivo de log
log_file = os.path.join(log_dir, "smartSniffer.log")

# Configuração do logging
logging.basicConfig(
    filename= log_file,
    level=logging.ERROR, 
    format="%(asctime)s - %(message)s"
)

# Inicio do time 
inicio = time.time()

# ==================== INICIO DO ALGORTIMO ====================

# = ==== = Definição de estabelecimento e localização = = ==== =
try:
    print("===" * 10 + " SCRAPPING GOOGLE MAPS " + "===" *  10)
    print("Digite o tipo de estabelecimento e a localização para pesquisar no Google Maps.")
    
    entrada_tipo_estabelecimento = str(input("Tipo de estabelecimento a ser pesquisado: "))
    localizacao = str(input("Localização: "))
    qtd_minima_estabelencimentos = int(input("Quantidade Minima de Estabelecimentos: "))
    pesquisa = f"{entrada_tipo_estabelecimento} em {localizacao}"
    
    print("===" * 25)
except:
    print("Erro ao definir a pesquisa. Tente novamente.")
    exit()
    
    
# Inicializa o WebDriver

options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Para rodar em background
driver = webdriver.Chrome(options=options)

try:
    # Acessa o Google Maps
    driver.get("https://www.google.com/maps/")
    assert "Google Maps" in driver.title
    
    print("Google Maps acessado com sucesso!")
    
    # Encontra a caixa de pesquisa e digita o termo
    search_box = driver.find_element(By.ID, "searchboxinput")
    search_box.send_keys(pesquisa, Keys.RETURN)

    # Maximiza a janela
    driver.maximize_window()

    # Aguarda os resultados carregarem
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "hfpxzc"))
    )

    # = == = Realiza o scroll para carregar todos os resultados = == =
    # Rolagem da página
    scrollable_div = driver.find_element(By.CSS_SELECTOR, 'div[role="feed"]')
    driver.execute_script(
        """
        var scrollableDiv = arguments[0];
        function scrollWithinElement(scrollableDiv) {
            return new Promise((resolve, reject) => {
                var totalHeight = 0;
                var distance = 1000;
                var scrollDelay = 4500;
                
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
    """,
        scrollable_div,
    )

    # Armazena temporariamente os dados de cada estabelecimento
    dados = []

    # Localizar todos os resultados dos estabelecimentos
    estabelecimentos = driver.find_elements(By.CLASS_NAME, "hfpxzc")

    # Limita a coleta a no máximo 5 estabelecimentos
    estabelecimentos = estabelecimentos[:5]
    

    print(f"Encontrados {len(estabelecimentos)} estabelecimentos.")
    print("===" * 30)
    
    # Verifica se a quantidade de estabelecimentos é maior que a 
    # quantidade mínima para realizar a coleta dos dados
    if int(len(estabelecimentos)) > qtd_minima_estabelencimentos:
       
        # Iterar sobre os resultados e coletar as informações desejadas
        for index, estabelecimento in enumerate(estabelecimentos):    
            try:
                print(f"Coletando dados do item {index + 1} de {len(estabelecimentos)}...")
                
                # Certificar que o elemento está visível antes de clicar
                WebDriverWait(driver, 20).until(EC.element_to_be_clickable(estabelecimento))
                
                # Rola a tela até o elemento usando JavaScript
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", estabelecimento)
                time.sleep(1)  # Pequena pausa para garantir visibilidade

                # Move para o elemento antes de clicar
                actions = ActionChains(driver)
                actions.move_to_element(estabelecimento).perform()
                estabelecimento.click()
                time.sleep(4)  # Espera para carregar os detalhes

                # Espera o sidebar abrir
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "m6QErb"))
                )

                # Coleta de Dados
                try:
                    nome = driver.find_element(
                        By.XPATH, "//h1[@class='DUwDvf lfPIob']"
                    ).text
                except:
                    nome = "Nome não encontrado"

                try:
                    media_avaliacoes = driver.find_element(
                        By.XPATH, "//div[@class='F7nice ']//span[@aria-hidden='true']"
                    ).text
                except:
                    media_avaliacoes = "Média de avaliações não disponível"

                try:
                    qtd_avaliacoes = driver.find_element(
                        By.XPATH, '//div[@class="F7nice "]/span[2]/span'
                    ).text
                except:
                    qtd_avaliacoes = "Quantidade de avaliações não disponível"

                try:
                    endereco = driver.find_element(
                        By.XPATH, '//div[@class="rogA2c "]/div'
                    ).text
                except:
                    endereco = "Endereço não disponível"

                try:
                    tipo_estabelecimento = driver.find_element(
                        By.XPATH,
                        "/html/body/div[1]/div[3]/div[8]/div[9]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/div[2]/span[1]/span",
                    ).text
                except:
                    tipo_estabelecimento = "Informação adicional não disponível"

                try:
                    # Coleta todos os elementos com a classe do telefone/endereço
                    divs = driver.find_elements(By.CLASS_NAME, "Io6YTe")

                    contato = "Contato não disponível"

                    # Percorre os elementos e verifica qual contém um telefone
                    for div in divs:
                        texto = div.text
                        if re.search(r'\(\d{2}\) \d{4,5}-\d{4}', texto):  # Verifica se tem um telefone válido
                            contato = texto
                            break  # Para no primeiro telefone encontrado

                except Exception as e:
                    contato = "Erro ao coletar telefone"
                    
                # Adicionar os dados à lista
                dados.append(
                    [
                        nome,
                        media_avaliacoes,
                        qtd_avaliacoes,
                        tipo_estabelecimento,
                        contato,
                        endereco                   
                    ]
                )

            except Exception as e:
                logging.error(f"Erro no item {index}: {str(e)}")
                continue
    else:        
        driver.quit()
        print(f"Quantidade de estabelecimentos encontrados é menor que a quantidade mínima de {qtd_minima_estabelencimentos}.")

    # ==================== TRATAMEMTO DE DADODS ====================

    df = create_data_frame(dados)
    df = dados_format(df)
    
    
    # Aplicar a função em cada linha do DataFrame
    df[["LOGRADOURO", "NUMERO", "BAIRRO", "CEP"]] = df["ENDERECO COMPLETO"].apply(
        lambda x: pd.Series(extrair_endereco(x)))
        
    # Dados Salvos
    save_data(df, pesquisa)

except Exception as e:
    print(f"Erro ao coletar dados: {str(e)}")

finally:
    # ==================== FIM DO ALGORTIMO ====================
    driver.quit()
    fim = time.time()
    tempo_total = ((fim - inicio) / 60) # Tempo total de execução
    print(f"Tempo total de extração: {tempo_total:.0f} minutos")
