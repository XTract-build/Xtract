from pathlib import Path

from xtract.transpiler import Transpiler


def load(p: str) -> str:
    return Path(p).read_text()


def normalize(s: str) -> str:
    return s.replace("\r\n", "\n").strip()


def test_simple_storage_shape():
    sol = load("test_cases/solidity/SimpleStorage.sol")
    expected = load("test_cases/expected/SimpleStorage.rs")
    actual = Transpiler().convert(sol)

    # Check contract name, storage, functions, and events present
    assert "pub trait SimpleStorage" in actual
    assert "#[storage_mapper(\"value\")]" in actual
    assert "fn value(&self) -> SingleValueMapper<BigUint<Self::Api>>;" in actual
    assert "#[event(\"ValueChanged\")]" in actual
    assert "fn value_changed_event(&self, #[indexed] newValue: BigUint<Self::Api>);" in actual or \
           "fn value_changed_event(&self, #[indexed] new_value: BigUint<Self::Api>);" in actual
    assert "#[view(getValue)]" in actual
    assert "fn get_value(&self) -> BigUint<Self::Api>" in actual

    # Check body generation
    assert "self.value().set(newValue);" in actual
    assert "self.value_changed_event(newValue);" in actual
    assert "return self.value().get();" in actual


def test_erc20_body_generation():
    # Test ERC20 require and emit statements
    sol = load("test_cases/solidity/ERC20Token.sol")
    actual = Transpiler().convert(sol)

    # Check basic structure
    assert "#![no_std]" in actual
    assert "use multiversx_sc::imports::*;" in actual
    assert "#[multiversx_sc::contract]" in actual
    assert "pub trait ERC20Token" in actual

    # Check storage mappers
    assert "#[storage_mapper(\"name\")]" in actual
    assert "fn name(&self) -> SingleValueMapper<ManagedBuffer<Self::Api>>;" in actual

    # Check require statements in transfer function
    assert 'require!(self.balance_of(&self.blockchain().get_caller()) >= _value, "Insufficient balance");' in actual

    # Check emit statements
    assert "self.transfer_event(self.blockchain().get_caller(), _to, _value);" in actual
    assert "self.transfer_event(ManagedAddress::zero(), self.blockchain().get_caller(), self.total_supply().get());" in actual

    # Check constructor/init body
    assert "self.name().set(_name);" in actual
    assert "self.total_supply().set" in actual


def test_voting_body_generation():
    # Test Voting contract with complex statements
    sol = load("test_cases/solidity/Voting.sol")
    actual = Transpiler().convert(sol)

    # Check basic structure
    assert "pub trait Voting" in actual

    # Check storage mappers
    assert "#[storage_mapper(\"chairperson\")]" in actual
    assert "fn chairperson(&self) -> SingleValueMapper<ManagedAddress<Self::Api>>;" in actual

    # Check require statements
    assert 'require!' in actual

    # Check emit statements
    assert "self.proposal_created_event" in actual or \
           "self.vote_cast_event" in actual or \
           "self.voting_closed_event" in actual

    # Check array length operations (since proposals is not being extracted as a mapping)
    assert ".len()" in actual


def test_nft_marketplace_body_generation():
    # Test NFT Marketplace with complex features
    sol = load("test_cases/solidity/NFTMarketplace.sol")
    actual = Transpiler().convert(sol)

    # Check basic structure
    assert "pub trait NFTMarketplace" in actual

    # Check storage mappers
    assert "#[storage_mapper(\"nextTokenId\")]" in actual
    assert "fn next_token_id(&self) -> SingleValueMapper<BigUint<Self::Api>>;" in actual

    # Check emit statements
    assert "_event" in actual

    # Check storage operations
    assert ".set(" in actual or ".push(" in actual or ".len()" in actual


def test_crowdfunding_body_generation():
    # Test Crowdfunding contract
    sol = load("test_cases/solidity/Crowdfunding.sol")
    actual = Transpiler().convert(sol)

    # Check basic structure
    assert "pub trait Crowdfunding" in actual

    # Check require statements (time-based logic)
    assert "require!" in actual

    # Check emit statements
    assert "_event" in actual

    # Check storage operations
    assert ".set(" in actual or ".get(" in actual


