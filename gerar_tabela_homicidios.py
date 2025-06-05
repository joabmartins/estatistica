# venv\Scripts\activate
import pandas as pd
# pip install faker
from faker import Faker
import random

# Inicializa o gerador de dados fictícios
fake = Faker('en_US') # 'en_US' para nomes de cidades americanas

def generate_city_data(num_rows):
    data = []
    # Usaremos um conjunto para garantir que as cidades geradas sejam únicas,
    # especialmente se num_rows não for muito grande.
    generated_cities = set()
    
    while len(data) < num_rows:
        city_name = fake.city()
        # Garante que a cidade seja única no conjunto de dados gerado até agora
        if city_name not in generated_cities:
            generated_cities.add(city_name)
            population = fake.random_int(min=10000, max=5000000) # População entre 10k e 5M
            murder_rate = round(random.uniform(1.0, 15.0), 1) # Taxa de homicídios entre 1.0 e 15.0, com uma casa decimal

            data.append({
                "City": city_name,
                "Population": population,
                "Murder rate": murder_rate
            })
    return pd.DataFrame(data)

# Número de linhas que você quer na sua tabela (exemplo: 10 linhas)
num_rows_to_generate = 10

# Gerar o DataFrame
df = generate_city_data(num_rows_to_generate)

# Exibir as primeiras linhas do DataFrame gerado
print("DataFrame gerado:")
print(df)

# Salvar o DataFrame em um arquivo CSV
output_csv_file = "murder_rate.csv"
df.to_csv(output_csv_file, index=False) # index=False para não salvar o índice do DataFrame como uma coluna

print(f"\nTabela salva em '{output_csv_file}' com sucesso!")