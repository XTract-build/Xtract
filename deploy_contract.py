#!/usr/bin/env python3
"""Deploy SimpleStorage contract to MultiversX devnet"""

from pathlib import Path
from multiversx_sdk_core import Address
from multiversx_sdk_network_providers import DevnetNetworkProvider
from multiversx_sdk_wallet import UserWallet
from multiversx_sdk_core.transaction_builders import ContractDeploymentBuilder, TransactionBuilder
from multiversx_sdk_core.codec import encode_string
from multiversx_sdk_core import TransactionComputer

# Configuration
WASM_FILE = Path("demo/simple_storage/output/simple_storage.wasm")
GAS_LIMIT = 50_000_000
PROXY_URL = "https://devnet-gateway.multiversx.com"
NETWORK = "devnet"

def main():
    # Check if WASM file exists
    if not WASM_FILE.exists():
        print(f"Error: WASM file not found at {WASM_FILE}")
        return
    
    # Load bytecode
    bytecode = WASM_FILE.read_bytes()
    print(f"Loaded bytecode: {len(bytecode)} bytes")
    
    # Get wallet address from MCP (we'll need to get PEM somehow)
    # For now, let's try to find the wallet or use the address
    wallet_address_bech32 = "erd1wgkeuxhpstdum8w5kmfeepdn0f2t3d6vl34e4l7fjnpclzyegyts40g6fw"
    print(f"Wallet address: {wallet_address_bech32}")
    
    # Create network provider
    provider = DevnetNetworkProvider(PROXY_URL)
    
    # Get account info
    wallet_address = Address.from_bech32(wallet_address_bech32)
    account = provider.get_account(wallet_address)
    print(f"Account nonce: {account.nonce}")
    print(f"Account balance: {account.balance}")
    
    # Build deployment transaction
    builder = ContractDeploymentBuilder(
        config=provider.get_network_config(),
        deployer=wallet_address,
        deploy_arguments=[],  # SimpleStorage has no init arguments
        code=bytecode,
        gas_limit=GAS_LIMIT
    )
    
    transaction = builder.build()
    transaction.nonce = account.nonce
    
    print(f"Transaction created:")
    print(f"  Nonce: {transaction.nonce}")
    print(f"  Gas limit: {transaction.gas_limit}")
    print(f"  Chain ID: {transaction.chain_id}")
    
    # Note: Transaction needs to be signed with wallet PEM
    # Since we don't have direct access to the PEM file from MCP,
    # we need to either:
    # 1. Find the PEM file location
    # 2. Use mxpy if available
    # 3. Have user provide PEM path
    
    print("\nNote: Transaction needs to be signed. Please provide PEM file path.")
    print("Or install mxpy and use: mxpy contract deploy")
    print(f"  --bytecode {WASM_FILE.absolute()}")
    print(f"  --proxy={PROXY_URL}")
    print(f"  --gas-limit {GAS_LIMIT}")
    print(f"  --pem=<path_to_pem>")
    print(f"  --send")

if __name__ == "__main__":
    main()
