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
    