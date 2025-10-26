# XTract Demo - SimpleStorage

This demo showcases XTract v0.25's transpilation capabilities by converting a simple Solidity storage contract to MultiversX Rust.

## What this demonstrates

- ✅ **Function body generation**: `setValue()` and `getValue()` with proper implementation
- ✅ **Storage operations**: Variable assignments converted to `self.value().set()`
- ✅ **Event emission**: `emit ValueChanged()` converted to `self.value_changed_event()`
- ✅ **Error handling**: Ready for `require()` statements
- ✅ **Type mapping**: Solidity `uint256` → MultiversX `BigUint<Self::Api>`

## Generated Contract

The `simple_storage/src/lib.rs` file contains the transpiled Rust contract that can be compiled and deployed on MultiversX.

## Building the Demo

```bash
cd demo/simple_storage
cargo check  # Verify compilation
cargo build  # Build WASM output
```

## Original Solidity

```solidity
contract SimpleStorage {
    uint256 private value;

    event ValueChanged(uint256 indexed newValue);

    function setValue(uint256 newValue) public {
        value = newValue;
        emit ValueChanged(newValue);
    }

    function getValue() public view returns (uint256) {
        return value;
    }
}
```

## Transpiled MultiversX Rust

The transpiler converts this to proper MultiversX patterns:
- Storage variables become storage mappers
- Events become MultiversX event definitions
- Function bodies include actual implementation logic
- Proper type conversions and API usage
