import pandas as pd
import re # For parameter extraction
import numpy as np # Added for new functions
import matplotlib.pyplot as plt # Added for plotting
import openvsp_integration # Módulo de integração OpenVSP
import os # Import os module for path manipulation
import json
from ditritium_simulator import DitritiumSimulator

# 1. Simulation Function
def simulate_space_travel(massa_nave, forca_motor, distancia_lua, dt, tempo_simulacao):
    if massa_nave <= 0: # Avoid division by zero and non-physical mass
        raise ValueError("massa_nave must be greater than zero for simulation.")

    posicao = 0
    velocidade = 0
    tempo = 0
    posicoes = [posicao]
    velocidades = [velocidade]
    tempos = [tempo]
    aceleracoes = []

    # Assuming no gravity for simplicity as per the last provided snippet
    # F_gravity = (G * massa_nave * M_terra) / (posicao + R_terra)**2 # If gravity were included

    while posicao < distancia_lua and tempo < tempo_simulacao:
        # Net Force (simplified, no gravity as per the last provided snippet)
        F_net = forca_motor # If F_gravity was included: forca_motor - F_gravity

        aceleracao = F_net / massa_nave
        velocidade += aceleracao * dt
        posicao += velocidade * dt
        tempo += dt
        posicoes.append(posicao)
        velocidades.append(velocidade)
        tempos.append(tempo)
        aceleracoes.append(aceleracao)

        if posicao >= distancia_lua:
            break

    data = {
        'Tempo (s)': tempos[:-1],
        'Posicao (m)': posicoes[:-1],
        'Velocidade (m/s)': velocidades[:-1],
        'Aceleracao (m/s^2)': aceleracoes,
        'Forca (N)': [forca_motor] * len(aceleracoes),
        'Massa (kg)': [massa_nave] * len(aceleracoes)
    }

    df = pd.DataFrame(data)
    return df

# 2. Parameter Extraction
def extract_parameters(design_text):
    """
    Extracts key simulation parameters from an LLM-generated spacecraft design description.
    This is a basic implementation and needs more sophisticated NLP for real-world use.
    """
    massa_nave = None
    forca_motor = None

    # Regex to find mass (e.g., "massa de 4200 kg", "peso de 1500,5 kg")
    # Added re.UNICODE flag to handle non-ASCII characters correctly
    # Added support for comma or period as decimal separator
    mass_match = re.search(r"(?:massa|peso|mass) (?:total )?(?:da sonda )?(?:é de |is |of |: |)([\d]+(?:[.,]\d+)?)\s*kg", design_text, re.IGNORECASE | re.UNICODE)
    if mass_match:
        massa_str = mass_match.group(1).replace(',', '.') # Replace comma with period for float conversion
        massa_nave = float(massa_str)

    # Regex to find thrust (e.g., "gerar 3500 N de thrust", "força do motor de 12000N")
    # Added re.UNICODE flag
    thrust_match = re.search(r"(?:gerar|generating|força do motor|thrust|propulsão|producing) (?:de |of |: |)([\d]+(?:[.,]\d+)?)\s*N(?: de thrust)?", design_text, re.IGNORECASE | re.UNICODE)
    if thrust_match:
        forca_str = thrust_match.group(1).replace(',', '.') # Replace comma with period
        forca_motor = float(forca_str)

    if massa_nave is not None and forca_motor is not None:
        return {"massa_nave": massa_nave, "forca_motor": forca_motor}
    return None

