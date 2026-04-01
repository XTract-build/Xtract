import { NetworkConfig } from './types';

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type AbiRegistry = any;
// eslint-disable-next-line @typescript-eslint/no-explicit-any
type TypedValue = any;

function requireSdkCore() {
  try {
    // eslint-disable-next-line @typescript-eslint/no-var-requires
    return require('@multiversx/sdk-core');
  } catch {
    throw new Error(
      '@multiversx/sdk-core is required for contract queries. Install it with: npm install @multiversx/sdk-core'
    );
  }
}

/**
 * Internal helper that wraps SmartContractQueriesController to execute
 * view/query calls against a MultiversX smart contract.
 */
export class QueryRunner {
  private readonly contractAddress: string;
  private readonly abi: AbiRegistry;
  private readonly network: NetworkConfig;

  constructor(contractAddress: string, abi: AbiRegistry, network: NetworkConfig) {
    this.contractAddress = contractAddress;
    this.abi = abi;
    this.network = network;
  }

  async run(endpoint: string, args: TypedValue[]): Promise<TypedValue[]> {
    const sdk = requireSdkCore();

    const { Address, SmartContractQueriesController, ProxyNetworkProvider } = sdk;

    const provider = new ProxyNetworkProvider(this.network.apiUrl);
    const controller = new SmartContractQueriesController({
      queryRunner: provider,
      abi: this.abi,
    });

    const query = controller.createQuery({
      contract: new Address(this.contractAddress),
      function: endpoint,
      arguments: args,
    });

    const response = await controller.runQuery(query);
    const parsed = controller.parseQueryResponse(response);

    return parsed as TypedValue[];
  }
}
