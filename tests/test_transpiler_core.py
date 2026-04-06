"""
XTract Transpiler Test Suite

This test suite validates the Solidity to MultiversX Rust transpilation.
It tests 50 different contract patterns including:
- Basic contracts
- Mappings (single and nested)
- Function modifiers
- Basic inheritance
- Various DeFi patterns
"""

import json
import subprocess
import sys
from pathlib import Path
import pytest

from xtract.transpiler import Transpiler


def load(p: str) -> str:
    return Path(p).read_text()


def normalize(s: str) -> str:
    """Normalize whitespace and line endings for comparison"""
    return s.replace("\r\n", "\n").strip()


def get_test_files():
    """Get all Solidity test files that have corresponding expected outputs"""
    solidity_dir = Path("test_cases/solidity")
    expected_dir = Path("test_cases/expected")

    test_files = []
    for sol_file in sorted(solidity_dir.glob("*.sol")):
        expected_file = expected_dir / sol_file.with_suffix(".rs").name
        if expected_file.exists():
            test_files.append((sol_file.stem, str(sol_file), str(expected_file)))

    return test_files


# Generate test cases for all contracts
TEST_CASES = get_test_files()


@pytest.mark.parametrize("name,sol_path,expected_path", TEST_CASES, ids=[t[0] for t in TEST_CASES])
def test_transpilation(name, sol_path, expected_path):
    """Test transpilation of each contract against expected output"""
    sol = load(sol_path)
    expected = load(expected_path)
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
        assert False, f"Generated output for {name} does not match expected file:\n{diff_str[:2000]}"


# Additional feature-specific tests

def test_simple_storage_features():
    """Test SimpleStorage contract has key features"""
    sol = load("test_cases/solidity/SimpleStorage.sol")
    actual = Transpiler().convert(sol)

    assert "pub trait SimpleStorage" in actual
    assert "#[storage_mapper(\"value\")]" in actual
    assert "fn value(&self) -> SingleValueMapper<BigUint<Self::Api>>;" in actual
    assert "#[event(\"ValueChanged\")]" in actual


def test_erc20_features():
    """Test ERC20Token contract has key features"""
    sol = load("test_cases/solidity/ERC20Token.sol")
    actual = Transpiler().convert(sol)

    assert "#![no_std]" in actual
    assert "use multiversx_sc::imports::*;" in actual
    assert "#[multiversx_sc::contract]" in actual
    assert "pub trait ERC20Token" in actual
    assert "#[storage_mapper(\"totalSupply\")]" in actual
    assert "require!" in actual


def test_nested_mapping_features():
    """Test nested mapping transpilation"""
    sol = load("test_cases/solidity/NestedMapping.sol")
    actual = Transpiler().convert(sol)

    assert "pub trait NestedMapping" in actual
    assert "#[storage_mapper(\"allowance\")]" in actual
    # Nested mapping should have two key parameters
    assert "key1:" in actual or "key2:" in actual


def test_modifier_features():
    """Test modifier transpilation"""
    sol = load("test_cases/solidity/OnlyOwner.sol")
    actual = Transpiler().convert(sol)

    assert "pub trait OnlyOwner" in actual
    assert "#[storage_mapper(\"owner\")]" in actual
    # Modifier should be converted to require! check
    assert "require!" in actual


def test_inheritance_features():
    """Test inheritance transpilation"""
    sol = load("test_cases/solidity/SimpleInheritance.sol")
    actual = Transpiler().convert(sol)

    # Should include inheritance comment or supertrait
    assert "pub trait SimpleInheritance" in actual
    assert "Ownable" in actual  # Parent contract reference


def test_multiple_modifiers():
    """Test contract with multiple modifiers"""
    sol = load("test_cases/solidity/Pausable.sol")
    actual = Transpiler().convert(sol)

    assert "pub trait Pausable" in actual
    assert "#[storage_mapper(\"paused\")]" in actual
    assert "require!" in actual


def test_staking_contract():
    """Test staking contract pattern"""
    sol = load("test_cases/solidity/Staking.sol")
    actual = Transpiler().convert(sol)

    assert "pub trait Staking" in actual
    assert "#[storage_mapper(\"stakes\")]" in actual
    assert "#[storage_mapper(\"rewards\")]" in actual
    assert "#[event(\"Staked\")]" in actual


