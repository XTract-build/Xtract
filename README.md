# XTract (v0.25)

[![CI](https://github.com/kaankacar/XTract/actions/workflows/ci.yml/badge.svg)](https://github.com/kaankacar/XTract/actions/workflows/ci.yml)
[![Tests](https://img.shields.io/badge/tests-100%25-success)](https://github.com/kaankacar/XTract/actions/workflows/ci.yml)

An open-source tool for converting Solidity smart contracts to MultiversX-compatible Rust smart contracts.

## Overview

XTract analyzes Solidity code and generates MultiversX Rust code that can be compiled and deployed on the MultiversX blockchain. It currently focuses on a core subset to enable fast iteration and testing.

## Version 0.25 ✅

This version introduces **statement-level code generation** with the following capabilities:
- **Function body transpilation**: Converts `require()`, `emit()`, `return`, and assignments
- **Error handling**: Maps Solidity `require()` → MultiversX `require!()` and `revert()` → `sc_panic!()`
- **Event emission**: Properly converts Solidity events to MultiversX event calls
- **Storage operations**: Handles variable assignments and storage access patterns
- **Single-level mapping support**: Converts `balanceOf[address]` → `self.balance_of(&address)` (tested and validated)

**Test Coverage**: 100% unit test success across 5+ Solidity contracts with comprehensive body validation.

For full implementation details, see the [v0.25 documentation](docs/v0.25/README.md).

## What it can do today

- Convert Solidity contracts to MultiversX Rust with the proper contract trait scaffold
- Detect and emit:
  - Functions (basic, including view vs endpoint detection)
  - Events (with indexed parameters)
  - Variable definitions (single value mappers for common types)
  - Structs
- **NEW**: Function body generation with statement transpilation
- **NEW**: Error handling patterns (`require`, `revert`)
- **NEW**: Event emission in function bodies
- Map common Solidity types to MultiversX equivalents (uint256, address, string, bool)
- Provide a simple CLI and comprehensive unit tests

## Early Adopter Guide

### Supported Patterns
✅ **Basic contracts**: SimpleStorage, ERC20 basic transfers, Voting systems
✅ **Events**: `emit EventName(args)` → `self.event_name_event(args)`
✅ **Error handling**: `require(condition, "msg")` → `require!(condition, "msg")`
✅ **Storage**: `variable = value` → `self.variable().set(&value)`
✅ **Returns**: `return expression` → `expression` (MultiversX style)

### Known Limitations & Rewrites
⚠️ **SpaceVM Push Model**: MultiversX uses explicit value transfer (users send tokens with calls) vs Ethereum's approval/pull model
⚠️ **Approvals**: ERC20 `approve`/`allowance` patterns don't map 1:1 - consider escrow or deposit patterns
⚠️ **Complex expressions**: Advanced Solidity expressions may need manual review
⚠️ **Inheritance**: Not yet supported - flatten contracts before transpilation

### Migration Strategy
1. **Start simple**: Test with basic contracts (SimpleStorage, simple transfers)
2. **Review generated code**: Check function bodies for correctness
3. **Adapt patterns**: Replace approvals with explicit transfers or escrow contracts
4. **Manual tuning**: Adjust complex logic that doesn't translate directly

## Getting Started

### Prerequisites

- Python 3.9+ (for Python CLI)
- Rust and Cargo (for Rust implementation)
- MultiversX SDK tools (for deployment)

### Installation

```bash
git clone https://github.com/XTract-build/Xtract.git
cd XTract

# Install Python CLI
python3 -m pip install --upgrade pip
python3 -m pip install -e .

# (optional) install test deps
python3 -m pip install pytest
```

After installing, the `xtract` CLI becomes available. If your system installs scripts under a user bin directory (e.g. `~/Library/Python/3.x/bin` on macOS), ensure it is on your PATH.

### Repository structure

```
XTract/
  xtract/            # Python package (CLI + core transpiler)
  tests/             # Unit tests for Python transpiler
  test_cases/        # Solidity inputs and expected Rust outputs
  rust-impl/         # Rust implementation (WIP)
  legacy/            # Legacy scripts, artifacts, and sample projects
  docs/              # Guides and technical documents
  .github/workflows/ # CI configuration
  pyproject.toml     # Python packaging config
```

### How XTract Works - Transpilation to Deployment Pipeline

XTract follows a clear pipeline from Solidity source code to deployed MultiversX contracts:

```
test_cases/solidity/*.sol          # 1. Solidity source files
  ↓ (xtract transpiler)
test_cases/expected/*.rs           # 2. Transpiled Rust output (direct transpiler output)
  ↓ (build_and_deploy_all.sh copies)
demo/*/src/lib.rs                  # 3. Build staging area (copied for compilation)
  ↓ (sc-meta build)
demo/*/output/*.wasm              # 4. Compiled WASM bytecode
  ↓ (mxpy deploy)
MultiversX Devnet                 # 5. Deployed smart contracts
```

**Key Points:**
- ✅ **Source**: All Solidity contracts start in `test_cases/solidity/`
- ✅ **Transpiled Output**: Python transpiler (`xtract/transpiler.py`) generates Rust code to `test_cases/expected/`
- ✅ **Deployment**: Scripts copy from `test_cases/expected/` to `demo/` for building and deployment
- ✅ **Direct Output**: Deployed contracts are **direct transpiler output** - no manual edits after transpilation
- ✅ **Verified**: All deployed contracts match their transpiler output (file comparison verified)

### Usage

#### Quick Start Guide

**1. Write Your Solidity Contract**

You can write your Solidity contract anywhere:
```bash
# Create a new contract file
touch my_contract.sol

# Or use the examples in test_cases/
vim test_cases/solidity/SimpleStorage.sol
```

**2. Run the Transpiler**

```bash
# Basic usage (output defaults to my_contract.rs)
python3 -m xtract.cli my_contract.sol

# Specify custom output location
python3 -m xtract.cli my_contract.sol output/my_contract.rs

# Transpile one of the built-in examples
python3 -m xtract.cli test_cases/solidity/SimpleStorage.sol
python3 -m xtract.cli test_cases/solidity/ERC20Token.sol
```

**3. Review Generated Code**

```bash
# View the transpiled MultiversX Rust contract
cat my_contract.rs
```

#### Complete Example

```bash
# Create a simple Solidity contract
cat > my_storage.sol << 'EOF'
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract MyStorage {
    uint256 public value;
    
    event ValueChanged(uint256 indexed newValue);
    
    function setValue(uint256 newValue) public {
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
python3 -m xtract.cli my_storage.sol

# Check the generated MultiversX Rust code
cat my_storage.rs
```

#### Python CLI (Recommended)

```bash
# Install the package
pip install -e .[dev]

# Use the transpiler (two options):

# Option 1: Python module (works immediately, recommended)
python3 -m xtract.cli <solidity_file.sol> [output.rs]

# Option 2: Direct command (if Python bin is in PATH)
xtract <solidity_file.sol> [output.rs]
```

**Note:** If `xtract` command is not found, use Option 1 or add `~/Library/Python/3.9/bin` to your PATH.

#### Alternative Methods

**Legacy script:**
```bash
python3 legacy/simplified_transpiler.py <solidity_file.sol> <output_file.rs>
```

**Rust Implementation (WIP):**
```bash
cd rust-impl
cargo run <solidity_file.sol>
```

## Examples

The `test_cases/` directory contains 5 fully working examples:
- **SimpleStorage.sol** - Basic storage with events and functions
- **ERC20Token.sol** - Basic token implementation with transfers
- **Voting.sol** - Voting system with proposals and vote tracking
- **NFTMarketplace.sol** - NFT marketplace with listing and sales
- **Crowdfunding.sol** - Campaign management with pledges and claims

Each example demonstrates different transpilation features and patterns.

## Documentation

### 📚 General Documentation
- **[docs/DEVELOPER_GUIDE.md](docs/DEVELOPER_GUIDE.md)** - Getting started guide and usage instructions (always up-to-date)

### 📦 Version-Specific Documentation

#### Current Version: v0.25 (Milestone 1) ✅
- **[docs/v0.25/](docs/v0.25/)** - Complete documentation for v0.25
  - [CHANGELOG.md](docs/v0.25/CHANGELOG.md) - Full release notes and features
  - [IMPLEMENTATION_REPORT.md](docs/v0.25/IMPLEMENTATION_REPORT.md) - Technical architecture
  - [TEST_RESULTS.md](docs/v0.25/TEST_RESULTS.md) - Test coverage and results
  - [IMPLEMENTATION_SUMMARY.md](docs/v0.25/IMPLEMENTATION_SUMMARY.md) - Feature details

## Roadmap - Milestone 2 (In Development)

**Milestone 2: Expanded Solidity Feature Support & Beta Release**

### Core Features
- **Nested Mappings**: Full support for `allowance[from][to]` patterns with comprehensive testing
- **Complex Mappings**: Arrays of mappings, mappings of structs, and advanced patterns
- **Modifiers**: Function modifiers and access control patterns
- **Basic Inheritance**: Contract inheritance structures and abstract contracts
- **Enhanced Error Handling**: Improved diagnostic messaging and error reporting
- **Advanced Expressions**: Complex arithmetic, conditionals, and loops
- **Type System**: Extended type mappings and custom type support

### Beta Release Goals
- **npm Package**: Published beta with easy installation
- **50+ Test Cases**: Expanded from current 5 to 50+ successfully converted contracts
- **80% Documentation**: Comprehensive coverage of all features
- **Community Feedback**: Active engagement through GitHub issues

**Target**: Beta release with production-ready support for most common Solidity patterns

## Testing & Validation

- Comprehensive test suite with 100% coverage of core transpilation features
- Integration tests with MultiversX chain simulator
- Performance benchmarks and gas optimization guidance

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.