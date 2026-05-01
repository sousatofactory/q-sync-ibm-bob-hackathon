import pandas as pd
import math
import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.metrics import pairwise_distances
import random
import folium
import argparse
from scipy.ndimage import gaussian_filter

# --- Constants and Parameters ---
POPULATION_SIZE = 50
NUM_GENERATIONS = 20
MUTATION_RATE = 0.1
BASE_SPEED = 60
MAX_SPEED = 100
GRAVE_PROBLEM_AVOIDANCE_IMPACT = 0.8
TARGET_EFFICIENCY = 100
FIXED_COST = 500

# --- Utility Functions ---
def calculate_lref_d0(df):
    df['Lref'] = df['sequence'].apply(len)
    df['d0'] = df['Lref'].apply(lambda lref: 0.6 * math.sqrt(lref - 0.5) - 2.5)
    return df

# --- Genetic Algorithm Functions ---
def create_individual():
    return {
        'speed_factor': random.uniform(0.8, 1.2),
        'route_preference': random.uniform(0.0, 1.0)
    }

def calculate_efficiency(individual, distance, patients, time, grave_problem_avoided, fixed_cost):
    effective_speed = BASE_SPEED * individual['speed_factor']
    if effective_speed > MAX_SPEED:
        effective_speed = MAX_SPEED

    adjusted_distance = distance * (1 - individual['route_preference'] * 0.1)
    adjusted_time = time * (1 + individual['route_preference'] * 0.1)
    penalization_simulation = GRAVE_PROBLEM_AVOIDANCE_IMPACT if grave_problem_avoided else 0.0
    
    denominator = (adjusted_distance * (1 + penalization_simulation) + fixed_cost)
    if adjusted_time == 0 or denominator == 0:
        return 0
        
    efficiency = ((patients / adjusted_time) / denominator)
    return efficiency

def evaluate_fitness(individual, distances, patients_list, times_list, grave_problems_avoided_list, fixed_cost):
    total_efficiency = 0
    num_scenarios = len(distances)
    for i in range(num_scenarios):
        efficiency = calculate_efficiency(individual, distances[i], patients_list[i], times_list[i], grave_problems_avoided_list[i], fixed_cost)
        total_efficiency += efficiency
    return total_efficiency / num_scenarios if num_scenarios > 0 else 0

def crossover(parent1, parent2):
    child = {}
    for key in parent1.keys():
        if random.random() < 0.5:
            child[key] = parent1[key]
        else:
            child[key] = parent2[key]
    return child

def mutate(individual):
    for key in individual.keys():
        if random.random() < MUTATION_RATE:
            if key == 'speed_factor':
                individual[key] += random.uniform(-0.1, 0.1)
                individual[key] = max(0.8, min(1.2, individual[key]))
            else:
                individual[key] += random.uniform(-0.2, 0.2)
                individual[key] = max(0.0, min(1.0, individual[key]))
    return individual

def genetic_algorithm(distances, patients_list, times_list, grave_problems_avoided_list, fixed_cost):
    population = [create_individual() for _ in range(POPULATION_SIZE)]
    fitness_history = []
    best_individual_history = []

    for generation in range(NUM_GENERATIONS):
        fitness_scores = [evaluate_fitness(ind, distances, patients_list, times_list, grave_problems_avoided_list, fixed_cost) for ind in population]

        if not fitness_scores:
            print("Warning: Fitness scores list is empty. Stopping GA.")
            return create_individual(), [], []

        best_individual_index = np.argmax(fitness_scores)
        best_individual = population[best_individual_index]
        best_fitness = fitness_scores[best_individual_index]
        fitness_history.append(best_fitness)
        best_individual_history.append(best_individual)

        min_score = min(fitness_scores)
        weights = [(s - min_score) + 1e-9 for s in fitness_scores]
        if sum(weights) == 0:
            weights = [1] * len(population)

        selected_population = random.choices(population, weights=weights, k=POPULATION_SIZE)

        new_population = []
        for i in range(0, POPULATION_SIZE, 2):
            parent1 = selected_population[i]
            parent2 = selected_population[i + 1] if (i + 1) < POPULATION_SIZE else selected_population[0]
            child1 = crossover(parent1, parent2)
            child2 = crossover(parent2, parent1)
            new_population.append(mutate(child1))
            new_population.append(mutate(child2))
        
        population = new_population[:POPULATION_SIZE]

        print(f"Generation {generation}: Best Fitness = {best_fitness}")

    best_individual_index = np.argmax([evaluate_fitness(ind, distances, patients_list, times_list, grave_problems_avoided_list, fixed_cost) for ind in population])
    return population[best_individual_index], fitness_history, best_individual_history

