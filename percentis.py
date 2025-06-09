# pip install pandas numpy Faker
# venv\Scripts\activate
import pandas as pd
import numpy as np
from faker import Faker

# --- 1. Geração de Dados Fictícios ---
# Criar uma instância do Faker
fake = Faker('pt_BR') # Usar localidade brasileira para nomes

# Gerar notas aleatórias para 100 alunos (simulando a prova de matemática)
# Usamos np.random.randint para garantir notas inteiras entre 0 e 100
# Ou np.random.normal para notas mais próximas de uma distribuição normal, arredondando depois
# Para este exemplo, vamos usar uma distribuição normal para simular notas mais "reais"
# A média e o desvio padrão podem ser ajustados para simular diferentes cenários.
media_notas = 70
desvio_padrao_notas = 10
num_alunos = 100

# Gerar dados normais inteiros de 0 a 100
np.random.randint(0, 101, size=100)
# Gerar notas normalmente distribuídas e garantir que estejam entre 0 e 100
# No nosso exemplo, np.random.normal(loc=media_notas, scale=desvio_padrao_notas, size=num_alunos) 
# significa que estamos gerando notas que tendem a se agrupar em torno da media_notas (70), 
# com uma dispersão típica de desvio_padrao_notas (10). 
# Ou seja, a maioria das notas estará entre 60 e 80, mas algumas podem cair fora dessa faixa.
notas = np.random.normal(loc=media_notas, scale=desvio_padrao_notas, size=num_alunos)
#  pega todas as notas geradas por np.random.normal e:
# Se uma nota for menor que 0, ela se torna 0.
# Se uma nota for maior que 100, ela se torna 100.
# Se uma nota estiver entre 0 e 100, ela permanece inalterada.
notas = np.clip(notas, 0, 100).astype(int) # Limita as notas entre 0 e 100 e converte para int

# Gerar nomes fictícios para os alunos
nomes_alunos = [fake.name() for _ in range(num_alunos)]

# Criar um DataFrame com os dados dos alunos
df_alunos = pd.DataFrame({
    'Nome': nomes_alunos,
    'Nota': notas
})

# Opcional: Mostrar as primeiras linhas do DataFrame para verificar os dados
print("--- DataFrame Original de Notas dos Alunos ---")
print(df_alunos.head())
print("\n")

# --- 2. Cálculos de Quartis ---
# Calculando os quartis usando o método .quantile()
# 0.25 -> 25º percentil (Primeiro Quartil)
# 0.50 -> 50º percentil (Segundo Quartil / Mediana)
# 0.75 -> 75º percentil (Terceiro Quartil)
q1 = df_alunos['Nota'].quantile(0.25)
q2 = df_alunos['Nota'].quantile(0.50)
q3 = df_alunos['Nota'].quantile(0.75)

# Criar um DataFrame para os quartis
df_quartis = pd.DataFrame({
    'Quartil': ['Primeiro (Q1)', 'Segundo (Q2 - Mediana)', 'Terceiro (Q3)'],
    'Valor': [q1, q2, q3]
})

print("--- Quartis das Notas ---")
print(df_quartis)
print("\n")

# --- 3. Cálculos de Decis ---
# Calculando os decis (percentis de 10 em 10)
# Criamos uma lista de percentis de 0.10 a 1.00
decis_percentis = [i / 10.0 for i in range(1, 11)]
decis_valores = [df_alunos['Nota'].quantile(p) for p in decis_percentis]

# Criar uma lista de nomes para os decis (e.g., "1º Decil", "2º Decil")
decis_nomes = [f"{i}º Decil" for i in range(1, 11)]

# Criar um DataFrame para os decis
# sendo o primeiro decil (10%) 58.0 diz que 10% dos alunos tiraram nota 58.0 para baixo
# sendo o segundo decil (20%) 63.0 diz que 20% dos alunos tiraram nota 63.0 para baixo (metade abaixo de 10% e metade entre 10% e 20%)
df_decis = pd.DataFrame({
    'Decil': decis_nomes,
    'Percentil': [f"{int(p*100)}%" for p in decis_percentis], # Formatar como porcentagem
    'Valor': decis_valores
})

print("--- Decis das Notas ---")
print(df_decis)
print("\n")


# --- 4. Cálculo da Amplitude Interquartil (AIQ) ---
# AIQ é a diferença entre o Terceiro Quartil (Q3) e o Primeiro Quartil (Q1)
amplitude_interquartil = q3 - q1

# Criar um DataFrame para a Amplitude Interquartil
df_aiq = pd.DataFrame({
    'Métrica': ['Amplitude Interquartil (AIQ)'],
    'Valor': [amplitude_interquartil]
})

print("--- Amplitude Interquartil ---")
print(df_aiq)
print("\n")

# --- Análise e Interpretação (Comentários para o exemplo) ---
# Com base nos resultados dos DataFrames acima, podemos interpretar:
# - df_quartis: Mostra as notas que separam os 25% mais baixos, a mediana (50% do meio) e os 25% mais altos.
#   Por exemplo, se o Q1 for 60, 25% dos alunos tiraram até 60.
# - df_decis: Fornece uma visão mais granular da distribuição. Podemos ver as notas que separam cada 10% dos alunos.
#   Por exemplo, o 1º Decil (10% dos alunos) e o 9º Decil (10% dos alunos mais altos) dão uma ideia dos extremos.
# - df_aiq: Indica a dispersão dos 50% centrais dos dados, sendo uma medida de variabilidade robusta a outliers.
#   Um AIQ maior significa que os 50% centrais dos dados estão mais espalhados.