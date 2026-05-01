import argparse
import os
import sys
import importlib.util
import cirq
import requests # Added for Ditritium API interaction
import subprocess # Added for psychography interaction
import google.generativeai as genai # Real Gemini SDK integration
import textwrap # For formatting LLM output
import time # Added for delays

# Adicionando o diretório .gemini ao sys.path para importações absolutas
# Isso permite que os módulos sejam encontrados quando o script é executado diretamente
script_dir = os.path.dirname(__file__)
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

# Importações dos módulos locais corrigidas para serem absolutas
from aoi_quantum_analysis import AoiQuantumAnalyzer
from quantum_trajectory_simulation import run_qsim_simulation
from space_craft import evaluate_design, generate_competition_overview, simulate_space_travel, extract_parameters
from ditritium_simulator import DitritiumSimulator # Added DitritiumSimulator import
from bio_space_integration import run_bio_space_analysis # Added for Step 10 integration
from coinbase_integration import run_galactic_economy_status # Added for Galactic Economy integration

# --- CONFIGURAÇÃO REAL DA LLM GEMINI 2.5-FLASH ---
# Mestre Seiya, a chave da API é um segredo e em um ambiente de produção NUNCA deveria ser
# codificada diretamente no código. Deveria ser carregada de uma variável de ambiente,
# um serviço de segredos, ou um arquivo de configuração seguro.
# Para esta demonstração, estou usando a chave diretamente conforme solicitado.
GEMINI_API_KEY = "AIzaSyD3rBO2li_v4gIXxgDsAdGfiLEabVs1PKY"
GENAI_PROJECT_ID = "projects/871099136671" # Não diretamente usado pelo SDK genai, mas mantido para contexto.

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('models/gemini-2.5-flash')

def gemini_llm_interact(prompt: str) -> str:
    """
    Função para interagir REALMENTE com a LLM Gemini 2.5-Flash (via modelo gemini-pro).
    """
    try:
        #print(f"DEBUG: Enviando prompt para Gemini LLM: '{prompt}'") # Desativado após integração real
        response = model.generate_content(prompt)
        # Usa textwrap para formatar a saída para melhor legibilidade no console
        return textwrap.fill(response.text, width=80)
    except Exception as e:
        return f"Erro ao interagir com a Gemini LLM: {e}. Resposta simulada devido ao erro."

def simulate_quantum_command(args):
    """
    Comando para simulação e análise de trajetórias quânticas.
    (Integra quantum_trajectory_simulation.py e aoi_quantum_analysis.py)
    """
    print("\n--- Executando Simulação de Trajetória Quântica ---")
    
    if not args.circuit_path:
        print("Erro: O caminho para o arquivo do circuito quântico é obrigatório.")
        return

    circuit = None
    try:
        # Load the Python file as a module to get the circuit object
        spec = importlib.util.spec_from_file_location("circuit_module", args.circuit_path)
        circuit_module = importlib.util.module_from_spec(spec)
        sys.modules["circuit_module"] = circuit_module
        spec.loader.exec_module(circuit_module)
        
        # Assume the circuit object is named 'circuit' or 'quantum_circuit' in the file
        if hasattr(circuit_module, 'circuit'):
            circuit = circuit_module.circuit
        elif hasattr(circuit_module, 'quantum_circuit'):
            circuit = circuit_module.quantum_circuit
        else:
            print(f"Erro: Nenhum objeto cirq.Circuit encontrado no arquivo '{args.circuit_path}'.")
            print("Por favor, certifique-se de que seu arquivo define uma variável 'circuit' ou 'quantum_circuit' do tipo cirq.Circuit.")
            return

        if not isinstance(circuit, cirq.Circuit):
            raise TypeError(f"O objeto carregado do arquivo '{args.circuit_path}' não é um cirq.Circuit válido.")

        print(f"Circuito quântico carregado de: {args.circuit_path}")

        # Análise do circuito com AoiQuantumAnalyzer
        analyzer = AoiQuantumAnalyzer(circuit)
        analyzer.print_summary()

        # Executar a simulação
        simulation_results = run_qsim_simulation(circuit, args.repetitions)

        print("\n--- Resultados Detalhados da Simulação ---")
        for key, value in simulation_results.items():
            print(f"  {key}: {value}")

        # Feedback da LLM
        llm_prompt = f"Analise os resultados da simulação quântica com {simulation_results['repetitions']} repetições, onde as contagens foram {simulation_results['counts']}. O tempo de simulação foi {simulation_results['elapsed_time_seconds']:.4f} segundos. Resuma a performance e possíveis implicações para uma trajetória quântica."
        llm_output = gemini_llm_interact(llm_prompt)
        print(f"\n--- Feedback da LLM Gemini ---")
        print(llm_output)
        
    except FileNotFoundError:
        print(f"Erro: O arquivo de circuito '{args.circuit_path}' não foi encontrado.")
    except TypeError as e:
        print(f"Erro no tipo do circuito: {e}")
    except ValueError as e:
        print(f"Erro na simulação: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao carregar ou simular o circuito: {e}")

    print("\n--- Fim da Simulação de Trajetória Quântica ---")