# --- "Cure" Generation Functions ---

def run_cure_generation(disease_name):
    """Generates a conceptual cure strategy based on Hessian analysis of a simulated cell."""
    print(f"--- Generating Conceptual Cure for: {disease_name} ---")
    
    # 1. Simulate a cell image
    np.random.seed(42)
    grid_size = 200
    image = np.zeros((grid_size, grid_size))
    # Create a few blob-like structures to simulate a cell
    x, y = np.mgrid[0:grid_size, 0:grid_size]
    image += 120 * np.exp(-((x - 70)**2 / 800.0 + (y - 80)**2 / 1200.0))
    image += 90 * np.exp(-((x - 130)**2 / 700.0 + (y - 120)**2 / 500.0))
    image = gaussian_filter(image, sigma=5)

    # 2. Calculate Hessian matrix (second derivatives)
    dx, dy = np.gradient(image)
    dxx, dxy = np.gradient(dx)
    dyx, dyy = np.gradient(dy)
    
    # Determinant of the Hessian (Discriminant)
    determinant = dxx * dyy - dxy**2

    # 3. Find critical points (conceptual vulnerabilities)
    # We'll find local maxima in the determinant as points of interest
    threshold = np.percentile(determinant, 99.8) # Top 0.2% of discriminant values
    critical_points = np.argwhere(determinant > threshold)

    # 4. Generate visualization
    plt.figure(figsize=(10, 8))
    plt.imshow(image, cmap='viridis', origin='lower')
    plt.title(f"Conceptual Targeting Map for {disease_name}")
    plt.colorbar(label="Cell Density (Simulated)")
    plt.scatter(critical_points[:, 1], critical_points[:, 0], c='red', marker='x', s=100, label='Intervention Points')
    plt.legend()
    plt.savefig("cure_targeting_map.png")
    plt.close()
    print("Cure targeting map saved to cure_targeting_map.png")

    # 5. Generate report
    report_content = f"""
    Conceptual Cure Strategy Report
    ----------------------------------
    Disease Analyzed: {disease_name}

    Methodology:
    A simulated cellular structure was analyzed using Hessian matrix-based discriminant analysis.
    The Hessian matrix identifies points of maximum and minimum curvature, which conceptually correspond
    to critical structural vulnerabilities or key functional hubs of the pathogenic entity.

    Identified Intervention Points:
    - Number of critical points identified: {len(critical_points)}
    - These points, marked in red on the accompanying `cure_targeting_map.png`, represent areas where
      the cellular structure is most susceptible to intervention.

    Conceptual Treatment Strategy:
    A targeted therapeutic agent would be conceptually designed to bind to these specific locations.
    By disrupting these critical points, the agent would aim to:
    1.  Inhibit key enzymatic or signaling pathways.
    2.  Destabilize the overall structure of the pathogen.
    3.  Prevent replication or interaction with host cells.

    This targeted approach minimizes off-target effects and maximizes therapeutic efficacy by focusing
    on the mathematically-determined points of greatest vulnerability.

    Disclaimer:
    This is a conceptual simulation. It does not represent a real medical treatment.
    """
    with open("cure_strategy_report.txt", "w") as f:
        f.write(report_content)
    print("Cure strategy report saved to cure_strategy_report.txt")

