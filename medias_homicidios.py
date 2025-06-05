# venv\Scripts\activate
import pandas as pd
# pip install scipy
from scipy.stats import trim_mean
import numpy as np

def getMedias(estado): 

     media_pop = estado['Population'].mean()
     print(f'media: {media_pop}')
     media_murd = estado['Murder rate'].mean()

     trim_percentage = trim_percentage = 0.2 # 10% de cada pont (1.6)
     media_aparada_pop = trim_mean(estado['Population'], proportiontocut=trim_percentage)
     media_aparada_murd = trim_mean(estado['Murder rate'], proportiontocut=trim_percentage)

     mediana_pop = estado['Population'].median()
     mediana_murd = estado['Murder rate'].median()

     media_ponderada = np.average(estado['Murder rate'], weights=estado['Population'])
     
     df_medias = pd.DataFrame({
        'Population': [media_pop, media_aparada_pop, mediana_pop, np.nan],
        'Murder rate': [media_murd, media_aparada_murd, mediana_murd, media_ponderada]
     }, index=['Média', 'Média Aparada', 'Mediana', 'Media Ponderada'])

     '''
     estado.loc['Média'] = [
          np.nan,
          media_pop,
          media_murd
     ]
     estado.loc['Média Aparada'] = [
          np.nan,
          media_aparada_pop,
          media_aparada_murd
     ]
     estado.loc['Mediana'] = [
          np.nan,
          mediana_pop,
          mediana_murd
     ]
     print(estado.to_string())
     '''
     # Concatena o DataFrame original com o DataFrame de estatísticas
     # axis=0 significa concatenar por linhas
     # ignore_index=False para manter os rótulos 'Média', 'Média Aparada', 'Mediana'
     # df_concat = pd.concat([estado, df_medias], axis=0)
     
     return df_medias

estado = pd.read_csv('murder_rate.csv')
print(estado.to_string(float_format="%.2f"))
df_medias = getMedias(estado)
print(df_medias.to_string(float_format="%.2f"))