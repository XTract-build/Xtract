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
| `int256` | `BigInt<Self::Api>` | MultiversX BigInt has limited negative number support; negative literal casts emit a warning |
| `int64` / `int32` / `int16` / `int8` | `i64` / `i32` / `i16` / `i8` | |
| `address` | `ManagedAddress<Self::Api>` | |
| `string` | `ManagedBuffer<Self::Api>` | |
| `bytes` | `ManagedBuffer<Self::Api>` | |
| `bytes1`–`bytes32` | `[u8; N]` | |
| `bool` | `bool` | |
| `mapping(K => V)` | `SingleValueMapper` / `MapMapper` | key-parameterised storage fn |
| `mapping(K => mapping(K2 => V))` | multi-key storage mapper | |
| `T[]` | `VecMapper<T>` | dynamic-length array; 1-indexed |
| `T[N]` | `ArrayMapper<Self::Api, T, N>` | |

`int256(...)` casts are emitted as `BigInt::from(...)`. Negative literals emit `BigInt::from(-Ni64)` plus a diagnostic warning because MultiversX BigInt negative values can behave differently from Solidity `int256` in storage and arithmetic. Non-literal `int256(...)` casts also warn so the source variable's signedness and runtime range can be verified.

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
| `int256` | `BigInt<Self::Api>` | Limited negative value semantics compared with Solidity `int256` |
| `address` | `ManagedAddress<Self::Api>` | |
| `string` | `ManagedBuffer<Self::Api>` | |
| `bool` | `bool` | |
| `mapping(k => v)` | `SingleValueMapper` / `MapMapper` | |
| Nested mapping | multi-key mapper | |
| State variables | `#[storage_mapper]` | dynamic detection, no whitelist |
| Events | `#[event]` with indexed params | |
| Custom errors | `sc_panic!` message when used with `revert` | typed args dropped with warning |
| Structs | Rust struct with codec derives | |
| Modifiers | inlined `require!()` + pre/post statements | pre and post body statements both emitted |
| `nonReentrant` | `locked.set(true)` / `locked.set(false)` around body | |
| Function visibility | `pub` / private / `#[view]` / `#[endpoint]` | |
| Payable functions | `#[payable("EGLD")]` | |
| `msg.sender` | `self.blockchain().get_caller()` | |
| `msg.value` | `self.call_value().egld_value()` | payable function must use `#[payable("EGLD")]` |
| `msg.data` | `ManagedBuffer::new()` stub | emits `TranspilationWarning`; manual conversion required |
| `msg.sig` | TODO stub | emits `TranspilationWarning`; no MultiversX equivalent |
| Constructor | `#[init]` fn with parameters | parameters mapped via type table |
| Inheritance (`is A`) | supertrait | |
| `require()` | `require!()` | |
| `revert()` | `sc_panic!("revert")` | |
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
| `array[]` storage variable | `VecMapper<T>` trait fn | declared as `fn name(&self) -> VecMapper<T>;` |
| `array.push(v)` | `self.array().push(&v)` | |
| `array.pop()` | `let last = self.array().len() - 1; self.array().remove(last);` | two-statement expansion |
| `array.length` | `self.array().len()` | called on VecMapper directly, not `.get().len()` |
| `array[i]` (read) | `self.array().get(i + 1)` | VecMapper is 1-indexed |
| `msg.sender` | `self.blockchain().get_caller()` | |
| `block.timestamp` | `self.blockchain().get_block_timestamp()` | |
| `block.number` | `self.blockchain().get_block_nonce()` | |
| `address(this)` | `self.blockchain().get_sc_address()` | |
| `now` | `self.blockchain().get_block_timestamp()` | Solidity alias for `block.timestamp` |
| `tx.origin` | `self.blockchain().get_caller()` | emits warning — see behavioral note below |
| `type(uint256).max` | `BigUint::from(u64::MAX)` | TODO comment: true max is 2^256-1 |
| `type(uint256).min` | `BigUint::zero()` | |
| `type(int256).max` | `BigInt::from(i64::MAX)` | TODO comment: true max is 2^255-1 |
| `type(int256).min` | `BigInt::from(i64::MIN)` | TODO comment: true min is -(2^255) |

---

## Cryptography

| Solidity | MultiversX output | Notes |
|---|---|---|
| `keccak256(data)` | `self.crypto().keccak256(&data)` | Input must be a `ManagedBuffer`; a transpilation warning is emitted |
| `sha256(data)` | `self.crypto().sha256(&data)` | Input must be a `ManagedBuffer`; a transpilation warning is emitted |
| `ecrecover(hash, v, r, s)` | `ManagedAddress::zero() /* TODO */` | No MultiversX equivalent — use off-chain verification; a transpilation warning is emitted |

### ManagedBuffer conversion

The `self.crypto()` API expects a `&ManagedBuffer` argument. If the input in your Solidity contract is `bytes` or `bytes32`, convert it before hashing:

```rust
let buf = ManagedBuffer::from(data.as_slice());
let hash = self.crypto().keccak256(&buf);
```

---

## Behavioral Notes

### `tx.origin` vs `msg.sender` on MultiversX

On EVM, `tx.origin` is the original EOA that initiated the transaction, while `msg.sender` is the immediate caller (which may be a contract). On MultiversX, there is no equivalent distinction — the caller is always the direct caller. XTract maps `tx.origin` to `self.blockchain().get_caller()` and emits a `TranspilationWarning` to flag this semantic difference for manual review.

### `type(uint256).max`

The true uint256 maximum is 2^256-1, which exceeds `u64::MAX`. XTract emits `BigUint::from(u64::MAX)` as a conservative placeholder with a TODO comment. Replace with the correct `BigUint` construction if your contract depends on the exact value.

---

## Revert and Custom Error Mapping

Solidity `revert` statements are mapped to MultiversX `sc_panic!`, which only accepts a string message:

| Solidity input | MultiversX output | Notes |
|---|---|---|
| `revert()` | `sc_panic!("revert")` | default fallback message |
| `revert("failed")` | `sc_panic!("failed")` | string message preserved |
| `revert CustomError()` | `sc_panic!("CustomError")` | custom error name preserved |
| `revert CustomError("failed")` | `sc_panic!("failed")` | string message argument used |
| `revert CustomError(a, b)` | `sc_panic!("CustomError")` | typed custom error arguments are dropped |

When typed custom error arguments are dropped, diagnostics include:

```text
Custom error arguments dropped — MultiversX sc_panic only supports string messages
```

Use string message arguments in custom error reverts when the generated MultiversX contract needs contextual panic text.

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
| `ecrecover` | No on-chain equivalent | Verify signatures off-chain |

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
