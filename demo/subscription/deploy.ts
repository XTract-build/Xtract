/**
 * Subscription — Deploy Script
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

const SOL_SOURCE  = path.join(__dirname, 'src', 'Subscription.sol');
const RUST_OUTPUT = path.join(__dirname, 'src', 'Subscription.rs');
const WASM_OUTPUT = path.join(__dirname, 'output', 'subscription.wasm');

async function main() {
    // ── Step 1: Transpile Solidity → MultiversX Rust ─────────────────────────
    console.log('Step 1: Transpiling Subscription.sol …');
    const transpiler = new XtractTranspiler();
    const result = await transpiler.transpileFile(SOL_SOURCE, RUST_OUTPUT);

    if (!result.success) {
        console.error('Transpilation failed:', result.diagnostics);
        process.exit(1);
    }
    console.log('  ✓ Written to', RUST_OUTPUT);

    // ── Step 2: Build .wasm via sc-meta ──────────────────────────────────────
    // Run manually if sc-meta is installed:
    //   cd demo/subscription && sc-meta all build
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

    // Subscription.init() takes no arguments — owner is set to deployer address
    const deployment = await deployer.deploy({
        wasmPath: WASM_OUTPUT,
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
    // Example: register a service and add a plan
    //
    // const serviceAddr = 'erd1...';
    // await deployer.call(deployment.contractAddress, 'registerService', [serviceAddr], {
    //     gasLimit: 10_000_000,
    // });
    //
    // price = 1 EGLD (10^18 atto-EGLD), duration = 30 days in seconds
    // await deployer.call(deployment.contractAddress, 'addPlan',
    //     [serviceAddr, '1000000000000000000', String(30 * 24 * 3600)],
    //     { gasLimit: 10_000_000 }
    // );
    //
    // const active = await deployer.query(deployment.contractAddress, 'isActive',
    //     [process.env.USER_ADDR, serviceAddr]);
    // console.log('Is active:', active.toString());
}

main().catch(err => {
    console.error(err);
    process.exit(1);
});
