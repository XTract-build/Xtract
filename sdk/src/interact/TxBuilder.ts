import { CallOptions, NetworkConfig } from './types';

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type AbiRegistry = any;
// eslint-disable-next-line @typescript-eslint/no-explicit-any
type TypedValue = any;
// eslint-disable-next-line @typescript-eslint/no-explicit-any
type Transaction = any;

function requireSdkCore() {
  try {
    // eslint-disable-next-line @typescript-eslint/no-var-requires
    return require('@multiversx/sdk-core');
  } catch {
    throw new Error(
      '@multiversx/sdk-core is required for building transactions. Install it with: npm install @multiversx/sdk-core'
    );
  }
}

const DEFAULT_GAS_LIMIT = 10_000_000;

/**
 * Internal helper that wraps SmartContractTransactionFactory to produce
 * unsigned MultiversX transactions for contract calls and ESDT transfers.
 */
export class TxBuilder {
  private readonly contractAddress: string;
  private readonly abi: AbiRegistry;
  private readonly network: NetworkConfig;

  constructor(contractAddress: string, abi: AbiRegistry, network: NetworkConfig) {
    this.contractAddress = contractAddress;
    this.abi = abi;
    this.network = network;
  }

  build(endpoint: string, args: TypedValue[], options: CallOptions): Transaction {
    const sdk = requireSdkCore();
    const { Address, SmartContractTransactionFactory, TransactionsFactoryConfig } = sdk;

    const config = new TransactionsFactoryConfig({ chainID: this.network.chainId });
    const factory = new SmartContractTransactionFactory({ config, abi: this.abi });

    const tx = factory.createTransactionForExecute({
      sender: new Address(options.caller ?? ''),
      contract: new Address(this.contractAddress),
      function: endpoint,
      gasLimit: BigInt(options.gasLimit ?? DEFAULT_GAS_LIMIT),
      arguments: args,
      nativeTransferAmount: options.value ?? BigInt(0),
    });

    return tx;
  }

  buildEsdtTransfer(
    tokenId: string,
    amount: bigint,
    endpoint: string,
    args: TypedValue[],
    options: CallOptions
  ): Transaction {
    const sdk = requireSdkCore();
    const { Address, SmartContractTransactionFactory, TransactionsFactoryConfig, Token, TokenTransfer } = sdk;

    const config = new TransactionsFactoryConfig({ chainID: this.network.chainId });
    const factory = new SmartContractTransactionFactory({ config, abi: this.abi });

    const tx = factory.createTransactionForExecute({
      sender: new Address(options.caller ?? ''),
      contract: new Address(this.contractAddress),
      function: endpoint,
      gasLimit: BigInt(options.gasLimit ?? DEFAULT_GAS_LIMIT),
      arguments: args,
      tokenTransfers: [
        new TokenTransfer({ token: new Token({ identifier: tokenId }), amount }),
      ],
    });

    return tx;
  }
}
