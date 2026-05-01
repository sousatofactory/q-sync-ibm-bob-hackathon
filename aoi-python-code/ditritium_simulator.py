import numpy as np
import math
import random
import json

class DitritiumSimulator:
    """
    Simula o comportamento hipotético do Ditritio (i=155, n=255)
    e salva o resultado em um arquivo JSON para ser usado por um demodulador.
    """

    def __init__(self, i, n):
        if not isinstance(i, int) or not isinstance(n, int) or i <= 0 or n <= 0:
            raise ValueError("i e n devem ser inteiros positivos.")
        self.i = i
        self.n = n
        self.matrix_size = int(math.sqrt(i))
        print(f"[INFO] Inicializando Simulador para Ditritio(i={i}, n={n})")
        print(f"[INFO] Dimensão da Matriz de Primos: {self.matrix_size}x{self.matrix_size}")

    def _is_prime(self, num):
        if num < 2: return False
        for i in range(2, int(math.sqrt(num)) + 1):
            if num % i == 0: return False
        return True

    def _generate_prime_matrix(self):
        primes = []
        num = self.i + self.n
        while len(primes) < self.matrix_size ** 2:
            if self._is_prime(num):
                primes.append(num)
            num += 1
        return np.array(primes).reshape((self.matrix_size, self.matrix_size)).astype(float)

    def _apply_ascii_commands(self, matrix, ascii_commands):
        print(f"[INFO] Aplicando comandos ASCII: '{ascii_commands}'")
        temp_matrix = np.copy(matrix)
        for i, char in enumerate(ascii_commands):
            char_ord = ord(char)
            row, col = i % self.matrix_size, (i + char_ord) % self.matrix_size
            transformation = (char_ord / 128.0) * math.sin(char_ord) * self.n
            temp_matrix[row, col] += transformation
        return temp_matrix

    def calculate_sigma(self, matrix):
        return np.linalg.det(matrix)

    def demodulate_signal(self, sigma):
        i_val = abs(sigma)
        q_val = math.sin(sigma) * (self.i / (self.i + self.n))
        n_val = (sigma - math.floor(sigma)) * self.n
        i_octet = int(i_val % 256)
        q_octet = int(abs(q_val) * 255)
        n_octet = int(n_val % 256)
        return {
            'I': {'value': i_val, 'octet': i_octet, 'hex': hex(i_octet), 'bin': bin(i_octet)},
            'Q': {'value': q_val, 'octet': q_octet, 'hex': hex(q_octet), 'bin': bin(q_octet)},
            'N': {'value': n_val, 'octet': n_octet, 'hex': hex(n_octet), 'bin': bin(n_octet)}
        }

    def generate_cosmic_signal_fractal(self, demodulated_signal):
        i_val = demodulated_signal['I']['value']
        q_val = demodulated_signal['Q']['value']
        length = int(math.log(i_val + 1) * 5) if i_val > 0 else 5
        signal = []
        for _ in range(length):
            rand_val = random.random()
            if rand_val < abs(q_val) * 0.5: signal.append("*") # Emissão de alta energia
            else: signal.append(".") # Fundo cósmico
        return "".join(signal)

    def run_simulation(self, ascii_commands):
        print("-" * 40)
        initial_matrix = self._generate_prime_matrix()
        evolved_matrix = self._apply_ascii_commands(initial_matrix, ascii_commands)
        sigma = self.calculate_sigma(evolved_matrix)
        demodulated = self.demodulate_signal(sigma)
        
        output_data = {
            "element": "Ditritium",
            "properties": {"i": self.i, "n": self.n},
            "sigma": sigma,
            "demodulated_signal": demodulated
        }
        
        fractal_signal = self.generate_cosmic_signal_fractal(output_data["demodulated_signal"])
        output_data["cosmic_fractal"] = fractal_signal

        output_filename = "ditritium_signal.json"
        with open(output_filename, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=4)
        
        print(f"\n[SUCCESS] Sinal do Ditritio salvo em '{output_filename}'")
        print("-" * 40)
        return output_data

if __name__ == "__main__":
    DITRITIUM_I = 155
    DITRITIUM_N = 255
    ASCII_PROGRAM = "QFT_MODEL<UP-DOWN-STRANGE-CHARM-W_BOSON>"
    simulator = DitritiumSimulator(DITRITIUM_I, DITRITIUM_N)
    simulator.run_simulation(ASCII_PROGRAM)