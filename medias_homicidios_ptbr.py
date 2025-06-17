# venv\Scripts\activate
import pandas as pd
# pip install scipy
from scipy.stats import trim_mean
import numpy as np

def getMedias(df_dados_brutos): 

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
   
   return df_medias

df_dados_brutos = pd.read_csv('taxa_homicidios.csv')
print(df_dados_brutos)
# >>> Colocar depois de fazer tudo para mostrar que os cálculos, principalmete a mediana é nos dados ordenados
# print(df_dados_brutos.sort_values(by='Populacao'))
# print(df_dados_brutos.sort_values(by='Taxa homicidios'))
df_medias = getMedias(df_dados_brutos)
print(df_medias.to_string(float_format="%.2f"))

def estimativas_variabilidade(dados_brutos, media):
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
   print(estimativas_variabilidade.__doc__) # Imprime a docstring da função
   # ordenar dados (de uma serie: explicar o que é Serie de um dataframe [cada uma das colunas])
   dados_brutos = dados_brutos.sort_values()
   # print(dados_brutos)
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

estimativas_variabilidade(df_dados_brutos['Taxa homicidios'], np.mean(df_dados_brutos['Taxa homicidios']))
   
def frequencias(df_dados_brutos):
   """
   A função frequencias tem como objetivo principal categorizar a coluna 'Populacao' de um DataFrame de entrada (df_dados_brutos) 
   em 10 segmentos (intervalos de população) e, em seguida, gerar uma tabela de frequência que mostra 
   quantos registros (cidades/estados) caem em cada intervalo, listando também as cidades que pertencem a cada intervalo.
   """
   print(frequencias.__doc__)
   # criar serie que mapeia os valores em (10) seguimentos
   numero_classes_k = 10
   classes_populacao = pd.cut(df_dados_brutos['Populacao'], numero_classes_k)
   # conta quantas ocorrências acontecem em cada intervalo
   print(classes_populacao.value_counts)
   classes_populacao.name = 'classes_populacao'
   # concat: concatena dois dataframes
   # axis: onde a concatenação irá ocorrer(horiz, vertic)
   df_dist_frequencia = pd.concat([df_dados_brutos, classes_populacao], axis=1)
   print(df_dados_brutos)
   df_dist_frequencia = df_dist_frequencia.sort_values(by='Populacao')
   groups = []
   # groupby: agrupa o dataframe com base nos valores únicos da coluna classes_populacao
   for group, subset in df_dist_frequencia.groupby(by='classes_populacao', observed=False):
      groups.append({
         'Classes': group,
         'Frequência absoluta': len(subset),
         'Cidades': ','.join(subset.Cidade)
      })
   print(pd.DataFrame(groups))

frequencias(df_dados_brutos)