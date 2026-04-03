# XTract TypeScript SDK Reference

The TypeScript SDK is bundled in the `xtract-cli` npm package and exposes the full transpile → deploy → interact pipeline programmatically.

> **Prerequisite:** The SDK shells out to the Python transpiler for transpilation.
> `pip install xtract` must be run first (Python 3.9+). Set `PYTHONPATH` if `xtract` is
> installed in a non-standard location, or use `XTRACT_PYTHON` to point to a specific
> Python binary.

```bash
npm install xtract-cli
# or globally:
npm install -g xtract-cli
```

---

## XtractTranspiler

**`sdk/src/transpiler/XtractTranspiler.ts`**

Python binary resolution: `python3` → `python`. The resolved binary is cached at module level.

```typescript
import { XtractTranspiler } from 'xtract-cli/sdk';
```

### Constructor

```typescript
new XtractTranspiler()
```

No options. Python binary is resolved automatically on first use.

### Methods

#### `transpileFile(solPath, options?): Promise<TranspileResult>`

Transpile a `.sol` file on disk.

```typescript
const transpiler = new XtractTranspiler();
const result = await transpiler.transpileFile('./MyContract.sol');
console.log(result.rustCode);
```

`TranspileOptions`:
```typescript
interface TranspileOptions {
  verbose?: boolean;   // pass --verbose to the CLI
}
```

#### `transpileCode(soliditySource): Promise<TranspileResult>`

Transpile a Solidity source string. Writes to a temp file internally, then cleans up.

```typescript
const result = await transpiler.transpileCode(`
  contract Foo {
    uint256 public value;
  }
`);
```

#### `static isInstalled(): Promise<boolean>`

Returns `true` if the `xtract` Python CLI responds to `--help` with exit code 0.

```typescript
if (!(await XtractTranspiler.isInstalled())) {
  console.error('Run: pip install xtract');
}
```

#### `static getVersion(): Promise<string>`

Returns the `xtract` CLI version string.

```typescript
const version = await XtractTranspiler.getVersion();
// → "1.0.0"
```

### TranspileResult

```typescript
interface TranspileResult {
  success: boolean;
  rustCode: string;
  diagnostics: Diagnostic[];
}

interface Diagnostic {
  message: string;
  line?: number;
  severity: 'warning' | 'error';
}
```

### TranspileError

Thrown on fatal transpiler failure (non-zero exit code + no recoverable output).

```typescript
import { TranspileError } from 'xtract-cli/sdk';

try {
  await transpiler.transpileFile('./Bad.sol');
} catch (e) {
  if (e instanceof TranspileError) {
    console.error('Exit code:', e.exitCode);
    console.error('Stderr:', e.stderr);
  }
}
```

---

## ContractDeployer

**`sdk/src/deploy/ContractDeployer.ts`**

Uses `@multiversx/sdk-core`: `ApiNetworkProvider`, `SmartContractTransactionsFactory`, `TransactionWatcher`.

```typescript
import { ContractDeployer } from 'xtract-cli/sdk';
```

### `deploy(config): Promise<DeployResult>`

```typescript
interface DeployConfig {
  network: 'devnet' | 'testnet' | 'mainnet' | string;
  wasmPath: string;
  abiPath: string;
  walletPath?: string;    // path to PEM file
  walletPem?: string;     // PEM content as string (alternative to walletPath)
  initArgs?: any[];       // constructor arguments
  gasLimit?: number;      // default: 60_000_000
}

interface DeployResult {
  contractAddress: string;
  txHash: string;
  explorerUrl: string;
}
```

```typescript
const deployer = new ContractDeployer();
const result = await deployer.deploy({
  network: 'devnet',
  wasmPath: './output/my_contract.wasm',
  abiPath: './output/my_contract.abi.json',
  walletPath: './wallet.pem',
});
console.log(result.contractAddress);  // erd1qqq...
console.log(result.explorerUrl);
```

### `upgrade(address, config): Promise<DeployResult>`

Upgrade an existing contract at `address`.

```typescript
await deployer.upgrade('erd1qqq...abc', {
  network: 'devnet',
  wasmPath: './output/my_contract_v2.wasm',
  abiPath: './output/my_contract_v2.abi.json',
  walletPath: './wallet.pem',
});
```

---

## WalletProvider

**`sdk/src/deploy/WalletProvider.ts`**

```typescript
import { WalletProvider } from 'xtract-cli/sdk';
```

All methods return a `UserSigner` from `@multiversx/sdk-core`.

### `static fromPemFile(pemPath): Promise<UserSigner>`

```typescript
const signer = await WalletProvider.fromPemFile('./wallet.pem');
```

### `static fromPemContent(pemContent): UserSigner`

```typescript
const signer = WalletProvider.fromPemContent(fs.readFileSync('./wallet.pem', 'utf8'));
```

### `static fromKeystore(keystorePath, password): Promise<UserSigner>`

