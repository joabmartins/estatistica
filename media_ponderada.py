# --- Exemplo 1: Média Ponderada para Dados de Sensores (Lidando com Precisão Desigual) ---

# Dados de temperatura de cada sensor (25 leituras no total)
# Sensor A (10 leituras - Mais Preciso)
sensor_a_data = [20.1, 20.3, 20.0, 20.2, 20.1, 20.3, 20.0, 20.2, 20.1, 20.3]
# Sensor B (10 leituras - Precisão Média)
sensor_b_data = [20.5, 20.0, 21.0, 20.2, 20.8, 20.1, 20.6, 20.3, 20.9, 20.4]
# Sensor C (5 leituras - Menos Preciso)
sensor_c_data = [21.5, 19.8, 22.0, 20.0, 19.5]

# Combinar todos os dados em uma única lista para processamento
all_data = sensor_a_data + sensor_b_data + sensor_c_data

# Definir os pesos para cada tipo de sensor
# Cada leitura do Sensor A terá peso 3, Sensor B peso 2, Sensor C peso 1
weights_a = [3] * len(sensor_a_data)  # Cria uma lista de 3s do tamanho de sensor_a_data
weights_b = [2] * len(sensor_b_data)  # Cria uma lista de 2s do tamanho de sensor_b_data
weights_c = [1] * len(sensor_c_data)  # Cria uma lista de 1s do tamanho de sensor_c_data

# Combinar todos os pesos na mesma ordem dos dados
all_weights = weights_a + weights_b + weights_c
print("all data")
print(all_data)
print("all weitghts")
print(all_weights)

# --- Cálculo da Média Ponderada ---

# Inicializar variáveis para o numerador e denominador da fórmula
sum_weighted_values = 0  # Numerador: Soma (valor * peso)
sum_of_weights = 0       # Denominador: Soma (peso)

# Iterar sobre cada valor e seu peso correspondente
for i in range(len(all_data)):
    value = all_data[i]       # Pega o valor atual
    weight = all_weights[i]   # Pega o peso correspondente

    # Acumula o produto do valor pelo peso no numerador
    sum_weighted_values += (value * weight)
    # Acumula o peso no denominador
    sum_of_weights += weight

# Calcular a média ponderada dividindo o numerador pelo denominador
if sum_of_weights != 0: # Evita divisão por zero caso não haja pesos
    weighted_mean_sensors = sum_weighted_values / sum_of_weights
    print(f"--- Exemplo 1: Dados de Sensores ---")
    print(f"Soma dos valores ponderados (numerador): {sum_weighted_values:.2f}")
    print(f"Soma dos pesos (denominador): {sum_of_weights:.0f}")
    print(f"Média Ponderada das Temperaturas: {weighted_mean_sensors:.2f} °C")
else:
    print("Erro: A soma dos pesos é zero, não é possível calcular a média ponderada.")

# --- Cálculo da Média Aritmética Simples para Comparação ---
simple_mean_sensors = sum(all_data) / len(all_data)
print(f"Média Aritmética Simples das Temperaturas: {simple_mean_sensors:.2f} °C")
print("-" * 50) # Separador para o próximo exemplo

# --- Exemplo 2: Média Ponderada para Experimento Online (Corrigindo Representatividade Desigual) ---

# Dados de satisfação dos usuários (escala de 1 a 10)
# Usuários Ativos (15 respondentes)
active_users_satisfaction = [8, 9, 7, 8, 9, 10, 7, 8, 9, 8, 9, 7, 10, 8, 9]
# Usuários Ocasionais (10 respondentes)
occasional_users_satisfaction = [5, 6, 7, 4, 5, 6, 7, 4, 5, 6]

# Combinar todos os dados em uma única lista
all_satisfaction_data = active_users_satisfaction + occasional_users_satisfaction

# Definir as proporções dos grupos na população (real)
population_proportion_active = 0.70  # 70% Usuários Ativos
population_proportion_occasional = 0.30 # 30% Usuários Ocasionais

# Definir as proporções dos grupos na amostra coletada
sample_proportion_active = len(active_users_satisfaction) / len(all_satisfaction_data) # 15/25 = 0.60
sample_proportion_occasional = len(occasional_users_satisfaction) / len(all_satisfaction_data) # 10/25 = 0.40

# Calcular os pesos de correção para cada grupo
# Peso = (Proporção na População) / (Proporção na Amostra)
weight_active_group = population_proportion_active / sample_proportion_active # 1.1666666666666667
weight_occasional_group = population_proportion_occasional / sample_proportion_occasional # 0.7499999999999999

# Criar a lista de pesos individuais para cada dado na amostra
# Cada nota de um usuário ativo terá o peso 'weight_active_group'
weights_for_active_users = [weight_active_group] * len(active_users_satisfaction) # [1.16, 1.16, 1.16, 1.16, 1.16, 1.16, 1.16, 1.16, 1.16, 1.16, 1.16, 1.16, 1.16, 1.16, 1.16]
# Cada nota de um usuário ocasional terá o peso 'weight_occasional_group'
weights_for_occasional_users = [weight_occasional_group] * len(occasional_users_satisfaction) # [0.74, 0.74, 0.74, 0.74, 0.74, 0.74, 0.74, 0.74, 0.74, 0.74]

# Combinar todos os pesos em uma única lista na mesma ordem dos dados
all_satisfaction_weights = weights_for_active_users + weights_for_occasional_users # [1.16, 1.16, 1.16, 1.16, 1.16, 1.16, 1.16, 1.16, 1.16, 1.16, 1.16, 1.16, 1.16, 1.16, 1.16, 0.74, 0.74, 0.74, 0.74, 0.74, 0.74, 0.74, 0.74, 0.74, 0.74]

# --- Cálculo da Média Ponderada ---

# Inicializar variáveis para o numerador e denominador
sum_weighted_satisfaction = 0
sum_of_satisfaction_weights = 0

# Iterar sobre cada valor de satisfação e seu peso correspondente
for i in range(len(all_satisfaction_data)):
    value = all_satisfaction_data[i]
    weight = all_satisfaction_weights[i]

    sum_weighted_satisfaction += (value * weight)
    sum_of_satisfaction_weights += weight

# Calcular a média ponderada
if sum_of_satisfaction_weights != 0:
    weighted_mean_satisfaction = sum_weighted_satisfaction / sum_of_satisfaction_weights
    print(f"--- Exemplo 2: Experimento Online ---")
    print(f"Peso para Usuários Ativos: {weight_active_group:.3f}")
    print(f"Peso para Usuários Ocasionais: {weight_occasional_group:.3f}")
    print(f"Soma dos valores ponderados (numerador): {sum_weighted_satisfaction:.2f}")
    print(f"Soma dos pesos (denominador): {sum_of_satisfaction_weights:.2f}")
    print(f"Média Ponderada da Satisfação do Usuário: {weighted_mean_satisfaction:.2f}")
else:
    print("Erro: A soma dos pesos é zero, não é possível calcular a média ponderada.")

# --- Cálculo da Média Aritmética Simples para Comparação ---
simple_mean_satisfaction = sum(all_satisfaction_data) / len(all_satisfaction_data)
print(f"Média Aritmética Simples da Satisfação do Usuário: {simple_mean_satisfaction:.2f}")