# 3. Scoring Function
def calculate_score(simulation_results, design_text, time_weight=1.0, energy_weight=1.0, creativity_weight=0.0):
    """
    Calculates a score for a spacecraft design based on simulation results and a creativity assessment.
    """
    if simulation_results is None or simulation_results.empty:
        return 0  # Penalize designs that fail simulation or have no results

    total_time = simulation_results['Tempo (s)'].max()
    # total_time + 1 will always be >= 1 since total_time is non-negative
    total_time_score = 1 / (total_time + 1) # smaller time more points, inverse function

    max_velocidade = simulation_results['Velocidade (m/s)'].max()
    # Using a fixed mass of 1000 kg for energy calculation as per the provided snippet
    # If massa_nave from parameters was desired, it would need to be passed here.
    energy = 0.5 * 1000 * max_velocidade**2 # estimative of the energy, 1000 is the mass that will always b

    # Placeholder for creativity score (needs external assessment)
    creativity_score = 0.5 # Example value, would be determined by LLM analysis or human review

    # Combine scores
    score = (time_weight * total_time_score) + \
            (energy_weight * (1 / (energy + 1))) + \
            (creativity_weight * creativity_score)

    return score

# 4. Evaluate Design Function (Orchestrator)
def evaluate_design(design_text, distancia_destino, dt, tempo_simulacao):
    """
    Evaluates a spacecraft design by extracting parameters, simulating its journey, and scoring its performance.
    """
    # 1. Parameter Extraction
    parameters = extract_parameters(design_text)

    if parameters is None:
        print("Failed to extract parameters. Cannot simulate.")
        return 0

    massa_nave = parameters["massa_nave"]
    forca_motor = parameters["forca_motor"]

    # 2. Simulation
    try:
        # Note: The simulate_space_travel function in the provided snippet uses 'distancia_lua'
        # but the evaluate_design function uses 'distancia_destino'.
        # I will use 'distancia_destino' as the target for consistency with evaluate_design's signature.
        simulation_results = simulate_space_travel(massa_nave, forca_motor, distancia_destino, dt, tempo_simulacao)
    except ValueError as e: # Catch the specific ValueError for massa_nave = 0
        print(f"Simulation error: {e}")
        return 0  # Penalize simulations that fail
    except Exception as e:
        print(f"General simulation error: {e}")
        return 0  # Penalize simulations that fail

    # 3. Scoring
    score = calculate_score(simulation_results, design_text)

    return score

# 5. Competition Overview Function
def generate_competition_overview(distancia_destino=384400000, dt=100, tempo_simulacao=100000):
    """
    Generates a formatted string that provides an overview of the competition rules
    and default values.
    """
    overview = """
## LLM Spacecraft Design Challenge: Journey to Mars

This competition challenges participants to design innovative spacecraft for a crewed mission to Mars using the power of Large Language Models (LLMs). Participants will leverage LLMs to generate detailed spacecraft designs, then evaluate their performance using a physics-based simulation. The goal is to create a spacecraft that minimizes travel time and approximates fuel consumption while adhering to realistic engineering constraints.

### Competition Overview

Participants will use LLMs to conceptualize and describe their spacecraft designs in detail.

Physics-Based Simulation and Evaluation: The generated designs will be evaluated using a Python-based simulation engine that models the spacecraft's journey to Mars, based on the generated characteristics.
The equations governing the simulation will include concepts of Newton's Laws of motion as well as estimates using the Tsiolkovsky rocket equation which is calculated as:

$$ \\Delta v = v_e \\ln(\\frac{{m_0}}{{m_f}}) $$

where:

*   ( \\Delta v ) is the change in velocity (Delta-v).
*   ( v_e ) is the effective exhaust velocity.
*   ( m_0 ) is the initial total mass (including propellant).
*   ( m_f ) is the final mass (without propellant).

### Submission Requirements

Each submission should include:

*   LLM-Generated Design Description: The full text output from the LLM, describing the spacecraft design.
*   Code for Parameter Extraction: The code used to extract the simulation parameters from the LLM output.
*   Simulation Code: The modified simulation code (if any) used to evaluate the design.

### Evaluation Criteria

Designs will be evaluated based on:

*   **Travel Time:** Shorter travel times are better.
*   **Energy Consumption:** Lower energy consumption is better.
*   (Optionally) Design Creativity (weighted at 0%)

## Default Simulation Parameters:

*   **Distance to Destination:** {distancia_destino} meters (Earth-Moon distance).
*   **Time Step (dt):** {dt} seconds.
*   **Total Simulation Time:** {tempo_simulacao} seconds.

## Important Notes:

*   The LLM-generated descriptions are the primary input for your design.
*   Accurate parameter extraction is crucial for a successful simulation.
*   The scoring function rewards efficient designs that minimize both travel time and energy consumption.
""".format(distancia_destino=distancia_destino, dt=dt, tempo_simulacao=tempo_simulacao)

    return overview

