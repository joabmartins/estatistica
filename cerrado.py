
import pandas as pd
import numpy as np
import matplotlib.pylab as plt

lista_idade = [21, 21, 21, 22, 22, 22, 23, 23, 23, 23,
              24, 24, 25, 25, 25, 26, 27, 27, 28, 28,
              30, 30, 31, 31, 31]
serie = pd.Series(lista_idade)
histograma = serie.plot.hist(density = True, bins = range(21, 32), figsize=(6, 4))
serie.plot.density(ax = histograma)
histograma.set_xlabel('Idade dos alunos')
histograma.set_ylabel('Frequência (densidade)')
plt.xlim(21, 31)
# plt.tight_layout()
plt.show()
