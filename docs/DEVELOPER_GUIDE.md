# XTract — Developer Guide

> For version-specific release notes see [docs/v1.0/README.md](v1.0/README.md).

---

## Overview

XTract converts Solidity smart contracts to MultiversX-compatible Rust. From v1.0 it also wraps the build and deployment steps, giving you a single tool for the full pipeline.

## Installation

```bash
# Transpile only
pip install xtract

# Full pipeline (wallet creation + deployment)
pip install xtract[deploy]

# Development (includes pytest)
pip install -e ".[dev]"
```

`mxpy` is required separately for the `xtract build` command:

```bash
pip install mxpy
```

## Python Package Structure

```
xtract/
  transpiler.py   — Solidity parser and Rust emitter
  cli.py          — Click command group (transpile / build / wallet / deploy)
  build.py        — mxpy contract build wrapper
  wallet.py       — BIP39 wallet generation via multiversx-sdk
  deploy.py       — Contract deployment via multiversx-sdk
```

## CLI Reference

### Transpile

```bash
xtract MyContract.sol              # writes MyContract.rs
xtract MyContract.sol output.rs    # explicit output path
xtract -v MyContract.sol           # verbose: show diagnostics
xtract -q MyContract.sol           # quiet: suppress non-error output
xtract --json MyContract.sol       # JSON output (success, code, warnings, errors)
```

### Build

```bash
xtract build ./my_contract/
```

Runs `mxpy contract build` inside `./my_contract/`. Outputs WASM and ABI to `./my_contract/output/`.

### Wallet

```bash
xtract wallet create                          # → ~/.multiversx/wallet.pem
xtract wallet create --output ./wallet.pem   # custom path
```

Prints address, mnemonic (save it — shown once), and faucet URLs for devnet/testnet.

### Faucet

```bash
xtract faucet                                             # devnet, wallet at ~/.multiversx/wallet.pem
xtract faucet --network testnet                           # testnet
xtract faucet --wallet ./wallet.pem                      # explicit wallet path
xtract faucet --address erd1...                          # by address (no wallet file needed)
```

Requests free EGLD from the MultiversX devnet or testnet faucet. `--network` accepts `devnet` (default) or `testnet`.

`xtract wallet create` automatically calls the faucet after generating a wallet unless `--no-faucet` is passed.

### Deploy

```bash
xtract deploy ./output/my_contract.wasm \
  --abi    ./output/my_contract.abi.json \
  --wallet ~/.multiversx/wallet.pem \
  --network devnet

# Options
#   --network   devnet | testnet | mainnet  (default: devnet)
#   --gas-limit N                           (default: 10_000_000)
#   --no-upgrade                            deploy as non-upgradeable
```

## Python API

```python
from xtract import transpile, Transpiler
from xtract import build_contract
from xtract import create_wallet, WalletInfo
from xtract import deploy_contract, DeployResult
```

### Transpilation

```python
from pathlib import Path
from xtract import transpile, Transpiler

# Simple: file in, file out
transpile(Path("MyContract.sol"), Path("MyContract.rs"))

# With diagnostics
result = Transpiler().convert_with_diagnostics(solidity_source_str)
print(result.success)   # bool
print(result.code)      # Rust string
print(result.warnings)  # list of Diagnostic
print(result.errors)    # list of str
```

### Build

```python
from pathlib import Path
from xtract import build_contract

ok = build_contract(Path("./my_contract/"))
```

### Wallet

```python
from pathlib import Path
from xtract import create_wallet

info = create_wallet(Path("./wallet.pem"))
print(info.address)   # erd1...
print(info.mnemonic)  # 24-word phrase
print(info.pem_path)  # Path to saved file
```

### Deploy

```python
from pathlib import Path
from xtract import deploy_contract

result = deploy_contract(
    wasm_path=Path("./output/my_contract.wasm"),
    abi_path=Path("./output/my_contract.abi.json"),
    wallet_path=Path("./wallet.pem"),
    network="devnet",          # "devnet" | "testnet" | "mainnet"
    gas_limit=10_000_000,
    upgradeable=True,
)
print(result.contract_address)  # erd1qqq...
print(result.tx_hash)
print(result.explorer_url)
```

