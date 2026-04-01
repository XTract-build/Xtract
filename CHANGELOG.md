# Changelog

### v1.0.0 (Stable Release)

#### Transpiler
- Fixed variable declaration stub — local vars now correctly emit let mut
- Dynamic storage variable detection replaces hardcoded whitelist
- Added do-while loop support
- Added unchecked block passthrough
- Added delete operation → .clear()
- Added SafeMath / using-for library inlining
- Added ABI encoding → ManagedBuffer serialization
- Added new ContractType() stub with diagnostic

#### SDK
- New TypeScript SDK (@xtract/sdk) — typed transpiler wrapper
- MultiversX deployment helpers (ContractDeployer, WalletProvider)
- Contract interaction helpers (ContractInteractor, QueryRunner)
- New CLI subcommands: build, deploy, scaffold

#### Samples
- 4 new deployable demo contracts (DEX, NFT Staking, DAO, Subscription)
- deploy.ts scripts for all 9 demo contracts
