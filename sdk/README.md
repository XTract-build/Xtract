# @xtract/sdk

TypeScript wrapper around the **XTract** Python transpiler — converts Solidity smart contracts to MultiversX-compatible Rust.

## Prerequisites

The SDK shells out to the `xtract` Python CLI. Install it before using this package:

```bash
pip install xtract
```

> Python 3.8+ is required. Verify with `xtract --version`.

## Installation

```bash
npm install @xtract/sdk
```

## Quick Start

```typescript
import { XtractTranspiler } from '@xtract/sdk';

const t = new XtractTranspiler();
const result = await t.transpileCode('contract Foo { uint x; }');
console.log(result.rustCode);
```

## Full Documentation

See the [main repository README](https://github.com/kaankacar/XTract#readme) for the complete feature reference, CLI usage, and advanced options.