# --- New Functions for Hydrogen Propulsion and Advanced Trajectory ---

# New function: Conceptual Hydrogen Engine Model
def conceptual_hydrogen_engine_model(R, n, R1, R2, R3):
    """
    Calculates a conceptual 'XK' value based on the provided Japanese formulas,
    representing aspects of hydrogen engine propulsion and space wind effects.
    Avoids division by zero.
    """
    # Ensure R1 + 2R2^2 + 3R3 is not zero
    denominator = R1 + 2 * (R2**2) + 3 * R3
    if denominator == 0:
        raise ValueError("Denominator (R1 + 2R2^2 + 3R3) cannot be zero for conceptual engine model.")

    # XK = 2 (3R^2)^2√3 + (-2n^9) 3πR^2 / (R1 + 2R2^2 + 3R3)
    term1 = 2 * (3 * (R**2))**2 * np.sqrt(3)
    term2_numerator = (-2 * (n**9)) * 3 * np.pi * (R**2)
    term2 = term2_numerator / denominator

    XK = term1 + term2
    return XK

# --- New Functions for Ditritium Propulsion ---
def read_ditritium_signal(filename="ditritium_signal.json"):
    """Reads the sigma value from the ditritium signal file."""
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            return data.get("sigma")
    except FileNotFoundError:
        print(f"Error: {filename} not found. Run ditritium_simulator.py first.")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {filename}.")
        return None

def conceptual_ditritium_engine_model(sigma, factor=1e-18):
    """
    Calculates a conceptual engine force based on the sigma value from Ditritium simulation.
    A factor of 1e-18 is used to scale the force to a more realistic level.
    """
    if sigma is None:
        return 0
    # The formula is conceptual: a larger absolute sigma yields more force.
    # The factor is for scaling the force to a reasonable level.
    return abs(sigma) * factor

# New function: Conceptual Trajectory Dynamics
def conceptual_trajectory_dynamics(J_pi, A0, y, x):
    """
    Calculates a conceptual value representing spacecraft dynamic behavior,
    acceleration, or energy change based on the provided Japanese formula.
    """
    # J^1π + 2 (A0ye)^2 + 3 - (1/2) y^x
    # Assuming J^1π is J * pi (J to the power of 1 is just J)
    # Assuming 'e' is Euler's number (np.exp(1))
    term1 = J_pi # This term is ambiguous, interpreting as J * pi
    term2 = 2 * (A0 * y * np.exp(1))**2
    term3 = 3
    term4 = (1/2) * (y**x)

    dynamic_value = term1 + term2 + term3 - term4
    return dynamic_value

# New function: Simulate Trajectory (Advanced)
def simulate_trajectory(initial_state, time_steps, thrust_profile, gravity_model=None):
    """
    Simulates spacecraft trajectory using numerical integration (placeholder for Runge-Kutta).
    initial_state: tuple (initial_position, initial_velocity) - np.array for vectors
    time_steps: list of time points
    thrust_profile: function(time, current_state) -> thrust_vector
    gravity_model: function(position) -> gravitational_force_vector (optional)
    """
    print("--- Advanced Trajectory Simulation (Conceptual) ---")
    print("This function would implement a numerical integration method (e.g., Runge-Kutta).")
    print("It considers initial state, time steps, thrust profile, and an optional gravity model.")

    trajectory = []
    current_position, current_velocity = initial_state
    
    # Placeholder for integration loop
    for t in time_steps:
        # In a real implementation, current_position and current_velocity would be updated
        # based on the integration step and forces.
        trajectory.append((current_position.copy(), current_velocity.copy())) # Append copies to avoid reference issues

        # Simple conceptual update for demonstration
        # This is NOT a real Runge-Kutta integration
        current_position += current_velocity * (time_steps[1] - time_steps[0] if len(time_steps) > 1 else 1)
        current_velocity += np.array([0.1, 0.1, 0.1]) # Conceptual acceleration

    print("Trajectory simulation complete (conceptual).")
    return trajectory

