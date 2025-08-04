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

ax = telecom.plot.scatter(x='T', y='VZ', figsize=(4, 4), marker='$\u25EF$')
ax.set_xlabel('ATT (T)')
ax.set_ylabel('Verizon (VZ)')
ax.axhline(0, color='grey', lw=1)
ax.axvline(0, color='grey', lw=1)

plt.tight_layout()
plt.show()

ax = telecom.plot.scatter(x='T', y='VZ', figsize=(4, 4), marker='$\u25EF$', alpha=0.5)
ax.set_xlabel('ATT (T)')
ax.set_ylabel('Verizon (VZ)')
ax.axhline(0, color='grey', lw=1)
print(ax.axvline(0, color='grey', lw=1))
