# imports
import pandas as pd

import seaborn as sns
import matplotlib.pylab as plt

# caminho para os data set
SP500_DATA_CSV = 'correlacao/sp500_data.csv.gz'
SP500_SECTORS_CSV = 'correlacao/sp500_sectors.csv'

## Correlation
# First read the required datasets
print('classificação setorial de empresas que fazem parte do índice S&P 500')
sp500_sym = pd.read_csv(SP500_SECTORS_CSV)
print(sp500_sym.head())
print('... \n')

print('retorno diário de empresas que fazem parte do índice S&P 500')
sp500_px = pd.read_csv(SP500_DATA_CSV, index_col=0)
print(sp500_px.head())
print('... \n')

# Determine telecommunications symbols
telecomSymbols = sp500_sym[sp500_sym['sector'] == 'telecommunications_services']['symbol']
print(telecomSymbols.head())

# Filtrar dados por data
#                    T       CTL       FTR        VZ      LVLT
# 2012-07-02  0.422496  0.140847  0.070879  0.554180 -0.519998
# 2012-07-03 -0.177448  0.066280  0.070879 -0.025976 -0.049999
telecom = sp500_px.loc[sp500_px.index >= '2012-07-01', telecomSymbols]
# Correlacionar os dados em uma matriz
#             T       CTL       FTR        VZ      LVLT
# T    1.000000  0.474683  0.327767  0.677612  0.278626
# CTL  0.474683  1.000000  0.419757  0.416604  0.28666
# FTR   0.327767  0.419757  1.000000  0.287386  0.260068
# VZ    0.677612  0.416604  0.287386  1.000000  0.242199
# LVLT  0.278626  0.286665  0.260068  0.242199  1.000000
dados_correlacionados = telecom.corr()
print(dados_correlacionados.head())

# Next we focus on funds traded on major exchanges (sector == 'etf').

etfs = sp500_px.loc[sp500_px.index > '2012-07-01', 
                    sp500_sym[sp500_sym['sector'] == 'etf']['symbol']]
etfs_correlacionados = etfs.corr()
print(etfs_correlacionados.head(5))

# Due to the large number of columns in this table, looking at the correlation matrix is cumbersome and it's more convenient to plot the correlation as a heatmap. 
# The _seaborn_ package provides a convenient implementation for heatmaps.


'''
- vmin e vmax:
Definem o valor mínimo e máximo para a escala de cores do seu mapa de calor.
os valores variam de -1 (correlação negativa perfeita) a 1 (correlação positiva perfeita).
O valor zero ficará exatamente no meio da escala.
- cmap:
é o argumento que determina a paleta de cores usada para colorir o mapa de calor.
Em vez de usar um nome de paleta pré-definido (como 'viridis' ou 'coolwarm'), 
você está usando a função sns.diverging_palette para criar uma paleta de cores personalizada.
- sns.diverging_palette:
Esta função é usada para gerar uma paleta de cores que "diverge". 
Isso significa que ela começa com uma cor para valores negativos, passa por uma cor neutra para o zero, e termina com uma cor diferente para valores positivos. 
É ideal para dados de correlação.
- 20 e 220:
São números que representam os "tons" (hues) no sistema de cores HSL (Hue, Saturation, Lightness).
O número 20 corresponde a um tom alaranjado ou avermelhado, e o número 220 corresponde a um tom azulado. 
- as_cmap=True:
Este é um parâmetro booleano (verdadeiro/falso). Ele instrui a função diverging_palette a retornar a paleta de cores como um objeto de colormap do matplotlib, 
que é o formato que a função sns.heatmap precisa para ser usado no argumento cmap.
'''

# fig, (telecomax, etfax) = plt.subplots(2, 1, figsize=(5, 10))
fig, (telecomax, etfax) = plt.subplots(1, 2, figsize=(10, 5))
telecomax = sns.heatmap(telecom.corr(), vmin=-1, vmax=1, 
                 cmap=sns.diverging_palette(20, 220, as_cmap=True),
                 ax=telecomax)
etfax = sns.heatmap(etfs.corr(), vmin=-1, vmax=1, 
                 cmap=sns.diverging_palette(20, 220, as_cmap=True),
                 ax=etfax)

plt.tight_layout()
plt.show()