# New function: Optimize Trajectory
def optimize_trajectory(objective_function, constraints, initial_guess=None):
    """
    Optimizes spacecraft trajectory (placeholder for genetic algorithms or other methods).
    Minimizes fuel consumption, subject to time and other constraints.
    objective_function: function(trajectory_parameters) -> value_to_minimize
    constraints: list of functions(trajectory_parameters) -> boolean
    initial_guess: initial set of parameters for the optimization
    """
    print("--- Trajectory Optimization (Conceptual) ---")
    print("This function would implement an optimization algorithm (e.g., Genetic Algorithms).")
    print("It aims to find the best trajectory by minimizing an objective function (e.g., fuel) ")
    print("subject to various constraints (e.g., time, safety).")

    # Placeholder for optimization logic
    best_trajectory_parameters = initial_guess if initial_guess else "Optimized Parameters"
    print("Optimization complete (conceptual).")
    return best_trajectory_parameters

# --- New Functions for Analysis and Visualization ---

def plot_velocity_vector_field(positions, velocities, title="Campo Vetorial de Velocidade", output_dir=".", filename="velocity_vector_field.png"): # New function
    """
    Plota um campo vetorial de velocidade 2D simplificado.
    Assume que positions e velocities são listas de tuplas/arrays 2D (x, y).
    Salva o gráfico como um arquivo PNG.
    """
    if not positions or not velocities:
        print("Dados insuficientes para plotar o campo vetorial de velocidade.")
        return

    # Para simplificar, vamos pegar apenas as componentes x e y se for 3D
    x_coords = [p[0] for p in positions]
    y_coords = [p[1] for p in positions]
    u_vectors = [v[0] for v in velocities]
    v_vectors = [v[1] for v in velocities]

    plt.figure(figsize=(10, 8))
    plt.quiver(x_coords, y_coords, u_vectors, v_vectors, color='blue', scale=1, scale_units='xy')
    plt.xlabel("Posição X (m)")
    plt.ylabel("Posição Y (m)")
    plt.title(title)
    plt.grid(True)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.savefig(f"{output_dir}/{filename}")
    plt.close() # Fecha a figura para evitar que ela seja exibida inesperadamente

def calculate_euclidean_distances(positions): # New function
    """
    Calcula a distância euclidiana acumulada entre pontos consecutivos da trajetória.
    Assume que positions é uma lista de tuplas/arrays (x, y) ou (x, y, z).
    """
    distances = [0.0]
    for i in range(1, len(positions)):
        p1 = np.array(positions[i-1])
        p2 = np.array(positions[i])
        dist = np.linalg.norm(p2 - p1)
        distances.append(distances[-1] + dist)
    return distances