## TypeScript SDK

The `xtract-cli` npm package bundles the same pipeline as a TypeScript API:

```bash
npm install xtract-cli   # or: npm install -g xtract-cli
```

```typescript
import { XtractTranspiler, ContractDeployer } from 'xtract-cli/sdk';

const transpiler = new XtractTranspiler();
const { rustCode } = await transpiler.transpileCode('contract Foo { uint x; }');

const deployer = new ContractDeployer();
const { contractAddress, explorerUrl } = await deployer.deploy({
  network: 'devnet',
  wasmPath: './output/foo.wasm',
  abiPath: './output/foo.abi.json',
  walletPath: './wallet.pem',
});
```

> The TypeScript SDK also shells out to the Python `xtract` CLI for transpilation — `pip install xtract` is still required.

## Solidity → Rust Type Mapping

| Solidity | MultiversX Rust |
|----------|----------------|
| `bool` | `bool` |
| `address` | `ManagedAddress<Self::Api>` |
| `string` | `ManagedBuffer<Self::Api>` |
| `uint8` / `uint16` / `uint32` / `uint64` | `u8` / `u16` / `u32` / `u64` |
| `uint128` / `uint256` | `BigUint<Self::Api>` |
| `int8` / `int16` / `int32` / `int64` | `i8` / `i16` / `i32` / `i64` |
| `int128` / `int256` | `BigInt<Self::Api>` |
| `bytes` | `ManagedBuffer<Self::Api>` |
| `bytes1`–`bytes32` | `[u8; N]` |
| `mapping(K => V)` | `MapMapper<Self::Api, K, V>` |
| `T[]` | `VecMapper<T>` | 1-indexed dynamic array |
| `T[N]` | `ArrayMapper<Self::Api, T, N>` |

### `bytes` / `bytes32` Cast Inputs

The expression converter handles `bytes(x)` and `bytes32(x)` according to the input form:

| Input | Generated output |
|---|---|
| string literal | `ManagedBuffer::from(b"...")` |
| hex literal | `ManagedBuffer::from(&[0x.., ...])` |
| known `bytes`, `string`, or `ManagedBuffer` variable | no-op |
| known `uint*` value or numeric literal | TODO stub plus `TranspilationWarning` |
| unknown expression or variable type | TODO stub plus `TranspilationWarning` |

When adding parser paths that introduce new local symbols, keep `_current_var_types` up to date before expressions that may cast those symbols to `bytes` or `bytes32`. Numeric casts must stay conservative unless the byte width and endian semantics are explicit; prefer warning with guidance to use `.to_bytes_be()` or a contract-specific conversion.

Signed integer note: primitive signed casts (`int8`, `int16`, `int32`, `int64`) map directly to Rust primitives, but `int256` maps to MultiversX `BigInt<Self::Api>`. MultiversX BigInt has limited negative number support compared with Solidity `int256`, especially around storage and arithmetic behavior. The transpiler warns on negative `int256` literal casts and non-literal `int256(...)` casts so developers can verify the generated behavior against the original Solidity contract.

## VecMapper — 1-Indexed Array Access

MultiversX `VecMapper` uses **1-based indexing**, unlike Solidity arrays (0-based).
The transpiler handles this automatically:

| Solidity | MultiversX Rust |
|---|---|
| `arr[]` storage var | `fn arr(&self) -> VecMapper<T>;` |
| `arr.push(v)` | `self.arr().push(&v)` |
| `arr.pop()` | `let last_idx = self.arr().len() - 1;` + `self.arr().remove(last_idx);` |
| `arr.length` | `self.arr().len()` |
| `arr[i]` (read) | `self.arr().get(i + 1)` |

> **Why `+ 1`?**  `VecMapper::get` is 1-indexed.  Index 0 is out-of-bounds in MultiversX.
> If your Solidity code already adjusts indices, review the generated `+ 1` manually.

## Supported Solidity Features

