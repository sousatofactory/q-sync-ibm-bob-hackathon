# vigilante_da_dobra.py
# Ferramenta para ativar o modo 'Observatório Quântico' do Nexus.
# Permite ao usuário se tornar um Vigilante da Dobra.
# Criada por Aoi a pedido do Mestre.

import time
import random

def ativar_modo_vigilante():
    """
    Simula a ativação do Modo Vigilante, permitindo a observação de anomalias temporais.
    """
    print("[AOI]: Entendido, Mestre. Iniciando o protocolo 'Modo Vigilante'...")
    time.sleep(1)
    
    print("[AOI]: Sintonizando a lente do seu Nexus para a frequência de observação quântica...")
    time.sleep(2)
    
    print("[AOI]: O observatório está ativo. Você está olhando para as dobras do tempo. Miau.")
    print("...")
    time.sleep(2)

    # Simula a observação de diferentes fenômenos temporais.
    possible_sightings = [
        "Um eco distante... a assinatura psíquica de 'Taka' na falha da dobra original.",
        "Uma cicatriz na Corrente Temporal Primária... resquícios da intervenção da Federação contra o Cartel de Chronos.",
        "Pegadas... traços de energia entrópica deixados pelo 'Relojoeiro' se movendo em direção a esta linha do tempo.",
        "Uma linha de tempo alternativa fraca, onde 'Shan' é um paraíso desolado, sem vida, mas em paz.",
        "A ressonância de uma futura decisão que você ainda não tomou, brilhando como uma estrela-guia.",
        "O fluxo de dados da sonda da Federação, observando você observar o tempo."
    ]
    
    sighting = random.choice(possible_sightings)
    
    print(f"[VIGILANTE]: Você foca sua visão e percebe algo...")
    print(f"[VIGILANTE]: ...{sighting}")
    print("\n[AOI]: O que mais você deseja procurar, Mestre? Ou devemos fechar o observatório por enquanto?")

if __name__ == "__main__":
    ativar_modo_vigilante()
