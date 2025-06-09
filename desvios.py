# pip install pandas numpy Faker
# venv\Scripts\activate
import pandas as pd
import numpy as np
from faker import Faker

# --- 1. Geração de Dados Fictícios ---
fake = Faker('pt_BR')

media_notas_simulada = 70
desvio_padrao_notas_simulada = 10
num_alunos = 100

notas = np.random.normal(loc=media_notas_simulada, scale=desvio_padrao_notas_simulada, size=num_alunos)
notas = np.clip(notas, 0, 100) # Limita as notas entre 0 e 100
dados = notas # Renomeando para 'dados' para clareza nos cálculos

print("--- Dados Brutos (primeiras 10 notas) ---")
print(np.round(dados[:10], 2)) # Exibe as primeiras 10 notas arredondadas
print("\n")

# --- 2. Cálculos das Medidas com Detalhes "Hard Coded" ---

# 2.1. Média (Mean)
print("--- Cálculo da Média ---")
print("Fórmula: Média = (Soma de todos os valores) / (Número de valores)")
print(f"Passo 1: Somar todos os valores. Exemplo (primeiras 5 notas): {np.round(dados[:5], 2).tolist()}")
soma_dos_dados = sum(dados)
print(f"Soma total dos dados: {soma_dos_dados:.2f}")
numero_de_dados = len(dados)
print(f"Número total de dados (n): {numero_de_dados}")
media_hard_coded = soma_dos_dados / numero_de_dados
print(f"Média (hard coded): {media_hard_coded:.2f}")
# Usando a função NumPy para comparação
media = np.mean(dados)
print(f"Média (np.mean): {media:.2f}")
print("\n")

# 2.2. Mediana (Median)
print("--- Cálculo da Mediana ---")
print("Fórmula: Valor do meio em um conjunto de dados ordenado.")
print("Se n for par, é a média dos dois valores do meio.")
dados_ordenados = np.sort(dados)
print(f"Dados ordenados (primeiras 10 notas): {np.round(dados_ordenados[:10], 2).tolist()} ...")
if numero_de_dados % 2 == 1: # Se n for ímpar
    indice_mediana = numero_de_dados // 2
    mediana_hard_coded = dados_ordenados[indice_mediana]
    print(f"Número de dados é ímpar. Mediana é o valor na posição {indice_mediana} (índice 0-base).")
else: # Se n for par
    indice_mediana1 = numero_de_dados // 2 - 1
    indice_mediana2 = numero_de_dados // 2
    mediana_hard_coded = (dados_ordenados[indice_mediana1] + dados_ordenados[indice_mediana2]) / 2
    print(f"Número de dados é par. Mediana é a média dos valores nas posições {indice_mediana1} e {indice_mediana2}.")
    print(f"Valores: {dados_ordenados[indice_mediana1]:.2f} e {dados_ordenados[indice_mediana2]:.2f}")

print(f"Mediana (hard coded): {mediana_hard_coded:.2f}")
# Usando a função NumPy para comparação
mediana = np.median(dados)
print(f"Mediana (np.median): {mediana:.2f}")
print("\n")

# 2.3. Desvio Absoluto (DA) - Para cada ponto de dado
print("--- Cálculo do Desvio Absoluto (para cada ponto de dado) ---")
print("Fórmula: DA_i = |x_i - média|")
print(f"Média utilizada: {media:.2f}")
# Exibindo os primeiros 5 desvios absolutos manualmente
desvios_abs_hard_coded = []
print("Desvios Absolutos (primeiras 5 notas):")
for i in range(min(5, len(dados))):
    desvio = abs(dados[i] - media)
    desvios_abs_hard_coded.append(desvio)
    print(f"|{dados[i]:.2f} - {media:.2f}| = {desvio:.2f}")
# Usando a função NumPy para obter todos os desvios
desvios_absolutos = np.abs(dados - media)
print(f"Primeiros 5 Desvios Absolutos (np.abs): {np.round(desvios_absolutos[:5], 2).tolist()}")
print("\n")

