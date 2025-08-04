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
print(sp500_sym.head(2))
print('... \n')

print('retorno diário de empresas que fazem parte do índice S&P 500')
sp500_px = pd.read_csv(SP500_DATA_CSV, index_col=0)
print(sp500_px.head(2))
print('... \n')

# Determine telecommunications symbols
telecomSymbols = sp500_sym[sp500_sym['sector'] == 'telecommunications_services']['symbol']

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

# Next we focus on funds traded on major exchanges (sector == 'etf').

etfs = sp500_px.loc[sp500_px.index > '2012-07-01', 
                    sp500_sym[sp500_sym['sector'] == 'etf']['symbol']]
etfs_correlacionados = etfs.corr()
print(etfs_correlacionados.head(5))

# Due to the large number of columns in this table, looking at the correlation matrix is cumbersome and it's more convenient to plot the correlation as a heatmap. The _seaborn_ package provides a convenient implementation for heatmaps.

fig, ax = plt.subplots(figsize=(5, 4))
ax = sns.heatmap(etfs.corr(), vmin=-1, vmax=1, 
# ax = sns.heatmap(telecom.corr(), vmin=-1, vmax=1, 
                 cmap=sns.diverging_palette(20, 220, as_cmap=True),
                 ax=ax)

plt.tight_layout()
plt.show()