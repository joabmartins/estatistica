
import matplotlib.pylab as plt
import seaborn as sb
import pandas as pd

df = pd.DataFrame({'alunos': ['Matheus', 'Fernando', 'Ana', 'Beatriz', 'Bruna'],
                     'horas': [2, 4, 6, 8, 10],
                     'notas': [50, 70, 85, 95, 100]})
print(df)

# Criar o gráfico de dispersão, alpha é a tranparência dos pontos
plt.figure() # Define o tamanho da figura
plt.xlim(0, 12)
sb.regplot(x = 'horas', y = 'notas', data = df, truncate=False) 

# Adicionar rótulos e título
plt.xlabel('Horas de Estudo')
plt.ylabel('Notas da Prova')
plt.title('Gráfico de Dispersão: Horas de Estudo vs. Desempenho nas Provas')
# Mostrar o gráfico
plt.show()