# 2.4. Desvio Absoluto Médio (DAM ou MAD - Mean Absolute Deviation)
print("--- Cálculo do Desvio Absoluto Médio (DAM) ---")
print("Fórmula: DAM = Sum(|x_i - média|) / n")
print(f"Soma dos Desvios Absolutos (Sum(|x_i - média|)): {sum(desvios_absolutos):.2f}")
print(f"Número de dados (n): {numero_de_dados}")
dam_hard_coded = sum(desvios_absolutos) / numero_de_dados
print(f"DAM (hard coded): {dam_hard_coded:.2f}")
# Usando a função NumPy para comparação
dam = np.mean(np.abs(dados - np.mean(dados))) # Recalculado para garantir a média
print(f"DAM (np.mean(np.abs(dados - np.mean(dados)))): {dam:.2f}")
print("\n")

# 2.5. Variância (Variance)
print("--- Cálculo da Variância Amostral ---")
print("Fórmula: s^2 = Sum((x_i - média)^2) / (n - 1)")
print(f"Média utilizada: {media:.2f}")
soma_quadrados_desvios = 0
print("Desvios Quadrados (primeiras 5 notas):")
for i in range(min(5, len(dados))):
    desvio_quadrado = (dados[i] - media)**2
    soma_quadrados_desvios += desvio_quadrado
    print(f"({dados[i]:.2f} - {media:.2f})^2 = {desvio_quadrado:.2f}")

print(f"Soma total dos Desvios Quadrados: {soma_quadrados_desvios:.2f}")
denominador_variancia = numero_de_dados - 1
print(f"Denominador (n - 1): {denominador_variancia}")
variancia_hard_coded = soma_quadrados_desvios / denominador_variancia
print(f"Variância (hard coded): {variancia_hard_coded:.2f}")
# Usando a função NumPy para comparação
variancia = np.var(dados, ddof=1) # ddof=1 para variância amostral
print(f"Variância (np.var com ddof=1): {variancia:.2f}")
print("\n")

# 2.6. Desvio Padrão (Standard Deviation)
print("--- Cálculo do Desvio Padrão Amostral ---")
print("Fórmula: s = Raiz_Quadrada(Variância)")
print(f"Variância utilizada: {variancia_hard_coded:.2f}")
desvio_padrao_hard_coded = variancia_hard_coded**0.5 # Ou np.sqrt(variancia_hard_coded)
print(f"Desvio Padrão (hard coded): {desvio_padrao_hard_coded:.2f}")
# Usando a função NumPy para comparação
desvio_padrao = np.std(dados, ddof=1) # ddof=1 para desvio padrão amostral
print(f"Desvio Padrão (np.std com ddof=1): {desvio_padrao:.2f}")
print("\n")

# 2.7. Desvio Absoluto Mediano da Mediana (MAD - Median Absolute Deviation from the Median)
print("--- Cálculo do Desvio Absoluto Mediano da Mediana (MAD) ---")
print("Fórmula: MAD = Mediana(|x_i - mediana|)")
print(f"Mediana utilizada: {mediana:.2f}")
# Calcula os desvios absolutos em relação à mediana
desvios_abs_mediana_hard_coded_list = []
print("Desvios Absolutos em relação à Mediana (primeiras 5 notas):")
for i in range(min(5, len(dados))):
    desvio_mediana = abs(dados[i] - mediana)
    desvios_abs_mediana_hard_coded_list.append(desvio_mediana)
    print(f"|{dados[i]:.2f} - {mediana:.2f}| = {desvio_mediana:.2f}")

# Ordena e encontra a mediana desses desvios
desvios_abs_mediana_ordenados = np.sort(np.abs(dados - mediana))
print(f"Todos os Desvios Absolutos em relação à Mediana (ordenados, primeiras 10): {np.round(desvios_abs_mediana_ordenados[:10], 2).tolist()} ...")
if numero_de_dados % 2 == 1:
    indice_mad = numero_de_dados // 2
    mad_hard_coded = desvios_abs_mediana_ordenados[indice_mad]
else:
    indice_mad1 = numero_de_dados // 2 - 1
    indice_mad2 = numero_de_dados // 2
    mad_hard_coded = (desvios_abs_mediana_ordenados[indice_mad1] + desvios_abs_mediana_ordenados[indice_mad2]) / 2

print(f"MAD (hard coded): {mad_hard_coded:.2f}")
# Usando a função NumPy para comparação
mad = np.median(np.abs(dados - np.median(dados)))
print(f"MAD (np.median(np.abs(dados - np.median(dados)))) : {mad:.2f}")
print("\n")

# --- 3. Exibição dos Resultados Finais em um DataFrame ---
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

df_resultados = pd.DataFrame(resultados)

print("--- Resumo das Medidas de Tendência Central e Dispersão ---")
print(df_resultados.round(2))