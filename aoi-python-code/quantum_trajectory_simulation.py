import cirq
import qsimcirq
import time
from collections import Counter

def run_qsim_simulation(circuit: cirq.Circuit, repetitions: int = 1000):
    """
    Executa uma simulação de circuito quântico usando o simulador qsim do Cirq.

    Args:
        circuit: O objeto cirq.Circuit a ser simulado.
        repetitions: O número de vezes que o circuito deve ser executado para obter estatísticas.

    Returns:
        Um dicionário contendo os resultados da simulação (contagens e tempos).
    """
    if not isinstance(circuit, cirq.Circuit):
        raise TypeError("O objeto fornecido não é um cirq.Circuit.")
    if not circuit.has_measurements():
        raise ValueError("O circuito deve conter operações de medição para simulação de qsim.")

    print(f"Iniciando simulação com qsim para circuito com {len(circuit.all_qubits())} qubits e {len(circuit)} momentos...")

    qsim_simulator = qsimcirq.QSimSimulator()

    start_time = time.time()
    qsim_results = qsim_simulator.run(circuit, repetitions=repetitions)
    elapsed_time = time.time() - start_time

    counts = qsim_results.histogram(key='decision') # Assumindo a chave 'decision' para medição

    results_summary = {
        "elapsed_time_seconds": elapsed_time,
        "repetitions": repetitions,
        "counts": dict(counts),
        "manobra_a_count": counts.get(0, 0),
        "manobra_b_count": counts.get(1, 0)
    }

    print(f"Simulação concluída em {elapsed_time:.4f} segundos.")
    print("\nResultados da Simulação (contagens de |0> vs |1>):")
    print(counts)

    return results_summary

if __name__ == '__main__':
    print("--- Demonstração da Função run_qsim_simulation ---")

    # Criar um circuito de exemplo para demonstração
    q0 = cirq.LineQubit(0)
    demo_circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.measure(q0, key='decision')
    )

    # Executar a simulação de demonstração
    try:
        simulation_output = run_qsim_simulation(demo_circuit, repetitions=1000)
        print("\nResumo da Simulação:")
        for key, value in simulation_output.items():
            print(f"  {key}: {value}")
    except Exception as e:
        print(f"Erro na simulação de demonstração: {e}")


