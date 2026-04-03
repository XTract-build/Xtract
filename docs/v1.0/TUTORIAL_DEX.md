# Tutorial: DEX Token Swap — End-to-End

This tutorial walks through building and deploying the `DexTokenSwap` constant-product AMM from `demo/dex_tokenswap/`.

The contract implements x·y = k liquidity pools with deposit, withdraw, and swap endpoints.

---

## 1. Transpile + Build

### Transpile

```bash
xtract transpile demo/dex_tokenswap/src/DexTokenSwap.sol \
  -o demo/dex_tokenswap/src/DexTokenSwap.rs
```

The transpiler handles the full contract automatically:
- `locked` bool → `SingleValueMapper<bool>` (nonReentrant guard, lock+unlock inlined)
- `mapping(address => uint256) reserves` → single-key storage mapper
- `mapping(address => mapping(address => uint256)) balances` → two-key storage mapper
- All three events (`Deposit`, `Swap`, `Withdraw`) with indexed parameters
- `nonReentrant` modifier → `require!(!self.locked().get(), ...)` + `set(true)` / `set(false)` wrapper

### Build

```bash
xtract build ./demo/dex_tokenswap/
```

Expected output:

```
Building ./demo/dex_tokenswap/ …
Running: mxpy contract build
✓  WASM  → ./demo/dex_tokenswap/output/dex-token-swap.wasm
✓  ABI   → ./demo/dex_tokenswap/output/dex-token-swap.abi.json
```

A pre-built WASM is already committed at `demo/dex_tokenswap/output/dex-token-swap.wasm`.

---

## 2. Create a Wallet and Get Devnet EGLD

```bash
xtract wallet create
```

Fund your wallet:

1. Copy the printed `erd1...` address.
2. Open https://devnet-wallet.multiversx.com/
3. Go to **Faucet** and paste your address. You will receive 30 devnet EGLD.

---

## 3. Deploy the DEX Contract

```bash
xtract deploy demo/dex_tokenswap/output/dex-token-swap.wasm \
  --abi  demo/dex_tokenswap/output/dex-token-swap.abi.json \
  --wallet ~/.multiversx/wallet.pem \
  --network devnet
```

Expected output:

```
Deploying to devnet…

✅  Contract deployed!
   Address : erd1qqq...dex123
   Tx hash : abc123...
   Explorer: https://devnet-explorer.multiversx.com/transactions/abc123...
```

---

## 4. Issue Two ESDT Test Tokens

On MultiversX, tokens are protocol-level assets. Use `mxpy` to issue them:

```bash
# Issue token A
mxpy --verbose contract issue-esdt \
  --token-name=TokenA \
  --token-ticker=TKA \
  --supply=1000000000000000000000 \
  --decimals=18 \
  --pem ~/.multiversx/wallet.pem \
  --chain D \
  --proxy https://devnet-api.multiversx.com \
  --send

# Note the returned token identifier, e.g. TKA-abc123

# Issue token B
mxpy --verbose contract issue-esdt \
  --token-name=TokenB \
  --token-ticker=TKB \
  --supply=1000000000000000000000 \
  --decimals=18 \
  --pem ~/.multiversx/wallet.pem \
  --chain D \
  --proxy https://devnet-api.multiversx.com \
  --send

# Note: TKB-def456
```

---

## 5. Add Liquidity

```typescript
import * as path from 'path';
import {
  ContractInteractor,
  WalletProvider,
} from 'xtract-cli/sdk';

const CONTRACT_ADDRESS = 'erd1qqq...dex123';  // from deploy output
const ABI_PATH         = './demo/dex_tokenswap/output/dex-token-swap.abi.json';
const WALLET_PATH      = path.join(process.env.HOME!, '.multiversx/wallet.pem');

// Token identifiers from the issue step above
const TOKEN_A = 'TKA-abc123';
const TOKEN_B = 'TKB-def456';

async function main() {
  const wallet = await WalletProvider.fromPemFile(WALLET_PATH);
  const interactor = new ContractInteractor(
    CONTRACT_ADDRESS,
    ABI_PATH,
    'devnet',
    wallet,
  );

  // Deposit 1000 units of Token A
  console.log('Depositing Token A…');
  const depositA = await interactor.call(
    'deposit',
    [TOKEN_A, BigInt('1000000000000000000000')],  // token address, amount
  );
  console.log('Deposit A tx:', depositA.txHash);

  // Deposit 2000 units of Token B
  console.log('Depositing Token B…');
  const depositB = await interactor.call(
    'deposit',
    [TOKEN_B, BigInt('2000000000000000000000')],
  );
  console.log('Deposit B tx:', depositB.txHash);
```

---

## 6. Execute a Swap

```typescript
  // Swap 10 Token A for Token B
  const amountIn = BigInt('10000000000000000000');  // 10 TKA

  console.log('Swapping Token A → Token B…');
  const swap = await interactor.call(
    'swap',
    [TOKEN_A, amountIn, TOKEN_B],
  );
  console.log('Swap tx:', swap.txHash);
  console.log('Explorer:', swap.explorerUrl);
```

---

## 7. Query Price and Reserves

```typescript
  // Query reserves
  const [reserveA] = await interactor.query('getReserve', [TOKEN_A]);
  const [reserveB] = await interactor.query('getReserve', [TOKEN_B]);
  console.log('Reserve A:', reserveA.toString());
  console.log('Reserve B:', reserveB.toString());

  // Query spot price (scaled by 1e18)
  const [price] = await interactor.query('getPrice', [TOKEN_A, TOKEN_B]);
  console.log('Price TKA→TKB (×1e18):', price.toString());
}

main().catch(console.error);
```

---

## Contract Reference

| Endpoint | Visibility | Description |
|---|---|---|
| `deposit(token, amount)` | `#[endpoint]` | Add liquidity for a token |
| `withdraw(token, amount)` | `#[endpoint]` | Remove liquidity |
| `swap(tokenIn, amountIn, tokenOut)` | `#[endpoint]` | Constant-product swap |
| `getPrice(tokenIn, tokenOut)` | `#[view]` | Spot price scaled by 1e18 |
| `getReserve(token)` | `#[view]` | Total reserve for a token |

All state-changing endpoints are `nonReentrant` (reentrancy guard inlined by the transpiler).

---

## See Also

- [REAL_WORLD_EXAMPLES.md](../../REAL_WORLD_EXAMPLES.md) — detailed breakdown of what XTract generates for this contract
- [MIGRATION_GUIDE.md](MIGRATION_GUIDE.md) — ERC20 vs ESDT, cross-contract calls
- `demo/dex_tokenswap/deploy.ts` — programmatic deploy + smoke test script
