# venv\Scripts\activate
# .\venv\Scripts\activate
# venv\Scripts\activate.sp1
import pandas as pd
import numpy as np
# pip install scipy
from scipy.stats import trim_mean

def get_medias(df_dados_brutos):
    # medias simples:
    media_populacao = df_dados_brutos['Populacao'].mean()
    media_homicidios = df_dados_brutos['Taxa homicidios'].mean()
    # medias aparadas:
    proporcao_corte = 0.1 # corte de 10% de cada ponta
    media_aparada_populacao = trim_mean(df_dados_brutos['Populacao'], proportiontocut=proporcao_corte)
    media_aparada_homicidios = trim_mean(df_dados_brutos['Taxa homicidios'], proportiontocut=proporcao_corte)
    # medianas:
    mediana_populacao = df_dados_brutos['Populacao'].median()
    mediana_homicidios = df_dados_brutos['Taxa homicidios'].median()
    # media ponderada = soma(valor x peso) / soma(peso)
    # onde valor é a taxa_homicidio e o peso é populacao
    # calcular a média ponderada de homicídios onde o peso de cada cidade é sua população
    media_ponderada = np.average(df_dados_brutos['Taxa homicidios'], weights=df_dados_brutos['Populacao'])
# https://codeshare.io/29OdMK
    df_medias = pd.DataFrame({
        'Populacao': [media_populacao, media_aparada_populacao, mediana_populacao, np.nan],
        'Taxa homicidios': [media_homicidios, media_aparada_homicidios, mediana_homicidios, media_ponderada]
    }, index=['Média','Média Aparada', 'Mediana', 'Media Ponderada'])
    return df_medias

df_dados_brutos = pd.read_csv('taxa_homicidios.csv')
print(df_dados_brutos)
df_medias = get_medias(df_dados_brutos)
print(df_medias.to_string(float_format="%.2f"))