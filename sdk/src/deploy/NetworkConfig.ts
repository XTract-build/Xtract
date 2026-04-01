export interface NetworkConfig {
  apiUrl: string;
  chainId: string;
}

export const Networks: Record<string, NetworkConfig> = {
  devnet: { apiUrl: 'https://devnet-api.multiversx.com', chainId: 'D' },
  testnet: { apiUrl: 'https://testnet-api.multiversx.com', chainId: 'T' },
  mainnet: { apiUrl: 'https://api.multiversx.com', chainId: '1' },
};

export type NetworkName = 'devnet' | 'testnet' | 'mainnet';

export function getNetworkConfig(network: NetworkName | string): NetworkConfig {
  const config = Networks[network];
  if (!config) {
    throw new Error(`Unknown network: "${network}". Valid options: ${Object.keys(Networks).join(', ')}`);
  }
  return config;
}
