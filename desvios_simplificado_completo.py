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
print(f"notas random: {notas}")
notas = np.clip(notas, 0, 100) # Limita as notas entre 0 e 100
print(f"notas clipped: {notas}")
# Não convertemos para int aqui para manter a precisão dos cálculos flutuantes,
# mas se preferir notas inteiras, adicione .astype(int)

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

# 2.3. Desvio (em relação à Média) - Para cada ponto de dado
# É a diferença entre cada valor e a média.
# Desvio_i = x_i - média
desvios = dados - media

# 2.4. Desvio Absoluto (DA) - Para cada ponto de dado
# É a diferença absoluta entre cada valor e a média.
# DA_i = |x_i - média|
desvios_absolutos = np.abs(dados - media)

# 2.5. Variância Individual (Quadrado do Desvio) - Para cada ponto de dado
# É o quadrado da diferença entre cada valor e a média.
# Variancia_i = (x_i - média)^2
variancias_individuais = (dados - media)**2

# 2.6. Variância (Variance) do conjunto de dados
# Fórmula para variância amostral (com n-1 no denominador):
# s^2 = Sum((x_i - média)^2) / (n - 1)
# O pandas e numpy usam n-1 por padrão para a variância (ddof=1)
variancia = np.var(dados, ddof=1) # ddof=1 para variância amostral (n-1)

# 2.7. Desvio Padrão (Standard Deviation) do conjunto de dados
# Fórmula para desvio padrão amostral:
# s = Raiz_Quadrada(Variância)
desvio_padrao = np.std(dados, ddof=1) # ddof=1 para desvio padrão amostral (n-1)

# 2.8. Desvio Absoluto Médio (DAM ou MAD - Mean Absolute Deviation)
# Fórmula: Média dos desvios absolutos em relação à média.
# DAM = Sum(|x_i - média|) / n
dam = np.mean(desvios_absolutos)

# 2.9. Desvios Absolutos em relação à Mediana (valores individuais)
# Esta é a parte que você destacou: |x_i - mediana| para cada x_i
desvios_abs_em_relacao_mediana_individuais = np.abs(dados - mediana)

# 2.10. Desvio Absoluto Mediano da Mediana (MAD - Median Absolute Deviation from the Median)
# Fórmula: Mediana dos desvios absolutos de cada valor em relação à MEDIANA.
# MAD = Mediana(|x_i - mediana|)
mad = np.median(desvios_abs_em_relacao_mediana_individuais)

# --- 3. Exibição dos Resultados em DataFrames ---

# --- DataFrame 1: Dados Brutos, Desvios e Variâncias Individuais ---
# Este DataFrame mostrará os primeiros 10 valores (conforme solicitado),
# mesmo que os cálculos tenham sido feitos para os 100 valores gerados.
df_detalhes = pd.DataFrame({
    'Dados Brutos': dados,
    'Desvio (x - média)': desvios,
    'Variância Individual (x - média)^2': variancias_individuais,
    'Desvio Absoluto (x - média)': desvios_absolutos, # Antigo 'Desvio Absoluto (DA)'
    'Desvio Absoluto (x - mediana)': desvios_abs_em_relacao_mediana_individuais # Novo: Desvio Absoluto em relação à Mediana
})

print("--- DataFrame 1: Dados Brutos, Desvios e Variâncias Individuais (Primeiros 10 valores) ---")
# Imprime apenas as 10 primeiras linhas, conforme solicitado.
print(df_detalhes.head(10).round(2)) # Arredondar para 2 casas decimais para melhor visualização
print("\n")

# --- DataFrame 2: Medidas de Tendência Central e Dispersão (Valores Únicos) ---
# Criar um dicionário com os nomes das métricas e seus valores
resultados_estatisticos_unicos = {
    'Métrica Estatística': [
        'Média',
        'Mediana',
        'Desvio Padrão',
        'Variância',
        'Desvio Absoluto Médio (DAM)', # Média dos desvios absolutos em relação à média
        'Desvio Absoluto Mediano da Mediana (MAD)' # Mediana dos desvios absolutos em relação à mediana
    ],
    'Valor Calculado': [
        media,
        mediana,
        desvio_padrao,
        variancia,
        dam,
        mad
    ]
}

# Criar o DataFrame
df_resultados_unicos = pd.DataFrame(resultados_estatisticos_unicos)

print("--- DataFrame 2: Medidas de Tendência Central e Dispersão (Valores Únicos) ---")
print(df_resultados_unicos.round(3)) # Arredondar para 3 casas decimais para melhor visualização