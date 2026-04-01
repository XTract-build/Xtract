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
| `T[]` | `VecMapper<Self::Api, T>` |
| `T[N]` | `ArrayMapper<Self::Api, T, N>` |

## Supported Solidity Features

### Fully supported
- Contract declarations, constructors, state variables
- Single and nested mappings
- Events with indexed parameters
- Custom errors, structs
- Public/private/view/payable functions
- Function modifiers (`onlyOwner`, custom)
- Basic inheritance (`contract A is B, C`)
- `require` / `revert`, if/else, for loops, while loops
- Automatic `#[payable("EGLD")]` annotation

### Requires manual review
- Complex arithmetic expressions
- External contract calls

### Not yet supported
- Do-while loops, inline assembly, try-catch
- Libraries, diamond inheritance

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
3. **Payment handling** — Solidity's `msg.value` / ether model maps to `#[payable("EGLD")]` in MultiversX; review payable functions carefully.
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
