import sys
from unittest.mock import MagicMock, patch
import pytest
from pathlib import Path
from xtract.wallet import create_wallet

def test_create_wallet_import_error():
    # Force ImportError for multiversx_sdk
    with patch.dict("sys.modules", {"multiversx_sdk": None}):
        with pytest.raises(ImportError) as excinfo:
            create_wallet(Path("some/path"))
        assert "Run: pip install xtract[deploy]" in str(excinfo.value)

def test_create_wallet_file_exists(tmp_path):
    output = tmp_path / "wallet.pem"
    output.write_text("existing content")

    # Mock multiversx_sdk so it doesn't fail on import
    mock_sdk = MagicMock()
    with patch.dict("sys.modules", {"multiversx_sdk": mock_sdk}):
        with pytest.raises(FileExistsError) as excinfo:
            create_wallet(output)
        assert f"Wallet already exists at {output}" in str(excinfo.value)

def test_create_wallet_success(tmp_path):
    # Use a sub-directory to test directory creation
    output = tmp_path / "subdir" / "new_wallet.pem"

    mock_sdk = MagicMock()
    mock_mnemonic = MagicMock()
    mock_mnemonic.get_text.return_value = "mock mnemonic"
    mock_sdk.Mnemonic.generate.return_value = mock_mnemonic

    mock_account = MagicMock()
    mock_account.address.to_bech32.return_value = "erd1mockaddress"
    mock_sdk.Account.return_value = mock_account

    # Simulate Account.save_to_pem creating the file
    def fake_save_to_pem(path):
        Path(path).touch()

    mock_account.save_to_pem.side_effect = fake_save_to_pem

    with patch.dict("sys.modules", {"multiversx_sdk": mock_sdk}):
        info = create_wallet(output)

    assert info.address == "erd1mockaddress"
    assert info.mnemonic == "mock mnemonic"
    assert info.pem_path == output

    assert output.exists()
    # Check permissions (0o400)
    assert (output.stat().st_mode & 0o777) == 0o400

    mock_sdk.Mnemonic.generate.assert_called_once()
    mock_mnemonic.derive_key.assert_called_once_with(0)
    mock_sdk.Account.assert_called_once_with(mock_mnemonic.derive_key.return_value)
    mock_account.save_to_pem.assert_called_once_with(output)
