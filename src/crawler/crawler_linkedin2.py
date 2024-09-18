import json
import time
import requests
from bs4 import BeautifulSoup
from random import randrange


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

        job_link = card.find('a', class_='base-card__full-link')['href'].strip()

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
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
    }
    params = {
        'keywords': 'Engenheiro De Dados',
        'location': 'São Paulo, São Paulo, Brasil',
        'geoId': 104746682,
        'distance': 25,
        'refresh': 'true',
        'f_TPR': 'r2592000',
        'position': 1,
        'pageNum': 0,
        'start': 1  # Parâmetro que indica o início da página
    }

    all_jobs = []
    total_pages = 10  # Definindo o limite de páginas a serem buscadas
    results_per_page = 10  # Número de resultados por página (pode variar)

    for page in range(total_pages):
        print(f"Extraindo dados da página {page + 1}...")
        params['start'] = page * results_per_page  # Atualiza o valor de início da próxima página
        html_content = extract_html(base_url, params, headers)

        if html_content:
            jobs = parse_job_cards(html_content)
            if not jobs:  # Se não houver mais vagas, encerra o loop
                print("Nenhuma vaga encontrada na página. Finalizando o scraping.")
                break
            all_jobs.extend(jobs)
            qtd_sec = randrange(60,180)
            time.sleep(qtd_sec)  # Pausa de 2 segundos entre as requisições para evitar sobrecarga
            print(f'espere, qtd_sec {qtd_sec}')
        else:
            print(f"Erro ao buscar os dados da página {page + 1}. Tentando a próxima página.")
            continue

    save_to_json(all_jobs)
    print(f"Foram extraídas {len(all_jobs)} vagas e salvas em 'vagas.json'.")


if __name__ == "__main__":
    main()
