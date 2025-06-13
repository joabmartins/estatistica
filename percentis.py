import pandas as pd
import numpy as np
from faker import Faker

# Geração do dados
fake = Faker('pt_BR')

# Gerar notas
media_notas = 70
desvio_padrao_notas = 10
num_alunos = 100
notas = np.random.normal(loc=media_notas, scale=desvio_padrao_notas, size=num_alunos)
notas = np.clip(notas, 0, 100).astype(int)
# simples
notas_simples = np.random.randint(0, 101, size=100)

# nome alunos
nomes_alunos = [fake.name() for _ in range(num_alunos)]
df_alunos = pd.DataFrame({
    'Nome': nomes_alunos,
    'Nota': notas
})
print("--- DataFrame Alunos e Notas")
print(df_alunos.head())

# -- Cálculos de Quartis
q1 = df_alunos['Nota'].quantile(0.25)
q2 = df_alunos['Nota'].quantile(0.50)
q3 = df_alunos['Nota'].quantile(0.75)
df_quartis = pd.DataFrame({
    'Quartil': ['Primeiro (Q1)', 'Segundo (Q2 = Mediana)', 'Terceiro (Q3)'],
    'Valor': [q1, q2, q3]
})
print(df_quartis)