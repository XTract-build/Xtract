# Changelog — v1.0.0

## v1.0.0

### Breaking changes

- `xtract` is now a command group. `xtract MyContract.sol` still works unchanged via a compatibility shim, but the canonical subcommand is `xtract transpile MyContract.sol`.

### New features

- **`xtract build <dir>`** — wraps `mxpy contract build`; compiles Rust contract to WASM inside the given directory.
- **`xtract wallet create [--output path]`** — generates a BIP39 wallet, saves it as a PEM file (default: `~/.multiversx/wallet.pem`), prints the mnemonic and devnet/testnet faucet URLs.
- **`xtract deploy <wasm> --abi <abi> --wallet <pem> --network <net>`** — deploys a compiled WASM contract via `multiversx-sdk`; supports devnet, testnet, and mainnet; prints contract address and explorer link.
- **`pip install xtract[deploy]`** — new optional dependency group that pulls in `multiversx-sdk>=2.0.0`. The base `pip install xtract` remains lightweight (only `click`).
- **TypeScript SDK** — `xtract-cli` npm package now exposes `XtractTranspiler` and `ContractDeployer` at `xtract-cli/sdk` for programmatic pipeline use.
- **Python API** — `build_contract`, `create_wallet`, `WalletInfo`, `deploy_contract`, and `DeployResult` are now exported from the top-level `xtract` package.

### Changes

- `sdk/package.json` marked `private: true` — the SDK is distributed as part of `xtract-cli`, not as a standalone npm package.
- CI expanded: Python matrix now covers 3.9–3.12; new `sdk` job installs `xtract` from source then builds and tests the TypeScript SDK.
- `README.md` updated with full 4-step pipeline quick start.
- `docs/DEVELOPER_GUIDE.md` updated to reflect current package structure and commands.

### Previous releases

- [v0.30.1 release notes](../v0.30/README.md)
- [v0.25 release notes](../v0.25/README.md)
