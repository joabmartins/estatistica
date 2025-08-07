# python -m venv sklearn-env
# sklearn-env\Scripts\activate  # activate
# pip install -U scikit-learn
#In order to check your installation, you can use:
#python -m pip show scikit-learn

from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

LUNG_CSV = 'DATA/LungDisease.csv'

## Simple Linear Regression
### The Regression Equation

lung = pd.read_csv(LUNG_CSV)
print(lung.head())

'''
lung.plot.scatter(x='Exposure', y='PEFR')
plt.tight_layout()
plt.show()
'''

predictors = ['Exposure']
outcome = 'PEFR'

model = LinearRegression()
model.fit(lung[predictors], lung[outcome])

'''
O intercepto, ou b0, é 424,583 e pode ser interpretado como o PFE previsto para um trabalhador com zero anos de exposição. 
O coeficiente de regressão, ou b1, pode ser interpretado da seguinte forma: 
para cada ano adicional de exposição de um trabalhador ao pó de algodão, a medição do PFE do trabalhador é reduzida em -4,185.
'''
print(f'Intercept: {model.intercept_:.3f}')
print(f'Coefficient Exposure: {model.coef_[0]:.3f}')

# Criar o gráfico de dispersão, alpha é a tranparência dos pontos
plt.figure(figsize=(10, 6)) # Define o tamanho da figura
sns.regplot(x='Exposure', y='PEFR', data = lung) 

# Mostrar o gráfico
plt.show()