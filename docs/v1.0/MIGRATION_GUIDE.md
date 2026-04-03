# Migration Guide: EVM → MultiversX

This guide covers the conceptual and syntactic differences EVM developers encounter when moving Solidity contracts to MultiversX Rust via XTract.

---

## Error Handling

### `try-catch` → Async Callbacks

MultiversX has no synchronous try-catch for cross-contract calls. Use async callback patterns:

**Solidity:**
```solidity
try externalContract.someCall() returns (uint256 result) {
    // success
} catch {
    // failure
}
```

**MultiversX Rust:**
```rust
// Cross-contract calls are async; use #[callback] to handle results
self.tx()
    .to(&external_address)
    .gas(10_000_000u64)
    .typed(ExternalContractProxy)
    .some_call()
    .with_result(OriginalCaller::new(self.blockchain().get_caller()))
    .async_call_and_exit();

#[callback]
fn some_call_callback(
    &self,
    #[call_result] result: ManagedAsyncCallResult<BigUint>,
) {
    match result {
        ManagedAsyncCallResult::Ok(value) => { /* success */ }
        ManagedAsyncCallResult::Err(err) => { /* failure */ }
    }
}
```

### `require()` → `require!()`

XTract transpiles this automatically.

```solidity
require(amount > 0, "Must be positive");
```
```rust
require!(amount > BigUint::zero(), "Must be positive");
```

### `revert()` → `sc_panic!()`

```solidity
revert("Not allowed");
```
```rust
sc_panic!("Not allowed");
```

---

## Proxy Patterns

### `delegatecall` → Composability / Proxy Contracts

`delegatecall` has no MultiversX equivalent. Use the composability pattern — deploy a separate contract and call it via async cross-contract calls, or use a shared storage layout with the `multiversx_sc_modules` proxy helpers.

---

## Cross-Contract Calls

**Solidity:**
```solidity
IToken(tokenAddress).transfer(recipient, amount);
```

**MultiversX Rust:**
```rust
// Define a proxy interface
mod token_proxy {
    multiversx_sc::imports!();
    #[multiversx_sc::proxy]
    pub trait Token {
        #[endpoint]
        fn transfer(&self, recipient: ManagedAddress, amount: BigUint);
    }
}

// Call it
self.tx()
    .to(&token_address)
    .typed(token_proxy::TokenProxy)
    .transfer(recipient, amount)
    .async_call_and_exit();
```

---

## Token Standards

### ERC20 → ESDT

ESDT (eStandard Digital Token) is a fundamental difference from ERC20:

| EVM (ERC20) | MultiversX (ESDT) |
|---|---|
| Contract-level balance mapping | Protocol-level balance ledger |
| `transfer()` updates a mapping in the contract | Protocol routes token transfers natively |
| Approve/transferFrom for DeFi composability | No approve needed; direct ESDT transfers |
| `msg.value` for ETH | `#[payable("EGLD")]` + `self.call_value().egld_value()` |
| ERC20 `transferFrom` in DeFi | ESDT `ESDTTransfer` built-in function |

**To receive ESDT in a contract:**
```rust
#[payable("*")]
#[endpoint]
fn deposit(&self) {
    let (token_id, amount) = self.call_value().single_fungible_esdt();
    // token_id: TokenIdentifier, amount: BigUint
}
```

---

## Context Variables

| Solidity | MultiversX Rust |
|---|---|
| `msg.sender` | `self.blockchain().get_caller()` |
| `msg.value` (ETH) | `self.call_value().egld_value()` (EGLD) |
| `block.timestamp` | `self.blockchain().get_block_timestamp()` |
| `block.number` | `self.blockchain().get_block_nonce()` |
| `address(this).balance` | `self.blockchain().get_sc_balance(&EgldOrEsdtTokenIdentifier::egld(), 0)` |
| `address(this)` | `self.blockchain().get_sc_address()` |
| `tx.origin` | `self.blockchain().get_owner_address()` (not exactly equivalent) |

---

## Payments

### Sending EGLD

**Solidity:**
```solidity
payable(recipient).transfer(amount);
```

**MultiversX Rust:**
```rust
self.tx()
    .to(&recipient)
    .egld(&amount)
    .transfer();
```

### Receiving EGLD

**Solidity:**
```solidity
function deposit() public payable { ... }
```

**MultiversX Rust:**
```rust
#[payable("EGLD")]
#[endpoint]
fn deposit(&self) {
    let amount = self.call_value().egld_value().clone_value();
    // ...
}
```

---

## Events

### `emit EventName(...)` → `self.event_name_event().emit(...)`

**Solidity:**
```solidity
event Transfer(address indexed from, address indexed to, uint256 value);

emit Transfer(sender, recipient, amount);
```

**MultiversX Rust:**
```rust
#[event("Transfer")]
fn transfer_event(
    &self,
    #[indexed] from: &ManagedAddress<Self::Api>,
    #[indexed] to: &ManagedAddress<Self::Api>,
    value: &BigUint<Self::Api>,
);

// Emit:
self.transfer_event(&sender, &recipient, &amount);
```

XTract generates the event declaration and call automatically.

---

## Ownership Patterns

### `onlyOwner`

**Solidity:**
```solidity
modifier onlyOwner() {
    require(msg.sender == owner, "Not owner");
    _;
}
```

**MultiversX Rust (XTract output):**
```rust
// Inlined into each endpoint:
let caller = self.blockchain().get_caller();
require!(caller == self.owner().get(), "Not owner");
```

Or use the built-in `multiversx_sc_modules::only_owner` module.

---

## Storage

### State Variables → Storage Mappers

**Solidity:**
```solidity
uint256 public totalSupply;
mapping(address => uint256) public balances;
```

**MultiversX Rust:**
```rust
#[storage_mapper("totalSupply")]
fn total_supply(&self) -> SingleValueMapper<BigUint<Self::Api>>;

#[storage_mapper("balances")]
fn balances(&self, addr: &ManagedAddress<Self::Api>) -> SingleValueMapper<BigUint<Self::Api>>;
```

Read: `self.total_supply().get()`
Write: `self.total_supply().set(&new_val)`

---

## Summary Table

| EVM Concept | MultiversX Equivalent |
|---|---|
| ETH | EGLD |
| ERC20 | ESDT (protocol-native) |
| `msg.sender` | `self.blockchain().get_caller()` |
| `msg.value` | `self.call_value().egld_value()` |
| `block.timestamp` | `self.blockchain().get_block_timestamp()` |
| `block.number` | `self.blockchain().get_block_nonce()` |
| `address(this).balance` | `self.blockchain().get_sc_balance(...)` |
| `emit Event(...)` | `self.event_name_event().emit(...)` |
| `try-catch` | Async callbacks |
| `delegatecall` | Composability patterns |
| `selfdestruct` | No equivalent (design without it) |
| State variable | `#[storage_mapper]` fn |
