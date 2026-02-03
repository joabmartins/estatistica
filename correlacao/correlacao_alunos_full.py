import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# 1. Carregar dados de exemplo (Dataset Iris)
df = pd.DataFrame({'alunos': ['Matheus', 'Fernando', 'Ana', 'Beatriz', 'Bruna'],
                     'estudo_h': [2, 4, 6, 8, 10],
                     'notas': [50, 70, 85, 95, 100],
                    'gaming_h': [9, 8, 5, 4, 2]
})

# 2. Calcular a matriz de correlação (apenas colunas numéricas)
corr_matrix = df.corr(numeric_only=True)
print(corr_matrix)

# 3. Criar o mapa de calor
fig, (sctplot, sctplot2, heatplot) = plt.subplots(1, 3, figsize=(15,5))
# plt.figure(figsize=(8, 6)) # Define o tamanho da figura
sns.heatmap(corr_matrix, 
            annot=True,     # Mostra os valores dentro das células
            cmap="coolwarm", # Paleta de cores (azul=negativo, vermelho=positivo)
            fmt=".2f",      # Formato dos números (2 casas decimais)
            linewidths=0.5, ax = heatplot) # Linha entre os quadrados

# 4. Adicionar título e exibir
heatplot.set_title("Mapa de Calor de Correlação (Dataset Iris)")

# plt.xlim(0, 12)
sns.regplot(x = 'estudo_h', y = 'notas', data = df, truncate=False, ax=sctplot) 
sns.regplot(x = 'gaming_h', y = 'notas', data = df, truncate=False, ax=sctplot2) 

# Adicionar rótulos e título
sctplot.set_title('Gráfico de Dispersão: Horas de Estudo/Gaming vs. Desempenho nas Provas')
plt.show()
