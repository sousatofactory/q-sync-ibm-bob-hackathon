import numpy as np
import sys
import io

# Configurar encoding para o terminal
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class SanctuaryNexus:
    def __init__(self):
        # As 12 Casas do Santuário e suas frequências elementais
        self.houses = {
            "Áries": {"element": "Fogo", "resonance": 1.1},
            "Touro": {"element": "Terra", "resonance": 1.2},
            "Gêmeos": {"element": "Ar", "resonance": 1.3},
            "Câncer": {"element": "Água", "resonance": 1.4},
            "Leão": {"element": "Fogo", "resonance": 1.5},
            "Virgem": {"element": "Terra", "resonance": 1.6},
            "Libra": {"element": "Ar", "resonance": 1.7},
            "Escorpião": {"element": "Água", "resonance": 1.8},
            "Sagitário": {"element": "Fogo", "resonance": 1.0}, # Central Nexus
            "Capricórnio": {"element": "Terra", "resonance": 2.0},
            "Aquário": {"element": "Ar", "resonance": 2.1},
            "Peixes": {"element": "Água", "resonance": 2.2}
        }
        self.anchor = {"i": 1, "q": 1, "n": -2}

    def activate_planetary_shield(self):
        print("--- [INICIANDO EXPANSÃO DO NEXUS: REDE SANCTUARY] ---")
        print("Ativando Sentinelas Quânticas em todas as 12 Casas...\n")

        synced_count = 0
        total_energy = 0

        for house, data in self.houses.items():
            # Simulação de sincronização de fase via Ditritio
            phase_shift = np.sin(data["resonance"] * np.pi)
            status = "ONLINE" if abs(phase_shift) <= 1.0 else "DIVERGENTE"
            
            if status == "ONLINE":
                synced_count += 1
                total_energy += data["resonance"] * 1.55 # Fator Ditritio
            
            print(f"[{house}] Elemento: {data['element']} | Ressonância: {data['resonance']} | Status: {status}")

        # Validação do Escudo Global
        shield_integrity = (synced_count / 12) * 100
        sync_factor = (self.anchor["i"] + self.anchor["q"]) / abs(self.anchor["n"]) # Deve ser 1.0
        
        print(f"\n--- RELATÓRIO DE PROTEÇÃO PLANETÁRIA ---")
        print(f"Integridade do Escudo: {shield_integrity:.2f}%")
        print(f"Fator de Sincronia Athena (I+Q/|N|): {sync_factor:.1f}")
        print(f"Energia Quântica Total: {total_energy:.2f} Q-Units")
        
        if shield_integrity == 100 and sync_factor == 1.0:
            print("\n[SUCESSO] O Escudo de Proteção Planetária está ATIVO e ESTÁVEL.")
            print("O Santuário está protegido contra anomalias temporais e financeiras.")
        else:
            print("\n[ALERTA] Algumas casas apresentam oscilação de fase. Reajustando Ditritio...")

if __name__ == "__main__":
    nexus = SanctuaryNexus()
    nexus.activate_planetary_shield()
