# XTract (v1.0.0)

[![CI](https://github.com/XTract-build/Xtract/actions/workflows/ci.yml/badge.svg)](https://github.com/XTract-build/Xtract/actions/workflows/ci.yml)
[![Tests](https://img.shields.io/badge/tests-100%25-success)](https://github.com/XTract-build/Xtract/actions/workflows/ci.yml)
[![npm](https://img.shields.io/npm/v/xtract-cli)](https://www.npmjs.com/package/xtract-cli)
[![PyPI](https://img.shields.io/pypi/v/xtract)](https://pypi.org/project/xtract/)

An open-source tool for converting Solidity smart contracts to MultiversX-compatible Rust smart contracts.

## Quick Start

```bash
# Install
pip install xtract           # transpile only
pip install xtract[deploy]   # + wallet creation and on-chain deployment

# 1. Transpile Solidity → Rust
xtract MyContract.sol        # writes MyContract.rs

# 2. Build Rust → WASM  (requires mxpy)
xtract build ./my_contract/

# 3. Create a wallet (first time)
xtract wallet create         # saves to ~/.multiversx/wallet.pem
#    → prints your address and funding URLs for devnet/testnet

# 4. Deploy
xtract deploy ./my_contract/output/my_contract.wasm \
  --abi ./my_contract/output/my_contract.abi.json \
  --wallet ~/.multiversx/wallet.pem \
  --network devnet
#    → prints contract address and explorer link
```

**npm package:** [https://www.npmjs.com/package/xtract-cli](https://www.npmjs.com/package/xtract-cli)

## Overview

XTract analyzes Solidity code and generates MultiversX Rust code that can be compiled and deployed on the MultiversX blockchain. It supports a comprehensive set of Solidity features including control flow, mappings, modifiers, and inheritance.

## v1.0.0 — What's New

v1.0 adds the full deployment pipeline on top of the transpiler. See [docs/v1.0/CHANGELOG.md](docs/v1.0/CHANGELOG.md) for the complete change list.

### New in v1.0
- **`xtract build`** — compiles transpiled Rust to WASM via `mxpy`
- **`xtract wallet create`** — generates a BIP39 wallet, saves as PEM
- **`xtract deploy`** — deploys compiled WASM to devnet/testnet/mainnet
- **`pip install xtract[deploy]`** — optional dep group for the above
- **TypeScript SDK** — `xtract-cli/sdk` exposes `XtractTranspiler` and `ContractDeployer`

### Transpiler Features

### Core Features
- **Function body transpilation**: Converts `require()`, `emit()`, `return`, and assignments
- **Error handling**: Maps Solidity `require()` → MultiversX `require!()` and `revert()` → `sc_panic!()`
- **Event emission**: Properly converts Solidity events to MultiversX event calls
- **Storage operations**: Handles variable assignments and storage access patterns

### Mapping Support
- **Single mappings**: `mapping(address => uint256)` → storage mappers with key parameters
- **Nested mappings**: `mapping(address => mapping(address => uint256))` → multi-key storage mappers

### Control Flow
- **If/else statements**: Full if/else transpilation with proper Rust syntax
- **For loops**: Counter-based loops transpiled to `for i in 0..n` syntax
- **While loops**: While loop transpilation with condition conversion
- **Payable functions**: Automatic `#[payable("EGLD")]` annotation

### Advanced Features
- **Function modifiers**: `onlyOwner`, `whenNotPaused`, custom modifiers
- **Basic inheritance**: Contract inheritance with supertrait generation
- **Enhanced diagnostics**: Detailed warnings for unsupported features and semantic differences, including `int256` casts that rely on MultiversX `BigInt` negative values

### Signed Integer Limitation

`int8`, `int16`, `int32`, and `int64` casts map to Rust `i8`, `i16`, `i32`, and `i64`. `int256` maps to MultiversX `BigInt<Self::Api>`, which has more limited negative number support than Solidity `int256`; review warnings on negative literals or variable casts before relying on equivalent storage or arithmetic behavior.

**Test Coverage**: 100% unit test success across 50 Solidity contracts with 64 test functions.

## TypeScript SDK

The `xtract-cli` package bundles a full TypeScript SDK for programmatic use:

```typescript
import { XtractTranspiler, ContractDeployer } from 'xtract-cli/sdk';

// Transpile Solidity to Rust
const transpiler = new XtractTranspiler();
const result = await transpiler.transpileCode('contract Foo { uint x; }');
console.log(result.rustCode);

// Deploy compiled contract to MultiversX
const deployer = new ContractDeployer();
const deployed = await deployer.deploy({
  network: 'devnet',
  wasmPath: './output/foo.wasm',
  abiPath: './output/foo.abi.json',
  walletPath: './wallet.pem',
});
console.log(deployed.contractAddress);
```

> **Prerequisite:** the SDK shells out to the Python transpiler — `pip install xtract` must be run first (Python 3.9+).

## Installation

```bash
# Transpile only (lightweight — just click)
pip install xtract

# Full pipeline: transpile + build wrapper + wallet + deploy
pip install xtract[deploy]

# CLI tool for npm users (includes TypeScript SDK)
npm install -g xtract-cli
```

`mxpy` is required separately for the `xtract build` command:
```bash
pip install mxpy
```

## CLI Reference

```bash
# Transpile
xtract transpile MyContract.sol              # → MyContract.rs
xtract transpile MyContract.sol -o output.rs
xtract transpile -v MyContract.sol           # verbose diagnostics
xtract transpile --json MyContract.sol       # JSON to stdout

# Flags can be passed before the file without the 'transpile' subcommand:
xtract --json MyContract.sol       # shorthand for 'xtract transpile --json'
xtract -v MyContract.sol           # shorthand for 'xtract transpile -v'

# Build (requires mxpy)
xtract build ./my_contract/

# Wallet  (requires xtract[deploy])
xtract wallet create
xtract wallet create --output ./wallet.pem

# Faucet  (requires xtract[deploy])
xtract faucet                            # devnet EGLD → default wallet
xtract faucet --network testnet
xtract faucet --address erd1...          # by address

# Deploy  (requires xtract[deploy])
xtract deploy ./output/my_contract.wasm \
  --abi    ./output/my_contract.abi.json \
  --wallet ~/.multiversx/wallet.pem \
  --network devnet          # devnet | testnet | mainnet
```

### Quick Example

```bash
# Create a simple Solidity contract
cat > MyStorage.sol << 'EOF'
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MyStorage {
    uint256 public value;
    address public owner;

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    event ValueChanged(uint256 indexed newValue);

    constructor() {
        owner = msg.sender;
    }

    function setValue(uint256 newValue) public onlyOwner {
        require(newValue > 0, "Value must be positive");
        value = newValue;
        emit ValueChanged(newValue);
    }

    function getValue() public view returns (uint256) {
        return value;
    }
}
EOF

# Transpile it
xtract MyStorage.sol

# View the generated MultiversX Rust code
cat MyStorage.rs
```

## Supported Solidity Features

### Fully Supported
- Contract declarations, constructors (with parameters) mapped to `#[init]`, state variables
- Single and nested mappings
- Events with indexed parameters
- Custom errors, structs
- Functions (public, private, view, payable)
- `msg.value` → `self.call_value().egld_value()`
- `msg.sender` → `self.blockchain().get_caller()`
- Function modifiers — full pre/post body inlining, including `nonReentrant`
- Basic inheritance (`contract A is B, C`)
- `require` / `revert`, if/else, for loops, while loops, do-while loops
- Ternary expressions (`cond ? a : b` → `if cond { a } else { b }`)
- `delete var` → `.clear()`, `unchecked { }` passthrough
- `SafeMath` / `using-for` → inlined arithmetic operators
- `bytes` / `bytes32` casts from string and hex literals → `ManagedBuffer`

### Requires Manual Review
- Complex arithmetic expressions
- External contract calls
- `bytes` / `bytes32` casts from numeric or unknown input types

### Cleanly Stripped with TODO Markers
- **Inline assembly** — replaced with `// TODO: inline assembly removed — no MultiversX equivalent`
- **Try-catch blocks** — replaced with `// TODO: try-catch block removed — implement error handling manually`

### Not Yet Supported
- Libraries
- Diamond inheritance

## Examples

The `test_cases/` directory contains 50 fully working examples including:

| Category | Examples |
|----------|----------|
| Basic | SimpleStorage, Counter, Config |
| Tokens | ERC20Token, SimpleToken, TokenMinter |
| NFTs | NFTMarketplace, Certificate, Badge |
| DeFi | Staking, RewardPool, TokenSwap, Vesting |
| Governance | Voting, Governance, Poll, Multisig |
| Access Control | OnlyOwner, AccessControl, Pausable |
| Patterns | Escrow, Auction, Lottery, Vault |

## Documentation

### Current version
- **[docs/v1.0/GETTING_STARTED.md](docs/v1.0/GETTING_STARTED.md)** — 5-minute quickstart for EVM developers
- **[docs/v1.0/TRANSPILER_REFERENCE.md](docs/v1.0/TRANSPILER_REFERENCE.md)** — full Solidity feature coverage table and `--json` output format
- **[docs/v1.0/SDK_REFERENCE.md](docs/v1.0/SDK_REFERENCE.md)** — TypeScript SDK API reference
- **[docs/v1.0/MIGRATION_GUIDE.md](docs/v1.0/MIGRATION_GUIDE.md)** — EVM → MultiversX concept mapping
- **[docs/v1.0/TUTORIAL_ERC20.md](docs/v1.0/TUTORIAL_ERC20.md)** — end-to-end ERC20 walkthrough
- **[docs/v1.0/TUTORIAL_DEX.md](docs/v1.0/TUTORIAL_DEX.md)** — end-to-end DEX walkthrough
- **[docs/v1.0/README.md](docs/v1.0/README.md)** — v1.0 feature overview and full pipeline walkthrough
- **[docs/v1.0/CHANGELOG.md](docs/v1.0/CHANGELOG.md)** — what changed from v0.30 to v1.0
- **[docs/DEVELOPER_GUIDE.md](docs/DEVELOPER_GUIDE.md)** — CLI reference, Python API, TypeScript SDK, type mapping

## Repository Structure

```
XTract/
  xtract/            # Python package
    transpiler.py    #   Solidity parser and Rust emitter
    cli.py           #   CLI entry point (transpile / build / wallet / deploy)
    build.py         #   mxpy contract build wrapper
    wallet.py        #   BIP39 wallet generation
    deploy.py        #   Contract deployment via multiversx-sdk
  sdk/               # TypeScript SDK (bundled into xtract-cli npm package)
  tests/             # Python unit tests (64 test functions)
  test_cases/        # Solidity inputs and expected Rust outputs (50 contracts)
  docs/              # Documentation
  .github/workflows/ # CI configuration
  package.json       # xtract-cli npm package
  pyproject.toml     # Python packaging config
```

## How It Works

XTract follows a clear pipeline from Solidity source code to MultiversX Rust:

```
Solidity Source (.sol)
        ↓  xtract MyContract.sol
┌─────────────────────┐
│  Transpiler         │
│  (parse + emit)     │
└──────────┬──────────┘
           ↓
   Rust Source (.rs)
        ↓  xtract build ./my_contract/
┌─────────────────────┐
│  mxpy contract      │
│  build              │
└──────────┬──────────┘
           ↓
   WASM + ABI
        ↓  xtract deploy ...
┌─────────────────────┐
│  multiversx-sdk     │
│  (sign + broadcast) │
└──────────┬──────────┘
           ↓
  Live contract on MultiversX
```

## Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_transpiler_core.py::test_nested_mapping_features -v

# Run with coverage
pytest tests/ --cov=xtract
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
