### INICIALIZAÇÃO
## IMPORTAR BIBLIOTECAS

import json
import os
import subprocess
import time
from datetime import datetime
from warnings import catch_warnings

from requests import post
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

task_name = "Verhaw2"
python_path = r"C:\Users\Daniel Bianchi\AppData\Local\Programs\Python\Python312\python.exe"  # Caminho do executável do Python
script_path = os.path.abspath(__file__)
path = f'C:/Users/Daniel Bianchi/Downloads/receitas-{datetime.now().strftime('%Y-%m-%d')}.csv'

command = f"""
schtasks /create /tn "{task_name}" /tr "{python_path} \"{script_path}\"" /sc once /rl highest /f
"""
subprocess.run(command, shell=True)

Autor = 'Daniel Bianchi dos Santos'
Data_atual = datetime.now().strftime('%Y-%m-%d')

## IMPORTAR O WEBDRIVER DO CHROME E MAXIMIZAR A JANELA
try:
    dictionary = {'Autor': Autor, 'Data': Data_atual}

    df = pd.read_csv(path, sep=';')
except FileNotFoundError:
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
    _path = 'C:/Users/Daniel Bianchi/Downloads/receitas.csv'
    path = f'C:/Users/Daniel Bianchi/Downloads/receitas-{datetime.now().strftime('%Y-%m-%d')}.csv'

    try:
        os.rename(_path, path)
    except FileExistsError:
        print("Arquivo ja existe")
    df = pd.read_csv(path, sep=';')

cols = ['Órgão', 'Espécie', 'Orçamento Atualizado (Valor Previsto)', 'Receita Realizada (Valor Arrecadado)']

df2 = df[cols]

data = df2.to_json(orient="records", indent=4)

data_list = json.loads(data)

dictionary['Dados'] = data_list

url = 'https://devbunnycofco.azurewebsites.net/acontador.aspx'

response = post(url, json=dictionary)

print(f"Status: {response.status_code}")