# Getting Started with XTract v1.0

A 5-minute quickstart for EVM developers.

---

## 1. Installation

### Prerequisites

| Requirement | Version | Notes |
|---|---|---|
| Python | >= 3.9 | Required for the transpiler and deploy pipeline |
| Node.js | >= 18 | Required for the CLI npm package and TypeScript SDK |
| mxpy | latest | Required for `xtract build` |
| Rust + wasm32 target | stable | Required for building contracts |

```bash
# Python transpiler — transpile only
pip install xtract

# Full pipeline (transpile + wallet creation + deployment)
pip install xtract[deploy]

# CLI tool and TypeScript SDK (npm)
npm install -g xtract-cli

# mxpy (required for build step)
pip install mxpy

# Rust wasm target (required for build step)
rustup target add wasm32-unknown-unknown
cargo install multiversx-sc-meta
```

---

## 2. Hello World — Transpile a Solidity Contract

Create a simple Solidity file:

```solidity
// SimpleStorage.sol
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

Transpile it:

```bash
xtract SimpleStorage.sol
```

Or with the explicit subcommand and output path:

```bash
xtract transpile SimpleStorage.sol -o SimpleStorage.rs
```

Expected output:

```
Transpiling SimpleStorage.sol...
✓  Written SimpleStorage.rs
```

The generated `SimpleStorage.rs` is a MultiversX-ready Rust smart contract using the `multiversx-sc` framework.

---

## 3. Create a Wallet

```bash
xtract wallet create
```

Expected output:

```
Generating BIP39 wallet...

Address  : erd1qqqqqqqqqqqqqpgq...
Mnemonic : word1 word2 word3 word4 word5 word6 word7 word8 word9 word10
           word11 word12 word13 word14 word15 word16 word17 word18
           word19 word20 word21 word22 word23 word24

Saved to : /Users/you/.multiversx/wallet.pem

⚠  Save your mnemonic — it is shown only once and cannot be recovered.

Fund your wallet before deploying:
  Devnet : https://devnet-wallet.multiversx.com/
  Testnet: https://testnet-wallet.multiversx.com/
```

To save to a custom path:

```bash
xtract wallet create --output ./my_wallet.pem
```

---

## 4. Build the Contract

After placing the transpiled `.rs` file inside a MultiversX contract project (with a `Cargo.toml` and `multiversx.json`):

```bash
xtract build ./my_contract/
```

Expected output:

```
Building ./my_contract/ …
Running: mxpy contract build
✓  WASM  → ./my_contract/output/my-contract.wasm
✓  ABI   → ./my_contract/output/my-contract.abi.json
```

Requires `mxpy` and `sc-meta` on `PATH`. See [demo/dex_tokenswap/](../../demo/dex_tokenswap/) for a complete project layout example.

---

## 5. Deploy to Devnet

```bash
xtract deploy ./my_contract/output/my-contract.wasm \
  --abi    ./my_contract/output/my-contract.abi.json \
  --wallet ~/.multiversx/wallet.pem \
  --network devnet
```

Expected output:

```
Deploying to devnet…

✅  Contract deployed!
   Address : erd1qqq...abc123
   Tx hash : a1b2c3d4e5f6...
   Explorer: https://devnet-explorer.multiversx.com/transactions/a1b2c3d4e5f6...
```

Deploy options:

| Flag | Default | Description |
|---|---|---|
| `--network` | `devnet` | `devnet`, `testnet`, or `mainnet` |
| `--gas-limit N` | `10000000` | Gas limit for the deploy transaction |
| `--no-upgrade` | upgradeable | Deploy as non-upgradeable contract |

---

## Full Pipeline in One Script

```bash
# Install
pip install xtract[deploy]
pip install mxpy

# Transpile
xtract MyToken.sol
# → MyToken.rs

# (Set up Cargo project around MyToken.rs, then:)

# Build
xtract build ./my_token/
# → ./my_token/output/my_token.wasm + my_token.abi.json

# Create wallet (first time only)
xtract wallet create
# prints address + 24-word mnemonic — save it
# fund at: https://devnet-wallet.multiversx.com/

# Deploy
xtract deploy ./my_token/output/my_token.wasm \
  --abi ./my_token/output/my_token.abi.json \
  --wallet ~/.multiversx/wallet.pem \
  --network devnet
# ✅ Contract deployed!
#    Address : erd1qqq...
#    Tx hash : ...
```

---

## Next Steps

- [TRANSPILER_REFERENCE.md](TRANSPILER_REFERENCE.md) — full Solidity feature coverage table
- [SDK_REFERENCE.md](SDK_REFERENCE.md) — TypeScript SDK API
- [TUTORIAL_ERC20.md](TUTORIAL_ERC20.md) — end-to-end ERC20 walkthrough
- [TUTORIAL_DEX.md](TUTORIAL_DEX.md) — end-to-end DEX walkthrough
- [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) — EVM → MultiversX concept mapping
