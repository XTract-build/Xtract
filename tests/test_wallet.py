import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
import pytest

# Mock multiversx_sdk before importing create_wallet if possible,
# but create_wallet does a local import.
# So we need to mock it in sys.modules

mock_sdk = MagicMock()
sys.modules["multiversx_sdk"] = mock_sdk

from xtract.wallet import create_wallet

def test_create_wallet_permissions_race_condition(capsys):
    """
    Test that the wallet file has restricted permissions BEFORE save_to_pem is called.
    In the vulnerable version, it's created with default permissions and then chmoded.
    """
    mock_mnemonic_class = mock_sdk.Mnemonic
    mock_account_class = mock_sdk.Account

    mock_mnemonic = mock_mnemonic_class.generate.return_value
    mock_mnemonic.derive_key.return_value = b"fake_key"
    mock_mnemonic.get_text.return_value = "fake mnemonic"

    mock_account = mock_account_class.return_value
    mock_account.address.to_bech32.return_value = "erd1..."

    test_wallet_path = Path("test_wallet_race.pem")
    if test_wallet_path.exists():
        test_wallet_path.unlink()

    # We want to check permissions DURING save_to_pem call
    def side_effect_save_to_pem(path):
        if os.path.exists(path):
            perms = oct(os.stat(path).st_mode & 0o777)
            print(f"DEBUG: Permissions during save_to_pem: {perms}")
        else:
            print("DEBUG: File does NOT exist during save_to_pem")

    mock_account.save_to_pem.side_effect = side_effect_save_to_pem

    try:
        create_wallet(test_wallet_path)

        captured = capsys.readouterr()
        # In vulnerable version, it will print "File does NOT exist during save_to_pem"
        # because it only calls save_to_pem which creates it (and it doesn't exist yet).
        # We want it to exist with 0o600.
        assert "Permissions during save_to_pem: 0o600" in captured.out or "Permissions during save_to_pem: 0o400" in captured.out

        # The final permissions should be 0o400
        assert oct(test_wallet_path.stat().st_mode & 0o777) == "0o400"
    finally:
        if test_wallet_path.exists():
            test_wallet_path.unlink()
