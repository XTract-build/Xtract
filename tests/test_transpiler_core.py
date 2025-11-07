from pathlib import Path

from xtract.transpiler import Transpiler


def load(p: str) -> str:
    return Path(p).read_text()


def normalize(s: str) -> str:
    """Normalize whitespace and line endings for comparison"""
    return s.replace("\r\n", "\n").strip()


def test_simple_storage_shape():
    sol = load("test_cases/solidity/SimpleStorage.sol")
    expected = load("test_cases/expected/SimpleStorage.rs")
    actual = Transpiler().convert(sol)

    # Normalize both for comparison
    expected_normalized = normalize(expected)
    actual_normalized = normalize(actual)

    # Primary validation: compare normalized expected vs actual
    if expected_normalized != actual_normalized:
        # Provide helpful diff output
        import difflib
        diff = difflib.unified_diff(
            expected_normalized.splitlines(keepends=True),
            actual_normalized.splitlines(keepends=True),
            fromfile="expected",
            tofile="actual",
            lineterm=""
        )
        diff_str = "".join(diff)
        assert False, f"Generated output does not match expected file:\n{diff_str}"

    # Secondary validation: check key features are present (for additional confidence)
    assert "pub trait SimpleStorage" in actual
    assert "#[storage_mapper(\"value\")]" in actual
    assert "fn value(&self) -> SingleValueMapper<BigUint<Self::Api>>;" in actual
    assert "#[event(\"ValueChanged\")]" in actual
    assert "fn value_changed_event" in actual
    assert "#[view(getValue)]" in actual
    assert "fn get_value(&self) -> BigUint<Self::Api>" in actual
    assert "self.value().set(&newValue);" in actual
    assert "self.value_changed_event(&newValue);" in actual
    assert "return self.value().get();" in actual


def test_erc20_body_generation():
    # Test ERC20 require and emit statements
    sol = load("test_cases/solidity/ERC20Token.sol")
    expected = load("test_cases/expected/ERC20Token.rs")
    actual = Transpiler().convert(sol)

    # Normalize both for comparison
    expected_normalized = normalize(expected)
    actual_normalized = normalize(actual)

    # Primary validation: compare normalized expected vs actual
    if expected_normalized != actual_normalized:
        import difflib
        diff = difflib.unified_diff(
            expected_normalized.splitlines(keepends=True),
            actual_normalized.splitlines(keepends=True),
            fromfile="expected",
            tofile="actual",
            lineterm=""
        )
        diff_str = "".join(diff)
        assert False, f"Generated output does not match expected file:\n{diff_str}"

    # Secondary validation: check key features are present
    assert "#![no_std]" in actual
    assert "use multiversx_sc::imports::*;" in actual
    assert "#[multiversx_sc::contract]" in actual
    assert "pub trait ERC20Token" in actual
    assert "#[storage_mapper(\"totalSupply\")]" in actual
    assert "#[storage_mapper(\"balance\")]" in actual
    assert 'require!(self.balance().get() >= _value' in actual
    assert "self.transfer_event" in actual
    assert "return true;" in actual


def test_voting_body_generation():
    # Test Voting contract with complex statements
    sol = load("test_cases/solidity/Voting.sol")
    expected = load("test_cases/expected/Voting.rs")
    actual = Transpiler().convert(sol)

    # Normalize both for comparison
    expected_normalized = normalize(expected)
    actual_normalized = normalize(actual)

    # Primary validation: compare normalized expected vs actual
    if expected_normalized != actual_normalized:
        import difflib
        diff = difflib.unified_diff(
            expected_normalized.splitlines(keepends=True),
            actual_normalized.splitlines(keepends=True),
            fromfile="expected",
            tofile="actual",
            lineterm=""
        )
        diff_str = "".join(diff)
        assert False, f"Generated output does not match expected file:\n{diff_str}"

    # Secondary validation: check key features are present
    assert "pub trait Voting" in actual
    assert "#[storage_mapper(\"chairperson\")]" in actual
    assert "fn chairperson(&self) -> SingleValueMapper<ManagedAddress<Self::Api>>;" in actual
    assert 'require!' in actual
    assert "self.proposal_created_event" in actual
    assert "self.vote_cast_event" in actual


def test_nft_marketplace_body_generation():
    # Test NFT Marketplace with complex features
    sol = load("test_cases/solidity/NFTMarketplace.sol")
    expected = load("test_cases/expected/NFTMarketplace.rs")
    actual = Transpiler().convert(sol)

    # Normalize both for comparison
    expected_normalized = normalize(expected)
    actual_normalized = normalize(actual)

    # Primary validation: compare normalized expected vs actual
    if expected_normalized != actual_normalized:
        import difflib
        diff = difflib.unified_diff(
            expected_normalized.splitlines(keepends=True),
            actual_normalized.splitlines(keepends=True),
            fromfile="expected",
            tofile="actual",
            lineterm=""
        )
        diff_str = "".join(diff)
        assert False, f"Generated output does not match expected file:\n{diff_str}"

    # Secondary validation: check key features are present
    assert "pub trait NFTMarketplace" in actual
    assert "#[storage_mapper(\"nextTokenId\")]" in actual
    assert "fn next_token_id(&self) -> SingleValueMapper<BigUint<Self::Api>>;" in actual
    assert "_event" in actual
    assert ".set(" in actual or ".push(" in actual


def test_crowdfunding_body_generation():
    # Test Crowdfunding contract
    sol = load("test_cases/solidity/Crowdfunding.sol")
    expected = load("test_cases/expected/Crowdfunding.rs")
    actual = Transpiler().convert(sol)

    # Normalize both for comparison
    expected_normalized = normalize(expected)
    actual_normalized = normalize(actual)

    # Primary validation: compare normalized expected vs actual
    if expected_normalized != actual_normalized:
        import difflib
        diff = difflib.unified_diff(
            expected_normalized.splitlines(keepends=True),
            actual_normalized.splitlines(keepends=True),
            fromfile="expected",
            tofile="actual",
            lineterm=""
        )
        diff_str = "".join(diff)
        assert False, f"Generated output does not match expected file:\n{diff_str}"

    # Secondary validation: check key features are present
    assert "pub trait Crowdfunding" in actual
    assert "require!" in actual
    assert "_event" in actual
    assert ".set(" in actual or ".get(" in actual


