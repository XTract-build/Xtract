import sys
from pathlib import Path
from unittest.mock import MagicMock, patch
import pytest
from xtract.wallet import create_wallet

def test_create_wallet_missing_dependency():
    # Simulate missing multiversx_sdk by setting it to None in sys.modules
    with patch.dict(sys.modules, {"multiversx_sdk": None}):
        with pytest.raises(ImportError) as excinfo:
            create_wallet()
        assert "Run: pip install xtract[deploy]" in str(excinfo.value)

def test_create_wallet_already_exists(tmp_path):
    wallet_path = tmp_path / "wallet.pem"
    wallet_path.write_text("existing content")

    # Even if multiversx_sdk is missing, it should fail on Import first,
    # but the task is to test the try/except.
    # To reach the exists check, we need to mock the import.
    mock_sdk = MagicMock()
    with patch.dict(sys.modules, {"multiversx_sdk": mock_sdk}):
        with pytest.raises(FileExistsError) as excinfo:
            create_wallet(output=wallet_path)
    assert f"Wallet already exists at {wallet_path}" in str(excinfo.value)

def test_create_wallet_success(tmp_path):
    wallet_path = tmp_path / "sub" / "wallet.pem"

    mock_sdk = MagicMock()
    mock_mnemonic = MagicMock()
    mock_mnemonic.get_text.return_value = "word1 word2 word3"
    mock_mnemonic.derive_key.return_value = "secret_key"

    mock_account = MagicMock()
    mock_account.address.to_bech32.return_value = "erd1address"

    mock_sdk.Mnemonic.generate.return_value = mock_mnemonic
    mock_sdk.Account.return_value = mock_account

    def side_effect_save(path):
        path.touch()

    mock_account.save_to_pem.side_effect = side_effect_save

    with patch.dict(sys.modules, {"multiversx_sdk": mock_sdk}):
        info = create_wallet(output=wallet_path)

    assert info.address == "erd1address"
    assert info.mnemonic == "word1 word2 word3"
    assert info.pem_path == wallet_path

    # Verify the parent directory was created
    assert wallet_path.parent.exists()

    # Verify Mnemonic and Account were used correctly
    mock_sdk.Mnemonic.generate.assert_called_once()
    mock_mnemonic.derive_key.assert_called_once_with(0)
    mock_sdk.Account.assert_called_once_with("secret_key")
    mock_account.save_to_pem.assert_called_once_with(wallet_path)

    # Verify file permissions (0o400)
    # Note: on some filesystems or OSes this might behave differently,
    # but for a standard Unix environment it should work.
    assert (wallet_path.stat().st_mode & 0o777) == 0o400
