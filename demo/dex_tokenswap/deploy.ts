/**
 * DexTokenSwap — Deploy Script
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

const SOL_SOURCE  = path.join(__dirname, 'src', 'DexTokenSwap.sol');
const RUST_OUTPUT = path.join(__dirname, 'src', 'DexTokenSwap.rs');
const WASM_OUTPUT = path.join(__dirname, 'output', 'dex-token-swap.wasm');

async function main() {
    // ── Step 1: Transpile Solidity → MultiversX Rust ─────────────────────────
    console.log('Step 1: Transpiling DexTokenSwap.sol …');
    const transpiler = new XtractTranspiler();
    const result = await transpiler.transpileFile(SOL_SOURCE, RUST_OUTPUT);

    if (!result.success) {
        console.error('Transpilation failed:', result.diagnostics);
        process.exit(1);
    }
    console.log('  ✓ Written to', RUST_OUTPUT);

    // ── Step 2: Build .wasm via sc-meta ──────────────────────────────────────
    // Run manually if sc-meta is installed:
    //   cd demo/dex_tokenswap && sc-meta all build
    //
    // Or programmatically (requires sc-meta on PATH):
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
        // DexTokenSwap.init() takes no arguments — pass empty array
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
    // FILL IN: replace with a real ESDT token identifier on devnet
    // const tokenId = 'MYTOKEN-abc123';
    //
    // await deployer.call(deployment.contractAddress, 'deposit', [tokenId, 1000n], {
    //     gasLimit: 10_000_000,
    // });
    // const reserve = await deployer.query(deployment.contractAddress, 'getReserve', [tokenId]);
    // console.log('Reserve after deposit:', reserve.toString());
}

main().catch(err => {
    console.error(err);
    process.exit(1);
});
