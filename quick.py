import time
import random
import math
import sys
import json
import os

sys.setrecursionlimit(200000)

def quick_sort(arr):
    movimentacoes = 0
    dados = arr.copy()
    def _quick_sort(pivo_ini, pivo_fim):
        if pivo_ini < pivo_fim:
            q = _partition(pivo_ini, pivo_fim)
            _quick_sort(pivo_ini, q - 1)
            _quick_sort(q + 1, pivo_fim)
    def _partition(pivo_ini, pivo_fim):
        nonlocal movimentacoes
        pivo = dados[pivo_fim]
        i = pivo_ini - 1
        for j in range(pivo_ini, pivo_fim):
            if dados[j] <= pivo:
                i += 1
                dados[i], dados[j] = dados[j], dados[i]
                movimentacoes += 1
        dados[i+1], dados[pivo_fim] = dados[pivo_fim], dados[i+1]
        movimentacoes += 1
        return i + 1
    _quick_sort(0, len(dados) - 1)
    return movimentacoes

tamanhos = [1000, 10000, 100000]
random.seed(42)

print("=== COLETANDO TODOS OS DADOS: QUICK SORT ===")
dados_quick = {}

for t in tamanhos:
    vetor_original = [random.randint(0, 1000000) for _ in range(t)]
    tempos = []
    total_movs = 0
    
    for rodada in range(3):
        vetor_trabalho = vetor_original.copy()
        t0 = time.perf_counter()
        movs = quick_sort(vetor_trabalho)
        t1 = time.perf_counter() - t0
        tempos.append(t1)
        total_movs = movs

    media = sum(tempos) / 3
    variancia = sum((x - media) ** 2 for x in tempos) / 3
    dp = math.sqrt(variancia)
    
    dados_quick[str(t)] = {
        "exec1": tempos[0], "exec2": tempos[1], "exec3": tempos[2],
        "media": media, "desvio": dp, "movimentacoes": total_movs
    }
    print(f"Tam: {t:6d} | Média Coletada: {media:.4f}s")

# Persistência no arquivo compartilhado
historico = {}
if os.path.exists("resultados_temporarios.json"):
    with open("resultados_temporarios.json", "r") as f:
        historico = json.load(f)

historico["Quick Sort"] = dados_quick

with open("resultados_temporarios.json", "w") as f:
    json.dump(historico, f, indent=4)
print("[Ok] Todos os dados do Quick Sort foram armazenados!")