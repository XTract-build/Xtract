# XTract — Real-World Examples

This document walks through transpilation of a production-grade DEX contract,
showing exactly what XTract handles automatically and where manual review is
still needed.

---

## DexTokenSwap — Constant-Product AMM

**Location:** `demo/dex_tokenswap/`

A complete decentralised exchange implementing the x·y = k formula, with
deposit/withdraw liquidity management, a swap endpoint, and a price oracle view.

### Solidity source highlights

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DexTokenSwap {
    address public owner;
    bool public locked;                                         // ReentrancyGuard flag
    mapping(address => uint256) public reserves;               // per-token liquidity
    mapping(address => mapping(address => uint256)) public balances; // LP positions

    event Deposit(address indexed token, address indexed provider, uint256 amount);
    event Swap(address indexed tokenIn, address indexed tokenOut,
               address indexed trader, uint256 amountIn, uint256 amountOut);
    event Withdraw(address indexed token, address indexed provider, uint256 amount);

    modifier nonReentrant() {
        require(!locked, "Reentrant call");
        locked = true;
        _;
        locked = false;
    }

    function swap(address tokenIn, uint256 amountIn, address tokenOut)
        public nonReentrant
    {
        // ...
        uint256 amountOut = (amountIn * reserves[tokenOut])
                          / (reserves[tokenIn] + amountIn);
        // ...
    }
}
```

---

### What xtract generates automatically

Run:

```bash
xtract demo/dex_tokenswap/src/DexTokenSwap.sol \
        demo/dex_tokenswap/src/DexTokenSwap.rs
```

#### Storage mappers (A2 — dynamic detection)

Every state variable is detected at transpile time — no whitelist required
since the `fix/dynamic-storage-detection` (A2) merge.

| Solidity | Generated Rust |
|---|---|
| `address public owner` | `#[storage_mapper("owner")] fn owner() -> SingleValueMapper<ManagedAddress>` |
| `bool public locked` | `#[storage_mapper("locked")] fn locked() -> SingleValueMapper<bool>` |
| `mapping(address => uint256) public reserves` | `#[storage_mapper("reserves")] fn reserves(&self, key: &ManagedAddress) -> SingleValueMapper<BigUint>` |
| `mapping(address => mapping(address => uint256)) public balances` | `#[storage_mapper("balances")] fn balances(&self, key1: &ManagedAddress, key2: &ManagedAddress) -> SingleValueMapper<BigUint>` |

#### Events

```rust
#[event("Deposit")]
fn deposit_event(&self,
    #[indexed] token: &ManagedAddress<Self::Api>,
    #[indexed] provider: &ManagedAddress<Self::Api>,
    amount: &BigUint<Self::Api>);

#[event("Swap")]
fn swap_event(&self,
    #[indexed] tokenIn:  &ManagedAddress<Self::Api>,
    #[indexed] tokenOut: &ManagedAddress<Self::Api>,
    #[indexed] trader:   &ManagedAddress<Self::Api>,
    #[indexed] amountIn: &BigUint<Self::Api>,
    amountOut: &BigUint<Self::Api>);   // single data field
```

`indexed` attributes are preserved. MultiversX allows one non-indexed data
argument per event — `amountOut` becomes the data field.

#### Constructor

```rust
#[init]
fn init(&self) {
    self.owner().set(&(self.blockchain().get_caller()));
    self.locked().set(&false);
}
```

#### Modifier inlining — nonReentrant

```solidity
modifier nonReentrant() {
    require(!locked, "Reentrant call");
    locked = true;
    _;
    locked = false;
}
```

Currently expanded to the guard require at the top of each endpoint:

```rust
#[endpoint]
fn deposit(&self, token: ManagedAddress<Self::Api>, amount: BigUint<Self::Api>) {
    require!(!self.locked().get(), "Reentrant call");
    // …
}
```

The `locked = true / false` wrapper statements are added manually today;
full modifier body inlining is tracked as a future improvement.

#### Local variable declaration (A1)

```solidity
uint256 amountOut = (amountIn * reserves[tokenOut]) / (reserves[tokenIn] + amountIn);
```

Generated since `fix/variable-declaration-let-mut` (A1):

```rust
let mut amount_out: BigUint<Self::Api> =
    (&amountIn * &reserve_out) / (&reserve_in + &amountIn);
```

#### View functions

```solidity
function getPrice(address tokenIn, address tokenOut) public view returns (uint256)
```

```rust
#[view(getPrice)]
fn get_price(&self,
    tokenIn:  ManagedAddress<Self::Api>,
    tokenOut: ManagedAddress<Self::Api>,
) -> BigUint<Self::Api>
```

---

### What still requires a manual pass

| Gap | Workaround |
|---|---|
| Mapping reads in expressions: `self.reserves(&t)` needs `.get()` | Append `.get()` after generated mapper calls |
| Storage write statements (`reserves[t] = …`) not emitted | Add `self.reserves(&t).set(&new_val)` calls |
| `nonReentrant` lock/unlock wrapper not emitted | Add `self.locked().set(&true/false)` around body |

These are the only edits made to `DexTokenSwap.rs` beyond raw xtract output.
See the file header for the exact list.

---

### Build & deploy

```bash
# Build (from demo/dex_tokenswap/)
sc-meta all build
# → output/dex-token-swap.wasm  (~4 KB)

# Deploy to devnet
export WALLET_PEM=./wallet.pem
npx ts-node deploy.ts
```

See `demo/dex_tokenswap/README.md` for full instructions.

---

## Pattern reference

The DEX demo exercises the most common DeFi patterns. Use it as a
copy-paste reference when adapting XTract output for your own contracts.

### Nested mapping read

```rust
// Solidity: balances[token][msg.sender]
self.balances(&token, &caller).get()
```

### Nested mapping write

```rust
// Solidity: balances[token][msg.sender] = balances[token][msg.sender] + amount;
let new_val = self.balances(&token, &caller).get() + &amount;
self.balances(&token, &caller).set(&new_val);
```

### Constant-product swap formula

```rust
// amountOut = amountIn * reserveOut / (reserveIn + amountIn)
let reserve_in  = self.reserves(&tokenIn).get();
let reserve_out = self.reserves(&tokenOut).get();
let mut amount_out: BigUint<Self::Api> =
    (&amountIn * &reserve_out) / (&reserve_in + &amountIn);
```

### ReentrancyGuard with bool storage

```rust
require!(!self.locked().get(), "Reentrant call");
self.locked().set(&true);
// … endpoint body …
self.locked().set(&false);
```
