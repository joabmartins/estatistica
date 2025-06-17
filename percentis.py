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
print("--- Quartis das Notas")
print(df_quartis)
print("\n")
# https://codeshare.io/2j09nB
# --- Cálculos de Decis
decis_percentis = [i / 10.0 for i in range(1, 11)]
decis_valores = [df_alunos['Nota'].quantile(p) for p in decis_percentis]
decis_nomes = [f"{i}° Decil" for i in range(1, 11)] # 1° Decil
df_decis = pd.DataFrame({
    'Decil': decis_nomes,
    'Percentil': [f"{int(p*100)}%" for p in decis_percentis],
    'Valor': decis_valores
})
print("--- Decis das Notas ---")
print(df_decis)
print("\n")

amplitude_interquartil = q3 - q1
df_aiq = pd.DataFrame({
    'Métrica': ['Amplitude Interquartil (AIQ)'],
    'Valor': [amplitude_interquartil]
})
print("--- Apmlitude Interquartil ---")
print(df_aiq)
print("\n")