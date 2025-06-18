"""
Estimativas de Variabilidade
Indica o quão espalhados/dispersos os dados estão em relação ao centro (média, mediana, moda)
     Desvios
     Diferença entre os valores observados e uma estimativa de localização (média, mediana, moda)
     - Desvio: tx_homicidio - media
     - Desvio Absoluto: |tx_homicidio - media|
     - Desvio Absoluto Médio: soma dos desvios / num desvios
     - Variância: soma(desvio^2) / num desvios - 1
     - Desvio Padrão: Raiz quadrada da variância
     Estatísticas de Ordem
     Estatísticas baseadas em dados ordenados (order)
     - Amplitude: valor máximo - valor mínimo
     - Percentil: Divide os valores em porcentagens           [10%, 20%, 30%, 40%, 50%, 60%, 70%, 80%, 90%, 100%]
     - Quantil: Mesmo que percentil, mas com casas decimais   [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
     - Quartil: Divide os valores em quatro partes iguais     [Q1 = 25%, Q2 = 50%, Q3 = 75%]
     - Amplitude Interquartil: Q3 - Q1
     - Mediana: Divide os valores em duas partes iguais       [med = Q2]
     Percentis
"""

# venv\Scripts\activate
import pandas as pd
# pip install scipy
from scipy.stats import trim_mean
import numpy as np
import estimativas_variabilidade

# imprimir o docstring
print(estimativas_variabilidade.__doc__) # Imprime a docstring da função

# importar os dados do csv
df_dados_brutos = pd.read_csv('homicidios_por_populacao/taxa_homicidios.csv')
# ordenar dados (de uma serie: explicar o que é Serie de um dataframe [cada uma das colunas])
dados_brutos = df_dados_brutos['Taxa homicidios'].sort_values()
# media
media = np.mean(df_dados_brutos['Taxa homicidios'])
# desvios
desvios = dados_brutos - media
# desvios absolutos
desvios_absolutos = np.abs(desvios)
# desvio absoluto médio
desvio_absoluto_medio = np.mean(desvios_absolutos)
# variâncias (ddof = delta degree of freedom)
variancia = np.var(dados_brutos, ddof=1) 
# desvio padrão
desvio_padrao = np.std(dados_brutos, ddof=1)
# data frames
df_desvios_individuais = pd.DataFrame({
     'Dados Brutos': dados_brutos,
     'Desvio (x - média)': desvios,
     'Desvio Absoluto (x - média)': desvios_absolutos
})
df_media_desvios = pd.DataFrame({
     'Métrica Estatística': [
     'Média',
     'Desvio Padrão',
     'Variância',
     'Desvio Absoluto Médio (DAM)', # Média dos desvios absolutos em relação à média
     ],
     'Valor Calculado': [
     media,
     desvio_padrao,
     variancia,
     desvio_absoluto_medio
     ]
})
# imprimir dados
print(df_desvios_individuais.round(2))
print("\n")
print(df_media_desvios.round(2))
print("\n")
# quantil (decimal)
print("--- Quantis ---")
decimais = [0.05, 0.25, 0.5, 0.75, 0.95]
# print(dec_quantis)
df_quantis = pd.DataFrame(dados_brutos.quantile(decimais))
print(df_quantis.transpose())
print("\n")
# percentil (porcentagem)
print("--- Percentis ---")
df_percentis = pd.DataFrame(dados_brutos.quantile(decimais))
df_percentis.index = [f'{p * 100}%' for p in decimais]
print(df_percentis.transpose())
print("\n")
# quartil (/4)
print("--- Quartis ---")
quartis = [0.25, 0.5, 0.75]
df_quartis = pd.DataFrame(dados_brutos.quantile(quartis))
df_quartis.index = ['Q1', 'Q2', 'Q3']
print(df_quartis.transpose())
print("\n")
# amplitude
amplitude = dados_brutos.max()- dados_brutos.min()
amplitude_alt = dados_brutos.iloc[-1] - dados_brutos.iloc[0] # uma serie do dataframe não é um array, não pode usar dados_brutos[-1]
# amplitude interquartil
amplitude_interquartil = df_quartis.max() - df_quartis.min()
amplitude_interquartil_alt = dados_brutos.quantile(0.75) - dados_brutos.quantile(0.25)
# mediana
mediana = dados_brutos.median()
# data frame
df_amplitudes = pd.DataFrame({
     'Amplitude (max - min)': amplitude,
     'Amplitude Interquartil (Q3 - Q1)': amplitude_interquartil,
     'Mediana (Q2)': mediana
})
# imprimir dados
print(df_amplitudes.round(2))
print("\n")