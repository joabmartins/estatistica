import pandas as pd
import numpy as np
import math

def analisar_dados_estatisticos(dados_brutos, nome_do_conjunto):
    print(f"--- Análise Estatística para: {nome_do_conjunto} ---")

    # 1. Rol (Dados Ordenados)
    rol = sorted(dados_brutos)
    print("\n1. Rol (Dados Ordenados):")
    print(f" {rol}")

    # 2. Tamanho da Amostra (n)
    n = len(rol)
    print("\n2. Tamanho da Amostra (n):")
    print(f" n = {n}")

    # 3. Valor Máximo e Mínimo
    x_min = rol[0]
    x_max = rol[-1]
    print("\n3. Valor Máximo e Mínimo:")
    print(f" valor min: {x_min}")
    print(f" valor max: {x_max}")

    # 4. Amplitude Total (AT)
    at = x_max - x_min
    print("\n4. Amplitude Total (AT): ")
    print(f" AT = {at:.2f}")

    # 5. Número de Classes (K)
    k = math.ceil(math.sqrt(n))
    print("\n5. Número de Classes (K):")
    print(f"K = {k}")
    
    # 6. Amplitude das Classes (h)
    if at < 1:
        h = at /k
    else:
        h = math.ceil(at / k)
    print("\n6. Amplitude das Classes (h):")
    print(f"h = {h}")

    classes = []
    frequencias_absolutas = []
    pontos_medios = []
    frequencias_relativas_dec = []
    frequencias_relativas_perc = []
    frequencias_absolutas_acum = []

    frequencia_abs_acum = 0
    limite_inferior = x_min
    for i in range(k): # k = 5 (número de classes)
        limite_superior = limite_inferior + h # h = 2
        # Classes
        classes.append(f"[{limite_inferior:.2f} --| {limite_superior:.2f}]")
        # Frequência Absoluta
        if i == k - 1:
            frequencia_absoluta = len([x for x in rol if limite_inferior <= x <= limite_superior])
        else:
            frequencia_absoluta = len([x for x in rol if limite_inferior <= x < limite_superior])
        frequencias_absolutas.append(frequencia_absoluta)
        # Ponto médio da classe
        pontos_medios.append((limite_inferior + limite_superior) / 2)
        # Relativa Decimal
        frequencias_relativas_dec.append(frequencias_absolutas[i] / n)
        # Relativa Absoluta Acumulada
        frequencia_abs_acum = frequencia_abs_acum + frequencias_absolutas[i]
        frequencias_absolutas_acum.append(frequencia_abs_acum)
        # Relativa Percentual
        frequencias_relativas_perc.append(frequencias_relativas_dec[i] * 100)
        limite_inferior = limite_superior

    df_frequencia = pd.DataFrame({
        'Classe': classes,
        'Ponto Médio': pontos_medios,
        'Frequência Absoluta': frequencias_absolutas,
        'Frequência Relativa Decimal': frequencias_relativas_dec,
        'Frequência Relativa Percentual (%)': frequencias_relativas_perc,
        'Frequência Absuluta Acumulada': frequencias_absolutas_acum
    })

    df_frequencia.loc['Total'] = [
        'Total',
        np.nan,
        df_frequencia['Frequência Absoluta'].sum(),
        df_frequencia['Frequência Relativa Decimal'].sum(),
        df_frequencia['Frequência Relativa Percentual (%)'].sum(),
        np.nan
    ]
    return df_frequencia


# --- ESTUDO DE CASO 01: IDADE DOS ALUNOS
dados_idades = [21, 21, 21, 22, 22, 22, 23, 23, 23, 23, 24, 24, 25, 25, 25, 26, 27, 27, 28, 28, 30, 30, 31, 31, 31]
df_idades = analisar_dados_estatisticos(dados_idades, "Idades dos Alunos")
print(df_idades.to_string(float_format="%.2f"))

# -- ESTUDO DE CASO 02 : TEMPO DE ATENDIMENTO EM CALL CENTER
dados_call_center = [5.2, 8.1, 6.5, 12.0, 7.3, 5.8, 9.5, 11.2, 6.0, 7.8, 5.5, 10.1, 6.7, 7.0, 8.5, 13.5, 6.2, 7.5, 9.0, 10.5, 5.0, 8.8, 6.9, 7.2, 11.5, 6.3, 9.8, 10.0, 7.6, 8.0]
df_call_center = analisar_dados_estatisticos(dados_call_center, "Tempo de Atendimento em Call Center")
print(df_call_center.to_string(float_format="%.2f"))

# -- ESTUDO DE CASO 03 : Idade de Bebes de uma Pediatria
dados_idades_bebes = [0.2, 0.9, 0.4, 0.7, 0.1, 0.8, 0.3, 0.6, 0.5, 0.2, 1.0, 0.7, 0.3, 0.9, 0.5, 0.1, 0.8, 0.4, 0.6, 1.0, 0.2, 0.7, 0.5, 0.9, 0.3]
df_bebes= analisar_dados_estatisticos(dados_idades_bebes, "Idade de Bebes de uma Pediatria")
print(df_bebes.to_string(float_format="%.2f"))

print(df_idades.to_json(indent=4, orient='records', force_ascii=False))