def test_vault_contract():
    """Test vault contract pattern"""
    sol = load("test_cases/solidity/Vault.sol")
    actual = Transpiler().convert(sol)

    assert "pub trait Vault" in actual
    assert "#[storage_mapper(\"balances\")]" in actual
    assert "#[event(\"Deposited\")]" in actual
    assert "#[event(\"WithdrawalCompleted\")]" in actual


def test_governance_contract():
    """Test governance contract pattern"""
    sol = load("test_cases/solidity/Governance.sol")
    actual = Transpiler().convert(sol)

    assert "pub trait Governance" in actual
    assert "#[storage_mapper(\"proposalVotes\")]" in actual
    assert "#[event(\"ProposalCreated\")]" in actual
    assert "#[event(\"Voted\")]" in actual


def test_badge_nested_mapping():
    """Test contract with nested mapping (user => badgeId => bool)"""
    sol = load("test_cases/solidity/Badge.sol")
    actual = Transpiler().convert(sol)

    assert "pub trait Badge" in actual
    assert "#[storage_mapper(\"hasBadge\")]" in actual


# Diagnostics tests

def test_loops_are_supported():
    """Test that for loops are now transpiled (not just warned about)"""
    sol_with_loop = """
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.0;

    contract LoopContract {
        uint256 public sum;

        function sumToN(uint256 n) public {
            for (uint i = 0; i < n; i++) {
                sum = sum + 1;
            }
        }
    }
    """

    transpiler = Transpiler()
    result = transpiler.convert(sol_with_loop)

    # Should contain a for loop in Rust syntax
    assert "for i in 0.." in result


def test_if_statements_are_supported():
    """Test that if statements are now transpiled"""
    sol_with_if = """
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.0;

    contract IfContract {
        uint256 public value;

        function setIfPositive(uint256 x) public {
            if (x > 0) {
                value = x;
            }
        }
    }
    """

    transpiler = Transpiler()
    result = transpiler.convert(sol_with_if)

    # Should contain if statement in Rust syntax
    assert "if " in result and "{" in result


def test_convert_with_diagnostics():
    """Test convert_with_diagnostics returns proper result"""
    sol = load("test_cases/solidity/SimpleStorage.sol")

    transpiler = Transpiler()
    result = transpiler.convert_with_diagnostics(sol)

    assert result.success
    assert "pub trait SimpleStorage" in result.code


def test_local_declaration_generates_let():
    """Test that local variable declarations emit let mut bindings"""
    sol = load("test_cases/solidity/VariableDeclarations.sol")
    expected = load("test_cases/expected/VariableDeclarations.rs")
    actual = Transpiler().convert(sol)
    assert normalize(actual) == normalize(expected), (
        f"Declaration transpilation mismatch:\n"
        f"Expected:\n{normalize(expected)}\n\nActual:\n{normalize(actual)}"
    )
    assert "let mut sum: u64 = x + y;" in actual
    assert "let mut ok: bool = true;" in actual
    assert "let mut result: u64 = sum;" in actual


def test_delete_generates_clear():
    """Test that delete statements emit .clear() calls"""
    sol = load("test_cases/solidity/DeleteOp.sol")
    expected = load("test_cases/expected/DeleteOp.rs")
    actual = Transpiler().convert(sol)
    assert normalize(actual) == normalize(expected), (
        f"Delete transpilation mismatch:\n"
        f"Expected:\n{normalize(expected)}\n\nActual:\n{normalize(actual)}"
    )
    assert "self.counter().clear();" in actual
    assert "self.balances(&user).clear();" in actual
    assert "self.allowance(&owner, &spender).clear();" in actual


def test_dynamic_storage_detection():
    """Storage variables not in the old hardcoded whitelist are correctly converted"""
    sol = """
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.0;

    contract CustomVars {
        uint256 public my_custom_var;
        uint256 public anotherUniqueField;

        function getCustom() public view returns (uint256) {
            return my_custom_var;
        }

        function getUnique() public view returns (uint256) {
            return anotherUniqueField;
        }
    }
    """
    result = Transpiler().convert(sol)
    # Storage declaration must exist
    assert '#[storage_mapper("my_custom_var")]' in result or '#[storage_mapper("anotherUniqueField")]' in result
    # Variable references must be converted to .get() — not left as bare identifiers
    assert "self.my_custom_var().get()" in result
    assert "self.another_unique_field().get()" in result


