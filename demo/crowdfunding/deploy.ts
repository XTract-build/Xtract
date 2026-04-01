import { ContractDeployer, WalletProvider, Networks } from '@xtract/sdk';

async function deploy() {
  const signer = await WalletProvider.fromEnv();
  const deployer = new ContractDeployer();
  const result = await deployer.deploy({
    network: 'devnet',
    wasmPath: './output/crowdfunding.wasm',
    abiPath: './output/crowdfunding.abi.json',
    walletPem: signer.getPem(),
    // Crowdfunding.init(target, deadline)
    // FILL IN: target in atto-EGLD (1 EGLD = 10^18), deadline as Unix timestamp
    initArgs: [
      '5000000000000000000',                          // 5 EGLD fundraising goal
      String(Math.floor(Date.now() / 1000) + 2592000), // 30 days from now
    ],
  });
  console.log('Deployed to:', result.contractAddress);
  console.log('Explorer:', result.explorerUrl);
}

deploy().catch(console.error);
