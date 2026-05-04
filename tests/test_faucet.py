"""Tests for the faucet command."""

import io
import urllib.error
from unittest.mock import patch, MagicMock

from xtract.wallet import request_faucet, FAUCET_API_URL


def _make_response(body: str, status: int = 200):
    resp = MagicMock()
    resp.read.return_value = body.encode()
    resp.__enter__ = lambda s: s
    resp.__exit__ = MagicMock(return_value=False)
    return resp


# ---------------------------------------------------------------------------
# request_faucet unit tests
# ---------------------------------------------------------------------------

class TestRequestFaucet:
    def test_devnet_sends_correct_url_and_body(self):
        address = "erd1qqqqqqqqqqqqqpgqtest000000000000000000000000000000000"
        captured = {}

        def fake_urlopen(req, timeout=None):
            captured["url"] = req.full_url
            captured["data"] = req.data
            captured["method"] = req.method
            return _make_response("OK")

        with patch("xtract.wallet.urllib.request.urlopen", side_effect=fake_urlopen):
            result = request_faucet(address, "devnet")

        assert captured["url"] == FAUCET_API_URL
        assert b"address=" + address.encode() in captured["data"]
        assert b"token=devnet" in captured["data"]
        assert captured["method"] == "POST"
        assert result.success is True

    def test_testnet_sends_token_testnet(self):
        address = "erd1qqqqqqqqqqqqqpgqtest000000000000000000000000000000000"
        captured = {}

        def fake_urlopen(req, timeout=None):
            captured["data"] = req.data
            return _make_response("OK")

        with patch("xtract.wallet.urllib.request.urlopen", side_effect=fake_urlopen):
            result = request_faucet(address, "testnet")

        assert b"token=testnet" in captured["data"]
        assert result.success is True

    def test_http_error_returns_failure(self):
        address = "erd1qqqqqqqqqqqqqpgqtest000000000000000000000000000000000"

        http_err = urllib.error.HTTPError(
            url=FAUCET_API_URL,
            code=429,
            msg="Too Many Requests",
            hdrs=None,
            fp=io.BytesIO(b"Rate limited"),
        )

        with patch("xtract.wallet.urllib.request.urlopen", side_effect=http_err):
            result = request_faucet(address, "devnet")

        assert result.success is False
        assert "Rate limited" in result.message

    def test_network_error_returns_failure(self):
        address = "erd1qqqqqqqqqqqqqpgqtest000000000000000000000000000000000"

        with patch("xtract.wallet.urllib.request.urlopen", side_effect=OSError("connection refused")):
            result = request_faucet(address, "devnet")

        assert result.success is False
        assert "connection refused" in result.message