def test_struct_field_update_generates_set():
    """Test that struct field updates on mapping values emit the load-mutate-store pattern"""
    sol = load("test_cases/solidity/StructFieldUpdate.sol")
    actual = Transpiler().convert(sol)

    assert "pub trait StructFieldUpdate" in actual
    assert "#[storage_mapper(\"listings\")]" in actual
    # activate function: load-mutate-store for bool field
    assert "let mut s = self.listings(&seller).get();" in actual
    assert "s.active = true;" in actual
    assert "self.listings(&seller).set(&s);" in actual
    # setPrice function: load-mutate-store for uint field
    assert "s.price = newPrice;" in actual


def test_do_while_generates_loop_break():
    """Test that do-while loops are transpiled to loop { ... if !(...) { break; } }"""
    sol = """
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.0;

    contract DoWhileTest {
        uint64 public count;

        function run(uint64 limit) public {
            uint64 i = 0;
            do {
                i = i + 1;
            } while (i < limit);
            count = i;
        }
    }
    """
    result = Transpiler().convert(sol)
    assert "loop {" in result
    assert "if !(" in result
    assert "break;" in result


def test_abi_encode_generates_managed_buffer():
    """Test that abi.encode/encodePacked produce ManagedBuffer block expressions"""
    sol = """
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.0;

    contract AbiTest {
        function encodeTwo(uint256 a, uint256 b) public pure returns (bytes memory) {
            return abi.encode(a, b);
        }

        function encodePackedTwo(uint256 a, uint256 b) public pure returns (bytes memory) {
            return abi.encodePacked(a, b);
        }
    }
    """
    result = Transpiler().convert(sol)
    assert "ManagedBuffer::new()" in result
    assert "codec::top_encode_to_managed_buffer(&a, &mut __buf)" in result
    assert "codec::top_encode_to_managed_buffer(&b, &mut __buf)" in result
    assert "__buf.append(&ManagedBuffer::from(&a.to_bytes_be_buffer()))" in result
    assert "__buf.append(&ManagedBuffer::from(&b.to_bytes_be_buffer()))" in result


def test_unchecked_generates_passthrough():
    """Test that unchecked blocks are stripped but inner statements remain"""
    sol = """
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.0;

    contract UncheckedTest {
        uint64 public result;

        function add(uint64 a, uint64 b) public {
            unchecked {
                result = a + b;
            }
        }
    }
    """
    result = Transpiler().convert(sol)
    assert "unchecked" not in result.replace("// NOTE: unchecked", "")
    assert "// NOTE: unchecked arithmetic" in result
    assert "result = a + b" in result or "a + b" in result


def test_safemath_inlining():
    """Test that SafeMath method calls (both using-for and static) are inlined to operators"""
    sol = """
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.0;

    contract SafeMathTest {
        using SafeMath for uint256;
        uint256 public total;

        function addValues(uint256 a, uint256 b) public {
            total = a.add(b);
        }

        function staticAdd(uint256 a, uint256 b) public {
            total = SafeMath.add(a, b);
        }

        function subValues(uint256 a, uint256 b) public {
            total = a.sub(b);
        }

        function mulValues(uint256 a, uint256 b) public {
            total = a.mul(b);
        }
    }
    """
    result = Transpiler().convert(sol)

    # Library method calls must be inlined — no raw SafeMath calls in output
    assert "a.add(" not in result
    assert "SafeMath.add(" not in result
    assert "a.sub(" not in result
    assert "a.mul(" not in result

    # Inlined operators must appear
    assert "a + b" in result
    assert "a - b" in result
    assert "a * b" in result


def test_unknown_library_warning():
    """Unknown using-for libraries emit a TranspilationWarning"""
    sol = """
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.0;

    contract Foo {
        using MyCustomLib for uint256;
        uint256 public x;

        function doThing(uint256 a) public {
            x = a.customOp();
        }
    }
    """
    transpiler = Transpiler()
    transpiler.convert(sol)

    warning_messages = [w.message for w in transpiler._warnings]
    assert any("MyCustomLib" in msg for msg in warning_messages)


