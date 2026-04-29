import os
from dataclasses import dataclass
from pathlib import Path
import urllib.request
import urllib.parse
import urllib.error

DEFAULT_WALLET_PATH = Path.home() / ".multiversx" / "wallet.pem"

FAUCET_URLS = {
    "devnet": "https://devnet-wallet.multiversx.com/faucet",
    "testnet": "https://testnet-wallet.multiversx.com/faucet",
}

EXPLORER_URLS = {
    "devnet": "https://devnet-explorer.multiversx.com",
    "testnet": "https://testnet-explorer.multiversx.com",
}

FAUCET_API_URL = "https://r3d4.fr/faucet"


@dataclass
class FaucetResult:
    success: bool
    message: str


def request_faucet(address: str, network: str = "devnet") -> FaucetResult:
    """Request testnet/devnet EGLD from the faucet API."""
    data = urllib.parse.urlencode({"address": address, "token": network}).encode()
    req = urllib.request.Request(FAUCET_API_URL, data=data, method="POST")
    req.add_header("Content-Type", "application/x-www-form-urlencoded")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode().strip()
            return FaucetResult(success=True, message=body)
    except urllib.error.HTTPError as e:
        body = e.read().decode().strip()
        return FaucetResult(success=False, message=body or str(e))
    except Exception as e:
        return FaucetResult(success=False, message=str(e))


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

    output.parent.mkdir(parents=True, exist_ok=True)

    # Securely create the file with restricted permissions (0o600)
    # and atomize the existence check.
    try:
        fd = os.open(output, os.O_CREAT | os.O_WRONLY | os.O_EXCL, 0o600)
        os.close(fd)
    except FileExistsError:
        raise FileExistsError(f"Wallet already exists at {output}. Will not overwrite.")

    mnemonic = Mnemonic.generate()
    account = Account(mnemonic.derive_key(0))
    account.save_to_pem(output)
    output.chmod(0o400)

    return WalletInfo(
        address=account.address.to_bech32(),
        mnemonic=mnemonic.get_text(),
        pem_path=output,
    )
