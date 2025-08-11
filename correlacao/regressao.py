# python -m venv sklearn-env
# sklearn-env\Scripts\activate  # activate
# pip install -U scikit-learn
#In order to check your installation, you can use:
#python -m pip show scikit-learn

# 1. Importação de Bibliotecas
from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# 2. Carregamento e Preparação dos Dados

# Define o caminho para o arquivo de dados.
LUNG_CSV = 'DATA/LungDisease.csv'
# Lê o arquivo CSV e armazena os dados em um DataFrame
lung = pd.read_csv(LUNG_CSV)
# Exibe as primeiras 5 linhas do DataFrame, permitindo uma visualização rápida dos dados.
print(lung.head())

'''
# Cria o gráfico de DISPERSÃO
lung.plot.scatter(x='Exposure', y='PEFR')
# Exibe o gráfico de DISPERSÃO
plt.show()
'''

# 3. Configuração e Treinamento do Modelo

# Define a variável preditora (independente), que é a Exposure e a variável de resultado (dependente), que é o PEFR.
predictors = ['Exposure']
outcome = 'PEFR'
# Instancia o modelo de regressão linear.
model = LinearRegression()
# etapa de treinamento. O modelo ajusta a melhor linha de regressão aos dados, encontrando os valores ideais para o intercepto
# e o coeficiente angular Ele usa lung[predictors] como os dados de entrada (X) e lung[outcome] como os dados de saída (Y).
model.fit(lung[predictors], lung[outcome])

# 4. Exibição dos Coeficientes

'''
O intercepto, ou b0, é 424,583 e pode ser interpretado como o PEFR previsto para um trabalhador com zero anos de exposição. 
O coeficiente de regressão, ou b1, pode ser interpretado da seguinte forma: 
para cada ano adicional de exposição de um trabalhador ao pó de algodão, a medição do PEFR do trabalhador é reduzida em -4,185.
'''
# Retorna o valor do intercepto (beta_0), que é o ponto onde a linha de regressão cruza o eixo Y.
print(f'Intercept: {model.intercept_:.3f}')
# Retorna o coeficiente angular (beta_1) para a variável Exposure. 
# Como há apenas uma variável, acessamos o primeiro (e único) elemento do array de coeficientes.
print(f'Coefficient Exposure: {model.coef_[0]:.3f}')

# 5. Geração do Gráfico

# Criar o gráfico de dispersão, alpha é a tranparência dos pontos
#plt.figure(figsize=(10, 6)) # Define o tamanho da figura
#sns.regplot(x='Exposure', y='PEFR', data = lung) 

# Cria uma figura e um conjunto de eixos para dois gráficos.
fig, (reg, ax, res) = plt.subplots(1, 3, figsize=(12, 4))
# O primeiro gráfico é um gráfico de CORRELAÇÃO, é igual o de dispersão mas ele calcula e traça a reta usando o coef. angular
reg = sns.regplot(x='Exposure', y='PEFR', data = lung, ax=reg)
# Definem os limites dos eixos X e Y.
ax.set_xlim(0, 23)
ax.set_ylim(295, 450)
# Definem os rótulos dos eixos.
ax.set_xlabel('Exposure')
ax.set_ylabel('PEFR')
# Plota os pontos de dados (os valores reais de Exposure e PEFR) como círculos ('o') no gráfico. Isso gera os pontos azuis.
# ax.plot(lung['Exposure'], lung['PEFR'], 'o')
# ax.plot((0, 23), model.predict(pd.DataFrame({'Exposure': [0, 23]})))

# A linha de regressão é plotada aqui. O código prevê os valores de PEFR para dois pontos específicos no eixo X (Exposure = 0 e Exposure = 23).
ax.plot(lung['Exposure'], model.predict(lung[predictors]), '-')
# Adiciona o texto "b_0" (o intercepto) no gráfico na coordenada (0.4, model.intercept_). 
# A sintaxe r'$b_0$' é usada para formatar a string com LaTeX, exibindo o b_0 de forma matemática.
ax.text(0.4, model.intercept_, r'$b_0$', size='larger')
# Cria um DataFrame para plotar o triângulo do coeficiente angular.
x = pd.DataFrame({'Exposure': [7.5,17.5]})
# Prevê os valores de PEFR para Exposure de 7.5 e 17.5.
y = model.predict(x)
# Plota as linhas tracejadas laranja que formam o triângulo, representando DeltaY e DeltaX.
ax.plot((7.5, 7.5, 17.5), (y[0], y[1], y[1]), '--')
# Adiciona as anotações de DeltaY e DeltaX ao gráfico.
ax.text(5, np.mean(y), r'$\Delta Y$', size='larger')
ax.text(12, y[1] - 10, r'$\Delta X$', size='larger')
# Adiciona a anotação para o coeficiente angular b₁ com a sua fórmula de cálculo.
ax.text(12, 390, r'$b_1 = \frac{\Delta Y}{\Delta X}$', size='larger')