def test_json_flag_output():
    """Test --json flag outputs valid JSON with expected fields"""
    sol_path = "test_cases/solidity/ERC20Token.sol"
    result = subprocess.run(
        [sys.executable, "-m", "xtract.cli", "--json", sol_path],
        capture_output=True,
        text=True,
    )
    output = json.loads(result.stdout)

    assert output["success"] is True
    assert "#[multiversx_sc::contract]" in output["code"]
    assert isinstance(output["warnings"], list)
    assert isinstance(output["errors"], list)
    assert result.returncode == 0


def test_contract_new_generates_stub():
    """Test that 'new ContractType()' emits a deployment stub with TODO comment and ManagedAddress::zero()"""
    sol = load("test_cases/solidity/ContractFactory.sol")
    transpiler = Transpiler()
    actual = transpiler.convert(sol)

    assert "TODO: deploy Child" in actual
    assert "ManagedAddress::zero()" in actual

    warning_messages = [w.message for w in transpiler._warnings]
    assert any("ContractDeploy" in msg for msg in warning_messages)


def test_mapping_assignment_emits_set():
    """Test that mapping write statements (mapping[key] = expr) emit .set(...)"""
    sol = """
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.0;

    contract ReservePool {
        mapping(address => uint64) public reserves;

        function deposit(address token, uint64 amount) public {
            reserves[token] = reserves[token] + amount;
        }
    }
    """
    result = Transpiler().convert(sol)
    assert ".set(" in result, "Expected .set() call for mapping write"
    assert "self.reserves(" in result


def test_int256_cast_variable():
    """int256(someVar) → BigInt::from(someVar)"""
    sol = """
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.0;

    contract CastTest {
        function cast(int256 someVar) public pure returns (int256) {
            return int256(someVar);
        }
    }
    """
    result = Transpiler().convert(sol)
    assert "BigInt::from(someVar)" in result


def test_int256_cast_positive_literal():
    """int256(42) → BigInt::from(42i64)"""
    sol = """
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.0;

    contract CastTest {
        function cast() public pure returns (int256) {
            return int256(42);
        }
    }
    """
    result = Transpiler().convert(sol)
    assert "BigInt::from(42i64)" in result


def test_int256_cast_negative_literal_emits_warning():
    """int256(-5) → BigInt::from(-5i64) and a warning is emitted"""
    sol = """
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.0;

    contract CastTest {
        function cast() public pure returns (int256) {
            return int256(-5);
        }
    }
    """
    transpiler = Transpiler()
    result = transpiler.convert(sol)
    assert "BigInt::from(-5i64)" in result
    warning_messages = [w.message for w in transpiler._warnings]
    assert any("int256" in msg and "negative" in msg.lower() for msg in warning_messages)


def test_bool_cast_from_one():
    """bool(1) → true"""
    sol = """
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.0;

    contract CastTest {
        function cast() public pure returns (bool) {
            return bool(1);
        }
    }
    """
    result = Transpiler().convert(sol)
    assert "return true;" in result


def test_bool_cast_from_zero():
    """bool(0) → false"""
    sol = """
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.0;

    contract CastTest {
        function cast() public pure returns (bool) {
            return bool(0);
        }
    }
    """
    result = Transpiler().convert(sol)
    assert "return false;" in result


def test_bool_cast_from_variable():
    """bool(someVar) → someVar != 0"""
    sol = """
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.0;

    contract CastTest {
        function cast(uint256 someVar) public pure returns (bool) {
            return bool(someVar);
        }
    }
    """
    result = Transpiler().convert(sol)
    assert "someVar != 0" in result


def test_nested_mapping_assignment_emits_set():
    """Test that nested mapping writes (mapping[k1][k2] = expr) emit .set(...)"""
    sol = """
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.0;

    contract Allowances {
        mapping(address => mapping(address => uint64)) public allowance;

        function approve(address owner, address spender, uint64 amount) public {
            allowance[owner][spender] = amount;
        }
    }
    """
    result = Transpiler().convert(sol)
    assert ".set(" in result, "Expected .set() call for nested mapping write"
    assert "self.allowance(" in result


