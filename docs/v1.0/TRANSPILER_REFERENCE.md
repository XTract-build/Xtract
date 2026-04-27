# XTract Transpiler Reference

Full feature coverage for the v1.0 transpiler (`xtract/transpiler.py`).

---

## Type Mapping

| Solidity Type | MultiversX Rust Type | Notes |
|---|---|---|
| `uint256` | `BigUint<Self::Api>` | |
| `uint64` | `u64` | |
| `uint32` | `u32` | |
| `uint16` | `u16` | |
| `uint8` | `u8` | |
| `int256` | `BigInt<Self::Api>` | |
| `int64` / `int32` / `int16` / `int8` | `i64` / `i32` / `i16` / `i8` | |
| `address` | `ManagedAddress<Self::Api>` | |
| `string` | `ManagedBuffer<Self::Api>` | |
| `bytes` | `ManagedBuffer<Self::Api>` | |
| `bytes1`–`bytes32` | `[u8; N]` | |
| `bool` | `bool` | |
| `mapping(K => V)` | `SingleValueMapper` / `MapMapper` | key-parameterised storage fn |
| `mapping(K => mapping(K2 => V))` | multi-key storage mapper | |
| `T[]` | `VecMapper<Self::Api, T>` | |
| `T[N]` | `ArrayMapper<Self::Api, T, N>` | |

---

## Type Cast Mapping

`bytes(x)` and `bytes32(x)` casts are emitted as `ManagedBuffer` conversions when the input shape is known:

| Solidity Cast | MultiversX Rust Output | Notes |
|---|---|---|
| `bytes32("hello")` / `bytes("hello")` | `ManagedBuffer::from(b"hello")` | string literal input |
| `bytes32(0xdeadbeef)` / `bytes(0xdeadbeef)` | `ManagedBuffer::from(&[0xde, 0xad, 0xbe, 0xef])` | hex literal input |
| `bytes32(someBytes)` / `bytes(someBytes)` | `someBytes` | no-op when `someBytes` is known to be `bytes`, `string`, or `ManagedBuffer` |
| `bytes32(someUint)` / `bytes(someUint)` | `ManagedBuffer::new() /* TODO: ... */` | emits `bytes32(uint) cast requires manual conversion — use .to_bytes_be() or similar` |
| `bytes32(x)` / `bytes(x)` with unknown input type | `ManagedBuffer::new() /* TODO: bytes32(x) — verify input type */` | emits a `TranspilationWarning` |

Numeric casts to bytes require manual review because the correct byte order and width depend on the Solidity intent. Use `.to_bytes_be()` or an equivalent explicit conversion before wiring the generated stub into production code.

---

## Fully Supported Features

| Solidity Feature | MultiversX Rust Output | Notes |
|---|---|---|
| `uint256` | `BigUint<Self::Api>` | |
| `uint64/32/16/8` | `u64/u32/u16/u8` | |
| `int256` | `BigInt<Self::Api>` | |
| `address` | `ManagedAddress<Self::Api>` | |
| `string` | `ManagedBuffer<Self::Api>` | |
| `bool` | `bool` | |
| `mapping(k => v)` | `SingleValueMapper` / `MapMapper` | |
| Nested mapping | multi-key mapper | |
| State variables | `#[storage_mapper]` | dynamic detection, no whitelist |
| Events | `#[event]` with indexed params | |
| Custom errors | `require!` with message | |
| Structs | Rust struct with codec derives | |
| Modifiers | inlined `require!()` + pre/post statements | pre and post body statements both emitted |
| `nonReentrant` | `locked.set(true)` / `locked.set(false)` around body | |
| Function visibility | `pub` / private / `#[view]` / `#[endpoint]` | |
| Payable functions | `#[payable("EGLD")]` | |
| Constructor | `#[init]` fn with parameters | parameters mapped via type table |
| Inheritance (`is A`) | supertrait | |
| `require()` | `require!()` | |
| `revert()` | `sc_panic!()` | |
| `if/else` | direct | |
| `for` loops | `for` loop | counter-based |
| `while` loops | `while` loop | |
| `do-while` | `loop { ... if !cond { break } }` | |
| `unchecked { }` | passthrough + comment | |
| `delete var` | `.clear()` | `StorageMapper::clear()` |
| `SafeMath` / `using-for` | inlined arithmetic operators | `add/sub/mul/div/mod` |
| `abi.encode` / `abi.encodePacked` | `ManagedBuffer` serialization | partial |
| `new ContractType()` | `ManagedAddress::zero()` + TODO comment | stub with warning |
| Mapping read in expression | `.get()` appended automatically | scoped to known storage vars |
| Mapping write (assignment) | `.set()` emitted | |
| Function parameter `.clone()` | emitted for all params, not just `_to`/`_from` | uses actual param introspection |

