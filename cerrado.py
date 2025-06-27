
import pandas as pd

lista_idade = [21, 21, 21, 22, 22, 22, 23, 23, 23, 23,
              24, 24, 25, 25, 25, 26, 27, 27, 28, 28,
              30, 30, 31, 31, 31]

serie = pd.Series(lista_idade)

quartis = [0.25, 0.5, 0.75]
serie_quartis = serie.quantile(quartis)

print(serie_quartis)
