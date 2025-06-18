"""
Distribuição de Frequência
Agrupa os dados em intervalos (classes) e indica quantas ocorrências existem em cada intervalo (frequência)
   - Frequência Absoluta:
   Quantas ocorrências ocorrem em cada intervalo (inteiro)
   - Frequência Relativa Decimal/Percentual:
   Frequência de ocorrências em em cada intervalo em relação ao todo (decimal/porcentagem)
   - Rol: dados ordenados em ordem crescente ou decrescente
   - Tamanho da amostra (n): quantidade total de itens da amostra
   - Classe: cada um dos intervalos
   - Amplitude total (AT): max - min
   diferença entre o valor máximo e o valor mínimo da amostra
   - Número de classes (K): sqrt(n)
   quantidade de intervalos sugerida para uma boa apresentação, pode ser arredondada pra cima
   - Amplitude da classe (h): AT / K
   indica quantos itens, ou o tamanho que cada intervalo (classe) deve ter
   define o limite inferior (min) e o limite superior (li + h) de cada classe
"""

# venv\Scripts\activate
import pandas as pd
# pip install scipy
from scipy.stats import trim_mean
import numpy as np
import distribuicao_frequencias
# pip install matplotlib
import matplotlib.pylab as plt

# imprimir o docstring
print(distribuicao_frequencias.__doc__) # Imprime a docstring da função

# importar os dados do csv
df_dados_brutos = pd.read_csv('homicidios_por_populacao/taxa_homicidios.csv')

# Serie trabalhada (População ou Taxa Homicídio)
# serie = df_dados_brutos['Populacao']
serie = df_dados_brutos['Taxa homicidios']
# Rol
rol = serie.sort_values()
# Tamanho da amostra
n = len(rol)
# Amplitude total
at = rol.max() - rol.min()
# Número de classes (usaremos numpy ao invés de math)
k = np.ceil(np.sqrt(n))
# Amplitude da classe
if at < 1:
   h = at / k
else:
   h = np.ceil(at / k)

# dataframe 01
df_variaveis_frequencia = pd.DataFrame({
   'Variável Estatística': [
      'Rol',
      'Tamanho Amostra (n)',
      'Amplitude Total (AT)',
      'Número de Classes (k)',
      'Amplitude da Classe (h)'
   ],
   'Valor Calculado': [
      rol.to_numpy(),
      n,
      at,
      k,
      h
   ]
})
print(df_variaveis_frequencia)

# separar os intervalos (classes)
classes = pd.cut(serie, k.astype(int))
# conta quantas ocorrências acontecem em cada intervalo (classes), Aqui já pode ser usado como tabela simples de frequência
print("\n Tabela simples de frequência: \n")
print(classes.value_counts())
print("\n")
# muda o nome da serie, na linha anterior imprimiu 'Name: count', nomeamos para não ficar se referindo a serie como count
classes.name = 'classes'
# concat: concatena dois dataframes ou series
# axis: onde a concatenação irá ocorrer(horiz, vertic)
df_dist_frequencia = pd.concat([df_dados_brutos, classes], axis=1)
# odena todo o dataframe baseado na população/Taxa homicídios (diferente do rol aqui é o dataframe inteiro e não apenas a serie isolada)
# df_dist_frequencia = df_dist_frequencia.sort_values(by='Populacao')
df_dist_frequencia = df_dist_frequencia.sort_values(by='Taxa homicidios')
# groupby: agrupa o dataframe com base nos valores únicos da coluna classes
# observed: diz se um intervalo(classe) vazio vai ou não aparecer [mudar k = 10 para mostrar que nosso cálculo sqrt(n) é justamente para evitar isso]
# group: valor do intervalo em cada loop. ex: (632060.75, 1430554.5]
# subset: dataframe com as frequências que existem em cada intervalo do loop. ex: [South Alexandra, 635242, 14.0, (632060.75, 1430554.5]]
groups = []
for group, subset in df_dist_frequencia.groupby(by='classes', observed=False):
   # mostrar para os alunos e depois apagar
   #print("\n group \n")
   #print(group)
   #print("\n subset \n")
   #print(subset)

   # frequencia absoluta
   # se supbset são todas as frequências do intervalo, contar vai dizer a frequência absoluta
   freq_abs = len(subset)
   # frequencia relativa
   freq_rel_dec = freq_abs / n
   freq_rel_perc = freq_rel_dec * 100
   # nome cidade
   cidades = ','.join(subset.Cidade)
   # data frame
   groups.append({
      'Classes': group, # classe_populacao no index informado
      'Frequência absoluta': freq_abs, 
      'Frequência relativa': np.round(freq_rel_dec, decimals=2),
      'Frequência relativa (%)': np.round(freq_rel_perc, decimals=2),
      'Cidades': cidades
   })
df_tabela_dist_freq =  pd.DataFrame(groups)
print(df_tabela_dist_freq.to_string(index=False))

'''
histograma = (df_dados_brutos['Populacao'] / 1_000_000).plot.hist(figsize=(4, 4))
histograma.set_xlabel('População (milhões)')
histograma.set_ylabel('Frequência (Número de Cidades)')
plt.tight_layout()
plt.show()
'''
bins_do_grafico = [1.387, 4.7, 8.0, 11.3]
# histograma = (df_dados_brutos['Taxa homicidios']).plot.hist(figsize=(4, 4))
histograma = (df_dados_brutos['Taxa homicidios']).plot.hist(figsize=(6, 4), bins=bins_do_grafico)
histograma.set_xlabel('Taxa de Homicídios')
histograma.set_ylabel('Frequência (Número de Cidades)')
plt.tight_layout()
plt.show()