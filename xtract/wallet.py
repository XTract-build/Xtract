from dataclasses import dataclass
from pathlib import Path

DEFAULT_WALLET_PATH = Path.home() / ".multiversx" / "wallet.pem"

FAUCET_URLS = {
    "devnet": "https://devnet-wallet.multiversx.com/",
    "testnet": "https://testnet-wallet.multiversx.com/",
}


@dataclass
class WalletInfo:
    address: str
    mnemonic: str
    pem_path: Path


def create_wallet(output: Path = DEFAULT_WALLET_PATH) -> WalletInfo:
    """Generate a new wallet and save it as a PEM file.

    Requires: pip install xtract[deploy]
    """
    try:
        from multiversx_sdk import Mnemonic, Account
    except ImportError:
        raise ImportError("Run: pip install xtract[deploy]")

    if output.exists():
        raise FileExistsError(f"Wallet already exists at {output}. Will not overwrite.")

    output.parent.mkdir(parents=True, exist_ok=True)
    mnemonic = Mnemonic.generate()
    account = Account(mnemonic.derive_key(0))
    account.save_to_pem(output)
    output.chmod(0o400)

    return WalletInfo(
        address=account.address.to_bech32(),
        mnemonic=mnemonic.get_text(),
        pem_path=output,
    )
