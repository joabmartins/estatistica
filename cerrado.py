# pandas para criar a serie e usar quantile​
import numpy as np
import matplotlib.pylab as plt
lista_idade = [5, 6, 8, 12, 20, 36, 68, 79, 95, 120, 135]

plt.boxplot(lista_idade, vert=False)

P25 = np.quantile(lista_idade, 0.25)
P50 = np.quantile(lista_idade, 0.50)
P75 = np.quantile(lista_idade, 0.75)
print(f'Q1: {P25}, Q2: {P50}, Q3: {P75}')
plt.show()