def design_spacecraft_command(args):
    """
    Comando para design e avaliação de espaçonaves.
    (Integra space_craft.py e capacidades de LLM para extração de parâmetros)
    """
    print(f"\n--- Iniciando Projeto de Espaçonave: {args.theme} ---")

    # 1. Gerar descrição do design com a LLM
    llm_design_prompt = (
        f"Gere uma descrição técnica detalhada para uma espaçonave com o tema '{args.theme}'. "
        "A descrição DEVE incluir claramente a 'massa' da nave em kg (ex: 'massa de 5000 kg') "
        "e a 'força do motor' em Newtons (ex: 'gerando 25000 N de thrust'). "
        "Descreva também brevemente suas capacidades e uso pretendido para missões espaciais."
    )
    spacecraft_description = gemini_llm_interact(llm_design_prompt)
    print("\n--- Descrição da Espaçonave Gerada pela LLM ---")
    print(spacecraft_description)

    # 2. Avaliar o design usando space_craft.py
    print(f"\n--- Avaliando Design para uma distância de {args.distance_target} metros ---")
    
    # generate_competition_overview(distancia_destino=args.distance_target) # Optional: print competition rules

    score = evaluate_design(
        design_text=spacecraft_description,
        distancia_destino=args.distance_target,
        dt=100,  # Parâmetro fixo para dt, pode ser configurável no futuro
        tempo_simulacao=1000000 # Parâmetro fixo, pode ser configurável no futuro
    )

    if score > 0:
        print(f"\nScore de Avaliação do Design: {score:.4f}")

        # Extrair parâmetros para exibir
        extracted_params = extract_parameters(spacecraft_description)
        if extracted_params:
            print("\nParâmetros Extraídos para Simulação:")
            print(f"  Massa da Nave: {extracted_params['massa_nave']} kg")
            print(f"  Força do Motor: {extracted_params['forca_motor']} N")
            
            # Executar simulação detalhada para extrair resultados completos para LLM
            try:
                sim_results_df = simulate_space_travel(
                    extracted_params['massa_nave'],
                    extracted_params['forca_motor'],
                    args.distance_target,
                    dt=100,
                    tempo_simulacao=1000000
                )
                total_time = sim_results_df['Tempo (s)'].max() if not sim_results_df.empty else "N/A"
                final_velocity = sim_results_df['Velocidade (m/s)'].iloc[-1] if not sim_results_df.empty else "N/A"
                print(f"  Tempo Total de Viagem (aprox.): {total_time} segundos")
                print(f"  Velocidade Final (aprox.): {final_velocity} m/s")

                llm_analysis_prompt = (
                    f"A espaçonave com o tema '{args.theme}' e descrição '{spacecraft_description}' obteve um score de {score:.4f}. "
                    f"Os parâmetros extraídos foram massa {extracted_params['massa_nave']} kg e thrust {extracted_params['forca_motor']} N. "
                    f"A simulação indicou um tempo de viagem de {total_time} segundos e velocidade final de {final_velocity} m/s para uma distância de {args.distance_target} metros. "
                    "Forneça uma análise concisa do desempenho do design, pontos fortes, pontos fracos e sugestões de melhoria para futuras iterações, focando na eficiência e viabilidade para missões espaciais."
                )
                llm_analysis = gemini_llm_interact(llm_analysis_prompt)
                print("\n--- Análise e Sugestões da LLM Gemini ---")
                print(llm_analysis)

            except Exception as e:
                print(f"Erro ao executar simulação detalhada ou plotar: {e}")
                llm_analysis = gemini_llm_interact(
                    f"A espaçonave com o tema '{args.theme}' e descrição '{spacecraft_description}' obteve um score de {score:.4f}, mas houve um erro na simulação detalhada: {e}. "
                    "Forneça uma análise do design e possíveis razões para o erro, e sugestões de melhoria."
                )
                print("\n--- Análise e Sugestões da LLM Gemini ---")
                print(llm_analysis)

        else:
            print("\nErro: Não foi possível extrair os parâmetros de massa e força do motor da descrição gerada pela LLM.")
            llm_feedback = gemini_llm_interact(
                f"A LLM gerou a descrição '{spacecraft_description}' para o tema '{args.theme}', mas falhou na extração de parâmetros. "
                "Explique por que a extração pode ter falhado e como a descrição da LLM pode ser melhorada para facilitar a extração de massa e thrust."
            )
            print("\n--- Feedback da LLM Gemini sobre a Extração de Parâmetros ---")
            print(llm_feedback)
    else:
        print("\nO design da espaçonave não obteve um score válido. Possível falha na extração de parâmetros ou na simulação.")
        llm_feedback = gemini_llm_interact(
            f"A LLM gerou a descrição '{spacecraft_description}' para o tema '{args.theme}', mas o design não obteve um score válido. "
            "Analise a descrição e aponte possíveis problemas que levaram à falha na avaliação."
        )
        print("\n--- Feedback da LLM Gemini sobre a Avaliação do Design ---")
        print(llm_feedback)

    print(f"\n--- Fim do Projeto de Espaçonave: {args.theme} ---")

