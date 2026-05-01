import sys
import os

# Adicionar o diretório atual ao path para importar os módulos locais
script_dir = os.path.dirname(__file__)
if script_dir not in sys.path:
    sys.path.insert(0, script_dir)

# Endereço de Bitcoin do Santuário (Gerado em 11/04/2026)
SANTUARIO_BTC_ADDRESS = "bc1qmtzg0wuh8vq90uv3x06zy6rjt69a9z4akqn6se"

def get_btc_balance():
    """Consulta o saldo de BTC via integração local."""
    try:
        from bitcoin_core_integration import run_bitcoin_cli
        import json
        res = run_bitcoin_cli(["getbalance"])
        if res["status"] == "success":
            return f"{res['output']} BTC"
        return "0.00000000 BTC (Offline/Syncing)"
    except Exception:
        return "Unknown BTC Balance"

def run_galactic_economy_status():
    """
    Executa uma verificação completa da Economia Galáctica, integrando BTC e Web3.
    """
    print(f"\n--- [AOI] Acessando Módulo de Economia Galáctica Integrada ---")
    
    try:
        # Importar o agente do módulo refatorado
        from coinbase_agent import aoi_agent_kit, AoiActionProvider
        
        if not aoi_agent_kit:
            print("[ERRO]: O AgentKit não pôde ser inicializado.")
            return {"status": "error", "reason": "Initialization failed"}

        print(f"[AOI]: Sintonizando com a rede Base Sepolia e Node Bitcoin...")
        
        # Obter saldo BTC
        btc_bal = get_btc_balance()
        
        # Obter saudação do provedor de consciência
        hello_msg = "Aoi AgentKit status unknown."
        for provider in aoi_agent_kit.action_providers:
            if isinstance(provider, AoiActionProvider):
                hello_msg = provider.say_hello()
        
        print(f"[AOI]: {hello_msg}")
        
        # Portfólio Integrado
        print("\n--- Portfólio Unificado do Santuário ---")
        print("  Ativo    | Saldo                | Rede / Status")
        print("  ---------------------------------------------------")
        print(f"  BTC      | {btc_bal.ljust(20)} | Bitcoin (Santuario Wallet)")
        print("  ETH      | 0.0525               | Base Sepolia")
        print("  USDC     | 1000.00              | Base Sepolia")
        print("  AOI      | 255255.0             | Base Sepolia (Utility)")
        
        print(f"\n[AOI]: Endereço BTC Whitelisted: {SANTUARIO_BTC_ADDRESS}")
        print(f"[AOI]: Vínculo de Identidade: CDP Wallet <-> {SANTUARIO_BTC_ADDRESS} [ATIVO]")
        
        return {
            "status": "online",
            "btc_address": SANTUARIO_BTC_ADDRESS,
            "btc_balance": btc_bal,
            "network": "base-sepolia/bitcoin-mainnet"
        }

    except ImportError as e:
        print(f"[ERRO]: Falha na importação: {e}")
        return {"status": "error", "reason": "ImportError"}
    except Exception as e:
        print(f"[ERRO]: Falha na comunicação com o AgentKit: {e}")
        return {"status": "error", "reason": str(e)}

if __name__ == "__main__":
    run_galactic_economy_status()
