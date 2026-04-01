#!/usr/bin/env node

/**
 * XTract CLI - Solidity to MultiversX Rust Transpiler
 *
 * This is a Node.js wrapper that invokes the Python transpiler.
 * It provides a seamless npm-based installation experience.
 */

const { spawn, spawnSync } = require('child_process');
const path = require('path');
const fs = require('fs');

// Get the package root directory
const packageRoot = path.resolve(__dirname, '..');

// Try to find Python executable
function findPython() {
    const pythonCommands = ['python3', 'python'];

    for (const cmd of pythonCommands) {
        try {
            const result = spawnSync(cmd, ['--version'], {
                encoding: 'utf-8',
                stdio: 'pipe'
            });
            if (result.status === 0) {
                return cmd;
            }
        } catch (e) {
            // Command not found, try next
        }
    }
    return null;
}

// ─── subcommand: transpile ────────────────────────────────────────────────────

function runTranspile(args) {
    const python = findPython();
    if (!python) {
        console.error('Error: Python 3.9+ is required but not found.');
        console.error('Please install Python from https://www.python.org/downloads/');
        process.exit(1);
    }

    const xtractPath = path.join(packageRoot, 'xtract');
    if (!fs.existsSync(xtractPath)) {
        console.error('Error: XTract Python module not found.');
        console.error('Please reinstall the package: npm install -g xtract-cli');
        process.exit(1);
    }

    const pythonArgs = ['-m', 'xtract.cli', ...args];

    const proc = spawn(python, pythonArgs, {
        cwd: packageRoot,
        stdio: 'inherit',
        env: {
            ...process.env,
            PYTHONPATH: packageRoot
        }
    });

    proc.on('error', (err) => {
        console.error(`Error running Python: ${err.message}`);
        process.exit(1);
    });

    proc.on('close', (code) => {
        process.exit(code || 0);
    });
}

// ─── subcommand: build ────────────────────────────────────────────────────────

function runBuild(args) {
    // Find optional -o / positional dir argument
    const contractDir = args.find(a => !a.startsWith('-')) || '.';
    const absDir = path.resolve(contractDir);

    if (!fs.existsSync(absDir)) {
        console.error(`Error: Directory not found: ${contractDir}`);
        process.exit(1);
    }

    // Check that sc-meta is available
    const check = spawnSync('sc-meta', ['--version'], { encoding: 'utf-8', stdio: 'pipe' });
    if (check.error || check.status !== 0) {
        console.error('Error: sc-meta not found.');
        console.error('Install it with:');
        console.error('  cargo install multiversx-sc-meta');
        process.exit(1);
    }

    console.log(`Building contract in ${absDir} ...`);

    const proc = spawn('sc-meta', ['build'], {
        cwd: absDir,
        stdio: 'inherit'
    });

    proc.on('error', (err) => {
        console.error(`Error running sc-meta: ${err.message}`);
        process.exit(1);
    });

    proc.on('close', (code) => {
        process.exit(code || 0);
    });
}

// ─── subcommand: deploy ───────────────────────────────────────────────────────

