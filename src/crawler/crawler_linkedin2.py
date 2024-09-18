import json
import time

import requests
from bs4 import BeautifulSoup


def extract_html(url, params, headers):
    """
    Extrai o conteúdo HTML da URL fornecida.
    """
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Lança uma exceção para códigos de status HTTP ruins
        return response.text
    except requests.RequestException as e:
        print(f"Erro ao fazer a requisição: {e}")
        return None


def parse_job_cards(html_content):
    """
    Analisa o conteúdo HTML e extrai informações dos cards de emprego.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    job_cards = soup.find_all('div', class_='base-card')

    jobs = []

    for card in job_cards:
        title = card.find('h3', class_='base-search-card__title')
        title = title.text.strip() if title else "Título não encontrado"

        company = card.find('h4', class_='base-search-card__subtitle')
        company = company.text.strip() if company else "Empresa não encontrada"

        location = card.find('span', class_='job-search-card__location')
        location = location.text.strip() if location else "Local não encontrado"

        time_element = card.find('time', class_='job-search-card__listdate')
        time_posted = time_element.text.strip() if time_element else "Tempo não encontrado"

        job_link = card.find(
            'a', class_='base-card__full-link')['href'].strip()

        job = {
            "titulo": title,
            "empresa": company,
            "local": location,
            "tempo": time_posted,
            "link_vaga": job_link
        }

        jobs.append(job)

    return jobs


def save_to_json(data, filename='vagas.json'):
    """
    Salva os dados em um arquivo JSON.
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def main():
    base_url = "https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    params = {
        'keywords': 'Engenheiro De Dados',
        'location': 'São Paulo, São Paulo, Brasil',
        'geoId': 104746682,  # Esse valor será incrementado no loop
        'distance': 25,
        'refresh': 'true',
        'f_TPR': 'r2592000',
        'position': 1,
        'pageNum': 0,
        'start': 0
    }

    html_content = extract_html(base_url, params, headers)
    if html_content:
        jobs = parse_job_cards(html_content)
        save_to_json(jobs)
        print(f"Foram extraídas {len(jobs)} vagas e salvas em 'vagas.json'")
    else:
        print("Não foi possível obter o conteúdo HTML.")


if __name__ == "__main__":
    main()
