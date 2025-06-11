
import pandas as pd
import numpy as np
from faker import Faker

# --- 1. Geração de Dados Fictícios ---
# Criar uma instância do Faker para nomes
fake = Faker('pt_BR')

# Gerar notas aleatórias para 100 alunos (simulando a prova de matemática)
media_notas = 70
desvio_padrao_notas = 10
num_alunos = 100

notas = np.random.normal(loc=media_notas, scale=desvio_padrao_notas, size=num_alunos)
notas = np.clip(notas, 0, 100) # Limita as notas entre 0 e 100
# Não convertemos para int aqui para manter a precisão dos cálculos flutuantes,
# mas se preferir notas inteiras, adicione .astype(int)

# Opcional: Gerar nomes (não serão usados nos cálculos, mas para contexto)
# nomes_alunos = [fake.name() for _ in range(num_alunos)]
# df_alunos = pd.DataFrame({'Nome': nomes_alunos, 'Nota': notas})
# print("--- DataFrame Original de Notas dos Alunos ---")
# print(df_alunos.head())
# print("\n")

# Para este exercício, vamos usar o array de notas diretamente
dados = notas

# --- 2. Cálculos das Medidas ---

# 2.1. Média (Mean)
# Fórmula: (Soma de todos os valores) / (Número de valores)
# Média (x_barra) = Sum(x_i) / n
media = np.mean(dados)

# 2.2. Mediana (Median)
# Fórmula: O valor do meio em um conjunto de dados ordenado.
# Se n for par, é a média dos dois valores do meio.
mediana = np.median(dados)

# 2.3. Desvio Absoluto (DA) - Para cada ponto de dado
# Não é uma medida de dispersão única para o conjunto, mas sim um conjunto de desvios.
# É a diferença absoluta entre cada valor e a média.
# DA_i = |x_i - média|
desvios_absolutos = np.abs(dados - media)

# 2.4. Desvio Absoluto Médio (DAM ou MAD - Mean Absolute Deviation)
# Fórmula: Média dos desvios absolutos em relação à média.
# DAM = Sum(|x_i - média|) / n
dam = np.mean(desvios_absolutos) # Ou np.mean(np.abs(dados - np.mean(dados)))

# 2.5. Variância (Variance)
# Fórmula para variância amostral (com n-1 no denominador):
# s^2 = Sum((x_i - média)^2) / (n - 1)
# O pandas e numpy usam n-1 por padrão para a variância (ddof=1)
variancia = np.var(dados, ddof=1) # ddof=1 para variância amostral (n-1)

# 2.6. Desvio Padrão (Standard Deviation)
# Fórmula para desvio padrão amostral:
# s = Raiz_Quadrada(Variância)
desvio_padrao = np.std(dados, ddof=1) # ddof=1 para desvio padrão amostral (n-1)

# 2.7. Desvio Absoluto Mediano da Mediana (MAD - Median Absolute Deviation from the Median)
# Fórmula: Mediana dos desvios absolutos de cada valor em relação à MEDIANA.
# MAD = Mediana(|x_i - mediana|)
desvios_abs_mediana = np.abs(dados - mediana)
mad = np.median(desvios_abs_mediana)

# --- 3. Exibição dos Resultados em um DataFrame ---
# Criar um dicionário com os nomes das métricas e seus valores
resultados = {
    'Métrica Estatística': [
        'Média',
        'Mediana',
        'Desvio Absoluto Médio (DAM)',
        'Variância',
        'Desvio Padrão',
        'Desvio Absoluto Mediano da Mediana (MAD)'
    ],
    'Valor Calculado': [
        media,
        mediana,
        dam,
        variancia,
        desvio_padrao,
        mad
    ]
}

# Criar o DataFrame
df_resultados = pd.DataFrame(resultados)

print("--- Medidas de Tendência Central e Dispersão ---")
print(df_resultados.round(2)) # Arredondar para 2 casas decimais para melhor visualização

# --- Opcional: Mostrar os desvios absolutos individuais (não é uma métrica única) ---
# print("\n--- Primeiros 10 Desvios Absolutos Individuais (em relação à média) ---")
# df_desvios_abs_ind = pd.DataFrame({
#     'Nota Original': dados[:10],
#     'Desvio Absoluto': desvios_absolutos[:10]
# })
# print(df_desvios_abs_ind.round(2))