async function runDeploy(args) {
    // Parse --config flag
    const configIdx = args.indexOf('--config');
    const configPath = configIdx !== -1 ? args[configIdx + 1] : 'xtract.config.json';

    if (!configPath) {
        console.error('Error: --config requires a path argument.');
        process.exit(1);
    }

    const absConfig = path.resolve(configPath);
    if (!fs.existsSync(absConfig)) {
        console.error(`Error: Config file not found: ${configPath}`);
        process.exit(1);
    }

    let config;
    try {
        config = JSON.parse(fs.readFileSync(absConfig, 'utf-8'));
    } catch (err) {
        console.error(`Error: Failed to parse config file: ${err.message}`);
        process.exit(1);
    }

    const { network, walletPath, wasmPath, abiPath, initArgs = [] } = config;

    // Resolve paths relative to the config file's directory
    const configDir = path.dirname(absConfig);
    const absWasm = path.resolve(configDir, wasmPath);
    const absAbi = path.resolve(configDir, abiPath);
    const absWallet = path.resolve(configDir, walletPath);

    for (const [label, p] of [['wasmPath', absWasm], ['abiPath', absAbi], ['walletPath', absWallet]]) {
        if (!fs.existsSync(p)) {
            console.error(`Error: ${label} not found: ${p}`);
            process.exit(1);
        }
    }

    // Load ContractDeployer from sdk/dist
    const deployerPath = path.join(packageRoot, 'sdk', 'dist', 'index.js');
    if (!fs.existsSync(deployerPath)) {
        console.error('Error: SDK not built. Run: npm run build:sdk');
        process.exit(1);
    }

    let ContractDeployer;
    try {
        ({ ContractDeployer } = require(deployerPath));
    } catch (err) {
        console.error(`Error: Failed to load SDK: ${err.message}`);
        process.exit(1);
    }

    try {
        const deployer = new ContractDeployer({ network, walletPath: absWallet });
        const result = await deployer.deploy({
            wasmPath: absWasm,
            abiPath: absAbi,
            initArgs
        });

        const explorerBase = network === 'mainnet'
            ? 'https://explorer.multiversx.com'
            : `https://${network}-explorer.multiversx.com`;

        console.log(`Deployed to: ${result.address}`);
        console.log(`Tx: ${explorerBase}/transactions/${result.txHash}`);
    } catch (err) {
        console.error(`Deploy failed: ${err.message}`);
        process.exit(1);
    }
}

// ─── subcommand: scaffold ─────────────────────────────────────────────────────

function runScaffold(args) {
    const name = args.find(a => !a.startsWith('-'));
    if (!name) {
        console.error('Error: Please provide a contract name.');
        console.error('Usage: xtract scaffold <name>');
        process.exit(1);
    }

    const destDir = path.resolve(name);
    if (fs.existsSync(destDir)) {
        console.error(`Error: Directory already exists: ${destDir}`);
        process.exit(1);
    }

    // Kebab-case package name for Cargo
    const kebab = name.replace(/([a-z])([A-Z])/g, '$1-$2').toLowerCase();

    // File contents
    const solContent =
`// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ${name} {
    address public owner;
    string public message;

    constructor() {
        owner = msg.sender;
        message = "Hello from ${name}!";
    }

    function getMessage() public view returns (string memory) {
        return message;
    }

    function setMessage(string memory newMessage) public {
        require(msg.sender == owner, "Not owner");
        message = newMessage;
    }
}
`;

    const cargoContent =
`[package]
name = "${kebab}"
version = "0.1.0"
edition = "2021"
publish = false

[lib]
path = "src/${name}.rs"

[dependencies.multiversx-sc]
version = "0.53.0"
features = []

[dev-dependencies.multiversx-sc-scenario]
version = "0.53.0"

[workspace]
members = [
    ".",
    "meta",
]
`;

    const multiversxJson = JSON.stringify({ language: 'rust' }, null, 4) + '\n';

    const xtractConfig = JSON.stringify({
        network: 'devnet',
        walletPath: './wallet.pem',
        wasmPath: `./output/${kebab}.wasm`,
        abiPath: `./output/${kebab}.abi.json`,
        initArgs: []
    }, null, 4) + '\n';

    const readmeContent =
`# ${name}

A MultiversX smart contract generated by [XTract](https://github.com/XTract-build/Xtract).

## Workflow

### 1. Transpile Solidity → Rust
\`\`\`bash
xtract transpile src/${name}.sol -o src/${name}.rs
\`\`\`

### 2. Build the contract
\`\`\`bash
xtract build .
\`\`\`

### 3. Deploy to devnet
Edit \`xtract.config.json\` with your wallet path, then:
\`\`\`bash
xtract deploy --config xtract.config.json
\`\`\`

## Requirements

- [Rust](https://rustup.rs/) with \`wasm32-unknown-unknown\` target
- \`sc-meta\`: \`cargo install multiversx-sc-meta\`
`;

    // Create directory tree
    fs.mkdirSync(path.join(destDir, 'src'), { recursive: true });
    fs.mkdirSync(path.join(destDir, 'wasm'), { recursive: true });
    fs.mkdirSync(path.join(destDir, 'meta', 'src'), { recursive: true });

    fs.writeFileSync(path.join(destDir, 'src', `${name}.sol`), solContent);
    fs.writeFileSync(path.join(destDir, 'Cargo.toml'), cargoContent);
    fs.writeFileSync(path.join(destDir, 'multiversx.json'), multiversxJson);
    fs.writeFileSync(path.join(destDir, 'xtract.config.json'), xtractConfig);
    fs.writeFileSync(path.join(destDir, 'README.md'), readmeContent);
    fs.writeFileSync(path.join(destDir, 'wasm', '.gitkeep'), '');

    // meta/Cargo.toml
    const metaCargo =
`[package]
name = "${kebab}-meta"
version = "0.1.0"
edition = "2021"
publish = false

[dependencies.${kebab}]
path = ".."

[dependencies.multiversx-sc-meta-lib]
version = "0.53.0"
default-features = false
`;
    fs.writeFileSync(path.join(destDir, 'meta', 'Cargo.toml'), metaCargo);

    // meta/src/main.rs
    const metaMain =
`fn main() {
    multiversx_sc_meta_lib::cli_main::<${kebab.replace(/-/g, '_')}::AbiProvider>();
}
`;
    fs.writeFileSync(path.join(destDir, 'meta', 'src', 'main.rs'), metaMain);

    console.log(`Scaffolded new contract: ${name}/`);
    console.log(`  src/${name}.sol`);
    console.log(`  Cargo.toml`);
    console.log(`  multiversx.json`);
    console.log(`  xtract.config.json`);
    console.log(`  README.md`);
    console.log(`  wasm/.gitkeep`);
    console.log(`  meta/Cargo.toml`);
    console.log(`  meta/src/main.rs`);
    console.log('');
    console.log(`Next steps:`);
    console.log(`  cd ${name}`);
    console.log(`  xtract transpile src/${name}.sol -o src/${name}.rs`);
    console.log(`  xtract build .`);
}

