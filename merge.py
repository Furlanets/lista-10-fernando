import time
import random
import math
import json
import os

def merge_sort(arr):
    movimentacoes = 0
    def _merge_sort(sub_arr):
        nonlocal movimentacoes
        if len(sub_arr) <= 1: return sub_arr
        meio = len(sub_arr) // 2
        esquerda = _merge_sort(sub_arr[:meio])
        direita = _merge_sort(sub_arr[meio:])
        resultado = []
        i = j = 0
        while i < len(esquerda) and j < len(direita):
            if esquerda[i] <= direita[j]:
                resultado.append(esquerda[i]); i += 1
            else:
                resultado.append(direita[j]); j += 1
            movimentacoes += 1
        while i < len(esquerda): resultado.append(esquerda[i]); i += 1; movimentacoes += 1
        while j < len(direita): resultado.append(direita[j]); j += 1; movimentacoes += 1
        return resultado
    _merge_sort(arr)
    return movimentacoes

tamanhos = [1000, 10000, 100000]
random.seed(42)

print("=== COLETANDO TODOS OS DADOS: MERGE SORT ===")
dados_merge = {}

for t in tamanhos:
    vetor_original = [random.randint(0, 1000000) for _ in range(t)]
    tempos = []
    total_movs = 0
    
    for rodada in range(3):
        vetor_trabalho = vetor_original.copy()
        t0 = time.perf_counter()
        movs = merge_sort(vetor_trabalho)
        t1 = time.perf_counter() - t0
        tempos.append(t1)
        total_movs = movs

    media = sum(tempos) / 3
    variancia = sum((x - media) ** 2 for x in tempos) / 3
    dp = math.sqrt(variancia)
    
    dados_merge[str(t)] = {
        "exec1": tempos[0], "exec2": tempos[1], "exec3": tempos[2],
        "media": media, "desvio": dp, "movimentacoes": total_movs
    }
    print(f"Tam: {t:6d} | Média Coletada: {media:.4f}s")

# Persistência no arquivo compartilhado
historico = {}
if os.path.exists("resultados_temporarios.json"):
    with open("resultados_temporarios.json", "r") as f:
        historico = json.load(f)

historico["Merge Sort"] = dados_merge

with open("resultados_temporarios.json", "w") as f:
    json.dump(historico, f, indent=4)
print("[Ok] Todos os dados do Merge Sort foram armazenados!")