# --- Vaccine Design Functions ---
def fetch_full_analysis_mock(disease_name):
    """
    Simulates the response from the Gemini API for vaccine design analysis.
    Returns mock data in the expected JSON format.
    """
    print(f"Simulating full analysis for disease: {disease_name}...")
    # Mock data structure based on the JavaScript in fasta_api.html
    mock_data = {
        "summary": f"Análise conceitual da doença '{disease_name}': Esta é uma simulação de uma patologia complexa que afeta sistemas biológicos em múltiplos níveis, com impacto significativo na homeostase celular e tecidual. A doença apresenta um perfil de progressão rápido e alta transmissibilidade em ambientes controlados.",
        "ambulanceUrgency": 0.75,
        "biomarkerAnalysis": {
            "Proteína_X": 0.85,
            "RNA_Y": 0.70,
            "Metabólito_Z": 0.60,
            "Gene_A": 0.92
        },
        "outbreakHotspots": [
            {"lat": -23.5505, "lng": -46.6333, "severity": 0.9}, # São Paulo
            {"lat": -22.9068, "lng": -43.1729, "severity": 0.8}, # Rio de Janeiro
            {"lat": -15.7801, "lng": -47.9292, "severity": 0.7}, # Brasília
            {"lat": -30.0346, "lng": -51.2177, "severity": 0.6}, # Porto Alegre
            {"lat": -8.0476, "lng": -34.8769, "severity": 0.5}  # Recife
        ],
        "vaccine": {
            "antigen_target": "Glicoproteína de Superfície Conceitual (GSC-1)",
            "vaccine_platform": "mRNA (RNA mensageiro): Esta plataforma permite uma resposta imune rápida e adaptável, ideal para patógenos emergentes.",
            "conceptual_fasta": f">TakaSystem_Vax|{disease_name.replace(' ', '_')}|Conceptual_Antigen\n"
                                "MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHGKKVADALTNAVAHVDDMPNALSALSDLHAHKLRVDPVNFKLLSHCLLVTLAAHLPAEFTPAVHASLDKFLASVSTVLTSKYR\n"
                                "Conceptual sequence for a highly immunogenic antigen.",
            "conceptual_mrna": f">TakaSystem_mRNA|{disease_name.replace(' ', '_')}|Optimized\n"
                                "AUGGUGCUGAGCCCAGCCGACGGCACCAACGUGAAGGCCGCUGUGGGCGGCAAGGUAGGAGCCCAUGCCGGGAGAGUACGGCGCCGAGGCGCUGGAGCGCAUGUUCUUGA\n"
                                "GCUUCCCACCAACCAAGACCUACUUCCCGCACUUUGACCUGAGCCACGGCAGCGCCCAGGUGAAGGGCCACGGCGGCAAGGUAGCCGACGCCCUGACCAACGCCGUGGC\n"
                                "CCACGUGGACGACAUGCCCAACGCCCUGAGCGCCCUGAGCGACCUGCAUGCCCACAAGCUGCGCGUAGACCCCGUGAACUUCAAGCUGCUGAGCCACUGCUGCUGGU\n"
                                "GACCUUGGCGGCCCACCUGCCGGCCGAGUUCACCCCGGCCGUGCAUGCCAGCCUGGGCAAGUUCUUGGCCAGCGUGAGCACCGUGCUGACCAGCAAGUACCGGUAA\n"
                                "AAAAAAAAAAAAAAAAA", # Poly-A tail
            "strategy_report": "A estratégia de design da vacina focou na identificação de epítopos conservados na GSC-1, utilizando modelagem computacional para prever a imunogeniciade e a estabilidade estrutural. A plataforma de mRNA foi selecionada pela sua flexibilidade e capacidade de induzir respostas imunes robustas de células T e B, essenciais para a proteção contra este patógeno simulado. A otimização de códons e a inclusão de UTRs específicos visam maximizar a expressão proteica e a estabilidade do mRNA in vivo, garantindo uma produção eficiente do antígeno vacinal."
        }
    }
    return mock_data