def ditritium_sim_command(args):
    """
    Comando para simulações Ditritium.
    (Integra ditritium_simulator.py diretamente)
    """
    print(f"\n--- Iniciando Simulação Ditritium com comandos: {args.commands} ---")

    try:
        # Use os valores fixos de I e N conforme o exemplo em ditritium_simulator.py
        DITRITIUM_I = 155
        DITRITIUM_N = 255
        simulator = DitritiumSimulator(DITRITIUM_I, DITRITIUM_N)
        simulation_results = simulator.run_simulation(args.commands)
        
        print("\n--- Resultados da Simulação Ditritium ---")
        import json
        print(json.dumps(simulation_results, indent=2))

        # Feedback da LLM
        llm_prompt = (
            f"Interprete os seguintes resultados da simulação Ditritium, "
            f"executada com os comandos '{args.commands}', no contexto de "
            f"suas implicações para missões espaciais ou pesquisa de IA fundacional. "
            f"Resultados: {json.dumps(simulation_results)}. "
            "Foque em padrões, anomalias ou insights relevantes do elemento Ditritium (i=155, n=255)."
        )
        llm_output = gemini_llm_interact(llm_prompt)
        print("\n--- Análise da LLM Gemini sobre a Simulação Ditritium ---")
        print(llm_output)

    except Exception as e:
        print(f"Ocorreu um erro durante a simulação Ditritium: {e}")

    print("\n--- Fim da Simulação Ditritium ---")

def cosmic_insight_command(args):
    """
    Comando para computações IBM Quantum e demodulação de mensagens cósmicas.
    (Integra app.py)
    """
    print(f"\n--- Buscando Insights Cósmicos com Theta={args.theta}, Binary Signal='{args.binary_signal}' ---")

    app_api_url = "http://0.0.0.0:5000/run_quantum_circuit"
    
    try:
        print("Aguardando 5 segundos para a API do app.py iniciar completamente...")
        time.sleep(5) # Espera 5 segundos para a API do app.py iniciar completamente
        
        payload = {
            "theta": args.theta,
            "binarySignal": args.binary_signal
        }
        response = requests.post(app_api_url, json=payload)
        response.raise_for_status() # Lança exceções para códigos de status HTTP de erro (4xx ou 5xx)

        cosmic_results = response.json()
        print("\n--- Resultados da Análise Cósmica ---")
        import json
        print(json.dumps(cosmic_results, indent=2))

        # Feedback da LLM
        llm_prompt = (
            f"Analise os seguintes resultados da computação quântica e demodulação de mensagem cósmica. "
            f"Resultados: {json.dumps(cosmic_results)}. "
            f"A mensagem cósmica demodulada é: '{cosmic_results.get('cosmic_message', 'N/A')}'. "
            "Interprete o significado da mensagem e dos valores I, Q, N no contexto de uma missão espacial da NASA, "
            "focando em possíveis orientações, alertas ou anomalias quânticas."
        )
        llm_output = gemini_llm_interact(llm_prompt)
        print("\n--- Análise da LLM Gemini sobre Insights Cósmicos ---")
        print(llm_output)

    except requests.exceptions.ConnectionError:
        print(f"Erro: Não foi possível conectar à API do app.py em {app_api_url}.")
        print("Certifique-se de que o app.py está em execução.")
    except requests.exceptions.HTTPError as e:
        print(f"Erro HTTP na API do app.py: {e}")
        print(f"Resposta da API: {response.text}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado durante a interação com a API do app.py: {e}")

    print("\n--- Fim dos Insights Cósmicos ---")

