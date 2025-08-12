# 1. Importação de Bibliotecas
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

## Multiple linear regression
# importa o CSV e define uma lista de colunas (subset) do arquivo CSV 'data/house_sales.csv' que serão utilizadas para a análise.
HOUSE_CSV = 'data/house_sales.csv'
subset = ['AdjSalePrice', 'SqFtTotLiving', 'SqFtLot', 'Bathrooms', 
          'Bedrooms', 'BldgGrade']
# O arquivo CSV é lido para um DataFrame house. O separador utilizado é a vírgula
house = pd.read_csv(HOUSE_CSV, sep='\t')
print(house[subset].head())

# As variáveis preditoras (SqFtTotLiving, SqFtLot, Bathrooms, Bedrooms, BldgGrade) 
# e a variável alvo (AdjSalePrice) são definidas para o modelo de regressão.
predictors = ['SqFtTotLiving', 'SqFtLot', 'Bathrooms', 
              'Bedrooms', 'BldgGrade']
outcome = 'AdjSalePrice'

# Uma instância do modelo de regressão linear (LinearRegression) é criada e atribuída à variável house_lm.
house_lm = LinearRegression()
# O modelo é treinado usando as variáveis preditoras e a variável alvo do DataFrame house. Este é o processo de ajuste do modelo aos dados.
house_lm.fit(house[predictors], house[outcome])

'''
O intercepto e os coeficientes do modelo são exibidos. 
O intercepto é o valor de AdjSalePrice quando todas as variáveis preditoras são zero. 
Cada coeficiente representa a mudança na variável alvo para cada aumento unitário na variável preditora correspondente, 
mantendo as outras variáveis constantes.
Intercepto: O valor de **228.830$ é o intercepto do modelo.
'''
print(f'Intercept: {house_lm.intercept_:.3f}')
'''
Coeficientes:
SqFtTotLiving: Para cada aumento de 1$ em SqFtTotLiving, AdjSalePrice aumenta em aproximadamente 218.83.
SqFtLot: Para cada aumento de 1$ em SqFtLot, AdjSalePrice aumenta em aproximadamente 0.05.
Bathrooms: Para cada aumento de 1$ em Bathrooms, AdjSalePrice aumenta em aproximadamente -1945. (Valor negativo)
Bedrooms: Para cada aumento de 1$ em Bedrooms, AdjSalePrice aumenta em aproximadamente -4776. (Valor negativo)
BldgGrade: Para cada aumento de 1$ em BldgGrade, AdjSalePrice aumenta em aproximadamente 106106.
'''
print('Coefficients:')
for name, coef in zip(predictors, house_lm.coef_):
    print(f' {name}: {coef}')

### Avaliar a Qualidade do modelo
# _Scikit-learn_ provides a number of metrics to determine the quality of a model. Here we use the `r2_score`.
# O modelo é usado para fazer previsões (fitted) com base nas variáveis preditoras.
fitted = house_lm.predict(house[predictors])
# O RMSE (Root Mean Squared Error) é calculado. O RMSE é uma medida da magnitude dos erros entre os valores previstos e os valores reais. 
# Valores menores de RMSE indicam um melhor ajuste.
RMSE = np.sqrt(mean_squared_error(house[outcome], fitted))
# O R2 score é calculado. O R2 (coeficiente de determinação) indica a 
# proporção da variância na variável alvo que é previsível a partir das variáveis preditoras. 
# Valores mais próximos de 1 indicam um melhor ajuste do modelo.
r2 = r2_score(house[outcome], fitted)
'''
 O valor de 261220 indica a magnitude média dos erros de previsão do modelo, na mesma unidade da variável AdjSalePrice.
'''
print(f'RMSE: {RMSE:.0f}')
'''
R² Score: O valor de 0.5406 indica que aproximadamente 54% da variabilidade no preço ajustado de venda pode ser explicada pelas variáveis preditoras no modelo.
'''
print(f'r2: {r2:.4f}')

'''
interpretar o RMSE. 
O valor de 261.220 não é necessariamente baixo ou alto por si só; sua interpretação depende diretamente da escala dos preços das casas no conjunto de dados.
O RMSE é uma medida da magnitude do erro na mesma unidade da variável que você está prevendo. 
Se o preço das casas varia, por exemplo, de R$ 300.000 a R$ 2.000.000, um erro médio de R$ 261.220 pode ser considerado alto. 
No entanto, se os preços das casas variam de R$ 1.500.000 a R$ 10.000.000, esse mesmo erro pode ser visto como mais aceitável.
Uma maneira mais robusta de avaliar o RMSE é compará-lo com:
- O desvio padrão da variável de saída: Se o RMSE for muito menor que o desvio padrão, isso sugere que o modelo tem algum poder preditivo.
- O valor médio da variável de saída: Você pode calcular o RMSE percentual para ter uma ideia do erro em relação ao valor médio.
'''
# 37. Calcula o desvio padrão da variável alvo
std_dev_adj_sale_price = np.std(house['AdjSalePrice'])
print(f'Desvio Padrão de AdjSalePrice: {std_dev_adj_sale_price:.2f}')

# 38. Calcula o RMSE percentual
# (Substitua a variável 'house[outcome]' pela sua variável alvo original)
rmse_percentual = (RMSE / np.mean(house['AdjSalePrice'])) * 100
print(f'RMSE Percentual: {rmse_percentual:.2f}%')

'''
Uma pontuação de 0,54 é um bom ponto de partida para um modelo preditivo, mostrando que ele é significativamente melhor do que simplesmente adivinhar o preço médio.
O RMSE de 261.220 e o Desvio Padrão de 385.394,37 nos contam uma história muito importante sobre o erro do modelo em relação à dispersão dos dados:
O desvio padrão representa a dispersão típica dos próprios preços das casas. Em seu conjunto de dados, os preços estão, em média, cerca de 385.394 distantes do preço médio. 
Isso indica um alto grau de variabilidade no mercado.
O RMSE representa o erro médio das previsões do seu modelo. O erro típico do modelo de 261.220 é menor do que a dispersão natural dos dados (385.394).
Isso é um sinal positivo! Significa que seu modelo, em média, está fazendo previsões que estão mais próximas dos preços reais do que uma simples suposição baseada no preço médio estaria.
O RMSE Percentual de 46,21% fornece um contexto mais intuitivo para o erro. Significa que, em média, o erro de previsão do modelo é de cerca de 46% do preço médio da casa. 
Esse número pode parecer alto à primeira vista, mas está diretamente relacionado à alta variância nos dados.
'''

