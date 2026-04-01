import { ContractDeployer, WalletProvider, Networks } from '@xtract/sdk';

async function deploy() {
  const signer = await WalletProvider.fromEnv();
  const deployer = new ContractDeployer();
  const result = await deployer.deploy({
    network: 'devnet',
    wasmPath: './output/voting.wasm',
    abiPath: './output/voting.abi.json',
    walletPem: signer.getPem(),
    // Voting.init() takes no arguments — candidates are added after deploy
    initArgs: [],
  });
  console.log('Deployed to:', result.contractAddress);
  console.log('Explorer:', result.explorerUrl);
}

deploy().catch(console.error);
