"""
Histograma:
     Gráfico de barras que representa uma distribuição de frequência.
     - Eixo x (horiz): intervalos (classes) dos dados
     - Eixo y (vertc): frequência (contagem) de itens por intervalo
BoxPlot: 
     Diagrama de caixa que representa os extremos e mais os quartis
     - Min: O menor valor do conjunto de dados
     - Q1: Primeiro quartil dos dados (25%)
     - Q2: Segundo quartil dos dados, a mediana (50%)
     - Q3: Terceiro quartil dos dados (75%)
     - Max: O maior valor do conjunto de dados
Densidade:
     Gráfico que representa uma distribuição suavisada da frequência dos dados
     - Eixo x (horiz): intervalos (classes) dos dados
     - Eixo y (vertc): frequência (contagem) de itens por intervalo
Dispersão:
     Gráfico que representa a relação entre dois conjunto de dados
     - Eixos: Cada eixo representará um dos dois conjunto de dados
     - Pontos: Cada ponto representa a interseção entre as variáveis de ambos os conjuntos.

"""
# pip install matplotlib
import matplotlib.pylab as plt
import seaborn as sb
import graficos
import pandas as pd

# imprimir o docstring
print(graficos.__doc__) # Imprime a docstring da função

# importar os dados do csv
df_dados_brutos = pd.read_csv('homicidios_por_populacao/taxa_homicidios.csv')

def histograma():
     bins_do_grafico = [1.387, 4.7, 8.0, 11.3]
     histograma = (df_dados_brutos['Taxa homicidios']).plot.hist(figsize=(6, 4), bins=bins_do_grafico)
     histograma.set_xlabel('Taxa de Homicídios')
     histograma.set_ylabel('Frequência (Número de Cidades)')
     # plt.tight_layout()
     plt.show()

def boxplot():
     #ax = (df_dados_brutos['Populacao']/1_000_000).plot.box()
     #ax.set_ylabel('Populacao (milhoes)')
     ax = (df_dados_brutos['Taxa homicidios']).plot.box()
     ax.set_ylabel('Taxa de homicídios')
     # plt.tight_layout()
     plt.show()

def densidade():
     # 'Taxa Homicidios' (ordenados): 1.4, 2.6, 4.2, 4.6, 6.8, 7.3, 9.4, 9.5, 14.0, 14.6
     print(df_dados_brutos.sort_values(by=['Taxa homicidios']))
     histograma = (df_dados_brutos['Taxa homicidios']).plot.hist(density = True, bins = range(1, 16), figsize=(6, 4))
     df_dados_brutos['Taxa homicidios'].plot.density(ax = histograma)
     histograma.set_xlabel('Taxa de Homicídios')
     histograma.set_ylabel('Frequência (densidade)')
     plt.xlim(0, 15)
     # plt.tight_layout()
     plt.show()

def dispersao():
     # Criar o gráfico de dispersão, alpha é a tranparência dos pontos
     plt.figure(figsize=(10, 6)) # Define o tamanho da figura
     plt.scatter(df_dados_brutos['Populacao'], df_dados_brutos['Taxa homicidios'], alpha=0.7) 

     # Adicionar rótulos e título
     plt.xlabel('População')
     plt.ylabel('Taxa de Homicídios')
     plt.title('Gráfico de Dispersão: Taxa de Homicídios vs. População')
     plt.grid(True) # Adiciona uma grade ao gráfico
     # Mostrar o gráfico
     plt.show()

def correlacao():
     correlacao = df_dados_brutos[['Populacao', 'Taxa homicidios']].corr()
     plt.figure(figsize=(6,4))
     # correlacao: a matriz a ser representada
     # annot: mostrar ou não a legenda dos dados
     # cmap: tema de cores (cool azul frio, warm vermelho quente)
     # fmt: formatação dos números (.2f = 2 casa decimais)
     # linewidths: espessura da linha entre as células
     # sb.heatmap(correlacao, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
     plt.imshow(correlacao, cmap='coolwarm', interpolation='nearest')
     plt.colorbar()
     plt.show()


# histograma()
# boxplot()
# densidade()
# dispersao()
correlacao()