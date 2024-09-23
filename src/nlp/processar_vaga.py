# %%

import spacy
from collections import Counter

# Carregando o modelo de linguagem em português
nlp = spacy.load("pt_core_news_sm")

# %%

# Exemplo de descrição de vaga de Engenharia de Dados em português
job_description = """
Procuramos um engenheiro de dados com experiência em Python/SQL e plataformas em nuvem como AWS e Azure.
Familiaridade com processos de ETL, data warehousing e ferramentas como Apache Spark, Kafka e Hadoop é necessária.
Experiência com Docker, Kubernetes e pipelines de CI/CD é um diferencial. Conhecimento de bancos de dados relacionais como PostgreSQL e MySQL,
além de bancos NoSQL como MongoDB, é vantajoso. Familiaridade com Git e sistemas de controle de versão também é esperada.
"""

# Lista de palavras-chave de tecnologias a serem verificadas (pode ser expandida)
tech_keywords = [
    "Python", "SQL", "AWS", "Azure", "ETL", "Spark", "Kafka", "Hadoop", "Docker", 
    "Kubernetes", "CI/CD", "PostgreSQL", "MySQL", "MongoDB", "Git"
]

# Aplicando o modelo spaCy à descrição da vaga
doc = nlp(job_description)

# Extraindo as tecnologias mencionadas no texto da vaga
extracted_technologies = [token.text for token in doc if token.text in tech_keywords]

for ent in doc.ents:
    print(ent.text, ent.label_)

# Contagem das tecnologias mencionadas
technology_count = Counter(extracted_technologies)
# %%

print(technology_count)

# %%
