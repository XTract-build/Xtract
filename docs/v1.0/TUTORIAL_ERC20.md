# Tutorial: ERC20 Token — End-to-End

This tutorial walks through transpiling a Solidity ERC20 contract to MultiversX Rust, building the WASM, deploying to devnet, and interacting with it using the TypeScript SDK.

---

## 1. The Solidity Source

The ERC20 contract is at `test_cases/solidity/ERC20Token.sol`:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ERC20Token {
    uint256 public totalSupply;
    uint256 public balance;

    event Transfer(address indexed from, address indexed to, uint256 value);

    constructor() {
        totalSupply = 1000000000000000000000000;
        balance = totalSupply;
    }

    function transfer(address _to, uint256 _value) public returns (bool success) {
        require(balance >= _value);
        balance = balance - _value;
        emit Transfer(msg.sender, _to, _value);
        return true;
    }
}
```

---

## 2. Transpile

```bash
xtract transpile test_cases/solidity/ERC20Token.sol -o erc20token/src/lib.rs
```

Or using the shorthand:

```bash
xtract test_cases/solidity/ERC20Token.sol
# writes ERC20Token.rs
```

The transpiler generates:

```rust
#![no_std]

use multiversx_sc::imports::*;
use multiversx_sc::derive_imports::*;

#[multiversx_sc::contract]
pub trait ERC20Token {
    #[storage_mapper("totalSupply")]
    fn total_supply(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("balance")]
    fn balance(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[event("Transfer")]
    fn transfer_event(
        &self,
        #[indexed] from: &ManagedAddress<Self::Api>,
        #[indexed] to: &ManagedAddress<Self::Api>,
        value: &BigUint<Self::Api>,
    );

    #[init]
    fn init(&self) {
        self.total_supply().set(BigUint::from(1000000000000000000000000u128));
        self.balance().set(self.total_supply().get());
    }

    #[endpoint]
    fn transfer(&self, _to: ManagedAddress<Self::Api>, _value: BigUint<Self::Api>) -> bool {
        require!(self.balance().get() >= _value, "");
        self.balance().set(self.balance().get() - &_value);
        self.transfer_event(&self.blockchain().get_caller(), &_to, &_value);
        true
    }
}
```

---

## 3. Build

Set up a MultiversX contract project layout. Your directory should look like:

```
erc20token/
  Cargo.toml         ← multiversx-sc dependency
  multiversx.json    ← contract metadata
  src/
    lib.rs           ← generated Rust from transpiler
  meta/
    Cargo.toml
    src/main.rs
  wasm/
    Cargo.toml
    src/lib.rs
```

See `demo/dex_tokenswap/` for a reference project layout.

Then build:

```bash
xtract build ./erc20token/
```

Expected output:

```
Building ./erc20token/ …
Running: mxpy contract build
✓  WASM  → ./erc20token/output/erc20-token.wasm
✓  ABI   → ./erc20token/output/erc20-token.abi.json
```

---

## 4. Create a Wallet

```bash
xtract wallet create
```

Fund your devnet wallet at: https://devnet-wallet.multiversx.com/

---

## 5. Deploy to Devnet

```bash
xtract deploy ./erc20token/output/erc20-token.wasm \
  --abi  ./erc20token/output/erc20-token.abi.json \
  --wallet ~/.multiversx/wallet.pem \
  --network devnet
```

Expected output:

```
Deploying to devnet…

✅  Contract deployed!
   Address : erd1qqq...abc123
   Tx hash : a1b2c3...
   Explorer: https://devnet-explorer.multiversx.com/transactions/a1b2c3...
```

---

## 6. Interact via TypeScript SDK

```typescript
import * as path from 'path';
import {
  ContractInteractor,
  WalletProvider,
} from 'xtract-cli/sdk';

const CONTRACT_ADDRESS = 'erd1qqq...abc123';   // from deploy output
const ABI_PATH         = './erc20token/output/erc20-token.abi.json';
const WALLET_PATH      = path.join(process.env.HOME!, '.multiversx/wallet.pem');

async function main() {
  const wallet = await WalletProvider.fromPemFile(WALLET_PATH);

  const interactor = new ContractInteractor(
    CONTRACT_ADDRESS,
    ABI_PATH,
    'devnet',
    wallet,
  );

  // ── Query totalSupply ────────────────────────────────────────────────────
  const [totalSupply] = await interactor.query('totalSupply');
  console.log('Total supply:', totalSupply.toString());

  // ── Query balance ────────────────────────────────────────────────────────
  const [balance] = await interactor.query('balance');
  console.log('Balance:', balance.toString());

  // ── Transfer tokens ──────────────────────────────────────────────────────
  const recipient = 'erd1...recipient';
  const amount    = BigInt('1000000000000000000');  // 1 token (18 decimals)

  const tx = await interactor.call('transfer', [recipient, amount]);
  console.log('Transfer tx:', tx.txHash);
  console.log('Explorer:', tx.explorerUrl);
}

main().catch(console.error);
```

---

## Notes on ERC20 vs ESDT

This tutorial transpiles the Solidity ERC20 pattern as-is — a contract that tracks balances internally. On MultiversX, production token contracts typically use the native **ESDT** protocol instead, which provides:

- Protocol-level balance tracking (no balance mapping in the contract)
- Native wallet/explorer support
- No approve/transferFrom pattern needed

For production token deployments, consider issuing an ESDT token using `mxpy` rather than deploying an ERC20-style contract. See [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md#erc20--esdt) for details.
