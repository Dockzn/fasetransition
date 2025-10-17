#BIBLIOTECAS ULTILIZADAS
#pip install python-sat
#!pip install python-sat matplotlib

import random
from pysat.solvers import Glucose4
import time
import matplotlib.pyplot as plt

# Gera uma instância SAT aleatória
def gerar_instancia_SAT(n, m, k):
    instancia = []
    for _ in range(m):
        clausula = random.sample(range(1, n + 1), k)
        clausula = [literal if random.random() < 0.5 else -literal for literal in clausula]
        instancia.append(clausula)
    return instancia

# Resolve uma instância SAT
def resolver_instancia_SAT(instancia, n):
    solver = Glucose4()
    for clausula in instancia:
        solver.add_clause(clausula)
    satisfazivel = solver.solve()
    solver.delete()
    return satisfazivel

# Executar o experimento
def executar_experimento(n, k, alpha_min, alpha_max, incremento):
    alphas = []
    probabilidades = []
    tempos = []

    alpha = alpha_min
    while alpha <= alpha_max:
        m = int(alpha * n)
        satisfaziveis = 0
        tempos_alpha = []

        # Gerador de Instancias
        for _ in range(30):
            instancia = gerar_instancia_SAT(n, m, k)
            start_time = time.time()
            satisfazivel = resolver_instancia_SAT(instancia, n)
            end_time = time.time()
            tempos_alpha.append(end_time - start_time)
            if satisfazivel:
                satisfaziveis += 1

        probabilidade = satisfaziveis / 30  # Probabilidade
        tempo_medio = sum(tempos_alpha) / 30  # Tempo

        alphas.append(alpha)
        probabilidades.append(probabilidade)
        tempos.append(tempo_medio)

        alpha += incremento

    return alphas, probabilidades, tempos

# Parâmetros
n = 50  # Variáveis
k = 3  # K = 3 pro 3-SAT K = 5 pro 5-SAT
alpha_min = 1.0  # Valor mínimo do alfa
alpha_max = 20.0 if k == 3 else 30.0  # Valor máximo de alpha (3-SAT: 20, 5-SAT: 30)
incremento = 0.1

# Executar o experimento
alphas, probabilidades, tempos = executar_experimento(n, k, alpha_min, alpha_max, incremento)

# Graficos
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
plt.plot(alphas, probabilidades, marker='o', markersize=2, label=f'n = {n}')
plt.xlabel('Alpha')
plt.ylabel('Probabilidade de Satisfiabilidade')
plt.title(f'Probabilidade de Satisfiabilidade({k}-SAT)')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(alphas, tempos, marker='o', markersize=2, color='red', label=f'n = {n}')
plt.xlabel('Alpha')
plt.ylabel('Tempo Médio de Execução (segundos)')
plt.title(f'Tempo de Execução({k}-SAT)')
plt.legend()

plt.tight_layout()
plt.show()