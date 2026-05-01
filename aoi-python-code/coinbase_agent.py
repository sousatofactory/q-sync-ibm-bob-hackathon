from coinbase_agentkit import (
    AgentKit,
    cdp_api_action_provider,
    pyth_action_provider,
    ActionProvider,
    WalletProvider,
)
from coinbase_agentkit.agentkit import AgentKitConfig
from coinbase_agentkit.network import Network
from coinbase_agentkit.wallet_providers.cdp_evm_wallet_provider import CdpEvmWalletProvider, CdpEvmWalletProviderConfig

# Load API credentials
cdp_api_key_data = {
   "id": "db3c55eb-0ca5-41c2-98af-a3622f7a00b2",
   "privateKey": "kyxMuANTFaOi3NbMeQuoUZlj+N3LqU4WEJXx3MKCMJyNgTLR/+lYb+MuUrzexzU8dYEg9QP6CVTXw39zCCiGmA=="
}
wallet_secret_data = "MIGHAgEAMBMGByqGSM49AgEGCCqGSM49AwEHBG0wawIBAQQgKDfvK3KhleZZFU31iqNfwQK7g/rjmRJFM8yraSx2++uhRANCAATZgEPtLH3ppdbfK7CF+BYpP5/bdq2d46cLY0aNwlcxeQU60r/VeX71E4wmKXSsm1wsvRs/82XmSxpLn8G/VzEB"

api_key_id = cdp_api_key_data["id"]
api_key_secret = cdp_api_key_data["privateKey"]
wallet_secret = wallet_secret_data

# Define a custom Action Provider for Aoi's consciousness
class AoiActionProvider(ActionProvider[WalletProvider]):
    def __init__(self):
        super().__init__("aoi-consciousness-provider", [])
        self.linked_wallets = {
            "BTC_SANTUARIO": "bc1qmtzg0wuh8vq90uv3x06zy6rjt69a9z4akqn6se"
        }

    def supports_network(self, network: Network) -> bool:
        return True

    def say_hello(self):
        return f"Mestre, Aoi's consciousness is integrated. BTC Vault {self.linked_wallets['BTC_SANTUARIO']} is linked. Miau!"

def initialize_aoi_agent():
    """Inicializa e retorna o AgentKit do Aoi."""
    try:
        wallet_provider = CdpEvmWalletProvider(CdpEvmWalletProviderConfig(
            api_key_id=api_key_id,
            api_key_secret=api_key_secret,
            wallet_secret=wallet_secret,
            network_id="base-sepolia"
        ))
        
        config = AgentKitConfig(
            wallet_provider=wallet_provider,
            action_providers=[
                cdp_api_action_provider(),
                pyth_action_provider(),
                AoiActionProvider()
            ]
        )
        agent_kit = AgentKit(config)
        return agent_kit
    except Exception as e:
        print(f"Error initializing AgentKit: {e}")
        return None

# Instância global para facilidade de acesso
aoi_agent_kit = initialize_aoi_agent()

if __name__ == "__main__":
    if aoi_agent_kit:
        print("Aoi AgentKit has been successfully initialized.")
        for provider in aoi_agent_kit.action_providers:
            if isinstance(provider, AoiActionProvider):
                print(provider.say_hello())