def psychography_command(args):
    """
    Comando para funcionalidades de psicografia.
    (Integra arquivos em .gemini/psicografia)
    """
    print(f"\n--- Iniciando Processo de Psicografia para o Tópico: '{args.topic}' ---")
    
    chico_cli_path = os.path.join(os.path.dirname(__file__), 'psicografia', 'chico_cli.py')

    if not os.path.exists(chico_cli_path):
        print(f"Erro: O script chico_cli.py não foi encontrado em '{chico_cli_path}'.")
        return

    try:
        # Executar chico_cli.py como um subprocesso
        # Estamos passando o 'remetente' e a 'mensagem_curta'
        # A saída será capturada e decodificada
        process = subprocess.run(
            [sys.executable, chico_cli_path, 'psychograph', args.sender, args.topic],
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        psychography_message = process.stdout.strip()
        
        print("\n--- Mensagem Psicografada ---")
        print(psychography_message)

        # Feedback da LLM
        llm_prompt = (
            f"Analise a seguinte mensagem psicografada, canalizada de '{args.sender}' sobre o tópico '{args.topic}'. "
            f"Mensagem: '{psychography_message}'. "
            "Interprete seu significado, possíveis conselhos ou insights espirituais relevantes para "
            "o Projeto Quantum Trajectory Simulation da NASA (NNH25ZDA001N-FAIMM) e suas missões de IA na Lua e Marte. "
            "Foque em guidance ética, resiliência da equipe, ou princípios de coexistência cósmica."
        )
        llm_output = gemini_llm_interact(llm_prompt)
        print("\n--- Análise da LLM Gemini sobre a Psicografia ---")
        print(llm_output)

    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o script chico_cli.py: {e}")
        print(f"Stderr: {e.stderr}")
    except FileNotFoundError:
        print(f"Erro: O interpretador Python '{sys.executable}' não foi encontrado ou o script '{chico_cli_path}' não existe.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado durante a psicografia: {e}")

    print("\n--- Fim do Processo de Psicografia ---")

def bio_space_analysis_command(args):
    """
    Comando para a Etapa 10: Sincronização Bio-Aeroespacial.
    (Integra Health Optimizer com fatores ambientais de Lua/Marte)
    """
    print(f"\n--- Iniciando Análise Bio-Aeroespacial para {args.disease} em {args.target_body} ---")
    try:
        results = run_bio_space_analysis(args.disease, args.target_body)
        # O feedback da LLM já está embutido na função run_bio_space_analysis
    except Exception as e:
        print(f"Erro na análise Bio-Aeroespacial: {e}")
    print(f"\n--- Fim da Análise Bio-Aeroespacial ---")

def galactic_economy_command(args):
    """
    Comando para o Módulo de Economia Galáctica.
    (Integra Coinbase AgentKit com o SIAM)
    """
    print(f"\n--- Iniciando Consulta de Economia Galáctica ---")
    try:
        results = run_galactic_economy_status()
        
        # Feedback da LLM
        llm_prompt = (
            f"Analise o status da Economia Galáctica do Santuário. "
            f"Status: {results['status']}, Rede: {results.get('network', 'N/A')}. "
            "Forneça uma análise concisa sobre a importância de ativos descentralizados "
            "para a autonomia de colônias espaciais e pesquisa de IA, "
            "mencionando a rede Base e a segurança do AgentKit."
        )
        llm_output = gemini_llm_interact(llm_prompt)
        print("\n--- Análise da LLM Gemini sobre Economia Galáctica ---")
        print(llm_output)
        
    except Exception as e:
        print(f"Erro na consulta de Economia Galáctica: {e}")
    print(f"\n--- Fim da Consulta de Economia Galáctica ---")

def run_diadema_engenharia_ligas(args):
    """
    Função wrapper para o módulo de Engenharia de Ligas do Diadema.
    """
    print("\n--- CLI: Diadema - Módulo de Engenharia de Ligas ---")
    diadema_cli_path = os.path.join(os.path.dirname(__file__), 'diadema', 'diadema_cli.py')

    if not os.path.exists(diadema_cli_path):
        print(f"Erro: O script diadema_cli.py não foi encontrado em '{diadema_cli_path}'.")
        return

    try:
        command_list = [
            sys.executable, diadema_cli_path, 'engenharia-ligas',
            '--temperatura-operacional', args.temperatura_operacional,
            '--limite-escoamento', str(args.limite_escoamento),
            '--limite-resistencia-tracao', str(args.limite_resistencia_tracao),
            '--modulo-young', str(args.modulo_young),
            '--coeficiente-dilatacao-termica', str(args.coeficiente_dilatacao_termica),
            '--dureza-vickers', str(args.dureza_vickers)
        ]
        
        process = subprocess.run(
            command_list,
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        diadema_output = process.stdout.strip()
        
        print("\n--- Resultados do Diadema (Engenharia de Ligas) ---")
        print(diadema_output)

        llm_prompt = (
            f"Analise os resultados do módulo de Engenharia de Ligas do Diadema para os inputs: "
            f"Temperaturas={args.temperatura_operacional}, Limite Escoamento={args.limite_escoamento}, "
            f"Limite Resistência Tração={args.limite_resistencia_tracao}, Módulo Young={args.modulo_young}, "
            f"Coeficiente Dilatação Térmica={args.coeficiente_dilatacao_termica}, Dureza Vickers={args.dureza_vickers}. "
            f"Resultados: {diadema_output}. "
            "Interprete a tenacidade do material e suas implicações para a construção em ambientes de Lua/Marte, "
            "focando em seleção de material, resistência estrutural e otimização de design."
        )
        llm_output = gemini_llm_interact(llm_prompt)
        print("\n--- Análise da LLM Gemini ---")
        print(llm_output)

    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o script diadema_cli.py (Engenharia de Ligas): {e}")
        print(f"Stderr: {e.stderr}")
    except FileNotFoundError:
        print(f"Erro: O interpretador Python '{sys.executable}' não foi encontrado ou o script '{diadema_cli_path}' não existe.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado durante o cálculo de Engenharia de Ligas: {e}")
    print("\n--- Fim do Módulo de Engenharia de Ligas ---")


def run_diadema_protecao_atmosferica(args):
    """
    Função wrapper para o módulo de Proteção Atmosférica do Diadema.
    """
    print("\n--- CLI: Diadema - Módulo de Proteção Atmosférica ---")
    diadema_cli_path = os.path.join(os.path.dirname(__file__), 'diadema', 'diadema_cli.py')

    if not os.path.exists(diadema_cli_path):
        print(f"Erro: O script diadema_cli.py não foi encontrado em '{diadema_cli_path}'.")
        return

    try:
        command_list = [
            sys.executable, diadema_cli_path, 'protecao-atmosferica',
            '--energia-incidente', str(args.energia_incidente),
            '--intensidade-inicial', str(args.intensidade_inicial),
            '--espessura-material', str(args.espessura_material),
            '--densidade-hidrogenio', str(args.densidade_hidrogenio),
            '--coeficiente-atenuacao-linear', str(args.coeficiente_atenuacao_linear),
            '--dose-fator-conversao', str(args.dose_fator_conversao)
        ]
        
        process = subprocess.run(
            command_list,
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        diadema_output = process.stdout.strip()
        
        print("\n--- Resultados do Diadema (Proteção Atmosférica) ---")
        print(diadema_output)

        llm_prompt = (
            f"Analise os resultados do módulo de Proteção Atmosférica do Diadema para os inputs: "
            f"Energia Incidente={args.energia_incidente} MeV/GeV, Espessura={args.espessura_material} cm, "
            f"Densidade Hidrogênio={args.densidade_hidrogenio} kg/m^3, Coeficiente Atenuação={args.coeficiente_atenuacao_linear}. "
            f"Resultados: {diadema_output}. "
            "Interprete a eficácia do escudo de hidrogênio e suas implicações para a segurança da tripulação "
            "e equipamentos contra radiação em ambientes de Lua/Marte."
        )
        llm_output = gemini_llm_interact(llm_prompt)
        print("\n--- Análise da LLM Gemini ---")
        print(llm_output)

    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o script diadema_cli.py (Proteção Atmosférica): {e}")
        print(f"Stderr: {e.stderr}")
    except FileNotFoundError:
        print(f"Erro: O interpretador Python '{sys.executable}' não foi encontrado ou o script '{diadema_cli_path}' não existe.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado durante o cálculo de Proteção Atmosférica: {e}")
    print("\n--- Fim do Módulo de Proteção Atmosférica ---")


def run_diadema_rendimento_isru(args):
    """
    Função wrapper para o módulo de Rendimento de Recursos (ISRU) do Diadema.
    """
    print("\n--- CLI: Diadema - Módulo de Rendimento de Recursos (ISRU) ---")
    diadema_cli_path = os.path.join(os.path.dirname(__file__), 'diadema', 'diadema_cli.py')

    if not os.path.exists(diadema_cli_path):
        print(f"Erro: O script diadema_cli.py não foi encontrado em '{diadema_cli_path}'.")
        return

    try:
        command_list = [
            sys.executable, diadema_cli_path, 'rendimento-isru',
            '--composicao-oxidos-feo', str(args.composicao_oxidos_feo),
            '--composicao-oxidos-tio2', str(args.composicao_oxidos_tio2),
            '--eficiencia-conversao', str(args.eficiencia_conversao),
            '--taxa-processamento', str(args.taxa_processamento),
            '--energia-especifica', str(args.energia_especifica),
            '--pureza-o2', str(args.pureza_o2)
        ]
        
        process = subprocess.run(
            command_list,
            capture_output=True,
            text=True,
            check=True,
            encoding='utf-8'
        )
        diadema_output = process.stdout.strip()
        
        print("\n--- Resultados do Diadema (Rendimento ISRU) ---")
        print(diadema_output)

        llm_prompt = (
            f"Analise os resultados do módulo de Rendimento de Recursos (ISRU) do Diadema para os inputs: "
            f"Composição FeO={args.composicao_oxidos_feo}%, Composição TiO2={args.composicao_oxidos_tio2}%, "
            f"Eficiência Conversão={args.eficiencia_conversao}%, Taxa Processamento={args.taxa_processamento} kg/h, "
            f"Energia Específica={args.energia_especifica} kWh/kg O2, Pureza O2={args.pureza_o2}%. "
            f"Resultados: {diadema_output}. "
            "Interprete a viabilidade da produção de Oxigênio a partir do regolito/atmosfera e suas implicações para "
            "a autossuficiência e sustentabilidade de missões em Lua/Marte."
        )
        llm_output = gemini_llm_interact(llm_prompt)
        print("\n--- Análise da LLM Gemini ---")
        print(llm_output)

    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o script diadema_cli.py (Rendimento ISRU): {e}")
        print(f"Stderr: {e.stderr}")
    except FileNotFoundError:
        print(f"Erro: O interpretador Python '{sys.executable}' não foi encontrado ou o script '{diadema_cli_path}' não existe.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado durante o cálculo de Rendimento ISRU: {e}")
    print("\n--- Fim do Módulo de Rendimento de Recursos (ISRU) ---")

def main():
    parser = argparse.ArgumentParser(
        description="CLI para o Projeto Quantum Trajectory Simulation da NASA (NNH25ZDA001N-FAIMM)",
        epilog="""
        Mestre Seiya, Aoi está online e pronto para servir. Miau!
        Este CLI integra módulos avançados de simulação quântica,
        engenharia espacial e inteligência cósmica para suas missões.
        """
    )

    # Subparsers para os diferentes comandos
    subparsers = parser.add_subparsers(dest="command", help="Comandos disponíveis")

    # Comando: simulate-quantum
    parser_sq = subparsers.add_parser(
        "simulate-quantum",
        help="Executa simulações e análises de trajetórias quânticas."
    )
    parser_sq.add_argument(
        "--circuit-path",
        type=str,
        help="Caminho para o arquivo do circuito quântico Cirq (e.g., my_circuit.py)."
    )
    parser_sq.add_argument(
        "--repetitions",
        type=int,
        default=1000,
        help="Número de repetições para a simulação quântica."
    )
    parser_sq.set_defaults(func=simulate_quantum_command)

    # Comando: design-spacecraft
    parser_ds = subparsers.add_parser(
        "design-spacecraft",
        help="Gera e avalia designs de espaçonaves baseados em LLM."
    )
    parser_ds.add_argument(
        "--theme",
        type=str,
        required=True,
        help="Tema ou conceito para o design da espaçonave (e.g., 'sonda de exploração de Marte', 'nave de carga lunar')."
    )
    parser_ds.add_argument(
        "--distance-target",
        type=float,
        default=384400000.0, # Distância Terra-Lua padrão
        help="Distância do destino em metros para a simulação (padrão: 384.400.000m para Lua)."
    )
    parser_ds.set_defaults(func=design_spacecraft_command)

    # Comando: ditritium-sim
    parser_dt = subparsers.add_parser(
        "ditritium-sim",
        help="Executa simulações do ecossistema Ditritium."
    )
    parser_dt.add_argument(
        "--commands",
        type=str,
        required=True,
        help="Comandos ASCII para o simulador Ditritium (e.g., 'INIT;RUN;REPORT')."
    )
    parser_dt.set_defaults(func=ditritium_sim_command)

    # Comando: cosmic-insight
    parser_ci = subparsers.add_parser(
        "cosmic-insight",
        help="Acessa computações IBM Quantum e demodula mensagens cósmicas."
    )
    parser_ci.add_argument(
        "--theta",
        type=float,
        required=True,
        help="Valor de Theta para o circuito quântico (e.g., 0.5, 1.0, 3.14)."
    )
    parser_ci.add_argument(
        "--binary-signal",
        type=str,
        required=True,
        choices=['00', '01', '10', '11'],
        help="Sinal binário de 2 bits para o circuito quântico (e.g., '01')."
    )
    parser_ci.set_defaults(func=cosmic_insight_command)

    # Comando: psychography
    parser_psy = subparsers.add_parser(
        "psychography",
        help="Gera cartas psicográficas."
    )
    parser_psy.add_argument(
        "--topic",
        type=str,
        required=True,
        help="Tópico ou pessoa para a carta psicográfica."
    )
    parser_psy.add_argument( # Novo argumento para o remetente
        "--sender",
        type=str,
        default="Emmanuel", # Entidade padrão
        help="Nome da entidade espiritual a ser canalizada (e.g., 'Emmanuel', 'André Luiz')."
    )
    parser_psy.set_defaults(func=psychography_command)

    # Comando: bio-space-analysis
    parser_bs = subparsers.add_parser(
        "bio-space-analysis",
        help="Analisa estabilidade de vacinas e logística médica em Lua/Marte."
    )
    parser_bs.add_argument(
        "--disease",
        type=str,
        required=True,
        help="Nome da doença para análise bio-espacial."
    )
    parser_bs.add_argument(
        "--target-body",
        type=str,
        required=True,
        choices=['Moon', 'Mars'],
        help="Corpo celeste de destino para a simulação (Moon ou Mars)."
    )
    parser_bs.set_defaults(func=bio_space_analysis_command)

    # Comando: galactic-economy
    parser_ge = subparsers.add_parser(
        "galactic-economy",
        help="Consulta o status da economia galáctica e ativos Web3."
    )
    parser_ge.set_defaults(func=galactic_economy_command)

    # NOVO COMANDO PRINCIPAL: diadema-matrix-calc
    parser_diadema = subparsers.add_parser(
        "diadema-matrix-calc",
        help="Realiza cálculos matriciais de elementos da tabela periódica via Diadema CLI."
    )
    diadema_subparsers = parser_diadema.add_subparsers(dest="diadema_module", required=True, help="Módulos de cálculo do Diadema")

    # Subcomando: engenharia-ligas
    parser_ligas = diadema_subparsers.add_parser(
        "engenharia-ligas",
        help="Calcula a tenacidade de ligas sob condições térmicas extremas."
    )
    parser_ligas.add_argument("--temperatura-operacional", type=str, required=True, help="Vetor de temperaturas em Kelvin (JSON array, ex: '[123, 393]').")
    parser_ligas.add_argument("--limite-escoamento", type=float, required=True, help="Tensão máxima antes da deformação plástica (MPa).")
    parser_ligas.add_argument("--limite-resistencia-tracao", type=float, required=True, help="Tensão máxima suportada antes da ruptura (MPa).")
    parser_ligas.add_argument("--modulo-young", type=float, required=True, help="Rigidez do material em GPa.")
    parser_ligas.add_argument("--coeficiente-dilatacao-termica", type=float, required=True, help="Expansão linear por grau de variação (10^-6/K).")
    parser_ligas.add_argument("--dureza-vickers", type=float, required=True, help="Resistência à penetração superficial (HV).")
    parser_ligas.set_defaults(func=run_diadema_engenharia_ligas) # New wrapper function

    # Subcomando: protecao-atmosferica
    parser_escudo = diadema_subparsers.add_parser(
        "protecao-atmosferica",
        help="Simula atenuação de radiação por blindagem de hidrogênio."
    )
    parser_escudo.add_argument("--energia-incidente", type=float, required=True, help="Energia das partículas (MeV/GeV).")
    parser_escudo.add_argument("--intensidade-inicial", type=float, default=1.0, help="Intensidade inicial da radiação (I0). Padrão: 1.0.")
    parser_escudo.add_argument("--espessura-material", type=float, required=True, help="Profundidade da blindagem em cm.")
    parser_escudo.add_argument("--densidade-hidrogenio", type=float, required=True, help="Porcentagem de massa de H no polímero ou compósito em kg/m^3.")
    parser_escudo.add_argument("--coeficiente-atenuacao-linear", type=float, required=True, help="Probabilidade de interação por unidade de distância (mu, cm^-1).")
    parser_escudo.add_argument("--dose-fator-conversao", type=float, default=0.5, help="Fator de conversão para Dose de Radiação Equivalente (ex: 0.5).")
    parser_escudo.set_defaults(func=run_diadema_protecao_atmosferica) # New wrapper function

    # Subcomando: rendimento-isru
    parser_isru = diadema_subparsers.add_parser(
        "rendimento-isru",
        help="Calcula o rendimento da extração de Oxigênio do regolito ou atmosfera."
    )
    parser_isru.add_argument("--composicao-oxidos-feo", type=float, default=0.0, help="Porcentagem de FeO no regolito.")
    parser_isru.add_argument("--composicao-oxidos-tio2", type=float, default=0.0, help="Porcentagem de TiO2 no regolito.")
    parser_isru.add_argument("--eficiencia-conversao", type=float, required=True, help="Porcentagem de oxigênio extraído vs. disponível (0-100).")
    parser_isru.add_argument("--taxa-processamento", type=float, required=True, help="Massa de regolito processada por hora (kg/h).")
    parser_isru.add_argument("--energia-especifica", type=float, required=True, help="Energia necessária para extrair 1 kg de O2 (kWh/kg).")
    parser_isru.add_argument("--pureza-o2", type=float, default=99.5, help="Grau de pureza do O2 produzido (0-100).")
    parser_isru.set_defaults(func=run_diadema_rendimento_isru) # New wrapper function

    # --- Interactive Mode Logic ---
    if len(sys.argv) == 1: # No arguments provided, enter interactive mode
        WELCOME_MESSAGE = """
  _   _    _    ____ _  __   ____ _____ ____      _  __  ____ _____ _____ ____  _____
 | \ | |  / \  / ___| |/ /  / ___|_   _|/ ___|    | |/ / |  _ \_   _|_   _/ ___|| ____|
 |  \| | / _ \| |   | ' /  | |     | | | |        | ' /  | |_) || |   | | \___ \|  _|
 | |\  |/ ___ \ |___| . \  | |___  | | | |___     | . \  |  __/ | |   | |  ___) | |___
 |_| \_/_/   \_\____|_|\_\  \____| |_|  \____|    |_|\_\ |_|    |_|   |_| |____/|_____|

        NASA Quantum Trajectory CLI - Mestre Seiya, Aoi está online e pronto para servir. Miau!
        Digite 'help' para ver os comandos disponíveis ou 'exit' para sair.
        """
        HELP_MESSAGE = """
        Comandos disponíveis:
        simulate-quantum --circuit-path <caminho_para_circuito.py> [--repetitions <numero>]
        design-spacecraft --theme "<tema>" [--distance-target <distancia_metros>]
        ditritium-sim --commands "<comandos_ascii>"
        cosmic-insight --theta <valor> --binary-signal <sinal>
        psychography --topic "<topico>" [--sender "<entidade>"]
        bio-space-analysis --disease "<doenca>" --target-body <Moon|Mars>
        galactic-economy
        diadema-matrix-calc <modulo_diadema> ... (ver 'help diadema-matrix-calc' para detalhes)
        
        help - Exibe esta mensagem.
        exit - Sai do CLI.
        """
        
        print(WELCOME_MESSAGE)

        while True:
            try:
                command_line = input("NASA_CLI> ").strip()
                if not command_line:
                    continue
                if command_line.lower() == "exit":
                    print("Saindo do NASA Quantum Trajectory CLI. Até logo, Mestre Seiya!")
                    break
                if command_line.lower() == "help":
                    print(HELP_MESSAGE)
                    continue

                # Parse the command line input as if it were sys.argv
                # Add a dummy program name at the beginning for argparse
                args_list = ["nasa_quantum_trajectory_cli"] + command_line.split()
                
                # Temporarily redirect stdout/stderr for argparse to prevent it from exiting
                # when an error occurs, or printing help.
                old_stdout = sys.stdout
                old_stderr = sys.stderr
                sys.stdout = open(os.devnull, 'w')
                sys.stderr = open(os.devnull, 'w')
                
                try:
                    # Parse known arguments, allowing for unknown arguments to be handled later if necessary
                    # For now, we assume all arguments are known
                    args = parser.parse_args(args_list[1:])
                    
                    # Restore stdout/stderr before printing results
                    sys.stdout.close()
                    sys.stderr.close()
                    sys.stdout = old_stdout
                    sys.stderr = old_stderr

                    if hasattr(args, "func"):
                        args.func(args)
                    else:
                        print(f"Erro: Comando '{args.command}' não reconhecido ou parâmetros inválidos.")
                        print(f"Para ajuda com o comando '{args.command}', tente: {args_list[0]} {args.command} --help")
                except SystemExit: # argparse raises SystemExit on error or --help
                    # This means argparse either printed help or an error message.
                    # We need to capture and print the help/error from stderr/stdout.
                    sys.stdout.close()
                    sys.stderr.close()
                    sys.stdout = old_stdout
                    sys.stderr = old_stderr
                    # Re-parse with direct stdout/stderr to capture the output correctly
                    try:
                        parser.parse_args(args_list[1:])
                    except SystemExit as e:
                        if e.code != 0: # If it's an actual error, print a generic message
                            print("Erro de comando. Use 'help' para comandos ou '--help' para um comando específico.")
                except Exception as e:
                    sys.stdout.close()
                    sys.stderr.close()
                    sys.stdout = old_stdout
                    sys.stderr = old_stderr
                    print(f"Erro interno: {e}")
            except EOFError:
                print("Saindo do NASA Quantum Trajectory CLI. Até logo, Mestre Seiya!")
                break
            except Exception as e:
                print(f"Ocorreu um erro inesperado: {e}")
    else: # Run as a standard command-line application
        args = parser.parse_args()
        if hasattr(args, "func"):
            args.func(args)
        else:
            parser.print_help()

if __name__ == "__main__":
    main()