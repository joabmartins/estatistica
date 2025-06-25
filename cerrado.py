
import pandas as pd
import numpy as np

lista_idade = [21, 21, 21, 22, 22, 22, 23, 23, 23, 23,
              24, 24, 25, 25, 25, 26, 27, 27, 28, 28,
              30, 30, 31, 31, 31]
# criando uma serie a partir de uma lista
serie_idades = pd.Series(lista_idade)
# usando a função pandas.median para calcular a moda
moda = serie_idades.mode()

print(moda)