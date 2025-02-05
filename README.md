#  Web Scrapping - SmartSniffer

O projeto **Smart Sniffer** é uma ferramenta desenvolvida para realizar a raspagem de informações de estabelecimentos existentes no **Google Maps**. 
Através de um script personalizado, a ferramenta extrai dados do Google Maps, trata as informações obtidas e as armazena em um **DataFrame** para melhor visualização e análise.

## Funcionalidades do Script

O script realiza a **extração automatizada de dados** de estabelecimentos no Google Maps com base nos parâmetros fornecidos pelo usuário, como tipo de estabelecimento e localização. Ele coleta os seguintes dados de cada estabelecimento:

1. **Nome do Estabelecimento**
2. **Endereço completo com CEP**
3. **Total de Avaliações**
4. **Média de Avaliações**
5. **Tipo de Estabelecimento**
6. **Contato do Estabelecimento**

Após coletar os dados, o script trata os dados coletados removendo duplicatas e espaços desnecessarios, armazena as informações em um **DataFrame** e salva em formatos **CSV** e **XLSX** para fácil análise posterior.

## Passos para Execução

1. **Definir parâmetros**: O usuário precisa inserir o tipo de estabelecimento (por exemplo, "Restaurante", "Loja") e a localização (por exemplo, "São Paulo"), além de definir a quantidade mínima de estabelecimentos a serem coletados.
   
2. **Processamento**: O script realiza a pesquisa no Google Maps e coleta as informações de cada estabelecimento que aparece nos resultados. Durante a coleta, o script utiliza **Selenium** para simular a navegação, realizar o scroll da página e acessar as informações de cada estabelecimento de forma dinâmica.

3. **Tratamento de Dados**: As informações extraídas são tratadas para garantir a uniformidade dos dados, como a formatação de nomes e endereços em maiúsculas.

4. **Armazenamento**: O DataFrame gerado é salvo em arquivos **CSV** e **XLSX** para facilitar a consulta e o uso posterior.

## Detalhes Técnicos do Script

O script utiliza a biblioteca **Selenium** para realizar a raspagem das informações diretamente no Google Maps. A seguir, estão as etapas principais do script:

- **Abertura do Google Maps**: O script inicia acessando a página do Google Maps.
- **Pesquisa e Scroll**: Realiza a busca pelo tipo de estabelecimento e localização fornecidos, e executa o scroll para carregar todos os resultados.
- **Coleta dos Dados**: Para cada estabelecimento encontrado, o script coleta informações como nome, avaliação, tipo, endereço e telefone.
- **Armazenamento em DataFrame**: Os dados são armazenados em um **DataFrame** do **Pandas** e salvos em arquivos **CSV** e **XLSX**.

## Exemplo de Saída

Os dados extraídos de cada estabelecimento serão organizados nas seguintes colunas:

- **NOME DO ESTABELECIMENTO**
- **MÉDIA DE AVALIAÇÕES**
- **QUANTIDADE DE AVALIAÇÕES**
- **TIPO DE ESTABELECIMENTO**
- **CONTATO DO ESTABELECIMENTO**
- **ENDEREÇO COMPLETO**
- **LOGRADOURO**
- **NUMERO**
- **BAIRRO**
- **CEP**


Além disso, o script possui um mecanismo de **log** para registrar possíveis erros durante o processo de raspagem.

## Requisitos

- Python 3.x
- Selenium
- Pandas
- WebDriver do Chrome (ChromeDriver)

## Instalação de Dependências/Requisitos

Para iniciar o projeto, siga os passos abaixo para baixar e instalar todas as dependências necessárias:

1. Clone o repositório:
    ```bash
    git clone https://github.com/usuario/scripping.git
    ```
2. Navegue até o diretório do projeto:
    ```bash
    cd scripping
    ```
3. Crie um Ambiente Virtual
    ```bash
    python -m venv .venv
    ```
4. Ative o Ambiente Virtual 
    ```bash
    .\.venv\Scripts\Activate.ps1
    ```
5. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

## Inicialização do Algoritmo

Após a instalação das dependências, você pode inicializar o algoritmo com o seguinte comando:

```bash
python main/main.py
```

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e pull requests no repositório.

## Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo `LICENSE` para mais detalhes.