### Fully supported
- Contract declarations, constructors, state variables
- Single and nested mappings
- Dynamic arrays (`T[]`) — VecMapper with full push/pop/length/index support
- Events with indexed parameters
- Custom errors, structs
- Public/external endpoints, public/external `view` and `pure` views, internal/private helper functions, including `fallback()` and payable `receive()`
- Function modifiers (`onlyOwner`, custom, parameterized modifiers with call-site argument substitution)
- Basic inheritance (`contract A is B, C`) as a supertrait stub with manual integration required
- `require` / `revert`, if/else, for loops, while loops, do-while loops
- Ternary expressions (`cond ? a : b` → `if cond { a } else { b }`)
- Automatic `#[payable("EGLD")]` annotation

### Custom error reverts

MultiversX `sc_panic!` only accepts a string message, so Solidity custom error reverts are reduced to a panic message:

| Solidity input | Generated MultiversX Rust |
|---|---|
| `revert CustomError()` | `sc_panic!("CustomError");` |
| `revert CustomError("low balance")` | `sc_panic!("low balance");` |
| `revert CustomError(amount, required)` | `sc_panic!("CustomError");` |

Typed custom error arguments are dropped and emit this warning:

```text
Custom error arguments dropped — MultiversX sc_panic only supports string messages
```

Use string message arguments for error context that should survive transpilation. Keep typed Solidity custom error fields as source-level metadata only; the generated MultiversX contract will not encode or expose them.

### Fallback and receive functions

Solidity `fallback()` and `receive()` declarations are converted to the MultiversX fallback entry point:

| Solidity input | Generated MultiversX Rust |
|---|---|
| `fallback() external` | `#[fallback] fn call(&self)` |
| `receive() external payable` | `#[payable("EGLD")]` + `#[fallback] fn call(&self)` |

Both mappings emit a `TranspilationWarning`. Review converted handlers manually because Solidity has separate dispatch for empty calldata payments and general fallback calls, while the generated MultiversX contract uses the `call` fallback entry point.

### Function visibility mapping

During conversion, visibility controls whether a Solidity function becomes a callable MultiversX endpoint:

| Solidity visibility and mutability | Generated MultiversX Rust |
|---|---|
| `public` / `external` | `#[endpoint]` for state-changing functions |
| `public view` / `external view` | `#[view(name)]` |
| `public pure` / `external pure` | `#[view(name)]` |
| `internal` / `private` | helper method with no endpoint or view annotation |

Internal and private Solidity functions are emitted for use by generated contract code, but they are not exposed as blockchain entry points. Pure functions are read-only and therefore use the same MultiversX `#[view]` annotation as Solidity view functions.

### Modifier inlining

Modifier definitions are parsed separately from function bodies. During function conversion, each applied modifier is inlined before the endpoint body for statements before `_;` and after the endpoint body for statements after `_;`.

Parameterized modifiers preserve their definition parameter names and their call-site arguments. Before conversion, parsed modifier statements substitute each parameter token with the matching call-site argument, so `onlyRole(adminRole)` inlines `role` references as `adminRole`.

Known edge cases:

- Argument substitution is token-based, not AST-based. It handles normal identifier parameters but should be reviewed for very complex modifier expressions.
- Modifier string literals are not rewritten during substitution.
- Inherited modifiers are not automatically imported; inherited contracts still require manual integration of parent modifiers and storage.

### Contract inheritance

The transpiler currently treats Solidity inheritance as an honest Rust supertrait stub. For example, `contract Child is Parent` emits `pub trait Child: Parent` plus a `TranspilationWarning` explaining that parent storage mappers and methods are not automatically inherited.

Before compiling or deploying an inherited contract, manually integrate the parent contract surface:

- Copy parent storage mapper declarations into the child trait when the child reads or writes parent state.
- Copy or compose required parent methods, modifiers, events, and initialization logic.
- Transpile the parent contract separately if you want to keep it as a separate trait, then import it and ensure the generated child trait has access to the required API.
- Review constructor and modifier behavior carefully, because Solidity base-constructor execution is not reproduced automatically.

Planned follow-up: replace the stub with explicit trait composition, including parent storage mapper copying for common single-inheritance cases and diagnostics for parent methods that must be declared or imported.

### Requires manual review
- Complex arithmetic expressions
- External contract calls
- Inheritance supertrait stubs; parent storage mappers, methods, and modifiers must be wired manually