```typescript
const signer = await WalletProvider.fromKeystore('./keystore.json', 'mypassword');
```

### `static fromEnv(envVar?): UserSigner`

Reads PEM content from environment variable (default: `XTRACT_WALLET_PEM`).

```typescript
// Uses process.env.XTRACT_WALLET_PEM
const signer = WalletProvider.fromEnv();

// Or a custom env var name
const signer = WalletProvider.fromEnv('MY_WALLET_PEM');
```

---

## NetworkConfig

**`sdk/src/deploy/NetworkConfig.ts`**

```typescript
import { Networks, getNetworkConfig, NetworkName } from 'xtract-cli/sdk';
```

### `Networks` constant

```typescript
const Networks: Record<string, NetworkConfig> = {
  devnet:  { apiUrl: 'https://devnet-api.multiversx.com',  chainId: 'D' },
  testnet: { apiUrl: 'https://testnet-api.multiversx.com', chainId: 'T' },
  mainnet: { apiUrl: 'https://api.multiversx.com',         chainId: '1' },
};
```

### `getNetworkConfig(network): NetworkConfig`

```typescript
const config = getNetworkConfig('devnet');
// → { apiUrl: 'https://devnet-api.multiversx.com', chainId: 'D' }
```

Throws `Error` for unknown network names.

---

## ContractInteractor

**`sdk/src/interact/ContractInteractor.ts`**

High-level helper for calling and querying deployed contracts. Handles ABI loading, argument encoding, signing, and broadcasting.

```typescript
import { ContractInteractor, WalletProvider } from 'xtract-cli/sdk';
```

### Constructor

```typescript
new ContractInteractor(
  contractAddress: string,
  abiPath: string,
  network: NetworkName | string,
  wallet: UserSigner
)
```

### `call(endpoint, args, options?): Promise<TxResult>`

Send a state-changing transaction.

```typescript
const result = await interactor.call('setValue', [42n]);
console.log(result.txHash);
```

`CallOptions`:
```typescript
interface CallOptions {
  gasLimit?: number;
  value?: bigint;    // EGLD value in atomic units
  caller?: string;
}
```

### `query(endpoint, args?): Promise<any[]>`

Execute a read-only view query (free, no transaction).

```typescript
const [value] = await interactor.query('getValue');
console.log(value.toString());
```

### `transferEsdtAndCall(tokenId, amount, endpoint, args?, options?): Promise<TxResult>`

Send ESDT tokens to the contract and call an endpoint (ESDTTransfer + call).

```typescript
await interactor.transferEsdtAndCall(
  'MYTOKEN-abc123',
  1000n,
  'deposit',
  []
);
```

### `transferEgldAndCall(amount, endpoint, args?, options?): Promise<TxResult>`

Send EGLD to the contract and call a `#[payable("EGLD")]` endpoint.

```typescript
await interactor.transferEgldAndCall(
  BigInt('1000000000000000000'),  // 1 EGLD in atomic units
  'stake',
  []
);
```

`TxResult`:
```typescript
interface TxResult {
  txHash: string;
  success: boolean;
  returnData: string[];
  explorerUrl: string;
}
```

---

## End-to-End Example: Transpile → Deploy → Call

```typescript
import * as path from 'path';
import {
  XtractTranspiler,
  ContractDeployer,
  ContractInteractor,
  WalletProvider,
} from 'xtract-cli/sdk';

async function main() {
  // ── 1. Transpile ──────────────────────────────────────────────────────────
  const transpiler = new XtractTranspiler();

  if (!(await XtractTranspiler.isInstalled())) {
    throw new Error('Python xtract not found. Run: pip install xtract');
  }

  const result = await transpiler.transpileFile('./MyContract.sol');
  if (!result.success) {
    console.error('Transpile failed:', result.diagnostics);
    process.exit(1);
  }
  console.log('Transpiled successfully');

  // ── 2. Deploy ─────────────────────────────────────────────────────────────
  // (assumes xtract build was already run: output/*.wasm + *.abi.json exist)

  const deployer = new ContractDeployer();
  const { contractAddress, explorerUrl } = await deployer.deploy({
    network: 'devnet',
    wasmPath: './output/my_contract.wasm',
    abiPath:  './output/my_contract.abi.json',
    walletPath: path.join(process.env.HOME!, '.multiversx/wallet.pem'),
    gasLimit: 60_000_000,
  });

  console.log('Contract address:', contractAddress);
  console.log('Explorer:', explorerUrl);

  // ── 3. Interact ───────────────────────────────────────────────────────────
  const wallet = await WalletProvider.fromPemFile(
    path.join(process.env.HOME!, '.multiversx/wallet.pem')
  );

  const interactor = new ContractInteractor(
    contractAddress,
    './output/my_contract.abi.json',
    'devnet',
    wallet,
  );

  // Write
  await interactor.call('setValue', [100n]);

  // Read
  const [value] = await interactor.query('getValue');
  console.log('Stored value:', value.toString());
}

main().catch(console.error);
```