---

## Not Supported (Documented Workarounds)

| Feature | Reason | Workaround |
|---|---|---|
| `try-catch` | No MultiversX equivalent | Stripped before parsing; a `// TODO: try-catch block removed — implement error handling manually` comment is emitted in its place. Replace it with async callbacks or `require!` guards. |
| Inline assembly | No EVM on MultiversX | Stripped before parsing; a `// TODO: inline assembly removed — no MultiversX equivalent` comment is emitted in its place. Rewrite using Rust/SC APIs. |
| `selfdestruct` | No equivalent | Design contracts without it |
| `delegatecall` | No equivalent | Use composability patterns |
| `abi.encodeWithSelector` | Partial | Manual `ManagedBuffer` |
| Diamond inheritance | Complex trait resolution | Flatten inheritance manually |
| Libraries | Not emitted | Inline library logic |

---

## `--json` Output Format

Pass `--json` to get machine-readable output on stdout:

```bash
xtract --json MyContract.sol
# or:
xtract transpile --json MyContract.sol
```

Output schema:

```json
{
  "success": true,
  "code": "#![no_std]\n\nuse multiversx_sc::imports::*;\n...",
  "warnings": [
    {
      "message": "delegatecall is not supported on MultiversX",
      "line": 42,
      "severity": "warning"
    }
  ],
  "errors": []
}
```

| Field | Type | Description |
|---|---|---|
| `success` | `bool` | `true` if transpilation produced usable output |
| `code` | `string` | Generated Rust source |
| `warnings` | `Diagnostic[]` | Non-fatal issues; contract was still generated |
| `errors` | `string[]` | Fatal errors that prevented code generation |

`Diagnostic` object:

```json
{ "message": "string", "line": 42, "severity": "warning" }
```

Exit code is `0` on success, non-zero on error.

---

## Example: SimpleStorage

**Solidity input:**

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleStorage {
    uint256 private value;
    event ValueChanged(uint256 newValue);

    function setValue(uint256 newValue) public {
        value = newValue;
        emit ValueChanged(newValue);
    }

    function getValue() public view returns (uint256) {
        return value;
    }
}
```

**Generated Rust:**

```rust
#![no_std]

use multiversx_sc::imports::*;
use multiversx_sc::derive_imports::*;

#[multiversx_sc::contract]
pub trait SimpleStorage {
    #[storage_mapper("value")]
    fn value(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[event("ValueChanged")]
    fn value_changed_event(&self, #[indexed] new_value: BigUint<Self::Api>);

    #[init]
    fn init(&self) {}

    #[endpoint]
    fn set_value(&self, new_value: BigUint<Self::Api>) {
        self.value().set(new_value.clone());
        self.value_changed_event(new_value);
    }

    #[view(getValue)]
    fn get_value(&self) -> BigUint<Self::Api> {
        self.value().get()
    }
}
```

---

## Constructor Parameter Mapping

Constructor parameters are emitted in the `#[init]` function signature using the same type mapping as regular functions.

**Solidity:**
```solidity
constructor(address _owner, uint256 _initialSupply) {
    owner = _owner;
    totalSupply = _initialSupply;
}
```

**Generated Rust:**
```rust
#[init]
fn init(&self, _owner: ManagedAddress<Self::Api>, _initialSupply: BigUint<Self::Api>) {
    self.owner().set(_owner);
    self.total_supply().set(_initialSupply);
}
```

Parameter names are preserved as-is (leading underscores included). Types are converted via the standard type mapping table (see [Type Mapping](#type-mapping)).

## Modifier Inlining

Modifiers are inlined into each endpoint that uses them. Both the pre-`_;` and post-`_;` statements are emitted:

**Solidity:**
```solidity
modifier nonReentrant() {
    require(!locked, "Reentrant call");
    locked = true;
    _;
    locked = false;
}

function deposit(address token, uint256 amount) public nonReentrant { ... }
```

**Generated Rust:**
```rust
#[endpoint]
fn deposit(&self, token: ManagedAddress<Self::Api>, amount: BigUint<Self::Api>) {
    require!(!self.locked().get(), "Reentrant call");
    self.locked().set(true);
    // ... endpoint body ...
    self.locked().set(false);
}
```