# Ajusta automaticamente os parâmetros da subtrama para que o gráfico caiba na área da figura.
plt.tight_layout()

# valores ajustados e resíduos
'''
A equação de regressão que você conhece, y=A+Bx, é uma forma simplificada de representar uma reta de regressão. 
Na realidade, a maioria dos dados no mundo real não se alinha perfeitamente a uma linha reta. 
É por isso que os modelos de regressão incluem um termo de erro e 
O resíduo é a diferença entre o valor observado e o valor ajustado (ou previsto).
O resíduo é, na prática, a sua estimativa do erro. Ele mostra o quanto a sua previsão errou em relação ao valor real.
Cada resíduo é a distância vertical de um ponto de dado até a linha de regressão.
'''
# 6. Gráfico de resíduos
# O terceiro gráfico, gerado por este código, é uma visualização dos resíduos do modelo de regressão. 
# Ele tem como objetivo mostrar a diferença (o erro de previsão) entre os valores reais e os valores previstos pelo modelo.

# Gera os valores ajustados (predicted) do modelo
fitted = model.predict(lung[predictors])
# Calcula os resíduos
residuals = lung[outcome] - fitted

# Conceitos importantes antes de partir para o gráfico:
 # lung.Exposure: Lista de valores reais coletados de x para cada y [0, 0, 0, 0, 1, 2, 2, 2] 
 # é o mesmo que lung[predictors] porém:
 # lung.Exposure retorna uma Series (unidimensional).
 # lung[predictors] retorna um DataFrame (bidimensional).
#print(f'exposure: \n {lung.Exposure}')
#print(f'predictors: \n {lung[predictors].head(10)}')
 # lung[outcome]: Lista de valores reais coletados de y para cada x [390, 410, 430, 460, 420, 280, 420, 520]
#print(f'outcome: \n {lung[outcome].head(10)}')
 # fitted: Lista de valores previstos para y para cada x [424.58 424.58 424.58 ... 332.52 332.52 328.33]
 # é a coodenada y na linha de regressão
#print(f'fitted: \n {fitted[0:3]} ... {fitted[119:121]}')
 # residuals: diferença entre o valor real e o valor previsto [-34.582807 -14.582807 5.417193 35.417193 -0.398230 -136.213654 3.786346 103.786346]
#print(f'residuals: \n {residuals.head(10)}')

# Exibe um gráfico de correlação, ou seja, apenas os pontos azuis coletados na posição x e y
res = lung.plot.scatter(x='Exposure', y='PEFR', ax = res)
# A função plt.plot(x, y) recebe uma lista ou array de valores para x e y. 
# Ela conecta os pontos sequencialmente na ordem em que eles aparecem nos arrays.
# Para traçar apenas pontos e não uma linha, você precisa especificar o formato. Por exemplo:
#    plt.plot(x, y, 'o') traçaria apenas os pontos como círculos.
#    plt.plot(x, y, '-') traçaria apenas a linha (o padrão).
res.plot(lung.Exposure, fitted)
# para cada valor de índice, pegue o índice de Exposure e atribua x, pegue o índice de PEFR e atribua yactual, pegue o índice de fitted e atribua yfitted
for x, yactual, yfitted in zip(lung.Exposure, lung.PEFR, fitted): 
    # para cada índice/valor trace uma linha pontilhada na cor secundária (C1=LARANJA) de x até x e de yatual até yfitted (reta vertical do ponto até a reta)
    res.plot((x, x), (yactual, yfitted), '--', color='C1')

# Exibe a figura e o gráfico na tela.
plt.show()

