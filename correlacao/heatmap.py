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

Correlação entre ETFs de Tecnologia e Defensivos:
Procure a linha/coluna do GLD (ouro). 
  Você verá que a maioria dos quadrados que cruzam com os ETFs de tecnologia (como QQQ, SPY, XLK) têm cores neutras (cinza) ou levesmente laranjas. 
  Isso indica uma correlação fraca ou, em alguns casos, levemente negativa. Por quê? Porque quando a economia está indo bem e as empresas de tecnologia estão subindo, 
  os investidores tendem a sair de ativos seguros como o ouro para buscar retornos mais altos. Quando a economia vai mal, eles fazem o movimento contrário, 
  o que faz o ouro subir enquanto as ações de tecnologia caem.
Procure a linha/coluna do VXX (volatilidade). 
  Essa é a evidência mais forte. Você pode ver que o VXX tem uma correlação negativa clara (quadrados em laranja/vermelho) com quase todos os outros ETFs, 
  especialmente os de tecnologia (QQQ, SPY, XLK). Isso é exatamente o que se espera: o VXX sobe (medo aumenta) quando o mercado de ações (e os ETFs de tecnologia) está caindo.
Procure a linha/coluna do USO (petróleo). 
  A correlação do USO com os outros ETFs parece ser mais fraca (cores neutras) ou até levemente negativa. 
  O preço do petróleo é muito influenciado por fatores que nem sempre se alinham com o desempenho do setor de tecnologia.

ETFs defensivos (GLD, VXX) são projetados para se comportar de maneira diferente dos ETFs tradicionais de ações (como QQQ e SPY), especialmente em momentos de incerteza econômica. 
Eles são ferramentas de diversificação.
O ouro (GLD) é um ativo de refúgio, que tende a ter correlação fraca/negativa com ações.
A volatilidade (VXX) tem uma correlação negativa, pois sobe em momentos de pânico e incerteza, quando as ações de tecnologia tendem a cair.
Isso mostra que um portfólio bem construído inclui ativos com correlações baixas ou negativas, para que quando um setor está em baixa, outro possa compensar as perdas.
'''