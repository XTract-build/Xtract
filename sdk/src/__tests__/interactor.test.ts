// Mock @multiversx/sdk-core so tests run without the peer dependency installed
jest.mock('@multiversx/sdk-core', () => {
  class Address {
    constructor(public readonly value: string) {}
    toString() { return this.value; }
  }

  class Transaction {
    constructor(public readonly fields: Record<string, unknown>) {}
    get function(): string { return this.fields['function'] as string; }
  }

  class TransactionsFactoryConfig {
    constructor(public readonly cfg: { chainID: string }) {}
  }

  class SmartContractTransactionFactory {
    constructor(private readonly opts: { config: TransactionsFactoryConfig; abi: unknown }) {}
    createTransactionForExecute(params: Record<string, unknown>): Transaction {
      return new Transaction(params);
    }
  }

  class SmartContractQueriesController {
    constructor(private readonly opts: unknown) {}
    createQuery(params: Record<string, unknown>) { return params; }
    async runQuery(query: unknown) { return query; }
    parseQueryResponse(_response: unknown): unknown[] { return []; }
  }

  class AbiRegistry {
    static create(json: unknown) { return new AbiRegistry(json); }
    constructor(public readonly raw: unknown) {}
  }

  class ProxyNetworkProvider {
    constructor(public readonly url: string) {}
    async getAccount(_addr: Address) { return { nonce: 0 }; }
    async sendTransaction(_tx: Transaction) { return 'mock-tx-hash'; }
  }

  class ArgSerializer {
    nativeToTyped(args: unknown[]) { return args; }
  }

  class Token { constructor(public readonly t: unknown) {} }
  class TokenTransfer { constructor(public readonly t: unknown) {} }

  return {
    Address,
    Transaction,
    TransactionsFactoryConfig,
    SmartContractTransactionFactory,
    SmartContractQueriesController,
    AbiRegistry,
    ProxyNetworkProvider,
    ArgSerializer,
    Token,
    TokenTransfer,
  };
});

import { TxBuilder } from '../interact/TxBuilder';
import { QueryRunner } from '../interact/QueryRunner';

const MOCK_NETWORK = {
  name: 'devnet' as const,
  chainId: 'D',
  apiUrl: 'https://devnet-api.multiversx.com',
  explorerUrl: 'https://devnet-explorer.multiversx.com',
};

const MOCK_ABI = { endpoints: [] };
const CONTRACT_ADDRESS = 'erd1qqqqqqqqqqqqqpgqd77fnev2sthnczp2lnfx0y5jdycynjfhzzgq6p3rax';

describe('TxBuilder', () => {
  it('build() produces a transaction with correct function name', () => {
    const builder = new TxBuilder(CONTRACT_ADDRESS, MOCK_ABI, MOCK_NETWORK);
    const tx = builder.build('setValue', [], { caller: CONTRACT_ADDRESS, gasLimit: 5_000_000 });
    // The mock SmartContractTransactionFactory records the function field
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    expect((tx as any).fields['function']).toBe('setValue');
  });

  it('buildEsdtTransfer() produces a transaction with correct function name', () => {
    const builder = new TxBuilder(CONTRACT_ADDRESS, MOCK_ABI, MOCK_NETWORK);
    const tx = builder.buildEsdtTransfer('TOKEN-abc123', BigInt(100), 'deposit', [], {
      caller: CONTRACT_ADDRESS,
    });
    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    expect((tx as any).fields['function']).toBe('deposit');
  });
});

describe('QueryRunner', () => {
  it('constructs correctly with address, abi, and network', () => {
    const runner = new QueryRunner(CONTRACT_ADDRESS, MOCK_ABI, MOCK_NETWORK);
    expect(runner).toBeInstanceOf(QueryRunner);
  });

  it('run() returns an array', async () => {
    const runner = new QueryRunner(CONTRACT_ADDRESS, MOCK_ABI, MOCK_NETWORK);
    const result = await runner.run('getValue', []);
    expect(Array.isArray(result)).toBe(true);
  });
});

// Integration test — only runs when RUN_INTEGRATION=true
const describeIntegration = process.env['RUN_INTEGRATION'] === 'true' ? describe : describe.skip;

describeIntegration('Integration: devnet SimpleStorage', () => {
  it('calls getValue view on devnet SimpleStorage', async () => {
    // Restore the real SDK for this test block
    jest.unmock('@multiversx/sdk-core');
    jest.resetModules();

    const { QueryRunner: RealQueryRunner } = await import('../interact/QueryRunner');
    const { AbiRegistry } = await import('@multiversx/sdk-core');

    const SIMPLE_STORAGE_ADDRESS =
      process.env['SIMPLE_STORAGE_ADDRESS'] ?? CONTRACT_ADDRESS;

    const abi = AbiRegistry.create({
      endpoints: [{ name: 'getValue', mutability: 'readonly', outputs: [{ type: 'u64' }] }],
    });

    const runner = new RealQueryRunner(SIMPLE_STORAGE_ADDRESS, abi, MOCK_NETWORK);
    const result = await runner.run('getValue', []);
    expect(Array.isArray(result)).toBe(true);
  });
});
