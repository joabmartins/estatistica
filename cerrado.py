
import pandas as pd
rol = [21, 21, 21, 22, 22, 22, 23, 23, 23, 23,
       24, 24, 25, 25, 25, 26, 27, 27, 28, 28,
       30, 30, 31, 31, 31]
# os limites inferiores e superiores
limites = [21, 23, 25, 27, 29, 31]
# criar um dataframe porque o pd.cut() precisa receber um dataframe
dataframe = pd.DataFrame({'Idades': rol})
# cortar (cut) o dataframe de acordo com os limites passados em bins
# passamos right=False para que o limite inferior seja incluso e o superior não
classes = pd.cut(dataframe['Idades'], bins=limites, right=False)
# fazendo um loop nas idades agrupadas de acordo com as classes
# - group: a descrição do intervalo em cada loop
# - subset: lista com os dados do intervalo em cada loop
for group, subset in dataframe.groupby(by=classes):
    # se subset é uma lista dos itens no intervalo
    # então é só verificar o tamanho da lista para obter 
    # quantos dados existem em cada intervalo
    freq_absoluta = len(subset)
    freq_relativa = freq_absoluta / len(rol)
    print(f"{group} | {freq_absoluta} | {freq_relativa}")