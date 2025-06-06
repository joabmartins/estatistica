# venv\Scripts\activate
import pandas as pd
# pip install faker
from faker import Faker
import random

# Inicializa o gerador de dados fictícios
fake = Faker('en_US') # 'en_US' para nomes de cidades americanas
# fake = Faker('pt_BR') 

def gerar_dados_brutos(num_registros):
    dados_brutos = []
    # Usaremos um conjunto para garantir que as cidades geradas sejam únicas,
    # especialmente se num_registros não for muito grande.
    lista_cidades = set()
    
    while len(dados_brutos) < num_registros:
        nome_cidade = fake.city()
        # Garante que a cidade seja única no conjunto de dados gerado até agora
        if nome_cidade not in lista_cidades:
            lista_cidades.add(nome_cidade)
            population = fake.random_int(min=10000, max=5000000) # População entre 10k e 5M
            taxa_homicidios = round(random.uniform(1.0, 15.0), 1) # Taxa de homicídios entre 1.0 e 15.0, com uma casa decimal

            dados_brutos.append({
                "Cidade": nome_cidade,
                "Populacao": population,
                "Taxa homicidios": taxa_homicidios
            })
    return pd.DataFrame(dados_brutos)

# Número de linhas que você quer na sua tabela (exemplo: 10 linhas)
num_registros = 10

# Gerar o DataFrame
df = gerar_dados_brutos(num_registros)

# Exibir as primeiras linhas do DataFrame gerado
print("DataFrame gerado:")
print(df)

# Salvar o DataFrame em um arquivo CSV
output_csv_file = "taxa_homicidios.csv"
df.to_csv(output_csv_file, index=False) # index=False para não salvar o índice do DataFrame como uma coluna

print(f"\nTabela salva em '{output_csv_file}' com sucesso!")