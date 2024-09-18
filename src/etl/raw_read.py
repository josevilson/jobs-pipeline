# %% 
import pandas as pd

def read_json(filename='../../vagas.json'):
    """
    Salva os dados em um arquivo JSON.
    """
    with open(filename, 'r', encoding='utf-8') as f:
        data = f.read()
    return data


data = read_json()

df = pd.read_json(data)
# %%
