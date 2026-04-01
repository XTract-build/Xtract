import { NetworkName } from './NetworkConfig';

export interface DeployConfig {
  network: NetworkName | string;
  walletPath?: string;
  walletPem?: string;
  wasmPath: string;
  abiPath: string;
  initArgs?: any[];
  gasLimit?: number;
  upgradeAddress?: string;
}

export interface DeployResult {
  contractAddress: string;
  txHash: string;
  explorerUrl: string;
}
