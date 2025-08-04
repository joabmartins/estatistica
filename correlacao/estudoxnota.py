
import matplotlib.pylab as plt
import seaborn as sb
import pandas as pd

df = pd.DataFrame({'alunos': ['Matheus', 'Fernando', 'Ana', 'Beatriz', 'Bruna'],
                     'horas': [2, 4, 6, 8, 10],
                     'notas': [50, 60, 85, 95, 100]})
print(df)

# Criar o gráfico de dispersão, alpha é a tranparência dos pontos
plt.figure(figsize=(10, 6)) # Define o tamanho da figura
sb.regplot(x = 'horas', y = 'notas', data = df) 

# Adicionar rótulos e título
plt.xlabel('Horas de Estudo')
plt.ylabel('Notas da Prova')
plt.title('Gráfico de Dispersão: Horas de Estudo vs. Desempenho nas Provas')
# Mostrar o gráfico
plt.show()