def test_blockchain_caller_no_extra_get():
    """self.blockchain().get_caller() must not become self.blockchain().get().get_caller()"""
    sol = """
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.0;

    contract CallerTest {
        function getCaller() public view returns (address) {
            return msg.sender;
        }
    }
    """
    result = Transpiler().convert(sol)
    assert "self.blockchain().get_caller()" in result
    assert "self.blockchain().get()" not in result


def test_storage_mapper_gets_get_in_expression():
    """A storage mapper (SingleValueMapper) used in a read expression must have .get() appended"""
    sol = """
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.0;

    contract AdminTest {
        address public admin;

        function getAdmin() public view returns (address) {
            return admin;
        }
    }
    """
    result = Transpiler().convert(sol)
    assert "self.admin().get()" in result


def test_ternary_operator_transpilation():
    """Test that ternary expressions are transpiled to Rust if-else expressions"""
    sol = """
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.0;

    contract FeeCalc {
        function calc(uint256 amount) public pure returns (uint256) {
            uint256 fee = amount > 1000 ? amount / 100 : 0;
            return fee;
        }
    }
    """
    result = Transpiler().convert(sol)
    assert "let mut fee: BigUint<Self::Api> = if amount > BigUint::from(1000u32) { amount / BigUint::from(100u32) } else { BigUint::zero() };" in result


# Count test to verify we have 50 test cases
def test_fifty_test_cases():
    """Verify we have at least 50 test cases"""
    assert len(TEST_CASES) >= 50, f"Expected at least 50 test cases, got {len(TEST_CASES)}"


# Type cast transpilation tests

def test_type_cast_uint256_zero():
    """uint256(0) should transpile to BigUint::zero()"""
    sol = """
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.0;
    contract C {
        uint256 public x;
        function reset() public {
            x = uint256(0);
        }
    }
    """
    result = Transpiler().convert(sol)
    assert "BigUint::zero()" in result


def test_type_cast_address_zero():
    """address(0) should transpile to ManagedAddress::zero()"""
    sol = """
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.0;
    contract C {
        address public owner;
        function clear() public {
            owner = address(0);
        }
    }
    """
    result = Transpiler().convert(sol)
    assert "ManagedAddress::zero()" in result


def test_type_cast_address_var():
    """address(someAddr) should transpile to ManagedAddress::from(&someAddr)"""
    sol = """
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.0;
    contract C {
        address public target;
        function setTarget(address someAddr) public {
            target = address(someAddr);
        }
    }
    """
    result = Transpiler().convert(sol)
    assert "ManagedAddress::from(" in result


def test_type_cast_uint256_var():
    """uint256(someVar) should transpile to BigUint::from(someVar)"""
    sol = """
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.0;
    contract C {
        uint256 public amount;
        function setAmount(uint64 someVar) public {
            amount = uint256(someVar);
        }
    }
    """
    result = Transpiler().convert(sol)
    assert "BigUint::from(" in result


def test_nested_type_cast_uint256_uint128():
    """uint256(uint128(x)) must not be silently skipped by a [^()]+ regex"""
    t = Transpiler()
    result = t._convert_expression("uint256(uint128(x))")
    assert result == "BigUint::from(x as u128)", f"Got: {result!r}"


def test_nested_type_cast_address_bytes20():
    """address(bytes20(x)) must be converted through both cast layers"""
    t = Transpiler()
    result = t._convert_expression("address(bytes20(x))")
    assert result == "ManagedAddress::from(&x)", f"Got: {result!r}"


def test_constructor_params_emitted_in_init():
    """Constructor parameters must appear in #[init] fn signature with correct types."""
    sol = """
    // SPDX-License-Identifier: MIT
    pragma solidity ^0.8.0;

    contract Token {
        address public owner;
        uint256 public totalSupply;

        constructor(address _owner, uint256 _initialSupply) {
            owner = _owner;
            totalSupply = _initialSupply;
        }
    }
    """
    result = Transpiler().convert(sol)
    assert "fn init(&self, _owner: ManagedAddress<Self::Api>, _initialSupply: BigUint<Self::Api>)" in result
