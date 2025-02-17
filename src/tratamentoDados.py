import re
import pandas as pd

# ==================== SAVE DATA ====================
def create_data_frame(data):
    # Cria o DataFrame com os dados coletados
    DataFrame = pd.DataFrame(data,
    columns=[
        "NOME DO ESTABELECIMENTO",
        "MED.AVALIACOES",
        "QNT.AVALIACOES",
        "TIPO DE ESTABELECIMENTO", 
        "CONTATO DO ESTABELECIMENTO",
        "ENDERECO COMPLETO",
    ],
    )
    return DataFrame


def dados_format(dataFrame):
    
    # Tratamento de dados - Converte todas as colunas de texto para maiúsculas
    colunas_para_maiusculas = ["NOME DO ESTABELECIMENTO", "ENDERECO COMPLETO", "TIPO DE ESTABELECIMENTO"]
    dataFrame[colunas_para_maiusculas] = dataFrame[colunas_para_maiusculas].fillna("").apply(lambda x: x.str.upper())
    
    # Formata o dados e normaliza para retirar as inconscistencias
    palavras_irregulares = {"RUA":"R", "R.": "R", "AVENIDA": "AV", "AV.":"AV"}
    for chave, valor in palavras_irregulares.items():
        dataFrame["ENDERECO COMPLETO"] = dataFrame["ENDERECO COMPLETO"].str.replace(chave, valor)
        
    # Remover as duplicatas existentes no Data Frame 
    dataFrameTrasformado = dataFrame.drop_duplicates()
    return dataFrameTrasformado


# Função para extrair partes do endereço
def extrair_endereco(endereco):
    
    # Inicializa as variáveis
    logradouro, numero, bairro, cep = "", "", "", ""
    
    # Padrão para logradouro: captura tudo antes da primeira vírgula
    padrao_logradouro = r"^([^,]+),"
    
    # Padrão para número: captura tudo entre a vírgula e o primeiro hífen (números, letras e espaços)
    padrao_numero = r",\s*([0-9A-Za-z\s]+?)\s*-"
    
    # Padrão para bairro: captura o texto que aparece após o hífen e antes da vírgula que antecede "ARACAJU"
    padrao_bairro = r"-\s*([^,-]+),\s*ARACAJU\s*- SE"
    
    # Padrão para CEP (formato 00000-000)
    padrao_cep = r"\b\d{5}-\d{3}\b"
    
    # Busca cada parte no endereço
    logradouro_match = re.search(padrao_logradouro, endereco)
    numero_match = re.search(padrao_numero, endereco)
    bairro_match = re.search(padrao_bairro, endereco)
    cep_match = re.search(padrao_cep, endereco)
    
    if logradouro_match:
        logradouro = logradouro_match.group(1).strip()
    
    if numero_match:
        numero = numero_match.group(1).strip()
    
    if bairro_match:
        bairro = bairro_match.group(1).strip()
    
    if cep_match:
        cep = cep_match.group(0).strip().replace("-", " ")
        cep = cep.replace(" ", "")
    
    return logradouro, numero, bairro, cep



def save_data(dataFrame, nome_arquivo):
    
    # Salvar o DataFrame em um arquivo .xlsx e .csv
    dataFrame.to_excel(
        f"C:\\Users\\gesbarreto\Downloads\\SmartSniffer\\src\\resultados\\XLSX\\estabelecimentos_{nome_arquivo}.xlsx",
        index=False,
    )

    dataFrame.to_csv(
        f"C:\\Users\\gesbarreto\\Downloads\\SmartSniffer\\src\\resultados\\CSV\\estabelecimentos_{nome_arquivo}.csv",
        sep=";",
        index=False
    )
    
    print("===" * 25)
    print("Dados salvos com sucesso em CSV e XLSX!")
    print("===" * 25)