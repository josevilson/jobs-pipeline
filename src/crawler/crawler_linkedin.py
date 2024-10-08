import json
from random import randrange
from time import sleep

import requests
from bs4 import BeautifulSoup


def extract_job_info(job_card):
    title = job_card.find('h3', class_='base-search-card__title').text.strip()
    company = job_card.find(
        'h4', class_='base-search-card__subtitle').text.strip()
    location = job_card.find(
        'span', class_='job-search-card__location').text.strip()

    try:
        date_posted = job_card.find(
            'time', class_='job-search-card__listdate').text.strip()
    except AttributeError:
        date_posted = None

    try:
        early_applicant = job_card.find(
            'span', class_='job-posting-benefits__text').text.strip()
    except AttributeError:
        early_applicant = None

    # Pegar o link da vaga
    job_link = job_card.find(
        'a', class_='base-card__full-link')['href'].strip()

    return {
        'title': title,
        'company': company,
        'location': location,
        'date_posted': date_posted,
        'early_applicant': early_applicant,
        'job_link': job_link  # Adicionando o link da vaga
    }

# Definir parâmetros gerais


base_url = "https://www.linkedin.com/jobs/search/"
base_url2 = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search/"


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

# Cabeçalho da requisição
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Lista para armazenar todas as vagas
all_jobs = []

# Definir o número de páginas a percorrer
num_pages = 1  # Você pode ajustar esse valor conforme necessário

# Loop para percorrer as páginas
for page in range(num_pages):
    qtd_sec = randrange(60, 180)
    print(f'espere! {qtd_sec} segs')
    # Atualizar o valor de 'start' para cada página (cada página tem 25 resultados)
    params['start'] = page * 25
    current_page = params['start']

    print(f'Pagina: {current_page}')

    # Fazer a requisição HTTP
    response = requests.get(base_url2, headers=headers, params=params)
    # sleep(qtd_sec)

    # Verificar se a requisição foi bem-sucedida
    if response.status_code == 200:
        # Obter o conteúdo HTML
        html_content = response.text
        print(html_content)

        # Criar um objeto BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Encontrar todos os cards de emprego
        job_cards = soup.find_all('div', class_='base-card')

        # Extrair informações de cada card
        jobs = [extract_job_info(card) for card in job_cards]

        # Adicionar as vagas extraídas à lista geral
        all_jobs.extend(jobs)
    else:
        print(f"Falha ao acessar a página {
              page+1}. Código de status: {response.status_code}")
        break

# Salvar as informações em um arquivo JSON
with open('linkedin_jobs.json', 'w', encoding='utf-8') as json_file:
    json.dump(all_jobs, json_file, ensure_ascii=False, indent=2)

print(f"Informações das vagas foram extraídas e salvas em 'linkedin_jobs.json'. Total de {
      len(all_jobs)} vagas coletadas.")
