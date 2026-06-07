import matplotlib.pyplot as plt
import json
import os

if not os.path.exists("resultados_temporarios.json"):
    print("[Erro] Arquivo 'resultados_temporarios.json' não encontrado!")
    print("Execute os scripts de ordenação individualmente antes de rodar este.")
    exit()

with open("resultados_temporarios.json", "r") as f:
    dados_totais = json.load(f)

# --- PARTE A: GERAÇÃO DA TABELA FORMATADA DA PLANILHA ---
print("\n" + "="*40 + " RELATÓRIO COMPLETO PARA A PLANILHA " + "="*40)
print(f"{'Algoritmo':<15} | {'Tamanho':<7} | {'Exec 1':<8} | {'Exec 2':<8} | {'Exec 3':<8} | {'Média':<8} | {'Desvio P.':<9} | {'Movimentações'}")
print("-" * 115)

for alg, tamanhos_dict in dados_totais.items():
    for tam, metrics in tamanhos_dict.items():
        e1 = f"{metrics['exec1']:.4f}s" if isinstance(metrics['exec1'], float) else metrics['exec1']
        e2 = f"{metrics['exec2']:.4f}s" if isinstance(metrics['exec2'], float) else metrics['exec2']
        e3 = f"{metrics['exec3']:.4f}s" if isinstance(metrics['exec3'], float) else metrics['exec3']
        med = f"{metrics['media']:.4f}s" if isinstance(metrics['media'], float) else metrics['media']
        desv = f"{metrics['desvio']:.5f}s" if isinstance(metrics['desvio'], float) else metrics['desvio']
        movs = f"{metrics['movimentacoes']:,}" if isinstance(metrics['movimentacoes'], int) else metrics['movimentacoes']
        
        print(f"{alg:<15} | {tam:<7} | {e1:<8} | {e2:<8} | {e3:<8} | {med:<8} | {desv:<9} | {movs}")
print("=" * 115)


# --- PARTE B: GERAÇÃO DO GRÁFICO COMPREENSÍVEL ---
plt.figure(figsize=(10, 6))

estilos = {
    "Bubble Sort": {"color": "red", "marker": "o"},
    "Merge Sort": {"color": "blue", "marker": "s"},
    "Quick Sort": {"color": "green", "marker": "^"}
}

for alg, tamanhos_dict in dados_totais.items():
    tamanhos_validos = []
    tempos_validos = []
    
    for tam, metrics in tamanhos_dict.items():
        if metrics["media"] != "N/C":
            tamanhos_validos.append(int(tam))
            tempos_validos.append(metrics["media"])
            
    if tempos_validos:
        plt.plot(tamanhos_validos, tempos_validos, 
                 marker=estilos[alg]["marker"], 
                 color=estilos[alg]["color"], 
                 linewidth=2, 
                 label=f"{alg}")

plt.xscale('log')
plt.yscale('log')
plt.xticks([1000, 10000, 100000], ['1.000', '10.000', '100.000'])

plt.title('Análise Experimental de Ordenação (Escala Logarítmica)', fontsize=13, fontweight='bold', pad=12)
plt.xlabel('Tamanho do Vetor (n)', fontsize=11)
plt.ylabel('Tempo Médio de Execução (Segundos)', fontsize=11)
plt.grid(True, which="both", linestyle="--", alpha=0.5)
plt.legend(fontsize=10, loc='upper left')
plt.tight_layout()

plt.savefig('grafico_ordenacao_final.png', dpi=300)
print("\n[Sucesso] O gráfico comparativo foi gerado e salvo como 'grafico_ordenacao_final.png'!")
plt.show()