def plot_euclidean_distance(times, distances, title="Distância Euclidiana Acumulada", output_dir=".", filename="euclidean_distance_plot.png"): # New function
    """
    Plota a distância euclidiana acumulada ao longo do tempo.
    Salva o gráfico como um arquivo PNG.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(times, distances, color='green')
    plt.xlabel("Tempo (s)")
    plt.ylabel("Distância Acumulada (m)")
    plt.title(title)
    plt.grid(True)
    plt.savefig(f"{output_dir}/{filename}")
    plt.close() # Fecha a figura para evitar que ela seja exibida inesperadamente

def plot_trajectory(times, positions, title="Trajetória da Espaçonave", output_dir=".", filename="trajectory_plot.png"): # New function
    """
    Plota a trajetória da espaçonave (Posição vs. Tempo).
    Salva o gráfico como um arquivo PNG.
    """
    plt.figure(figsize=(10, 6))
    plt.plot(times, positions, color='purple')
    plt.xlabel("Tempo (s)")
    plt.ylabel("Posição (m)")
    plt.title(title)
    plt.grid(True)
    plt.savefig(f"{output_dir}/{filename}")
    plt.close() # Fecha a figura para evitar que ela seja exibida inesperadamente

def run_space_simulation_and_analysis(massa_nave, forca_motor, distancia_lua, dt, tempo_simulacao, output_dir="."): # New orchestrator function
    """
    Executa a simulação espacial, realiza cálculos e gera dados para visualização.
    Retorna o DataFrame de simulação e métricas chave.
    """
    print("--- Executando Simulação Espacial e Análise ---")

    posicao = 0
    velocidade = 0
    tempo = 0
    posicoes_list = [posicao]
    velocidades_list = [velocidade]
    tempos_list = [tempo]
    aceleracoes_list = []

    full_simulation_text_data = [] # To store full text data
    full_simulation_text_data.append(f"Massa da Nave: {massa_nave} kg")
    full_simulation_text_data.append(f"Força do Motor: {forca_motor} N")
    full_simulation_text_data.append(f"Distância do Destino: {distancia_lua} m")
    full_simulation_text_data.append(f"Passo de Tempo (dt): {dt} s")
    full_simulation_text_data.append(f"Tempo Máximo de Simulação: {tempo_simulacao} s\n")
    full_simulation_text_data.append("Tempo (s), Posição (m), Velocidade (m/s), Aceleração (m/s^2)\n")

    while posicao < distancia_lua and tempo < tempo_simulacao:
        if massa_nave <= 0:
            print("Erro: Massa da nave deve ser maior que zero.")
            return None, None, None, None # Return None for all values
        aceleracao = forca_motor / massa_nave
        velocidade += aceleracao * dt
        posicao += velocidade * dt
        tempo += dt
        posicoes_list.append(posicao)
        velocidades_list.append(velocidade)
        tempos_list.append(tempo)
        aceleracoes_list.append(aceleracao)

        full_simulation_text_data.append(f"{tempo:.2f}, {posicao:.2f}, {velocidade:.2f}, {aceleracao:.2f}\n")

        if posicao >= distancia_lua:
            break

    # Criar DataFrame com os dados completos
    data = {
        'Tempo (s)': tempos_list[:-1],
        'Posicao (m)': posicoes_list[:-1],
        'Velocidade (m/s)': velocidades_list[:-1],
        'Aceleracao (m/s^2)': aceleracoes_list,
        'Forca (N)': [forca_motor] * len(aceleracoes_list),
        'Massa (kg)': [massa_nave] * len(aceleracoes_list)
    }
    df_simulacao = pd.DataFrame(data)

    # Cálculo da Energia (Joule)
    energia_total = 0.5 * massa_nave * velocidades_list[-1]**2 # Energia Cinética final

    print(f"Tempo total de viagem (aproximado): {tempo:.2f} segundos")
    print(f"Velocidade final (aproximada): {velocidade:.2f} m/s")
    print(f"Energia total usada (aproximada): {energia_total:.2f} Joules")
    print("--- Análise Concluída ---")

    # Save to CSV
    csv_path = os.path.join(output_dir, "simulacao_espacial.csv")
    df_simulacao.to_csv(csv_path, index=False)
    print(f"Dados da simulação salvos em '{csv_path}'")

    # Save full text data to TXT
    txt_path = os.path.join(output_dir, "simulacao_espacial_full_text.txt")
    with open(txt_path, "w", encoding="utf-8") as f:
        f.writelines(full_simulation_text_data)
    print(f"Dados da simulação em texto salvos em '{txt_path}'")

    # Generate and save plots
    positions_2d = [[p, 0] for p in posicoes_list] # For vector field, need 2D representation
    velocities_2d = [[v, 0] for v in velocidades_list]

    plot_velocity_vector_field(positions_2d, velocities_2d, title="Campo Vetorial de Velocidade da Espaçonave", output_dir=output_dir, filename="velocity_vector_field.png")
    euclidean_distances = calculate_euclidean_distances(positions_2d)
    plot_euclidean_distance(tempos_list, euclidean_distances, title="Distância Euclidiana Acumulada da Trajetória", output_dir=output_dir, filename="euclidean_distance_plot.png")
    plot_trajectory(tempos_list, posicoes_list, title="Trajetória da Espaçonave (Posição vs. Tempo)", output_dir=output_dir, filename="trajectory_plot.png")

    return df_simulacao, tempos_list, posicoes_list, velocidades_list

def test_lemuria_class():
    """
    Runs the simulation for the Lemuria-Class spacecraft.
    """
    print("--- Protocolo 'Mu de Lemúria' ---")
    print("--- Criando uma nova classe de nave espacial com propulsão baseada em Ditritium ---")

    # 1. Run Ditritium simulation to get the energy source
    DITRITIUM_I = 155
    DITRITIUM_N = 255
    ASCII_PROGRAM = "QFT_MODEL<UP-DOWN-STRANGE-CHARM-W_BOSON>"
    simulator = DitritiumSimulator(DITRITIUM_I, DITRITIUM_N)
    simulator.run_simulation(ASCII_PROGRAM)

    # 2. Read the sigma value from the generated file
    sigma_value = read_ditritium_signal()

    if sigma_value is not None:
        # 3. Define the "Lemuria-Class" spacecraft
        lemuria_class_mass = 2500  # Conceptual mass for the new class
        
        # 4. Calculate engine force using the new conceptual model
        # The factor is a conceptual scaling factor. It might need tuning.
        ditritium_force = conceptual_ditritium_engine_model(sigma_value)
        
        print(f"\n--- Especificações da Nave Classe-Lemúria ---")
        print(f"Massa da Nave: {lemuria_class_mass} kg")
        print(f"Sigma de Ditritium: {sigma_value}")
        print(f"Força do Motor (Propulsão XK): {ditritium_force} N")

        # 5. Run the simulation for the Lemuria-Class spacecraft
        dist_moon = 384400000  # Distance to the Moon
        time_step = 100
        sim_time = 1000000  # Increased simulation time

        try:
            sim_results_lemuria = simulate_space_travel(
                lemuria_class_mass, ditritium_force, dist_moon, time_step, sim_time
            )
            print("\n--- Resultados da Simulação da Classe-Lemúria ---")
            print(sim_results_lemuria.head())
            if not sim_results_lemuria.empty:
                print(f"Tempo total simulado: {sim_results_lemuria['Tempo (s)'].max()} segundos")
            else:
                print("A simulação não produziu resultados.")

            score_lemuria = calculate_score(sim_results_lemuria, "Conceptual Lemuria-Class Design")
            print(f"\nPontuação da Classe-Lemúria: {score_lemuria}")

        except ValueError as e:
            print(f"\nErro na simulação da Classe-Lemúria: {e}")
        except Exception as e:
            print(f"\nErro geral no teste: {e}")
    else:
        print("\n--- Simulação da Classe-Lemúria abortada: Não foi possível obter a energia do Ditritium ---")

# Example Usage (for testing the library)
if __name__ == "__main__":

    test_lemuria_class()

    print("\n--- Teste da Biblioteca de Espaçonave (Original) ---")

    # Test generate_competition_overview
    print(generate_competition_overview())

    # Test extract_parameters
    example_design = """
    The spaceship is a marvel of engineering. It has a mass of 1500 kg and a powerful ion engine capable of generating 12000 N of thrust. The spaceship contains solar sail.
    """
    params = extract_parameters(example_design)
    print(f"\nExtracted Parameters: {params}")

    if params:
        massa = params["massa_nave"]
        forca = params["forca_motor"]
        dist_moon = 384400000 # Distance to the Moon
        time_step = 100
        sim_time = 1000000 # Increased simulation time for a longer journey

        # Test simulate_space_travel
        try:
            sim_results = simulate_space_travel(massa, forca, dist_moon, time_step, sim_time)
            print("\nSimulation Results (first 5 rows):")
            print(sim_results.head())
            print(f"Total time simulated: {sim_results['Tempo (s)'].max()} seconds")

            # Test calculate_score
            score = calculate_score(sim_results, example_design)
            print(f"\nCalculated Score: {score}")

            # >>> ADICIONADO: Chamar a integração OpenVSP
            openvsp_integration.generate_vsp_model(massa, forca)
            # <<< FIM DA ADIÇÃO

        except ValueError as e:
            print(f"\nSimulation Test Error: {e}")
        except Exception as e:
            print(f"\nGeneral Test Error: {e}")

    # Test evaluate_design
    print("\n--- Testing evaluate_design ---")
    design_text_good = """
    My awesome rocket has a mass of 2000 kg and a thrust of 15000 N.
    """
    design_text_bad = """
    This is a bad design with no parameters.
    """
    design_text_zero_mass = """
    This design has a mass of 0 kg and a thrust of 1000 N.
    """

    score_good = evaluate_design(design_text_good, 384400000, 100, 1000000)
    print(f"Score for good design: {score_good}")

    score_bad = evaluate_design(design_text_bad, 384400000, 100, 1000000)
    print(f"Score for bad design: {score_bad}")

    score_zero_mass = evaluate_design(design_text_zero_mass, 384400000, 100, 1000000)
    print(f"Score for zero mass design: {score_zero_mass}")

    print("\n--- Testing New Hydrogen Propulsion and Trajectory Functions ---")

    # Test conceptual_hydrogen_engine_model
    try:
        xk_value = conceptual_hydrogen_engine_model(R=10, n=2, R1=1, R2=2, R3=3)
        print(f"Conceptual XK Value: {xk_value}")
        # Test division by zero
        # conceptual_hydrogen_engine_model(R=10, n=2, R1=0, R2=0, R3=0)
    except ValueError as e:
        print(f"Error in conceptual_hydrogen_engine_model: {e}")

    # Test conceptual_trajectory_dynamics
    dynamic_val = conceptual_trajectory_dynamics(J_pi=np.pi, A0=1, y=2, x=3)
    print(f"Conceptual Dynamic Value: {dynamic_val}")

    # Test simulate_trajectory (conceptual)
    initial_pos = np.array([0.0, 0.0, 0.0])
    initial_vel = np.array([10.0, 0.0, 0.0])
    time_points = np.linspace(0, 100, 10) # 10 time steps over 100 seconds
    
    # Placeholder thrust_profile and gravity_model
    def sample_thrust_profile(t, state):
        return np.array([100.0, 0.0, 0.0]) # Constant thrust

    def sample_gravity_model(position):
        return np.array([0.0, -9.8, 0.0]) # Simple gravity

    sim_traj = simulate_trajectory(
        initial_state=(initial_pos, initial_vel),
        time_steps=time_points,
        thrust_profile=sample_thrust_profile,
        gravity_model=sample_gravity_model
    )
    print(f"Simulated Trajectory (first point): {sim_traj[0]}")
    print(f"Simulated Trajectory (last point): {sim_traj[-1]}")

    # Test optimize_trajectory (conceptual)
    def sample_objective_function(params):
        return np.sum(params) # Simple objective

    sample_constraints = [lambda p: np.sum(p) > 0] # Simple constraint

    optimized_params = optimize_trajectory(
        objective_function=sample_objective_function,
        constraints=sample_constraints,
        initial_guess=[1.0, 2.0, 3.0]
    )
    print(f"Optimized Trajectory Parameters: {optimized_params}")

    