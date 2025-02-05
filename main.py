import os
import matplotlib.pyplot as plt
import numpy as np


# Lista de métricas a serem comparadas
from many_data import nomes_problemas, dados

metricas = ['nodes', 'goal', 'cost', 'actions']

# Diretório para salvar os gráficos
output_dir = "graficos_many_improved"
os.makedirs(output_dir, exist_ok=True)

for problema in nomes_problemas:
    resultados = dados[problema]
    algoritmos = list(resultados.keys())
    # Extrai os valores para cada algoritmo na ordem das métricas
    valores = {alg: [resultados[alg][metrica] for metrica in metricas] for alg in algoritmos}

    # Número de algoritmos e de métricas
    n_alg = len(algoritmos)
    n_metricas = len(metricas)

    # Cria um tamanho de figura maior conforme o número de algoritmos
    # Por exemplo, 2.5 polegadas para cada algoritmo e 8 polegadas no mínimo
    fig_width = max(8, n_alg * 2.5)
    fig, ax = plt.subplots(figsize=(fig_width, 6))

    # Posições das métricas no eixo x
    x = np.arange(n_metricas)

    # Para ter barras lado a lado, definimos uma largura menor para cada barra
    # e distribuímos o grupo centralizado em torno de cada posição em x.
    largura = 0.8 / n_alg
    deslocamentos = np.linspace(-largura * (n_alg - 1) / 2, largura * (n_alg - 1) / 2, n_alg)

    for i, alg in enumerate(algoritmos):
        pos = x + deslocamentos[i]
        # Plota as barras para cada algoritmo
        barras = ax.bar(pos, valores[alg], largura, label=alg)
        # Adiciona anotações para cada barra, ajustando o tamanho da fonte e o deslocamento vertical
        for barra in barras:
            altura = barra.get_height()
            # Se o valor for muito pequeno comparado ao máximo da métrica, aumentamos o deslocamento
            offset = 3 if altura < 100 else 5
            ax.annotate(f'{altura}',
                        xy=(barra.get_x() + barra.get_width() / 2, altura),
                        xytext=(0, offset),
                        textcoords="offset points",
                        ha='center', va='bottom',
                        fontsize=8)

    # Configura os rótulos e título
    ax.set_title(f"Desempenho para {problema}", fontsize=14)
    ax.set_xlabel("Métrica", fontsize=12)
    ax.set_ylabel("Valor", fontsize=12)
    ax.set_xticks(x)
    ax.set_xticklabels(metricas, fontsize=10)
    ax.legend(fontsize=10)

    plt.tight_layout()

    # Gera um nome de arquivo
    safe_nome = problema.replace("(", "").replace(")", "").replace(",", "_").replace(" ", "")
    filepath = os.path.join(output_dir, f"{safe_nome}.png")
    plt.savefig(filepath)
    print(f"Gráfico salvo em: {filepath}")
    plt.close(fig)

print(f"Foram criados {len(nomes_problemas)} gráficos.")
