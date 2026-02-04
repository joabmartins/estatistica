import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Criando o Dataset baseado nos casos de uso
data = {
    'Invest_Marketing': [10, 15, 20, 25, 30, 35, 40, 45, 50, 55],
    'Vendas_Mensais': [50, 55, 62, 68, 80, 85, 98, 105, 110, 125],
    'Horas_Treino': [2, 4, 6, 8, 10, 12, 14, 16, 18, 20],
    'Erros_Producao': [20, 18, 15, 16, 12, 10, 8, 9, 5, 4],
    'Idade_Imovel': [5, 50, 12, 35, 22, 40, 8, 15, 60, 2],
    'Preco_Venda': [300, 310, 290, 305, 315, 295, 300, 310, 305, 298]
}

df = pd.DataFrame(data)

# 2. Calculando a Matriz de Correlação (Pearson)
corr_matrix = df.corr()
print("Matriz de Correlação:")
print(corr_matrix)

# 3. Configurando a visualização
plt.figure(figsize=(14, 5))

# Gráfico de Calor (Heatmap)
plt.subplot(1, 2, 1)
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", linewidths=0.5)

plt.title('Mapa de Calor da Correlação')

# Gráfico de Dispersão (Exemplo: Marketing vs Vendas)
plt.subplot(1, 2, 2)
sns.scatterplot(x='Invest_Marketing', y='Vendas_Mensais', data=df, s=100, color='green')
plt.title('Dispersão: Marketing vs Vendas (Positiva)')
plt.grid(True)

plt.tight_layout()
plt.show()