### Cleanly stripped with TODO markers
- **Inline assembly** — replaced with `// TODO: inline assembly removed — no MultiversX equivalent`. Requires manual rewrite using Rust/SC APIs.
- **Try-catch blocks** — replaced with `// TODO: try-catch block removed — implement error handling manually`. Replace with async callbacks or `require!` guards.

### Cryptographic builtins (mapped with warnings)
- `keccak256(data)` → `self.crypto().keccak256(&data)` — input must be a `ManagedBuffer`
- `sha256(data)` → `self.crypto().sha256(&data)` — input must be a `ManagedBuffer`
- `ecrecover(hash, v, r, s)` → `ManagedAddress::zero() /* TODO */` — no on-chain equivalent; use off-chain verification

### Not yet supported
- Libraries, diamond inheritance
- `ecrecover` (stubbed with TODO and warning)

### Supported since v1.0
- Do-while loops → `loop { ... if !cond { break } }`
- `nonReentrant` modifier → full lock/unlock wrapper inlined
- Parameterized modifiers → definition parameters are replaced with call-site arguments before inlining
- `delete var` → `.clear()`
- `unchecked { }` → passthrough with comment
- Constructor parameters → emitted in `#[init]` signature with type mapping
- `msg.sender` → `self.blockchain().get_caller()`
- `block.timestamp` / `now` → `self.blockchain().get_block_timestamp()`
- `block.number` → `self.blockchain().get_block_nonce()`
- `address(this)` → `self.blockchain().get_sc_address()`
- `tx.origin` → `self.blockchain().get_caller()` + warning (see note below)
- `type(uint256).max` / `type(uint256).min` → `BigUint::from(u64::MAX)` / `BigUint::zero()` with TODO

> **`tx.origin` on MultiversX:** On EVM, `tx.origin` is the originating EOA; on MultiversX there is no such distinction — the caller is always the direct caller. XTract maps `tx.origin` to `get_caller()` and emits a warning. Review any access-control logic that relies on `tx.origin != msg.sender`.

### Constructor parameter mapping

Constructor parameters are carried through to the `#[init]` function using the same type-mapping rules as regular function parameters:

| Solidity type | MultiversX Rust type |
|---|---|
| `address` | `ManagedAddress<Self::Api>` |
| `uint256` | `BigUint<Self::Api>` |
| `uint128` / `uint64` / ... | `u128` / `u64` / ... |
| `bool` | `bool` |
| `bytes32` | `ManagedByteArray<Self::Api, 32>` |

Example: `constructor(address _owner, uint256 _supply)` becomes `fn init(&self, _owner: ManagedAddress<Self::Api>, _supply: BigUint<Self::Api>)`.

## Example: SimpleStorage

**Solidity:**
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

## Best Practices

1. **Start simple** — validate transpiler output on basic contracts before migrating complex DeFi logic.
2. **Always review output** — check generated function bodies, especially around arithmetic and state mutations.
3. **Payment handling** — Solidity's `msg.value` maps to `self.call_value().egld_value()` in MultiversX; payable functions are annotated with `#[payable("EGLD")]` automatically, including `receive() external payable` when it is mapped to `#[fallback] fn call(&self)`. `msg.sender` maps to `self.blockchain().get_caller()`. `msg.data` and `msg.sig` have no direct equivalent and emit TODO stubs with warnings — these require manual conversion.
4. **Test on devnet first** — use `--network devnet` until you're confident in the contract behaviour.
5. **Keep your mnemonic** — `xtract wallet create` shows it once; there is no recovery path.

## Troubleshooting

**`mxpy: command not found`**
```bash
pip install mxpy
```

**`ModuleNotFoundError: multiversx_sdk`** when using wallet/deploy commands
```bash
pip install xtract[deploy]
```

**Deploy transaction fails with "insufficient funds"**
Fund your wallet first via the devnet or testnet faucet:
- Devnet: https://devnet-wallet.multiversx.com/
- Testnet: https://testnet-wallet.multiversx.com/

**Generated Rust doesn't compile**
Open an issue at https://github.com/XTract-build/Xtract/issues with the Solidity input and the generated output.
