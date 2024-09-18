import json

import requests

# URL do endpoint que você deseja acessar
url = 'https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search/'

params = {
    'keywords': 'Engenheiro De Dados',
    'location': 'São Paulo, São Paulo, Brasil',
    'geoId': 104746682,  # Esse valor será incrementado no loop
    'distance': 25,
    'refresh': 'true',
    'f_TPR': 'r2592000',
    'position': 1,
    'pageNum': 0,
    'start': 25

}


# Cabeçalhos HTTP que podem ser necessários para a requisição (simulando um navegador, por exemplo)
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Fazendo a requisição GET
response = requests.get(url, headers=headers, params=params)

# Verificando se a requisição foi bem-sucedida
if response.status_code == 200:
    try:
        with open('pagina_linkedin.html', 'w', encoding='utf-8') as file:
            file.write(response.text)

        print("JSON baixado e salvo com sucesso.")
    except ValueError:
        print("Erro: a resposta não contém um JSON válido.")
else:
    print(f"Falha ao baixar a página. Status code: {response.status_code}")
