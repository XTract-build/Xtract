/**
 * NftStaking — Deploy Script
 *
 * Transpile → build → deploy to MultiversX devnet using the XTract SDK.
 *
 * Prerequisites:
 *   npm install @xtract/sdk                  # XTract programmatic API
 *   npm install @multiversx/sdk-core         # MultiversX JS SDK
 *   rustup target add wasm32-unknown-unknown # Wasm toolchain
 *   cargo install multiversx-sc-meta         # sc-meta CLI (for wasm build)
 */

import { XtractTranspiler, ContractDeployer, WalletProvider, Networks } from '@xtract/sdk';
import * as path from 'path';

const SOL_SOURCE  = path.join(__dirname, 'src', 'NftStaking.sol');
const RUST_OUTPUT = path.join(__dirname, 'src', 'NftStaking.rs');
const WASM_OUTPUT = path.join(__dirname, 'output', 'nft-staking.wasm');

async function main() {
    // ── Step 1: Transpile Solidity → MultiversX Rust ─────────────────────────
    console.log('Step 1: Transpiling NftStaking.sol …');
    const transpiler = new XtractTranspiler();
    const result = await transpiler.transpileFile(SOL_SOURCE, RUST_OUTPUT);

    if (!result.success) {
        console.error('Transpilation failed:', result.diagnostics);
        process.exit(1);
    }
    console.log('  ✓ Written to', RUST_OUTPUT);

    // ── Step 2: Build .wasm via sc-meta ──────────────────────────────────────
    // Run manually if sc-meta is installed:
    //   cd demo/nft_staking && sc-meta all build
    //
    console.log('Step 2: Building WASM …');
    const builder = await transpiler.buildWasm(__dirname);
    if (!builder.success) {
        console.error('Build failed. Ensure sc-meta is installed: cargo install multiversx-sc-meta');
        process.exit(1);
    }
    console.log('  ✓ WASM at', WASM_OUTPUT);

    // ── Step 3: Deploy to devnet ──────────────────────────────────────────────
    console.log('Step 3: Deploying to devnet …');

    // FILL IN: path to your PEM wallet file
    const walletPath = process.env.WALLET_PEM ?? './wallet.pem';

    const wallet   = await WalletProvider.fromPemFile(walletPath);
    const network  = Networks.devnet();         // change to Networks.mainnet() for production
    const deployer = new ContractDeployer(wallet, network);

    const deployment = await deployer.deploy({
        wasmPath: WASM_OUTPUT,
        // NftStaking.init() takes no arguments
        initArgs: [],
        gasLimit: 60_000_000,
    });

    if (!deployment.success) {
        console.error('Deployment failed:', deployment.error);
        process.exit(1);
    }

    console.log('  ✓ Contract deployed!');
    console.log('    Address :', deployment.contractAddress);
    console.log('    Tx hash :', deployment.txHash);
    console.log('    Explorer:', `https://devnet-explorer.multiversx.com/transactions/${deployment.txHash}`);

    // ── Step 4: Post-deploy smoke test ────────────────────────────────────────
    // On MultiversX, staking requires sending an NFT (ESDT Non-Fungible) as payment.
    // Replace with your actual NFT token identifier and nonce on devnet:
    //
    // const NFT_TOKEN_ID = 'MYNFT-abc123';
    // const NFT_NONCE = 1n;
    // const TOKEN_ID_HEX = Buffer.from(NFT_TOKEN_ID).toString('hex');
    //
    // await deployer.call(deployment.contractAddress, 'stake', [TOKEN_ID_HEX, NFT_NONCE, 1n], {
    //     gasLimit: 10_000_000,
    //     // Attach the NFT as payment (MultiversX ESDT transfer)
    //     esdtTransfers: [{ tokenIdentifier: NFT_TOKEN_ID, nonce: NFT_NONCE, amount: 1n }],
    // });
    // const isStaked = await deployer.query(deployment.contractAddress, 'isStaked', [NFT_NONCE]);
    // console.log('Is staked:', isStaked.toString());
}

main().catch(err => {
    console.error(err);
    process.exit(1);
});
