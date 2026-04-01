import * as fs from 'fs';
import {
  ApiNetworkProvider,
  SmartContractTransactionsFactory,
  TransactionWatcher,
  Address,
  TransactionsFactoryConfig,
  TransactionComputer,
} from '@multiversx/sdk-core';
import { DeployConfig, DeployResult } from './DeployConfig';
import { WalletProvider } from './WalletProvider';
import { getNetworkConfig } from './NetworkConfig';

const EXPLORER_URLS: Record<string, string> = {
  D: 'https://devnet-explorer.multiversx.com',
  T: 'https://testnet-explorer.multiversx.com',
  '1': 'https://explorer.multiversx.com',
};

export class ContractDeployer {
  async deploy(config: DeployConfig): Promise<DeployResult> {
    const { apiUrl, chainId } = getNetworkConfig(config.network);
    const provider = new ApiNetworkProvider(apiUrl);

    const signer = config.walletPem
      ? WalletProvider.fromPemContent(config.walletPem)
      : await WalletProvider.fromPemFile(config.walletPath!);

    const senderAddress = signer.getAddress();
    const account = await provider.getAccount(senderAddress);

    const wasmBuffer = fs.readFileSync(config.wasmPath);
    const abiJson = JSON.parse(fs.readFileSync(config.abiPath, 'utf8'));

    const factoryConfig = new TransactionsFactoryConfig({ chainID: chainId });
    const factory = new SmartContractTransactionsFactory({ config: factoryConfig, abi: abiJson });

    const tx = await factory.createTransactionForDeploy(senderAddress, {
      bytecode: wasmBuffer,
      gasLimit: BigInt(config.gasLimit ?? 60_000_000),
      arguments: config.initArgs ?? [],
    });

    tx.nonce = BigInt(account.nonce);
    const computer = new TransactionComputer();
    tx.signature = await signer.sign(computer.computeBytesForSigning(tx));

    const txHash = await provider.sendTransaction(tx);
    const watcher = new TransactionWatcher(provider);
    const outcome = await watcher.awaitCompleted(txHash);

    const contractAddress = (outcome as any).smartContractResults?.[0]?.receiver ?? '';
    const explorerBase = EXPLORER_URLS[chainId] ?? 'https://explorer.multiversx.com';

    return {
      contractAddress,
      txHash: txHash.toString(),
      explorerUrl: `${explorerBase}/transactions/${txHash}`,
    };
  }

  async upgrade(address: string, config: DeployConfig): Promise<DeployResult> {
    const { apiUrl, chainId } = getNetworkConfig(config.network);
    const provider = new ApiNetworkProvider(apiUrl);

    const signer = config.walletPem
      ? WalletProvider.fromPemContent(config.walletPem)
      : await WalletProvider.fromPemFile(config.walletPath!);

    const senderAddress = signer.getAddress();
    const account = await provider.getAccount(senderAddress);

    const wasmBuffer = fs.readFileSync(config.wasmPath);
    const abiJson = JSON.parse(fs.readFileSync(config.abiPath, 'utf8'));

    const factoryConfig = new TransactionsFactoryConfig({ chainID: chainId });
    const factory = new SmartContractTransactionsFactory({ config: factoryConfig, abi: abiJson });

    const tx = await factory.createTransactionForUpgrade(senderAddress, {
      contract: new Address(address),
      bytecode: wasmBuffer,
      gasLimit: BigInt(config.gasLimit ?? 60_000_000),
      arguments: config.initArgs ?? [],
    });

    tx.nonce = BigInt(account.nonce);
    const computer = new TransactionComputer();
    tx.signature = await signer.sign(computer.computeBytesForSigning(tx));

    const txHash = await provider.sendTransaction(tx);
    const watcher = new TransactionWatcher(provider);
    await watcher.awaitCompleted(txHash);

    const explorerBase = EXPLORER_URLS[chainId] ?? 'https://explorer.multiversx.com';

    return {
      contractAddress: address,
      txHash: txHash.toString(),
      explorerUrl: `${explorerBase}/transactions/${txHash}`,
    };
  }
}
