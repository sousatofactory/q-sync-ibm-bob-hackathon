
import json
import argparse
import sys

def calculate_ipp(salario, idade, massa):
    """
    Calcula o Índice de Proporcionalidade Pessoal (IPP).
    Fórmula: IPP = Salário Mensal / (Idade * Massa Corpórea)
    """
    denominador = idade * massa
    if denominador == 0:
        # Retorna um valor que representa pressão "infinita" se idade ou massa for 0
        return float('inf')
    
    return salario / denominador

def calculate_ipfp(salario_bruto, custos_dict, idade, massa):
    """
    Calcula o Índice de Pressão Financeira Pessoal (IPFP).
    Fórmula: IPFP = (Salário Mensal Bruto - Σ(Custos Mensais)) / (Idade × Massa Corpórea)
    """
    # Mensaliza os impostos anuais
    custo_impostos = (custos_dict.get('iptu_anual', 0) / 12) + (custos_dict.get('ipva_anual', 0) / 12)
    
    # Soma todos os outros custos mensais
    soma_outros_custos = sum(v for k, v in custos_dict.items() if not k.endswith('_anual'))

    soma_custos_total = soma_outros_custos + custo_impostos
    
    numerador = salario_bruto - soma_custos_total
    denominador = idade * massa

    if denominador == 0:
        # Se idade ou massa for 0, a pressão não pode ser calculada de forma padrão.
        # Se a renda líquida for positiva, a pressão é efetivamente 0. Se for negativa, é infinita.
        if numerador <= 0:
            return float('-inf') # Pressão máxima (dívida)
        else:
            return float('inf') # Nenhuma pressão, recursos "infinitos"
            
    return numerador / denominador

def main():
    """
    Ponto de entrada para execução via linha de comando.
    Processa os argumentos, chama a função de cálculo apropriada e imprime o resultado em JSON.
    """
    parser = argparse.ArgumentParser(description="Calculadora de Metabolismo Urbano")
    parser.add_argument('--formula', type=str, required=True, choices=['ipp', 'ipfp'], help="A fórmula a ser calculada.")
    
    # Argumentos para os cálculos
    parser.add_argument('--salario', type=float, help="Salário mensal bruto.")
    parser.add_argument('--idade', type=int, help="Idade do indivíduo.")
    parser.add_argument('--massa', type=float, help="Massa corpórea do indivíduo em kg.")
    parser.add_argument('--custos', type=str, help="Dicionário de custos em formato de string JSON.")

    args = parser.parse_args()

    result = {}
    
    try:
        if args.formula == 'ipp':
            if not all([args.salario, args.idade, args.massa]):
                raise ValueError("Para o IPP, os argumentos --salario, --idade e --massa são obrigatórios.")
            
            value = calculate_ipp(args.salario, args.idade, args.massa)
            result = {
                "value": value,
                "concept": "O IPP é um indicador adimensional que oferece uma primeira aproximação da relação entre o capital humano de um indivíduo e seu retorno financeiro. Um IPP baixo sugere um desequilíbrio, apontando para possíveis ineficiências de mercado, discriminação ou problemas de saúde."
            }

        elif args.formula == 'ipfp':
            if not all([args.salario, args.custos, args.idade, args.massa]):
                raise ValueError("Para o IPFP, os argumentos --salario, --custos, --idade e --massa são obrigatórios.")
            
            custos_dict = json.loads(args.custos)
            value = calculate_ipfp(args.salario, custos_dict, args.idade, args.massa)
            result = {
                "value": value,
                "concept": "O IPFP aprimora o IPP ao considerar o custo de vida. Ele mede a 'sobra' ou 'aperto' financeiro real em relação ao capital humano. Valores baixos ou negativos indicam alta pressão financeira e vulnerabilidade."
            }
            
    except Exception as e:
        result = {"error": str(e)}

    # Imprime o resultado como uma string JSON para ser capturado pelo processo pai (Electron)
    print(json.dumps(result))

if __name__ == "__main__":
    main()
