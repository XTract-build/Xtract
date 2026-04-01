import { ContractDeployer, WalletProvider, Networks } from '@xtract/sdk';

async function deploy() {
  const signer = await WalletProvider.fromEnv();
  const deployer = new ContractDeployer();
  const result = await deployer.deploy({
    network: 'devnet',
    wasmPath: './output/erc20token.wasm',
    abiPath: './output/erc20token.abi.json',
    walletPem: signer.getPem(),
    // ERC20Token.init(name, ticker, decimals, initialSupply)
    // FILL IN: replace with your token parameters
    initArgs: ['MyToken', 'MTK', '18', '1000000000000000000000000'],
  });
  console.log('Deployed to:', result.contractAddress);
  console.log('Explorer:', result.explorerUrl);
}

deploy().catch(console.error);