// ─── main ─────────────────────────────────────────────────────────────────────

function printHelp() {
    const pkg = require('../package.json');
    console.log(`
XTract v${pkg.version} - Solidity to MultiversX Rust Transpiler

Usage:
  xtract transpile <input.sol> [-o output.rs]   Transpile a Solidity file
  xtract build <contract-dir>                    Build with sc-meta
  xtract deploy --config <xtract.config.json>   Deploy a compiled contract
  xtract scaffold <name>                         Create new contract scaffolding

  xtract <input.sol> [output.rs]                 Shorthand for transpile (backward compat)

Transpile options:
  -v, --verbose    Show detailed diagnostics
  -q, --quiet      Suppress non-error output
  -o <file>        Output file (transpile only)

Global options:
  -h, --help       Show this help message
  --version        Show version

Examples:
  xtract MyContract.sol                          # transpile (backward compat)
  xtract transpile MyContract.sol -o out.rs
  xtract build ./my-contract
  xtract deploy --config xtract.config.json
  xtract scaffold HelloWorld

For more information: https://github.com/XTract-build/Xtract
`);
}

async function main() {
    const argv = process.argv.slice(2);

    // Global flags
    if (argv.includes('-h') || argv.includes('--help')) {
        printHelp();
        process.exit(0);
    }

    if (argv.includes('--version')) {
        const pkg = require('../package.json');
        console.log(`xtract v${pkg.version}`);
        process.exit(0);
    }

    const subcommand = argv[0];
    const rest = argv.slice(1);

    // Backward compat: if first arg looks like a .sol file, treat as transpile
    if (!subcommand || subcommand.endsWith('.sol')) {
        runTranspile(argv);
        return;
    }

    switch (subcommand) {
        case 'transpile':
            runTranspile(rest);
            break;
        case 'build':
            runBuild(rest);
            break;
        case 'deploy':
            await runDeploy(rest);
            break;
        case 'scaffold':
            runScaffold(rest);
            break;
        default:
            console.error(`Error: Unknown subcommand '${subcommand}'.`);
            console.error("Run 'xtract --help' for usage.");
            process.exit(1);
    }
}

main().catch((err) => {
    console.error(err.message);
    process.exit(1);
});