def run_vaccine_design(disease_name):
    """
    Executes the conceptual vaccine design process for a given disease.
    """
    print(f"--- Iniciando o Design Conceitual de Vacinas para: {disease_name} ---")
    try:
        full_analysis = fetch_full_analysis_mock(disease_name)

        print("\n### Análise Inicial da Doença ###")
        print(f"Sumário: {full_analysis['summary']}")

        print("\n### Análise de Biomarcadores ###")
        for biomarker, relevance in full_analysis['biomarkerAnalysis'].items():
            print(f"- {biomarker}: Relevância Diagnóstica = {relevance:.2f}")

        print("\n### Otimização Logística e Mapeamento de Surtos (Simulado) ###")
        print(f"Urgência de Ambulância (0.0-1.0): {full_analysis['ambulanceUrgency']:.2f}")
        print("Focos de Surto (Lat, Lng, Severidade):")
        for hotspot in full_analysis['outbreakHotspots']:
            print(f"- Lat: {hotspot['lat']}, Lng: {hotspot['lng']}, Severidade: {hotspot['severity']:.2f}")
        
        # Simulate ambulance optimization results (simplified)
        # This part would ideally call the existing genetic_algorithm from health_optimizer
        # For now, we'll just print a placeholder.
        print("\nResultados da Otimização de Ambulância (Simulado):")
        print("Parâmetros ótimos para ambulância: Velocidade: X.XX, Preferência de Rota: Y.YY")
        print("Resultados da Simulação: (Tabela de Eficiência Escalada)")
        print("  Dist(km) | Pac. | Tempo(h) | Efic. Escalada")
        print("  ---------------------------------------------")
        print("  100.0    | 6    | 2.0      | 85.00")
        print("  150.0    | 4    | 3.0      | 70.00")

        print("\n### Estratégia de Vacina Conceitual ###")
        vaccine_data = full_analysis['vaccine']
        print(f"Antígeno Alvo Identificado: {vaccine_data['antigen_target']}")
        print(f"Plataforma Vacinal Recomendada: {vaccine_data['vaccine_platform']}")
        print(f"Justificativa Científica (Auto-vigilância da IA): {vaccine_data['strategy_report']}")
        print("\nSequência da Proteína (FASTA):")
        print(vaccine_data['conceptual_fasta'])
        print("\nSequência de mRNA Otimizada:")
        print(vaccine_data['conceptual_mrna'])

    except Exception as e:
        print(f"Ocorreu um erro durante o design da vacina: {e}")
    print("--- Design Conceitual de Vacinas Concluído ---")

# --- Main Execution Modes ---

def run_ambulance_optimization():
    print("--- Running Ambulance Optimization ---")
    scenarios_df = pd.DataFrame({
        'Scenario': [1, 2, 3, 4],
        'Distance (km)': [100, 150, 200, 120],
        'Patients': [6, 4, 5, 4],
        'Time (hours)': [2.0, 3.0, 2.5, 2.2],
        'Grave Problem Avoided': [True, False, True, False]
    })
    
    distances = scenarios_df['Distance (km)'].tolist()
    patients_list = scenarios_df['Patients'].tolist()
    times_list = scenarios_df['Time (hours)'].tolist()
    grave_problems_avoided_list = scenarios_df['Grave Problem Avoided'].tolist()

    best_params, fitness_history, _ = genetic_algorithm(distances, patients_list, times_list, grave_problems_avoided_list, FIXED_COST)
    print("\nBest Ambulance Parameters Found:", best_params)

    avg_distance = np.mean(distances)
    avg_patients = np.mean(patients_list)
    avg_time = np.mean(times_list)
    avg_grave_problem_avoided = any(grave_problems_avoided_list)
    avg_efficiency_with_best_params = calculate_efficiency(best_params, avg_distance, avg_patients, avg_time, avg_grave_problem_avoided, FIXED_COST)
    K = TARGET_EFFICIENCY / avg_efficiency_with_best_params if avg_efficiency_with_best_params > 0 else 0
    print(f"\nCalculated K factor: {K}")

    if fitness_history:
        plt.figure(figsize=(10, 6))
        plt.plot(fitness_history)
        plt.xlabel("Generation")
        plt.ylabel("Best Fitness (Average Efficiency)")
        plt.title("Genetic Algorithm: Fitness Over Generations")
        plt.grid(True)
        plt.savefig("ambulance_fitness_history.png")
        plt.close()
        print("\nFitness history plot saved to ambulance_fitness_history.png")

    np.random.seed(42)
    patient_locations = pd.DataFrame({
        'lat': np.random.uniform(-90, 90, 20),
        'lon': np.random.uniform(-180, 180, 20),
        'severity': np.random.randint(1, 11, 20),
        'scenario': np.random.randint(1, 5, 20)
    })
    map_center = [patient_locations.lat.mean(), patient_locations.lon.mean()]
    patient_map = folium.Map(location=map_center, zoom_start=2)
    colors = {1: 'red', 2: 'blue', 3: 'green', 4: 'purple'}
    for _, row in patient_locations.iterrows():
        folium.CircleMarker(
            location=[row['lat'], row['lon']],
            radius=row['severity'] * 2,
            popup=f"Severity: {row['severity']} - Scenario: {row['scenario']}",
            color=colors[row['scenario']],
            fill=True,
            fill_color=colors[row['scenario']],
            fill_opacity=0.4
        ).add_to(patient_map)
    patient_map.save("patient_location_map.html")
    print("Patient location map saved to patient_location_map.html")

    unscaled_eff = [calculate_efficiency(best_params, d, p, t, g, FIXED_COST) for d, p, t, g in zip(distances, patients_list, times_list, grave_problems_avoided_list)]
    scaled_eff = [e * K for e in unscaled_eff]
    scenarios_df['Unscaled Efficiency'] = unscaled_eff
    scenarios_df['Scaled Efficiency'] = scaled_eff
    print("\n--- Simulation Scenario Results ---")
    print(scenarios_df.to_string())

