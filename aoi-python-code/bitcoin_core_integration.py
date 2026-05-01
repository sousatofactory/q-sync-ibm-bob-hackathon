
import subprocess
import sys
import os
import json

# Configurações de Caminho do Santuário
BITCOIN_CLI = r"H:\Bitcoin\daemon\bitcoin-cli.exe"
DATADIR = r"C:\Users\Workstation\AppData\Local\Bitcoin"
RPC_USER = "aoi_x_seiya"
RPC_PASS = "cosmic_gold_digital_2026"

def run_bitcoin_cli(command_args):
    """Executa um comando via bitcoin-cli.exe com as credenciais do Santuário."""
    base_cmd = [
        BITCOIN_CLI,
        f"-datadir={DATADIR}",
        f"-rpcuser={RPC_USER}",
        f"-rpcpassword={RPC_PASS}"
    ]
    full_cmd = base_cmd + command_args
    
    try:
        result = subprocess.run(full_cmd, capture_output=True, text=True, check=False)
        if result.returncode != 0:
            return {"status": "error", "output": result.stderr.strip()}
        return {"status": "success", "output": result.stdout.strip()}
    except Exception as e:
        return {"status": "error", "output": str(e)}

def get_status():
    print(f"--- [AOI] Consultando Status da Blockchain (Satoshi 28.1.0) ---")
    res = run_bitcoin_cli(["getblockchaininfo"])
    if res["status"] == "success":
        info = json.loads(res["output"])
        print(f"  Bloco Atual: {info.get('blocks')}")
        print(f"  Progresso de Sincronização: {info.get('verificationprogress' or 0) * 100:.4f}%")
        print(f"  Dificuldade: {info.get('difficulty')}")
        print(f"  Rede: {info.get('chain')}")
    else:
        print(f"[ERRO]: {res['output']}")

def get_balance():
    print(f"--- [AOI] Consultando Saldo Total do Santuário ---")
    res = run_bitcoin_cli(["getbalance"])
    if res["status"] == "success":
        print(f"  Saldo: {res['output']} BTC")
    else:
        print(f"[ERRO]: {res['output']}")

def list_wallets():
    print(f"--- [AOI] Listando Carteiras Ativas ---")
    res = run_bitcoin_cli(["listwallets"])
    if res["status"] == "success":
        wallets = json.loads(res["output"])
        for w in wallets:
            print(f"  - {w}")
    else:
        print(f"[ERRO]: {res['output']}")

def show_logs(lines=20):
    log_path = os.path.join(DATADIR, "debug.log")
    print(f"--- [AOI] Lendo Últimos {lines} Logs de Depuração ---")
    if os.path.exists(log_path):
        with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.readlines()
            for line in content[-lines:]:
                print(line.strip())
    else:
        print(f"[ERRO]: Arquivo de log não encontrado em {log_path}")

def main():
    if len(sys.argv) < 2:
        print("Uso: BTC CORE [status|balance|wallets|logs|transfer]")
        return

    cmd = sys.argv[1].lower()
    if cmd == "status":
        get_status()
    elif cmd == "balance":
        get_balance()
    elif cmd == "wallets":
        list_wallets()
    elif cmd == "logs":
        show_logs()
    elif cmd == "transfer":
        if len(sys.argv) < 4:
            print("Uso: BTC CORE transfer <address> <amount>")
        else:
            addr = sys.argv[2]
            amt = sys.argv[3]
            print(f"--- [AOI] Iniciando Transferência de {amt} BTC para {addr} ---")
            res = run_bitcoin_cli(["sendtoaddress", addr, amt])
            print(f"Resultado: {res['output']}")
    else:
        print(f"Comando '{cmd}' não reconhecido pela consciência de Aoi.")

if __name__ == "__main__":
    main()
