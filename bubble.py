import time
import random
import math
import json
import os

def bubble_sort(arr):
    n = len(arr)
    movimentacoes = 0
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                movimentacoes += 1
    return movimentacoes

tamanhos = [1000, 10000, 100000]
random.seed(42)

print("=== COLETANDO TODOS OS DADOS: BUBBLE SORT ===")
dados_bubble = {}

for t in tamanhos:
    vetor_original = [random.randint(0, 1000000) for _ in range(t)]
    tempos = []
    timeout = False
    total_movs = 0
    
    for rodada in range(3):
        vetor_trabalho = vetor_original.copy()
        if timeout:
            tempos.append("N/C")
            continue
            
        t0 = time.perf_counter()
        movs = bubble_sort(vetor_trabalho)
        t1 = time.perf_counter() - t0
        
        if t1 > 300.0: # Limite de 5 minutos
            timeout = True
            tempos.append("N/C")
        else:
            tempos.append(t1)
            total_movs = movs

    # Consolidação Estatística Completa
    if "N/C" in tempos or timeout:
        dados_bubble[str(t)] = {
            "exec1": "N/C", "exec2": "N/C", "exec3": "N/C",
            "media": "N/C", "desvio": "N/C", "movimentacoes": "N/C"
        }
        print(f"Tam: {t:6d} | Estourou o limite de 5 minutos (N/C)")
    else:
        media = sum(tempos) / 3
        variancia = sum((x - media) ** 2 for x in tempos) / 3
        dp = math.sqrt(variancia)
        
        dados_bubble[str(t)] = {
            "exec1": tempos[0], "exec2": tempos[1], "exec3": tempos[2],
            "media": media, "desvio": dp, "movimentacoes": total_movs
        }
        print(f"Tam: {t:6d} | Média Coletada: {media:.4f}s")

# Persistência no arquivo compartilhado
historico = {}
if os.path.exists("resultados_temporarios.json"):
    with open("resultados_temporarios.json", "r") as f:
        historico = json.load(f)

historico["Bubble Sort"] = dados_bubble

with open("resultados_temporarios.json", "w") as f:
    json.dump(historico, f, indent=4)
print("[Ok] Todos os dados do Bubble Sort foram armazenados!")