def run_rna_folding():
    print("\n--- Running RNA Folding Analysis ---")
    num_sequences = 10
    data = {
        'target_id': [f'seq_{i}' for i in range(num_sequences)],
        'sequence': ['AUCG' * (i + 1) for i in range(num_sequences)],
        'description': ['Generic sequence' for _ in range(num_sequences)]
    }
    test_df = pd.DataFrame(data)
    test_df = calculate_lref_d0(test_df)

    np.random.seed(42)
    helix_radius = 5.0
    helix_pitch = 3.0
    z_scaling_factor = 1.0

    def generate_helical_structure(sequence_length, structure_number, phase_shift=0):
        angles = np.linspace(0, 4 * np.pi, sequence_length) + phase_shift
        random_offsets = np.random.rand(sequence_length) * 1.0
        x_coords = helix_radius * np.cos(angles) + random_offsets
        y_coords = helix_radius * np.sin(angles) + random_offsets
        z_coords = helix_pitch * angles + z_scaling_factor * structure_number
        return x_coords, y_coords, z_coords

    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_title("3D Structures of RNA Sequences")

    results_data = []
    for index, row in test_df.iterrows():
        target_id = row['target_id']
        sequence = row['sequence']
        sequence_length = len(sequence)
        x_coords1, y_coords1, z_coords1 = generate_helical_structure(sequence_length, 1)
        x_coords2, y_coords2, z_coords2 = generate_helical_structure(sequence_length, 2, phase_shift=np.pi)
        ax.plot(x_coords1, y_coords1, z_coords1, label=f"{target_id} Helix 1")
        ax.plot(x_coords2, y_coords2, z_coords2, label=f"{target_id} Helix 2")
        all_coords = np.column_stack((np.concatenate([x_coords1, x_coords2]),
                                       np.concatenate([y_coords1, y_coords2]),
                                       np.concatenate([z_coords1, z_coords2])))
        distance_matrix = pairwise_distances(all_coords)
        avg_distance = np.mean(distance_matrix)
        results_data.append([target_id, sequence_length, avg_distance])

    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[:4], labels[:4])
    plt.savefig("rna_3d_structures.png")
    plt.close()
    print("RNA 3D structures plot saved to rna_3d_structures.png")

    results_df = pd.DataFrame(results_data, columns=['target_id', 'sequence_length', 'average_distance'])
    plt.figure(figsize=(10, 6))
    plt.bar(results_df['target_id'], results_df['average_distance'])
    plt.xlabel("Target ID")
    plt.ylabel("Average Distance (Singularity Measure)")
    plt.title("Comparison of Singularity Measures")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig("rna_singularity_measure.png")
    plt.close()
    print("RNA singularity measure plot saved to rna_singularity_measure.png")
    print("\n--- RNA Analysis Results ---")
    print(results_df.to_string())

def main():
    parser = argparse.ArgumentParser(description="TakaSystem Health Optimizer and Bio-Research Tool")
    parser.add_argument('--mode', type=str, required=True, choices=['ambulance', 'rna', 'cure', 'vaccine_design'],
                        help='The mode to run: "ambulance", "rna", "cure", or "vaccine_design".')
    parser.add_argument('--disease', type=str, default="Unknown Disease",
                        help='The name of the disease for cure generation or vaccine design mode.')
    
    args = parser.parse_args()

    if args.mode == 'ambulance':
        run_ambulance_optimization()
    elif args.mode == 'rna':
        run_rna_folding()
    elif args.mode == 'cure':
        run_cure_generation(args.disease)
    elif args.mode == 'vaccine_design':
        run_vaccine_design(args.disease)

if __name__ == "__main__":
    main()