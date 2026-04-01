import * as fs from 'fs';
import { CallOptions, NetworkConfig, NetworkName, TxResult, resolveNetwork } from './types';
import { QueryRunner } from './QueryRunner';
import { TxBuilder } from './TxBuilder';

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type UserSigner = any;

function requireSdkCore() {
  try {
    // eslint-disable-next-line @typescript-eslint/no-var-requires
    return require('@multiversx/sdk-core');
  } catch {
    throw new Error(
      '@multiversx/sdk-core is required for contract interaction. Install it with: npm install @multiversx/sdk-core'
    );
  }
}

function buildExplorerUrl(network: NetworkConfig, txHash: string): string {
  return `${network.explorerUrl}/transactions/${txHash}`;
}

/**
 * High-level contract interaction helper.
 * Handles ABI loading, argument encoding, transaction signing and broadcasting.
 */
export class ContractInteractor {
  private readonly contractAddress: string;
  private readonly abiPath: string;
  private readonly network: NetworkConfig;
  private readonly wallet: UserSigner;

  // Lazily initialised after ABI is loaded
  private queryRunner: QueryRunner | null = null;
  private txBuilder: TxBuilder | null = null;
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  private abi: any | null = null;

  constructor(
    contractAddress: string,
    abiPath: string,
    network: NetworkName | string,
    wallet: UserSigner
  ) {
    this.contractAddress = contractAddress;
    this.abiPath = abiPath;
    this.network =
      typeof network === 'string' && !['devnet', 'testnet', 'mainnet'].includes(network)
        ? (network as unknown as NetworkConfig)
        : resolveNetwork(network as NetworkName);
    this.wallet = wallet;
  }

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  private async ensureAbi(): Promise<any> {
    if (this.abi) return this.abi;

    const sdk = requireSdkCore();
    const { AbiRegistry } = sdk;

    const abiJson = JSON.parse(fs.readFileSync(this.abiPath, 'utf-8'));
    this.abi = AbiRegistry.create(abiJson);

    this.queryRunner = new QueryRunner(this.contractAddress, this.abi, this.network);
    this.txBuilder = new TxBuilder(this.contractAddress, this.abi, this.network);

    return this.abi;
  }

  async call(endpoint: string, args: unknown[], options: CallOptions = {}): Promise<TxResult> {
    await this.ensureAbi();

    const sdk = requireSdkCore();
    const { ProxyNetworkProvider, ArgSerializer } = sdk;

    const serializer = new ArgSerializer();
    const typedArgs = serializer.nativeToTyped(args);

    const tx = this.txBuilder!.build(endpoint, typedArgs, options);

    const provider = new ProxyNetworkProvider(this.network.apiUrl);
    const account = await provider.getAccount(tx.sender);
    tx.nonce = account.nonce;

    const signature = await this.wallet.sign(tx.serializeForSigning());
    tx.applySignature(signature);

    const txHash = await provider.sendTransaction(tx);

    return {
      txHash,
      success: true,
      returnData: [],
      explorerUrl: buildExplorerUrl(this.network, txHash),
    };
  }

  async query(endpoint: string, args: unknown[] = []): Promise<unknown[]> {
    await this.ensureAbi();

    const sdk = requireSdkCore();
    const { ArgSerializer } = sdk;

    const serializer = new ArgSerializer();
    const typedArgs = serializer.nativeToTyped(args);

    return this.queryRunner!.run(endpoint, typedArgs);
  }

  async transferEsdtAndCall(
    tokenId: string,
    amount: bigint,
    endpoint: string,
    args: unknown[] = [],
    options: CallOptions = {}
  ): Promise<TxResult> {
    await this.ensureAbi();

    const sdk = requireSdkCore();
    const { ProxyNetworkProvider, ArgSerializer } = sdk;

    const serializer = new ArgSerializer();
    const typedArgs = serializer.nativeToTyped(args);

    const tx = this.txBuilder!.buildEsdtTransfer(tokenId, amount, endpoint, typedArgs, options);

    const provider = new ProxyNetworkProvider(this.network.apiUrl);
    const account = await provider.getAccount(tx.sender);
    tx.nonce = account.nonce;

    const signature = await this.wallet.sign(tx.serializeForSigning());
    tx.applySignature(signature);

    const txHash = await provider.sendTransaction(tx);

    return {
      txHash,
      success: true,
      returnData: [],
      explorerUrl: buildExplorerUrl(this.network, txHash),
    };
  }

  async transferEgldAndCall(
    amount: bigint,
    endpoint: string,
    args: unknown[] = [],
    options: CallOptions = {}
  ): Promise<TxResult> {
    return this.call(endpoint, args, { ...options, value: amount });
  }
}
