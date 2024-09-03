### INICIALIZAÇÃO
## IMPORTAR BIBLIOTECAS

from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import json
from requests import post
import pandas as pd
import time


Autor = 'Daniel Bianchi dos Santos'
Data_atual = datetime.now().strftime('%Y-%m-%d')

## IMPORTAR O WEBDRIVER DO CHROME E MAXIMIZAR A JANELA

options = Options()
options.add_argument("--start-maximized")

#serviço que instala o chrome driver correspondente a versão do chrome atual
service = Service(ChromeDriverManager().install())
navigator = webdriver.Chrome(service=service, options=options)

## INICIAR UM DICIONARIO CONTENDO *AUTOR* E *DATA ATUAL*
dictionary = {'Autor': Autor, 'Data': Data_atual}

### NAVEGAÇÃO
## ACESSAR O PORTAL DA TRANSPARÊNCIA https://portaldatransparencia.gov.br/
navigator.get("https://portaldatransparencia.gov.br/")
time.sleep(2)

## Clicar no botão “despesas e receitas”.
navigator.find_element(By.XPATH,'//*[@id="despesas-card"]').click()
time.sleep(2)

## Clicar no item “Consulta” dentro do submenu “receitas”.
navigator.find_element(By.XPATH,'//*[@id="receitas-links"]/li[2]/a').click()
time.sleep(2)

## Clicar no ícone “baixar” em “Tabela de dados”.
navigator.find_element(By.XPATH,'//*[@id="btnBaixar"]').click()
time.sleep(2)


### PROCESSAMENTO DE DADOS
## Ler o arquivo CSV baixado utilizando PANDAS
path = 'C:/Users/Daniel Bianchi/Downloads/receitas.csv'

df = pd.read_csv(path, sep=';')

cols = ['Órgão', 'Espécie', 'Orçamento Atualizado (Valor Previsto)', 'Receita Realizada (Valor Arrecadado)']

df2 = df[cols]

data = df2.to_json(orient="records", indent=4)

data_list = json.loads(data)

dictionary['Dados'] = data_list

url = 'https://devbunnycofco.azurewebsites.net/acontador.aspx'

response = post(url, json=dictionary)

print(f"Status: {response.status_code}")