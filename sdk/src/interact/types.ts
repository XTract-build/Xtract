export type NetworkName = 'devnet' | 'testnet' | 'mainnet';

export interface NetworkConfig {
  name: NetworkName | string;
  chainId: string;
  apiUrl: string;
  explorerUrl: string;
}

export interface CallOptions {
  gasLimit?: number;
  value?: bigint;
  caller?: string;
}

export interface TxResult {
  txHash: string;
  success: boolean;
  returnData: string[];
  explorerUrl: string;
}

const NETWORK_CONFIGS: Record<string, NetworkConfig> = {
  devnet: {
    name: 'devnet',
    chainId: 'D',
    apiUrl: 'https://devnet-api.multiversx.com',
    explorerUrl: 'https://devnet-explorer.multiversx.com',
  },
  testnet: {
    name: 'testnet',
    chainId: 'T',
    apiUrl: 'https://testnet-api.multiversx.com',
    explorerUrl: 'https://testnet-explorer.multiversx.com',
  },
  mainnet: {
    name: 'mainnet',
    chainId: '1',
    apiUrl: 'https://api.multiversx.com',
    explorerUrl: 'https://explorer.multiversx.com',
  },
};

export function resolveNetwork(network: NetworkName | string): NetworkConfig {
  if (typeof network === 'string' && network in NETWORK_CONFIGS) {
    return NETWORK_CONFIGS[network];
  }
  throw new Error(
    `Unknown network "${network}". Provide a NetworkConfig object or use 'devnet' | 'testnet' | 'mainnet'.`
  );
}
