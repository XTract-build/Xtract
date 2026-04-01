import { ContractDeployer, WalletProvider, Networks } from '@xtract/sdk';

async function deploy() {
  const signer = await WalletProvider.fromEnv();
  const deployer = new ContractDeployer();
  const result = await deployer.deploy({
    network: 'devnet',
    wasmPath: './output/simple-storage.wasm',
    abiPath: './output/simple-storage.abi.json',
    walletPem: signer.getPem(),
    // SimpleStorage.init() takes no arguments
    initArgs: [],
  });
  console.log('Deployed to:', result.contractAddress);
  console.log('Explorer:', result.explorerUrl);
}

deploy().catch(console.error);
