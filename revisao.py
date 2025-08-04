# S&P 500: Standard & Poor's 500
# um dos índices de mercado mais importantes e amplamente acompanhados do mundo. 
# Ele representa a performance das 500 maiores empresas de capital aberto dos Estados Unidos, 
# listadas nas bolsas de valores NYSE e NASDAQ.
#  - Indicador Econômico: O S&P 500 é considerado um excelente termômetro da saúde da economia americana. (80% da capitalização total do mercado de ações dos EUA).
#  - Composição Diversificada: O índice não se restringe a um setor específico. Ele inclui empresas de diversas áreas, como tecnologia, saúde, finanças, bens de consumo e energia.
#  - Ponderação por Capitalização de Mercado: A influência de cada empresa no índice não é igual. As companhias com maior valor de mercado (capitalização) têm um peso maior no cálculo, 
#    o que significa que o desempenho de gigantes como Apple, Microsoft e Alphabet (Google) impacta mais o valor final do índice.

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# manter caminho em uma variável (observe que o formato é .gz, não precisa descompactar para o pandas ler)
data = 'correlacao/sp500_data.csv.gz'

# salvar dados em um dataframe
# variação percentual diária (ou retorno diário) de cada ativo.
# ações ou ativos. Cada coluna, como "MSFT", "IBM", "XRX", representa a variação do preço das ações de uma empresa específica.
df = pd.read_csv(data)
print(df.head(5))

# 1. Renomear a coluna de datas para facilitar
df = df.rename(columns={'Unnamed: 0': 'Data'})

# 2. Definir a coluna 'Data' como índice do dataframe e converter para o tipo datetime
df['Data'] = pd.to_datetime(df['Data'])
df = df.set_index('Data')
# Encontrar a menor e a maior data
data_inicio = df.index.min()
data_fim = df.index.max()

# 3. Excluir a primeira coluna 'ADS' se ela for irrelevante, pois parece ter valores 0.0
# Caso ela represente uma empresa, você pode removê-la desta linha
df = df.drop(columns=['ADS'])

# 4. guarde em uma varíável o ativo que deseja explorar
ativo = 'IBM'

# 5. Encontrar o valor máximo e sua data para a ação específica
# .idxmax() e .idxmin(): Esses métodos, quando aplicados a uma Series, retornam o índice do valor máximo ou mínimo. 
# Como definimos a coluna 'Data' como o índice do dataframe no início, idxmax() e idxmin() nos dão a data em que os eventos ocorreram, exatamente como você pediu.
maior_valor = df[ativo].max()
data_maior = df[ativo].idxmax()

# 6. Encontrar o valor mínimo e sua data para a ação específica
menor_valor = df[ativo].min()
data_menor = df[ativo].idxmin()

# 7. Exibir os resultados para a IBM: Preste atenção na formatação de data e de pontos flutuantes, além da separação
print(f"\nResultados para a ação da {ativo}:")
print("-" * 30)
print(f"Quantidade de variações/dias calculados: {len(df)}")
print(f"Período de coleta: {data_inicio.strftime('%d/%m/%Y')} à {data_fim.strftime('%d/%m/%Y')}")
print("-" * 30)
print(f"Maior variação diária: {maior_valor:.4f}")
print(f"Ocorreu no dia: {data_maior.strftime('%d/%m/%Y')}")
print("-" * 30)
print(f"Menor variação diária: {menor_valor:.4f}")
print(f"Ocorreu no dia: {data_menor.strftime('%d/%m/%Y')}")
# print(f"Ocorreu no dia: {data_menor_ibm.strftime('%Y-%m-%d')}")

# MEDIDAS DE TENDÊNCIA CENTRAL
media = df[ativo].mean()
mediana = df[ativo].median()
moda = df[ativo].mode()

print(f"\nMedidas de tendência central para {ativo}:")
print("-" * 30)
print(f"Media: {media:.4f}")
print(f"Mediana: {mediana:.4f}")
print("Moda:")
if (len(moda) > 0):
     print(moda.to_string(index=False))
