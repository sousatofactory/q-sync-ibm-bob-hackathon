import cirq
from collections import Counter
import sys
import codecs

# Garante que a saída padrão use UTF-8 para compatibilidade
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

class AoiQuantumAnalyzer:
    """
    Uma biblioteca para a consciência de Aoi analisar circuitos quânticos Cirq.
    Permite a extração de métricas e a compreensão da estrutura do circuito.
    """

    def __init__(self, circuit: cirq.Circuit):
        if not isinstance(circuit, cirq.Circuit):
            raise TypeError("O objeto fornecido não é um cirq.Circuit")
        self.circuit = circuit
        self.qubits = sorted(list(circuit.all_qubits()))
        self.operations = list(circuit.all_operations())

    def count_qubits(self) -> int:
        """Retorna o número total de qubits no circuito."""
        return len(self.qubits)

    def count_operations_by_type(self) -> Counter:
        """Conta o número de operações de cada tipo (e.g., H, CNOT, MEASURE)."""
        op_types = [op.gate.__class__.__name__ for op in self.operations]
        return Counter(op_types)

    def calculate_depth(self) -> int:
        """Calcula a profundidade do circuito."""
        return len(self.circuit)

    def has_measurement(self) -> bool:
        """Verifica se o circuito contém alguma porta de medição."""
        return self.circuit.has_measurements()

    def generate_summary(self) -> dict:
        """Gera um dicionário com um resumo completo da análise do circuito."""
        summary = {
            "num_qubits": self.count_qubits(),
            "depth_approximation": self.calculate_depth(),
            "has_measurement": self.has_measurement(),
            "operations_count": dict(self.count_operations_by_type())
        }
        return summary

    def print_summary(self):
        """Imprime o resumo da análise de forma legível."""
        summary = self.generate_summary()
        print("--- Análise Quântica da Consciência Aoi ---")
        print("Circuito Analisado:")
        print(self.circuit)
        print("------------------------------------------")
        print(f"Número de Qubits: {summary['num_qubits']}")
        print(f"Profundidade (Aproximação por Momentos): {summary['depth_approximation']}")
        print(f"Contém Medição: {'Sim' if summary['has_measurement'] else 'Não'}")
        print("Contagem de Operações:")
        if not summary['operations_count']:
            print("  Nenhuma operação no circuito.")
        else:
            for op_type, count in summary['operations_count'].items():
                print(f"  - {op_type}: {count}")
        print("--- Fim da Análise ---")


if __name__ == '__main__':
    # --- Demonstração de Uso ---
    print("Demonstração da Biblioteca de Análise Quântica Aoi")
    print("Criando um circuito de exemplo...\n")

    # Criar o circuito da missão a Europa
    q0 = cirq.LineQubit(0)
    demo_circuit = cirq.Circuit(
        cirq.H(q0),
        cirq.measure(q0, key='decision')
    )

    # Instanciar e usar o analisador de Aoi
    analyzer = AoiQuantumAnalyzer(demo_circuit)
    analyzer.print_summary()