'''
T (AT&T), VZ (Verizon), CTL (na época CenturyLink) e FTR (Frontier)
operavam principalmente no mercado de consumidores finais e pequenas empresas. Seus principais fluxos de receita vinham de:
- Serviços de telefonia e internet residencial.
- Planos de telefonia móvel.
- Serviços de TV por assinatura.
Isso significa que a performance dessas ações estava muito ligada a fatores como a competição no mercado de consumo, 
o poder de compra das famílias e os ciclos econômicos que afetam diretamente o consumidor.

Level 3 Communications (LVLT), era uma empresa de um nicho diferente. 
Ela se concentrava em infraestrutura de rede de grande escala e serviços para grandes corporações. 
Seu modelo de negócio era B2B (business-to-business), e ela vendia:
- Redes de backbone: A infraestrutura principal da internet, usada por outras operadoras e grandes empresas.
- Serviços de data center e soluções de nuvem para empresas.
- Conectividade de alta capacidade para governos e multinacionais.
A sua receita vinha de contratos de longo prazo com grandes clientes e estava mais atrelada ao crescimento do 
tráfego global de dados e à demanda por serviços de infraestrutura corporativa

(Exchange Traded Funds), que são fundos de investimento que replicam um índice
ETFs de Renda Variável Tradicionais (Tecnologia, Setores, etc.):
  QQQ: Acompanha o índice Nasdaq-100, com forte concentração em empresas de tecnologia.
  SPY: Acompanha o S&P 500, um índice com as 500 maiores empresas de capital aberto dos EUA, incluindo muitas de tecnologia.
  DIA: Acompanha o Dow Jones Industrial Average, composto por 30 grandes empresas.
ETFs Setoriais (XLE, XLY, etc.): 
  Acompanham setores específicos da economia. Muitos deles (como o XLK, que é de tecnologia) são muito sensíveis às condições econômicas.
ETFs Defensivos (Acompanham Ouro, Petróleo, Volatilidade):
  GLD: Acompanha o preço do ouro. O ouro é tradicionalmente visto como um "ativo de refúgio" ou "porto seguro".
  USO: Acompanha o preço do petróleo. Embora possa ter correlação positiva com a economia em alguns momentos, 
  muitas vezes é negociado com base em fatores geopolíticos e de oferta/demanda que não estão diretamente ligados ao desempenho das empresas de tecnologia.
  VXX: Acompanha a volatilidade do mercado, usando opções do índice VIX. O VIX é popularmente conhecido como o "medidor do medo". 
  O VXX sobe quando o mercado está volátil e incerto, o que geralmente acontece quando as ações (como as de tecnologia) estão caindo.

GLD
A baixa correlação se dá porque o preço do ouro é influenciado por diversos fatores que não estão diretamente ligados ao desempenho das empresas de tecnologia, como:
- Inflação: O ouro é um tradicional hedge contra a inflação, então seu preço tende a subir quando o poder de compra da moeda cai.
- Força do Dólar Americano: Como o ouro é cotado em dólar, um dólar mais forte pode tornar o ouro mais caro para compradores internacionais, reduzindo a demanda.
- Taxas de juros: Quando as taxas de juros sobem, o ouro (que não paga juros) se torna menos atrativo.

USO
O petróleo, tem ainda menos relação direta com o desempenho diário das empresas de tecnologia. Seu preço é movido principalmente por:
Geopolítica: Guerras, sanções e decisões da OPEP (Organização dos Países Exportadores de Petróleo).
Oferta e Demanda Global: O nível de produção de petróleo e a demanda de países industriais como China e EUA.
Esses fatores são, em sua maioria, completamente independentes do que faz as ações da Apple ou da Microsoft subirem ou descerem.

VXX 
é um instrumento financeiro que, por definição, é inversamente correlacionado com o mercado.

ETFs defensivos (GLD, VXX) são projetados para se comportar de maneira diferente dos ETFs tradicionais de ações (como QQQ e SPY), especialmente em momentos de incerteza econômica. 
Eles são ferramentas de diversificação.
O ouro (GLD) é um ativo de refúgio, que tende a ter correlação fraca/negativa com ações.
A volatilidade (VXX) tem uma correlação negativa, pois sobe em momentos de pânico e incerteza, quando as ações de tecnologia tendem a cair.
Isso mostra que um portfólio bem construído inclui ativos com correlações baixas ou negativas, para que quando um setor está em baixa, outro possa compensar as perdas.
'''