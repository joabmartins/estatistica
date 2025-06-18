
"""
Medidas de Tendência Central
Estima onde a maioria dos dados está localizado.
   - Tamanho da amostra (n): quantidade total de itens da amostra
   - Média: soma(valores) / n
   Valor médio dos dados
   - Média Aparada: soma(valores não descartados) / n - p
   Média calculada após descartar valores(p) de ambas as extremidades
   - Média Ponderada: soma(valor x w) / soma(w)
   Média Calculada após atribuir pesos(w) para cada valor
   - Mediana:
   Valor central da amostra, valor do meio se n for ímpar ou média dos dois valores do meio se n for par
   - Moda:
   Valor que aparece com mais frequência
   Amodal: Amostra que não possui moda
   Unimodal: Amostra que posssui apenas uma moda
   Bimodal: Amostra que possui duas modas
   Multimodal: Amostra que possui mais de duas modas
"""

# venv\Scripts\activate
import pandas as pd
# pip install scipy
from scipy.stats import trim_mean
import numpy as np
import medidas_tendencia_central

# imprimir o docstring
print(medidas_tendencia_central.__doc__) # Imprime a docstring da função

# importar os dados do csv
df_dados_brutos = pd.read_csv('homicidios_por_populacao/taxa_homicidios.csv')
# media
media_populacao = df_dados_brutos['Populacao'].mean()
print(f'media: {media_populacao}')
media_homicidios = df_dados_brutos['Taxa homicidios'].mean()

proporcao_corte = 0.1 # 10% de cada pont (1.6)
media_aparada_populacao = trim_mean(df_dados_brutos['Populacao'], proportiontocut=proporcao_corte)
media_aparada_homicidios = trim_mean(df_dados_brutos['Taxa homicidios'], proportiontocut=proporcao_corte)

mediana_populacao = df_dados_brutos['Populacao'].median()
mediana_homicidios = df_dados_brutos['Taxa homicidios'].median()

# media_ponderada = soma(valor x peso) / soma(peso)
# onde valor é a taxa_homicidio e o peso é populacao
# calcular a média ponderada de homicídios onde o peso de cada cidade é sua população.
media_ponderada = np.average(df_dados_brutos['Taxa homicidios'], weights=df_dados_brutos['Populacao'])

df_medias = pd.DataFrame({
   'Populacao': [media_populacao, media_aparada_populacao, mediana_populacao, np.nan],
   'Taxa homicidios': [media_homicidios, media_aparada_homicidios, mediana_homicidios, media_ponderada]
}, index=['Média', 'Média Aparada', 'Mediana', 'Media Ponderada'])
   
print(df_medias.to_string(float_format="%.2f"))
