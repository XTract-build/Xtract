# XTract v1.0 — Release Overview

XTract is a Solidity to MultiversX Rust transpiler. v1.0 is the first stable release and introduces the **full deployment pipeline**: transpile, build, create a wallet, and deploy — all from a single tool.

## What's New in v1.0

### Full Deployment Pipeline

Previous releases only handled transpilation. v1.0 adds the remaining steps so you can go from a `.sol` file to a live contract without leaving XTract:

| Step | Command | Requires |
|------|---------|----------|
| Transpile Solidity → Rust | `xtract MyContract.sol` | `pip install xtract` |
| Compile Rust → WASM | `xtract build ./my_contract/` | `mxpy` |
| Create a wallet | `xtract wallet create` | `pip install xtract[deploy]` |
| Deploy to chain | `xtract deploy ...` | `pip install xtract[deploy]` |

### New Commands

#### `xtract build`

Shells out to `mxpy contract build` inside the given contract directory.

```bash
xtract build ./my_contract/
```

Requires `mxpy` to be installed. Outputs `./my_contract/output/*.wasm` and `*.abi.json`.

#### `xtract wallet create`

Generates a new BIP39 wallet and saves it as a PEM file.

```bash
xtract wallet create
# Saved to: ~/.multiversx/wallet.pem  (default)

xtract wallet create --output ./my_wallet.pem
```

Prints the wallet address and mnemonic (shown once — save it). Also prints funding URLs for devnet and testnet since there is no programmatic faucet API.

#### `xtract deploy`

Deploys a compiled WASM contract to devnet, testnet, or mainnet.

```bash
xtract deploy ./my_contract/output/my_contract.wasm \
  --abi ./my_contract/output/my_contract.abi.json \
  --wallet ~/.multiversx/wallet.pem \
  --network devnet
```

Options:
- `--network` — `devnet` (default), `testnet`, or `mainnet`
- `--gas-limit` — gas for the deploy transaction (default: 10 000 000)
- `--no-upgrade` — deploy as non-upgradeable contract

Prints contract address, transaction hash, and explorer link on success.

### TypeScript SDK

The `xtract-cli` npm package now bundles a TypeScript SDK for programmatic use of both transpilation and deployment:

```typescript
import { XtractTranspiler, ContractDeployer } from 'xtract-cli/sdk';

const transpiler = new XtractTranspiler();
const result = await transpiler.transpileCode('contract Foo { uint x; }');

const deployer = new ContractDeployer();
const deployed = await deployer.deploy({
  network: 'devnet',
  wasmPath: './output/foo.wasm',
  abiPath: './output/foo.abi.json',
  walletPath: './wallet.pem',
});
console.log(deployed.contractAddress);
```

## Full Workflow Example

```bash
# Install
pip install xtract[deploy]

# 1. Transpile
xtract MyToken.sol
# → MyToken.rs

# Set up a MultiversX contract project around MyToken.rs, then:

# 2. Build
xtract build ./my_token/
# → ./my_token/output/my_token.wasm
# → ./my_token/output/my_token.abi.json

# 3. Create a wallet (first time only)
xtract wallet create
# Address: erd1...
# Mnemonic: word1 word2 ... word24  ← save this
# Fund at: https://devnet-wallet.multiversx.com/

# 4. Deploy
xtract deploy ./my_token/output/my_token.wasm \
  --abi ./my_token/output/my_token.abi.json \
  --wallet ~/.multiversx/wallet.pem \
  --network devnet
# ✅ Contract deployed!
#    Address : erd1qqq...
#    Tx hash : a1b2c3...
#    Explorer: https://devnet-explorer.multiversx.com/transactions/a1b2c3...
```

## Installation

```bash
# Transpile only
pip install xtract

# Full pipeline (transpile + build wrapper + wallet + deploy)
pip install xtract[deploy]

# CLI tool (includes TypeScript SDK)
npm install -g xtract-cli
```

## Supported Solidity Features

Inherited from v0.30.1 — see [docs/v0.30/README.md](../v0.30/README.md) for the complete feature matrix.

## Network Reference

| Network | API | Explorer |
|---------|-----|----------|
| Devnet | `https://devnet-api.multiversx.com` | `https://devnet-explorer.multiversx.com` |
| Testnet | `https://testnet-api.multiversx.com` | `https://testnet-explorer.multiversx.com` |
| Mainnet | `https://api.multiversx.com` | `https://explorer.multiversx.com` |
