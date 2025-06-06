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