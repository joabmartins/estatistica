# Dados de temperatura de cada sensor (25 leituras no total)
# Sensor A (10 leituras - Mais Preciso)
sensor_a_data = [20.1, 20.3, 20.0, 20.2, 20.1, 20.3, 20.0, 20.2, 20.1, 20.3]
# Sensor B (10 leituras - Precisão Média)
sensor_b_data = [20.5, 20.0, 21.0, 20.2, 20.8, 20.1, 20.6, 20.3, 20.9, 20.4]
# Sensor C (5 leituras - Menos Preciso)
sensor_c_data = [21.5, 19.8, 22.0, 20.0, 19.5]

all_data = sensor_a_data + sensor_b_data + sensor_c_data

peso_a = [3] * len(sensor_a_data)
peso_b = [2] * len(sensor_b_data)
peso_c = [1] * len(sensor_c_data)
all_pesos = peso_a + peso_b + peso_c
print(all_data)
print(all_pesos)

soma_valores = 0
soma_dos_pesos = 0

for i in range(len(all_data)):
    valor = all_data[i]
    peso = all_pesos[i]
    soma_valores += (valor * peso)
    soma_dos_pesos += peso

media_sensores = soma_valores / soma_dos_pesos
print(f">>> Exemplo 01: Dados dos Sensores <<<")
print(f"Soma dos valores ponderados: {soma_valores:.2f}")
print(f"Soma dos pesos: {soma_dos_pesos:.2f}")
print(f"Média Ponderada das Temperaturas:{media_sensores:.2f}")

media_simples = sum(all_data) / len(all_data)
print(f"Média Aritmética Simples das Temperaturas: {media_simples:.2f} °C")
    
print("*******")
# --- Exemplo 2: Média Ponderada para Experimento Online (Correção de Representatividade Desigual) ---

# Dados de satisfação dos usuários (escala de 1 a 10)
# Usuários Ativos (15 respostas)
satisfacao_usuarios_ativos = [8, 9, 7, 8, 9, 10, 7, 8, 9, 8, 9, 7, 10, 8, 9]
# Usuários Ocasionais (10 respostas)
satisfacao_usuarios_ocasionais = [5, 6, 7, 4, 5, 6, 7, 4, 5, 6]

amostra_completa = satisfacao_usuarios_ativos + satisfacao_usuarios_ocasionais

proporcao_populacao_ativa = 0.70 # 70% de todos são ativos
proporcao_populacao_ocasional = 0.30 # 30% de todos são ocasionais
proporcao_ativa_amostra = len(satisfacao_usuarios_ativos)/len(amostra_completa)
proporcao_ocasional_amostra = len(satisfacao_usuarios_ocasionais)/len(amostra_completa)
print(f"proporção usuários ativos na amostra: {proporcao_ativa_amostra}")
print(f"proporção usuários ocasionais na amostra: {proporcao_ocasional_amostra}")

peso_ativos_balanceado = proporcao_populacao_ativa / proporcao_ativa_amostra
peso_ocasionais_balanceado = proporcao_populacao_ocasional / proporcao_ocasional_amostra

array_pesos_ativos = [peso_ativos_balanceado] * len(satisfacao_usuarios_ativos)
array_pesos_ocasionais = [peso_ocasionais_balanceado] * len(satisfacao_usuarios_ocasionais)
array_todos_pesos = array_pesos_ativos + array_pesos_ocasionais

# -- Cálculo
soma_valores_ponderados = 0
soma_pesos = 0

for i in range(len(amostra_completa)):
    valor = amostra_completa[i]
    peso = array_todos_pesos[i]
    soma_valores_ponderados += (valor * peso)
    soma_pesos += peso

media_satisfacao_ponderada = soma_valores_ponderados / soma_pesos
print(f"Média Ponderada da Satisfação do usuário: {media_satisfacao_ponderada:.2f}")
media_simples = sum(amostra_completa) / len(amostra_completa)
print(f"Média Simples da Satisfação do usuário: {media_simples:.2f}")