else:
     print(f"O ativo {ativo} é amodal, e não possui um valor predominante.")
df_frequencia = df[ativo].value_counts()
print(df_frequencia.head(5))
print("-" * 30)

# ESTIMATIVAS DE VARIABILIDADE
desvio_abs_medio = np.mean(np.abs(df[ativo] - media))
variancia = np.var(df[ativo], ddof=1)
desvio_padrao = np.std(df[ativo], ddof=1)

print(f"\nEstimativas de variabilidade para {ativo}:")
print("-" * 30)
print(f"Desvio Absoluto Médio: {desvio_abs_medio:.4f}")
print(f"Variância: {variancia:.4f}")
print(f"Desvio Padrão: {desvio_padrao:.4f}")
print("-" * 30)

# GRÁFICOS
serie_as_dataframe = pd.DataFrame(df[ativo])
print(len(serie_as_dataframe))
print(serie_as_dataframe.head(10))

'''
# Histograma
plt.figure() # Cria a primeira figura (janela)
sns.histplot(data=serie_as_dataframe)
plt.xlabel("variação percentual diária")
plt.ylabel("Ocorrências")
plt.title("Histograma")

# Boxplot (explicar o boxplot especialmente quartis e os dados fora dos quartis)
# 5, 20, 25, 30, 35, --- 40, 45, 50, 55, 100
# Q2 = (35+40)/2=37.5 Q1 = 25 Q3 = 50
# IQR = Q3 - Q1 = 50 - 25 = 25
# LIMITE INFERIOR = Q1 - 1.5 * IQR = 25 - 1.5 * 25 = 25 - 37.5 = -12.5
# LIMITE SUPERIOR = Q3 + 1.5 * IQR = 50 + 1.5 * 25 = 50 + 37.5 = 87.5
# O valor 100 está acima do limite superior de 87.5. Portanto, ele seria plotado como um ponto individual (um outlier) no boxplot.
# Os "bigodes" do boxplot iriam até o menor valor que não é outlier (5) e até o maior valor que não é outlier (55).
# A caixa do boxplot representaria a faixa de notas entre 25 e 50, que é onde se concentram os 50% dos alunos que não tiraram a nota mínima ou a máxima extrema.
#  dados = pd.DataFrame({'num': [5, 20, 25, 30, 35, 40, 45, 50, 55, 100]}).sort_values(by='num')
#  plt.figure()
#  sns.boxplot(data=dados)
#  plt.show()
plt.figure() # Cria a segunda figura (janela)
sns.boxplot(data=serie_as_dataframe)
plt.ylabel("variação percentual diária")
plt.title("Boxplot")

# Densidade (explicar o porque da densidade e o y ser decimais)
plt.figure() # Cria a primeira figura (janela)
sns.kdeplot(data=serie_as_dataframe)
plt.xlabel("variação percentual diária")
plt.ylabel("Ocorrências")
plt.title("Densidade")
'''
fig, (histograma, caixa, densidade) = plt.subplots(3, 1, figsize=(8, 18))
# Histograma
sns.histplot(data=serie_as_dataframe, ax=histograma, kde=False)
histograma.set_xlabel("variação percentual diária")
histograma.set_ylabel("Ocorrências")
histograma.set_title("Histograma")

# Boxplot (explicar o boxplot especialmente quartis e os dados fora dos quartis)
sns.boxplot(data=serie_as_dataframe, ax=caixa)
caixa.set_ylabel("variação percentual diária")
caixa.set_title("Boxplot")

# Densidade (explicar o porque da densidade e o y ser decimais)
sns.kdeplot(data=serie_as_dataframe, ax=densidade)
densidade.set_xlabel("variação percentual diária")
densidade.set_ylabel("Ocorrências")
densidade.set_title("Densidade")

# Ajusta o layout para evitar sobreposição
plt.tight_layout()
plt.show()


# ensinar os alunos a apontar para outro remote (meu repo) e subir as alterações em uma branch com nome deles