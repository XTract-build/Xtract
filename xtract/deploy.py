from dataclasses import dataclass
from pathlib import Path

EXPLORER_URLS = {
    "devnet": "https://devnet-explorer.multiversx.com",
    "testnet": "https://testnet-explorer.multiversx.com",
    "mainnet": "https://explorer.multiversx.com",
}


@dataclass
class DeployResult:
    contract_address: str
    tx_hash: str
    explorer_url: str


def deploy_contract(
    wasm_path: Path,
    abi_path: Path,
    wallet_path: Path,
    network: str = "devnet",
    gas_limit: int = 10_000_000,
    upgradeable: bool = True,
) -> DeployResult:
    """Deploy a compiled WASM contract to MultiversX.

    Requires: pip install xtract[deploy]
    """
    try:
        from multiversx_sdk import DevnetEntrypoint, TestnetEntrypoint, MainnetEntrypoint, Account
        from multiversx_sdk.abi import Abi
    except ImportError:
        raise ImportError("Run: pip install xtract[deploy]")

    entrypoint_cls = {
        "devnet": DevnetEntrypoint,
        "testnet": TestnetEntrypoint,
        "mainnet": MainnetEntrypoint,
    }[network]

    entrypoint = entrypoint_cls()
    account = Account.new_from_pem(wallet_path)
    account.nonce = entrypoint.recall_account_nonce(account.address)

    abi = Abi.load(abi_path)
    controller = entrypoint.create_smart_contract_controller(abi=abi)

    tx = controller.create_transaction_for_deploy(
        sender=account,
        nonce=account.get_nonce_then_increment(),
        bytecode=wasm_path,
        gas_limit=gas_limit,
        is_upgradeable=upgradeable,
    )
    tx.signature = account.sign_transaction(tx)
    tx_hash = entrypoint.send_transaction(tx)
    outcome = controller.await_completed_deploy(tx_hash)

    contract_address = outcome.contracts[0].address.to_bech32()
    explorer_base = EXPLORER_URLS[network]

    return DeployResult(
        contract_address=contract_address,
        tx_hash=str(tx_hash),
        explorer_url=f"{explorer_base}/transactions/{tx_hash}",
    )
