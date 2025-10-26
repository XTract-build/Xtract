### MultiversX Initial Nodes Setup Example (nodesSetup.json)

Source: https://docs.multiversx.com/developers/overview/sovereign/distributed-setup

An example `nodesSetup.json` file for a MultiversX sovereign chain, illustrating how to configure initial network parameters such as start time, round duration, consensus group sizes, and a list of initial nodes with their public keys and associated addresses.

```json
{
  "startTime": 1733138599,
  "roundDuration": 6000,
  "consensusGroupSize": 2,
  "minNodesPerShard": 2,
  "metaChainConsensusGroupSize": 0,
  "metaChainMinNodes": 0,
  "hysteresis": 0,
  "adaptivity": false,
  "initialNodes": [
    {
      "pubkey": "6a1ee46baa8da9279f53addbfbc61a525604eb42d964bd3a25bf7f34097c3b3a31706728718ccdbe3d43386c37ec3011df6ceb4188e14025ab149bd568cafaba18a78b51e71c24046c5276a187a6c1d6da83e30590a6025875b8f6df8984ec05",
      "address": "erd1a2jq3rrqa0heta0fmlkrymky7yj247mrs54g6fyyx8dm45menkrsmu3dez",
      "initialRating": 0
    },
    {
      "pubkey": "40f3857218333f0b2ba8592fc053cbaebec8e1335f95957c89f6c601ce0758372ba31c30700f10f25202d8856bb948055f9f0ef53dea57b62f013ee01c9dc0346a2b3543f2b4d423166ee1981b310f2549fb879d4cd89de6c392d902a823d116",
      "address": "erd1pn564xpwk4anq9z50th3ae99vplsf7d2p55cnugf00eu0gcq6gdqcg7ytx",
      "initialRating": 0
    }
  ]
}
```

--------------------------------

### Run Observing Squad Installation Script

Source: https://docs.multiversx.com/developers/overview/integrators/observing-squad

Executes the primary installation script for the Observing Squad. This command initiates the setup process based on the configurations defined in `variables.cfg`.

```bash
./script.sh observing_squad
```

--------------------------------

### Start MultiversX Chain Simulator

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/chain-simulator-adder

Demonstrates how to start the Chain Simulator after successful installation, showing the command and the typical output indicating a successful startup with configuration details.

```Shell
my-adder/interactor$ sudo my-path/.cargo/bin/sc-meta cs start

```

```Shell
Attempting to start the Chain Simulator...
Successfully started the Chain Simulator.
INFO [2024-11-11 13:09:15.683]   using the override config files          files = [./config/nodeOverrideDefault.toml]
WARN [2024-11-11 13:09:15.684]   signature                                bypass = true
INFO [2024-11-11 13:09:15.699]   updated config value                     file = systemSmartContractsConfig.toml path = ESDTSystemSCConfig.BaseIssuingCost value = 50000000000000000
INFO [2024-11-11 13:09:15.699]   updated config value                     file = config.toml path = Debug.Process.Enabled value = false
INFO [2024-11-11 13:09:15.699]   updated config value                     file = config.toml path = VirtualMachine.Execution.WasmVMVersions value = [map[StartEpoch:0 Version:1.5]]
INFO [2024-11-11 13:09:15.699]   updated config value                     file = config.toml path = VirtualMachine.Querying.WasmVMVersions value = [map[StartEpoch:0 Version:1.5]]
INFO [2024-11-11 13:09:15.699]   updated config value                     file = config.toml path = WebServerAntiflood.WebServerAntifloodEnabled value = false
INFO [2024-11-11 13:09:15.699]   updated config value                     file = config.toml path = WebServerAntiflood.SimultaneousRequests value = 100000
...
```

--------------------------------

### Install docker-compose

Source: https://docs.multiversx.com/developers/overview/integrators/observing-squad

Ensure `docker-compose` is installed on your system. If not, use the `apt install` command to install it before proceeding with Docker-based setup.

```bash
apt install docker-compose
```

--------------------------------

### Example localnet startup logs

Source: https://docs.multiversx.com/developers/overview/developers/setup-local-testnet

Provides an illustrative example of the console output expected when the MultiversX localnet successfully starts. The logs indicate the initiation of key processes such as the seednode, blockchain nodes, and the proxy, confirming the network's operational status.

```text
INFO:cli.localnet:Starting localnet...
...
INFO:localnet:Starting process ['./seednode', ...
...
INFO:localnet:Starting process ['./node', ...
...
INFO:localnet:Starting process ['./proxy', ...
[PID=...] DEBUG[...] [process/block]       started committing block ...
```

--------------------------------

### Start MultiversX Observing Squad Docker Stack

Source: https://docs.multiversx.com/developers/overview/integrators/observing-squad

Navigate into the `mainnet` directory within the cloned repository and execute the `start_stack.sh` script. This script will install and run the entire Observing Squad using Docker.

```bash
cd mainnet
./start_stack.sh
```

--------------------------------

### Example: Installing 'testwallets' Dependency with mxpy

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/mxpy/mxpy-cli

A practical example demonstrating how to install the `testwallets` dependency using the `mxpy deps install` command. This command adds the specified component to the `mxpy` environment.

```Shell
mxpy deps install testwallets
```

--------------------------------

### Run Sovereign Bridge Prerequisites Script

Source: https://docs.multiversx.com/developers/overview/sovereign/local-setup

Executes the `prerequisites.sh` script to install required software dependencies and download cross-chain contracts, preparing the environment for the sovereign bridge setup.

```bash
./prerequisites.sh
```

--------------------------------

### Execute Prerequisites Script for MultiversX Localnet

Source: https://docs.multiversx.com/developers/overview/developers/setup-local-testnet-advanced

This command navigates into the `mx-chain-go` testnet scripts directory and executes the `prerequisites.sh` script. This script automates the installation of necessary packages and clones additional required repositories, streamlining the setup process for the local testnet.

```Bash
$ cd mx-chain-go/scripts/testnet
$ ./prerequisites.sh
```

--------------------------------

### Setup and Start MultiversX Localnet

Source: https://docs.multiversx.com/developers/overview/developers/setup-local-testnet

Executes the full setup process for the MultiversX localnet, including prerequisites, build, and configuration, and then initiates the localnet operation. This command is used after all configurations are finalized.

```bash
mxpy localnet setup
mxpy localnet start
```

--------------------------------

### Start Observing Squad Nodes and Proxy

Source: https://docs.multiversx.com/developers/overview/integrators/observing-squad

Starts all components of the installed Observing Squad, including the observer nodes and the associated proxy service. This command brings the entire squad online.

```bash
./script.sh start
```

--------------------------------

### Generate Adder Contract Template

Source: https://docs.multiversx.com/developers/overview/developers/meta/interactor/interactors-example

This command uses `sc-meta` to create a new contract folder, pre-populated with a copy of the `adder` contract, streamlining the setup process for the interactor example.

```Shell
sc-meta new --template adder
```

--------------------------------

### Example: Checking 'testwallets' Dependency with mxpy

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/mxpy/mxpy-cli

A practical example demonstrating how to check the installation status of the `testwallets` dependency using the `mxpy deps check` command. This verifies if the component is present and ready for use.

```Shell
mxpy deps check testwallets
```

--------------------------------

### List Running Docker Containers

Source: https://docs.multiversx.com/developers/overview/integrators/observing-squad

After starting the Docker stack, verify that the Observing Squad components are running by listing all active Docker containers using the `docker ps` command.

```bash
docker ps
```

--------------------------------

### MultiversX Genesis Configuration Example (genesis.json)

Source: https://docs.multiversx.com/developers/overview/sovereign/distributed-setup

An example `genesis.json` file demonstrating the structure for defining initial addresses, their supply, balance, and staking values. This file is crucial for funding genesis accounts and designating validators at the network's inception.

```json
[
  {
    "address": "erd1a2jq3rrqa0heta0fmlkrymky7yj247mrs54g6fyyx8dm45menkrsmu3dez",
    "supply": "10000000000000000000000000",
    "balance": "9997500000000000000000000",
    "stakingvalue": "2500000000000000000000",
    "delegation": {
      "address": "",
      "value": "0"
    }
  },
  {
    "address": "erd1pn564xpwk4anq9z50th3ae99vplsf7d2p55cnugf00eu0gcq6gdqcg7ytx",
    "supply": "10000000000000000000000000",
    "balance": "9997500000000000000000000",
    "stakingvalue": "2500000000000000000000",
    "delegation": {
      "address": "",
      "value": "0"
    }
  }
]
```

--------------------------------

### Start MultiversX Sovereign Extras Service

Source: https://docs.multiversx.com/developers/overview/sovereign/sovereign-api

This command initiates the MultiversX Sovereign Extras service in a custom environment. It leverages `npm` to execute the `start:faucet` script, which is typically defined within the project's `package.json` file. Users should ensure Node.js and npm are installed, and all project dependencies are satisfied before running this command.

```Shell
NODE_ENV=custom npm run start:faucet
```

--------------------------------

### Setup and Start MultiversX Localnet

Source: https://docs.multiversx.com/developers/overview/developers/setup-local-testnet

These commands are used to finalize the MultiversX localnet setup based on the `localnet.toml` configuration and then start the localnet. This step is performed after any configuration changes, such as sharding alterations or local source build settings.

```bash
mxpy localnet setup
mxpy localnet start
```

--------------------------------

### Install Dependencies and Start Sovereign Lite Wallet

Source: https://docs.multiversx.com/developers/overview/sovereign/sovereign-wallet

Executes `yarn install` to download and set up all necessary project dependencies, followed by `yarn start:sovereign` to launch the MultiversX Sovereign Lite Wallet application. This command initiates the wallet service, making it accessible.

```bash
yarn install
yarn start:sovereign
```

--------------------------------

### Configure Observing Squad Environment Variables

Source: https://docs.multiversx.com/developers/overview/integrators/observing-squad

Example configuration for the `config/variables.cfg` file. This snippet shows how to set the network environment (e.g., 'mainnet'), custom home directory, and user for the Observing Squad installation.

```bash
ENVIRONMENT="mainnet"
...
CUSTOM_HOME="/home/ubuntu"
CUSTOM_USER="ubuntu"
```

--------------------------------

### MultiversX CLI: Install Development Tools

Source: https://docs.multiversx.com/developers/overview/developers/meta/sc-meta-cli

Describes the `install` command used to set up necessary tools for MultiversX smart contract development, interaction, and testing. It supports installing all known tools or specific ones like `mx-scenario-go`, with an option to specify framework versions.

```APIDOC
install:
  description: "Installs tools needed for smart contract development, interaction and testing."
  parameters:
    all: "Installs all the known tools."
    mx-scenario-go: "Installs the `mx-scenario-go` tool. Can further specify the framework version on which the contracts should be created by using `--tag`."
```

--------------------------------

### Start MultiversX dApp

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/your-first-microservice

This command starts the MultiversX decentralized application in development mode. It compiles the dApp and serves it, allowing users to interact with the updated microservice integration.

```bash
npm run start
```

--------------------------------

### Install MultiversX dApp Development Prerequisites

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/your-first-dapp

Commands to install and verify the necessary tools for MultiversX dApp development, including Rust, `multiversx-sc-meta`, Node.js, and Yarn. These tools are essential for compiling smart contracts and managing frontend dependencies.

```Shell
stable Rust version ≥ 1.78.0 (install via rustup)
Node.js with version ≥ 20 (guide here)
```

```Rust
cargo install multiversx-sc-meta
```

```JavaScript
npm install --global yarn
```

--------------------------------

### Execute MultiversX Observing Squad Setup Commands

Source: https://docs.multiversx.com/developers/overview/bridge/axelar

This snippet provides a sequence of `bash` commands to clone the `mx-chain-scripts` repository, set up the Observing Squad using `./script.sh observing_squad`, and start the nodes and Proxy service with `./script.sh start`.

```bash
git clone https://github.com/multiversx/mx-chain-scripts
./script.sh observing_squad
./script.sh start
```

--------------------------------

### Setup MultiversX localnet in one go

Source: https://docs.multiversx.com/developers/overview/developers/setup-local-testnet

Executes a comprehensive setup process for the MultiversX localnet. This single command handles the creation, prerequisite checks, building, and configuration of the localnet components, streamlining the initial setup.

```bash
mxpy localnet setup
```

--------------------------------

### Create New MultiversX Smart Contract Project

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/crowdfunding-p1

Command to initialize a new MultiversX smart contract project using the `sc-meta` tool, based on a specified template. This sets up the basic directory structure and initial files.

```bash
sc-meta new --name crowdfunding --template empty
```

--------------------------------

### Clone MultiversX Repositories for Localnet Setup

Source: https://docs.multiversx.com/developers/overview/developers/setup-local-testnet-advanced

This command sequence creates a new directory and then clones the essential `mx-chain-go` and `mx-chain-proxy-go` repositories from GitHub, which are fundamental components for establishing a local MultiversX Testnet environment.

```Bash
$ mkdir mytestnet && cd mytestnet
$ git clone git@github.com:multiversx/mx-chain-go.git
$ git clone git@github.com/multiversx/mx-chain-proxy-go.git
```

--------------------------------

### Install Dependencies for MultiversX dApp Template

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/your-first-dapp

These commands ensure that the necessary package managers and development tools are available for the dApp. It first installs `yarn` globally and then adds `vite` as a development dependency, which is crucial for building and running the dApp.

```Shell
npm install --global yarn
yarn add vite --dev
```

--------------------------------

### Start MultiversX Testnet

Source: https://docs.multiversx.com/developers/overview/developers/setup-local-testnet-advanced

To initiate the Testnet, execute the `start.sh` script, optionally with the `debug` flag for verbose output. After execution, allow approximately one minute for nodes to become active.

```bash
./start.sh debug
```

--------------------------------

### Install and Start Redis on Linux

Source: https://docs.multiversx.com/developers/overview/sovereign/services

These commands facilitate the installation and automatic startup of the Redis server on Debian/Ubuntu-based systems. Redis is utilized for caching and data persistence within the Sovereign Chain services.

```Shell
sudo apt update
sudo apt install redis
sudo systemctl start redis
sudo systemctl enable redis
```

--------------------------------

### Start Sovereign API Service

Source: https://docs.multiversx.com/developers/overview/sovereign/sovereign-api

This command initiates the MultiversX Sovereign API service using `npm`. It specifically runs the `start:testnet` script, implying that it will use the testnet configuration files. Ensure all dependencies are installed before running this command.

```npm
npm run start:testnet
```

--------------------------------

### Install MultiversX sdk-dapp Library

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-dapp

Instructions to install the MultiversX sdk-dapp library, a React-based tool for MultiversX dApps, using npm or yarn package managers.

```shell
npm install @multiversx/sdk-dapp
```

```shell
yarn add @multiversx/sdk-dapp
```

--------------------------------

### Monitor MultiversX Observers with termui

Source: https://docs.multiversx.com/developers/overview/integrators/observing-squad

Use the `termui` utility, installed during the setup process, to monitor the status of running MultiversX Observer nodes for different shards and the Metachain. Replace `localhost` and ports as per your configuration.

```bash
~/elrond-utils/termui --address localhost:8080    # Shard 0
~/elrond-utils/termui --address localhost:8081    # Shard 1
~/elrond-utils/termui --address localhost:8082    # Shard 2
~/elrond-utils/termui --address localhost:8083    # Metachain
```

--------------------------------

### Start MultiversX Validator Node

Source: https://docs.multiversx.com/developers/overview/validators/nodes-scripts/install-update

This command uses the `script.sh` utility to initiate the MultiversX validator node. Executing this command brings the node online, allowing it to begin participating in the network.

```Bash
~/mx-chain-scripts/script.sh start
```

--------------------------------

### Constructing a Basic MultiversX Transaction in Rust

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/eth-to-mvx

Illustrates the fluent API for building a MultiversX transaction. Starting with `self.tx()`, developers chain methods like `from`, `to`, `payment`, `gas`, `raw_call`, and `with_result` to progressively define the transaction's parameters before execution. This example shows the initial construction phase.

```Rust
self.tx()
    .from(from)
    .to(to)
    .payment(payment)
    .gas(gas)
    .raw_call("function")
    .with_result(result_handler)
```

--------------------------------

### Clone MultiversX Observing Squad Repository

Source: https://docs.multiversx.com/developers/overview/integrators/observing-squad

To set up the Observing Squad using Docker, begin by cloning the official MultiversX Observing Squad GitHub repository to your local machine.

```bash
git clone https://github.com/multiversx/mx-chain-observing-squad.git
```

--------------------------------

### Example: Overwriting 'testwallets' Dependency Installation

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/mxpy/mxpy-cli

Demonstrates how to force an overwrite of an existing dependency installation using the `--overwrite` argument with `mxpy deps install`. This ensures that the latest version or a specific version of the dependency is installed, replacing any prior installation.

```Shell
mxpy deps install testwallets --overwrite
```

--------------------------------

### Set Up MultiversX Proxy Instance

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/proxy

This snippet provides the necessary shell commands to clone the MultiversX Proxy Go repository, navigate into the proxy's command directory, and build the executable. It's the initial step for hosting a local proxy instance.

```bash
git clone https://github.com/multiversx/mx-chain-proxy-go.git
cd elrond-proxy-go/cmd/proxy
go build .
```

--------------------------------

### Execute Prerequisites Script for Sovereign Chain Setup

Source: https://docs.multiversx.com/developers/overview/sovereign/local-setup

This script verifies and downloads all necessary packages required to run the MultiversX sovereign chain nodes. It also clones additional repositories such as 'mx-chain-deploy-sovereign-go', 'mx-chain-proxy-sovereign-go', 'mx-chain-sovereign-bridge-go', and 'mx-chain-tools-go', which are crucial for chain configuration, proxy services, cross-chain bridging, and elastic index updates.

```Bash
./prerequisites.sh
```

--------------------------------

### Underlying commands for mxpy localnet setup

Source: https://docs.multiversx.com/developers/overview/developers/setup-local-testnet

Details the individual mxpy sub-commands that are executed sequentially when 'mxpy localnet setup' is run. These commands include creating a new localnet instance, checking prerequisites, building components, and configuring the network.

```bash
mxpy localnet new
mxpy localnet prerequisites
mxpy localnet build
mxpy localnet config
```

--------------------------------

### Direct Command for MultiversX Node Installation

Source: https://docs.multiversx.com/developers/overview/validators/nodes-scripts/install-update

As an alternative to the interactive menu, this command directly triggers the node installation process using the `script.sh` utility. It provides a non-interactive way to initiate the setup of the MultiversX validator node.

```Bash
~/mx-chain-scripts/script.sh install
```

--------------------------------

### Install Rust Toolchain for MultiversX Development

Source: https://docs.multiversx.com/developers/overview/developers/meta/interactor/interactors-overview

These commands guide the installation of the Rust programming language and its necessary components for MultiversX smart contract development. It includes installing `rustup`, updating the toolchain, setting the default stable version, and adding the `wasm32-unknown-unknown` target, which is essential for compiling WebAssembly smart contracts.

```Shell
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

```Shell
rustup update
rustup default stable
rustup target add wasm32-unknown-unknown
```

```Shell
rustc --version
rustup show
```

--------------------------------

### Query MultiversX Observer Status with curl

Source: https://docs.multiversx.com/developers/overview/integrators/observing-squad

Alternatively, perform GET requests using `curl` to retrieve the status of MultiversX Observer nodes for different shards and the Metachain. The output is piped to `jq` for pretty printing and easier readability.

```bash
curl http://localhost:8080/node/status | jq    # Shard 0
curl http://localhost:8081/node/status | jq    # Shard 1
curl http://localhost:8082/node/status | jq    # Shard 2
curl http://localhost:8083/node/status | jq    # Metachain
```

--------------------------------

### Solidity Adder Smart Contract Example

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/eth-to-mvx

A basic smart contract written in Solidity for the Ethereum blockchain. It demonstrates a constructor to initialize a sum, a public function to add a value to the sum, and a constant function to retrieve the current sum.

```Solidity
contract Adder {
    uint private sum;

    constructor(uint memory initialValue) public {
        sum = initialValue;
    }

    function add(uint value) public {
        sum += value;
    }

    function getSum() public constant returns (uint) {
        return sum;
    }
}
```

--------------------------------

### Hyperblock Processing Log Example

Source: https://docs.multiversx.com/developers/overview/integrators/egld-integration-guide

Illustrates the sequence of operations for processing hyperblocks by nonce, including fetching, processing, saving the last processed nonce, and handling API errors for nonces not yet available. It demonstrates the system's behavior when waiting for new hyperblocks.

```Log Output
...\n-> fetched hyperblock with nonce 900\n-> processed hyperblock with nonce 900\n-> saved last processed nonce = 900\n-> waiting 2 seconds\n-> fetching hyperblock with nonce 901: API error (nonce not yet processed on chain side), skip\n-> waiting 2 seconds\n-> fetching hyperblock with nonce 901: API error (nonce not yet processed on chain side), skip\n-> waiting 2 seconds\n-> fetched the hyperblock with nonce 901\n-> processed hyperblock with nonce 901\n-> saved last processed nonce = 901\n-> waiting 2 seconds\n...
```

--------------------------------

### Create New Project Directory for Ping-Pong DApp

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/your-first-dapp

Initializes a new project folder named 'ping-pong' and navigates into it. This directory will serve as the root for the entire dApp project, containing subfolders for wallet, contract, and dapp components.

```bash
mkdir -p ping-pong
cd ping-pong/
```

--------------------------------

### MultiversX Crowdfunding Contract Project Structure

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/crowdfunding-p1

Displays the recommended directory layout for a MultiversX smart contract project, including source code, build outputs, and dedicated test folders for blackbox testing.

```Shell
.
├── Cargo.lock
├── Cargo.toml
├── meta
│   ├── Cargo.toml
│   └── src
├── multiversx.json
├── output
│   ├── crowdfunding.abi.json
│   ├── crowdfunding.imports.json
│   ├── crowdfunding.mxsc.json
│   └── crowdfunding.wasm
├── src
│   └── crowdfunding.rs
├── target
│   ├── CACHEDIR.TAG
│   ├── debug
│   ├── release
│   ├── tmp
│   └── wasm32-unknown-unknown
├── tests
│   └── crowdfunding_blackbox_test.rs
└── wasm
    ├── Cargo.lock
    ├── Cargo.toml
    └── src
```

--------------------------------

### Check pip3 Version

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/mxpy/installing-mxpy

This command verifies if pip3 is installed on the system and displays its version, which is a prerequisite for shell completion setup.

```Shell
pip3 --version
```

--------------------------------

### Start MultiversX dApp Development Server

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/your-first-dapp

This command initiates the local development server for a MultiversX dApp, allowing for local testing and interaction. It's typically used during the development phase to run the application and make it accessible via a web browser.

```Shell
yarn start:devnet
```

--------------------------------

### Start MultiversX Node Visual Interface (TermUI)

Source: https://docs.multiversx.com/developers/overview/validators/nodes-scripts/install-update

This snippet shows how to navigate to the `elrond-utils` directory and then launch the `TermUI` application. `TermUI` provides a visual interface to monitor the progress and status of a running validator node, connecting to its local REST API endpoint.

```Bash
cd $HOME/elrond-utils
./termui -address localhost:8080
```

--------------------------------

### Fetch MultiversX Localnet Software Prerequisites

Source: https://docs.multiversx.com/developers/overview/developers/setup-local-testnet

Downloads necessary software components like `mx-chain-go` and `mx-chain-proxy-go` into `~/multiversx-sdk` for the localnet setup. This step is crucial when `resolution = remote` is specified in `localnet.toml`.

```bash
mxpy localnet prerequisites
```

--------------------------------

### Installing mxpy Dependencies

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/mxpy/mxpy-cli

Shows the command for installing a new dependency using `mxpy`. This command takes the dependency's name as a positional argument, facilitating the setup of required components for `mxpy` operations.

```Shell
mxpy deps install <dependency-name>
```

--------------------------------

### Perform Smoke Test to Fetch Latest Hyperblock

Source: https://docs.multiversx.com/developers/overview/integrators/observing-squad

Execute a smoke test to fetch the latest synchronized hyperblock. This involves first querying the network status to get the highest final nonce, then using that nonce to retrieve the corresponding hyperblock data.

```bash
export NONCE=$(curl http://localhost:8079/network/status/4294967295 | jq '.data["status"]["erd_highest_final_nonce"]')
curl http://localhost:8079/hyperblock/by-nonce/$NONCE | jq
```

--------------------------------

### Install MultiversX Chain Simulator

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/chain-simulator-adder

Instructions for installing the Chain Simulator Docker image using `sc-meta cs install`. It also covers common troubleshooting steps for permission denied errors (requiring `sudo`) and `command not found` errors (finding and using the full path to `sc-meta`).

```Shell
my-adder/interactor$ sc-meta cs install
Attempting to install prerequisites for the Chain Simulator...
Successfully pulled the latest Chain Simulator image.

```

```Shell
Attempting to install prerequisites for the Chain Simulator...
Error: Failed to execute command: permission denied while trying to connect to the Docker daemon socket at unix:///var/run/docker.sock

```

```Shell
my-adder/interactor$ sudo sc-meta cs install

```

```Shell
sudo: sc-meta: command not found

```

```Shell
my-adder/interactor$ which sc-meta
my-path/.cargo/bin/sc-meta

```

```Shell
sudo my-path/.cargo/bin/sc-meta cs install

```

--------------------------------

### MultiversX Validator Script Menu Options

Source: https://docs.multiversx.com/developers/overview/validators/nodes-scripts/install-update

This displays the interactive menu presented by the `script.sh` utility, offering various actions like install, upgrade, start, stop, and cleanup for the validator node. Users select an option by entering its corresponding number.

```Bash
 1) install
 2) observing_squad
 3) multikey_group
 4) upgrade
 5) upgrade_multikey
 6) upgrade_squad
 7) upgrade_proxy
 8) remove_db
 9) start
10) start_all
11) stop
12) stop_all
13) cleanup
14) github_pull
15) add_nodes
16) get_logs
17) benchmark
18) quit
 Please select an action:1
```

--------------------------------

### Example Output of Get Staked Addresses Query

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/staking-contract

Illustrative output showing a single staked address in Bech32 format, as a result of the `getStakedAddresses` query.

```Plaintext
Result: erd1vx...
```

--------------------------------

### Create a new MultiversX staking smart contract project

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/staking-contract

This command initializes a new empty smart contract project named 'staking-contract' using the `sc-meta` tool. It sets up the basic directory structure required for MultiversX smart contract development.

```Bash
sc-meta new --name staking-contract --template empty
```

--------------------------------

### Configure Test Accounts in MultiversX Rust Blackbox Test

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/crowdfunding-p1

Rust code example showing how to define and initialize a mock account (`OWNER`) with a specific nonce and balance within the `ScenarioWorld` for blackbox testing MultiversX smart contracts.

```Rust
const OWNER: TestAddress = TestAddress::new("owner");

#[test]
fn crowdfunding_deploy_test() {
    let mut world = world();

    world.account(OWNER).nonce(0).balance(1000000);
}
```

--------------------------------

### Create New MultiversX Localnet Workspace

Source: https://docs.multiversx.com/developers/overview/developers/setup-local-testnet

Creates a new directory for a MultiversX localnet instance and navigates into it, preparing for individual setup steps. This allows for more granular control over the localnet configuration.

```bash
mkdir -p ~/my-second-localnet && cd ~/my-second-localnet
```

--------------------------------

### Source Management Script for Stop/Clean

Source: https://docs.multiversx.com/developers/overview/sovereign/local-setup

Sources `script.sh` to load functions required for stopping and cleaning the local Sovereign Chain and its associated services.

```bash
source script.sh
```

--------------------------------

### Example Output of MultiversX Smart Contract Deployment

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/your-first-dapp

This snippet shows the typical console output after successfully running the smart contract deployment command. It includes details such as the sender's nonce, transaction hash, and the newly deployed contract address, which are crucial for verification and further interaction.

```Shell
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.48s
     Running `/ping-pong/contract/target/debug/ping-pong-interact deploy --ping-amount 1000000000000000000 --duration-in-seconds 180`
sender's recalled nonce: 12422
-- tx nonce: 12422
sc deploy tx hash: b6ca6c8e6ac54ed168bcd6929e762610e2360674f562115107cf3702b8a22467
deploy address: erd1qqqqqqqqqqqqqpgqymj43x6anzr38jfz7kw3td2ew33v9jtrd8sse5zzk6
new address: erd1qqqqqqqqqqqqqpgqymj43x6anzr38jfz7kw3td2ew33v9jtrd8sse5zzk6
```

--------------------------------

### MultiversX Rust Staking Contract Test Setup

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/staking-contract

This Rust code snippet provides the initial setup for testing the MultiversX staking smart contract. It imports necessary modules, defines constants for addresses and contract paths, and sets up initial values like user balance and APY for test scenarios.

```Rust
mod staking_contract_proxy;
use multiversx_sc::{
    imports::OptionalValue,
    types::{BigUint, TestAddress, TestSCAddress},
};
use multiversx_sc_scenario::imports::*;
use staking_contract_proxy::StakingPosition;

const OWNER_ADDRESS: TestAddress = TestAddress::new("owner");
const USER_ADDRESS: TestAddress = TestAddress::new("user");
const STAKING_CONTRACT_ADDRESS: TestSCAddress = TestSCAddress::new("staking-contract");
const WASM_PATH: MxscPath = MxscPath::new("output/staking-contract.mxsc.json");
const USER_BALANCE: u64 = 1_000_000_000_000_000_000;
const APY: u64 = 10_00; // 10%

struct ContractSetup {
```

--------------------------------

### CLI: Build MultiversX Smart Contract

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/crowdfunding-p1

This command-line instruction is used to build a MultiversX smart contract. Running `sc-meta all build` compiles the contract code, ensuring it is ready for deployment and testing.

```CLI
sc-meta all build
```

--------------------------------

### Install Redis Server on Linux

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/your-first-microservice

This command installs the Redis server package on Debian/Ubuntu-based Linux distributions using the `apt` package manager. Redis is used for caching in the microservice.

```bash
sudo apt install redis-server
```

--------------------------------

### Navigate to Testnet Scripts Directory

Source: https://docs.multiversx.com/developers/overview/sovereign/local-setup

After cloning the repository, this command changes the current directory to the 'scripts/testnet' subdirectory within the 'mx-chain-sovereign-go' repository. This directory contains essential setup scripts.

```Bash
cd mx-chain-sovereign-go/scripts/testnet
```

--------------------------------

### Initialize Scenario World for Testing Environment

Source: https://docs.multiversx.com/developers/overview/developers/testing/rust/sc-blackbox-example

Defines the `world` function, which initializes a `ScenarioWorld` instance, registers the `adder` contract with its code path, and provides access to the testing framework's methods for environment setup.

```Rust
fn world() -> ScenarioWorld {
    let mut blockchain = ScenarioWorld::new();
    blockchain.register_contract(CODE_PATH, adder::ContractBuilder);
    blockchain
}

```

--------------------------------

### Example MultiversX Localnet Directory Tree Output

Source: https://docs.multiversx.com/developers/overview/developers/setup-local-testnet

Shows a typical directory structure generated after configuring a MultiversX localnet. It includes configuration files, shared libraries, and executable nodes for proxy, seednode, and multiple validator instances.

```text
├── localnet
│   ├── proxy
│   │   ├── config
│   │   └── proxy
│   ├── seednode
│   │   ├── config
│   │   ├── libwasmer_linux_amd64.so
│   |   ├── ...
│   │   └── seednode
│   ├── validator00
│   │   ├── config
│   │   ├── libwasmer_linux_amd64.so
│   |   ├── ...
│   │   └── node
│   ├── validator01
│   │   ├── config
│   │   ├── libwasmer_linux_amd64.so
│   |   ├── ...
│   │   └── node
│   └── validator02
│       ├── config
│       ├── libwasmer_linux_amd64.so
│       ├── ...
│       └── node
└── localnet.toml
```

--------------------------------

### Install Microservice Node.js Dependencies

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/your-first-microservice

This command installs all necessary Node.js package dependencies for the MultiversX microservice. It should be run in the microservice's root directory after cloning the repository.

```bash
npm install
```

--------------------------------

### Clone MultiversX Chain Scripts Repository

Source: https://docs.multiversx.com/developers/overview/integrators/observing-squad

Clones the official `mx-chain-scripts` repository from GitHub. This repository contains the necessary scripts for setting up and managing the MultiversX Observing Squad.

```bash
git clone https://github.com/multiversx/mx-chain-scripts
```

--------------------------------

### Install MultiversX SDK with Ledger Device Support

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-py

This command installs the MultiversX SDK along with additional dependencies required for interacting with Ledger hardware devices. The `[ledger]` extra specifies the optional components to be installed.

```Shell
pip install multiversx-sdk[ledger]
```

--------------------------------

### MultiversX API: Get NFT Data Response Example

Source: https://docs.multiversx.com/developers/overview/tokens/nft-tokens

An example JSON response structure returned by the 'Get NFT data for an address' API endpoint. It illustrates the typical fields contained within the 'tokenData' object, such as attributes, balance, creator, hash, name, nonce, properties, royalties, token identifier, and URIs, along with the overall status.

```JSON
{
  "data": {
    "tokenData": {
      "attributes": "YXR0cmlidXRl",
      "balance": "2",
      "creator": "erd1ukn0tukrdhuv0zzxn0zlr53g7h0fr68dz9dd56mkksev59nwuvnswnlyuy",
      "hash": "aGFzaA==",
      "name": "H",
      "nonce": 1,
      "properties": "",
      "royalties": "9000",
      "tokenIdentifier": "4W97C-32b5ce",
      "uris": ["bmZ0IHVyaQ=="]
    }
  },
  "error": "",
  "code": "successful"
}
```

--------------------------------

### Save Key-Value Pair to MultiversX Account using Factory (Python)

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-py

This snippet initiates the process of storing key-value pairs on a MultiversX account using the `AccountTransactionsFactory`. It demonstrates the setup of the entrypoint and factory, and the loading of the sender account from a PEM file. The provided code is a partial example, showing the initial setup for this operation.

```python
from pathlib import Path
from multiversx_sdk import Account, DevnetEntrypoint

# create the entrypoint and the account transactions factory
entrypoint = DevnetEntrypoint()
factory = entrypoint.create_account_transactions_factory()

# create the account to guard
alice = Account.new_from_pem(Path("../multiversx_sdk/testutils/testwallets/alice.pem"))
```

--------------------------------

### Install Rust using the official rustup script

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/troubleshooting/rust-setup

Executes the recommended `rustup` installation script to set up the Rust toolchain, followed by updating to the latest stable version.

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

```bash
rustup update
rustup default stable
```

--------------------------------

### Install Optional Linux Packages for MultiversX Localnet

Source: https://docs.multiversx.com/developers/overview/developers/setup-local-testnet-advanced

These commands install `tmux` and `gnome-terminal` using the `apt` package manager. These packages are optional but may be required depending on the specific Linux distribution to ensure full functionality and a complete environment for the MultiversX local testnet.

```Bash
sudo apt install tmux
sudo apt install gnome-terminal
```

--------------------------------

### MultiversX Rust Adder Smart Contract Example

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/eth-to-mvx

The equivalent 'Adder' smart contract implemented in Rust for the MultiversX blockchain, utilizing the SpaceCraftSDK. This example showcases MultiversX-specific annotations like `#[contract]`, `#[init]`, `#[endpoint]`, `#[view]`, and `#[storage_mapper]` to define contract logic and storage.

```Rust
#[multiversx_sc::contract]
pub trait Adder {
    #[init]
    fn init(&self, initial_value: BigUint) {
        self.sum().set(initial_value);
    }

    #[endpoint]
    fn add(&self, value: BigUint) {
        self.sum().update(|sum| *sum += value);
    }

    #[view(getSum)]
    #[storage_mapper("sum")]
    fn sum(&self) -> SingleValueMapper<BigUint>;
}
```

--------------------------------

### Source Management Script for Upgrade/Reset

Source: https://docs.multiversx.com/developers/overview/sovereign/local-setup

Sources `script.sh` to load functions necessary for upgrading and resetting the local Sovereign Chain and its associated services.

```bash
source script.sh
```

--------------------------------

### Start MultiversX Microservice on Devnet

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/your-first-microservice

This command initiates the MultiversX microservice, configured to connect to the devnet. It starts the service on a specified port, typically 3001, making its API endpoints accessible.

```bash
npm run start:devnet
```

--------------------------------

### Clone MultiversX Sovereign Go Repository

Source: https://docs.multiversx.com/developers/overview/sovereign/local-setup

This command clones the main MultiversX sovereign chain Go repository from GitHub. Ensure an SSH key for GitHub is configured on your machine before executing.

```Bash
git clone git@github.com:multiversx/mx-chain-sovereign-go.git
```

--------------------------------

### Create Account from Entrypoint

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-js/sdk-js-cookbook

Demonstrates how to initialize a new account directly from an entrypoint. Accounts are essential for signing transactions and messages, and for managing the account's nonce.

```JavaScript
{
    const entrypoint = new DevnetEntrypoint();
    const account = entrypoint.createAccount();
}
```

--------------------------------

### Start MultiversX Sovereign Validator Node (Multi Key)

Source: https://docs.multiversx.com/developers/overview/sovereign/distributed-setup

This command starts a MultiversX sovereign validator node configured with multiple validator keys. It enables profile mode, saves logs, sets log level to INFO, includes logger name and correlation IDs, uses a health service, exposes a REST API on port 8080, and specifies the working directory.

```bash
./sovereignnode --all-validator-keys-pem-file ./config/allValidatorsKey.pem --profile-mode --log-save --log-level *:INFO --log-logger-name --log-correlation --use-health-service --rest-api-interface :8080 --working-directory ~/my_validator_node
```

--------------------------------

### Define `adder_blackbox` Integration Test Function

Source: https://docs.multiversx.com/developers/overview/developers/testing/rust/sc-blackbox-example

Outlines the basic structure of an integration test function, `adder_blackbox`, which starts by initializing the testing environment using the `world()` function, preparing for subsequent transaction definitions and result checks.

```Rust
#[test]
fn adder_blackbox() {
    let mut world = world();

    ///
}

```

--------------------------------

### WalletConnect: Connect and Basic Login

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-js/sdk-js-signing-providers

Demonstrates how to initiate a WalletConnect connection, obtain the URI for QR code display, and complete a basic login session using the provider's `connect()` and `login()` methods.

```javascript
const { uri, approval } = await provider.connect();
// connect will provide the uri required for the qr code display
// and an approval Promise that will return the connection session
// once the user confirms the login

// openModal() is defined above
openModal(uri);

// pass the approval Promise
await provider.login({ approval });
```

--------------------------------

### Example Ampd Mainnet Configuration (config.toml)

Source: https://docs.multiversx.com/developers/overview/bridge/axelar

This TOML configuration file provides a basic setup for an `ampd` verifier on the Axelar mainnet. It defines network endpoints, event buffer capacity, service registry contract, broadcast parameters (like gas limits and chain ID), and `tofnd` connection details. It also includes a handler for MultisigSigner, which can be extended for additional chain support.

```toml
# replace with your Axelar mainnet node
tm_jsonrpc="http://127.0.0.1:26657"
tm_grpc="tcp://127.0.0.1:9090"
event_buffer_cap=100000

[service_registry]
cosmwasm_contract="axelar1rpj2jjrv3vpugx9ake9kgk3s2kgwt0y60wtkmcgfml5m3et0mrls6nct9m"

[broadcast]
batch_gas_limit="20000000"
broadcast_interval="1s"
chain_id="axelar-dojo-1"
gas_adjustment="2"
gas_price="0.007uaxl"
queue_cap="1000"
tx_fetch_interval="1000ms"
tx_fetch_max_retries="15"

[tofnd_config]
batch_gas_limit="10000000"
key_uid="axelar"
party_uid="ampd"
url="http://127.0.0.1:50051"

[[handlers]]
cosmwasm_contract="axelar14a4ar5jh7ue4wg28jwsspf23r8k68j7g5d6d3fsttrhp42ajn4xq6zayy5"
type="MultisigSigner"
```

--------------------------------

### MultiversX API: Get Transaction Details

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/rest-api/transactions

Documents the `GET /transaction/:txHash` endpoint for retrieving details of a MultiversX transaction. It specifies path and query parameters, their types, and descriptions, along with examples for the JSON responses (basic and extended).

```APIDOC
GET https://gateway.multiversx.com/transaction/:txHash

Description: This endpoint allows one to query the details of a Transaction.

Path Parameters:
  txHash: REQUIRED, string, The hash (identifier) of the Transaction.

Query Parameters:
  sender: OPTIONAL, string, The Address of the sender - a hint to optimize the request.
  withResults: OPTIONAL, bool, Boolean parameter to specify if smart contract results and other details should be returned.

Response (200 OK):
  Description: Transaction details retrieved successfully.
  Body:
    data: object
      transaction: object
        type: string
        nonce: number
        round: number
        epoch: number
        value: string
        receiver: string
        sender: string
        gasPrice: number
        gasLimit: number
        data: string
        signature: string
        sourceShard: number
        destinationShard: number
        blockNonce: number
        miniblockHash: string
        blockHash: string
        status: string
        receipt: object (OPTIONAL, if withResults=true)
          value: number
          sender: string
          data: string
          txHash: string
        smartContractResults: array of objects (OPTIONAL, if withResults=true)
          hash: string
          nonce: number
          value: number
          receiver: string
          sender: string
          data: string
          prevTxHash: string
          originalTxHash: string
          gasLimit: number
          gasPrice: number
          callType: number
    error: string
    code: string
```

```JSON
{
  "data": {
    "transaction": {
      "type": "normal",
      "nonce": 3,
      "round": 186580,
      "epoch": 12,
      "value": "1000000000000000000",
      "receiver": "erd1...",
      "sender": "erd1...",
      "gasPrice": 1000000000,
      "gasLimit": 70000,
      "data": "Zm9yIHRlc3Rz",
      "signature": "1047...",
      "sourceShard": 2,
      "destinationShard": 1,
      "blockNonce": 186535,
      "miniblockHash": "e927...",
      "blockHash": "50a1...",
      "status": "executed"
    }
  },
  "error": "",
  "code": "successful"
}
```

```JSON
{
  "data": {
    "transaction": {
      "type": "normal",
      "nonce": 3,
      "round": 186580,
      "epoch": 12,
      "value": "1000000000000000000",
      "receiver": "erd1...",
      "sender": "erd1...",
      "gasPrice": 1000000000,
      "gasLimit": 70000,
      "data": "Zm9yIHRlc3Rz",
      "signature": "1047...",
      "sourceShard": 2,
      "destinationShard": 1,
      "blockNonce": 186535,
      "miniblockHash": "e927...",
      "blockHash": "50a1...",
      "status": "executed",
      "receipt": {
        "value": 100,
        "sender": "erd1...",
        "data": "...",
        "txHash": "b37..."
      },
      "smartContractResults": [
        {
          "hash": "...",
          "nonce": 5,
          "value": 1000,
          "receiver": "erd1...",
          "sender": "erd1...",
          "data": "@6f6b",
          "prevTxHash": "3638...",
          "originalTxHash": "3638...",
          "gasLimit": 0,
          "gasPrice": 1000000000,
          "callType": 0
        }
      ]
    }
  },
  "error": "",
  "code": "successful"
}
```

--------------------------------

### Example MultiversX Mandos Scenario Trace JSON

Source: https://docs.multiversx.com/developers/overview/developers/meta/interactor/interactors-example

This JSON snippet illustrates the structure of a Mandos scenario trace file (`trace1.scen.json`) generated by the interactor's tracer. It captures a sequence of smart contract interactions, including state setup (`setState`), contract deployment (`scDeploy`), function calls (`scCall` for 'add'), and queries (`scQuery` for 'getSum'), along with their transaction details and expected outcomes.

```JSON
{
    "steps": [
        {
            "step": "setState",
            "newAddresses": [
                {
                    "creatorAddress": "0x0139472eff6886771a982f3083da5d421f24c29181e63888228dc81ca60d69e1",
                    "creatorNonce": "1427",
                    "newAddress": "bech32:erd1qqqqqqqqqqqqqpgqmauhsqd6zr7kt8pg80qhph2tw0ejed3pd8sszl98x7"
                }
            ]
        },
        {
            "step": "scDeploy",
            "id": "",
            "tx": {
                "from": "0x0139472eff6886771a982f3083da5d421f24c29181e63888228dc81ca60d69e1",
                "contractCode": "mxsc:../output/adder.mxsc.json",
                "arguments": [
                    "0x"
                ],
                "gasLimit": "5,000,000"
            },
            "expect": {
                "out": [],
                "status": "0"
            }
        },
        {
            "step": "scCall",
            "id": "",
            "tx": {
                "from": "0x0139472eff6886771a982f3083da5d421f24c29181e63888228dc81ca60d69e1",
                "to": "bech32:erd1qqqqqqqqqqqqqpgqmauhsqd6zr7kt8pg80qhph2tw0ejed3pd8sszl98x7",
                "function": "add",
                "arguments": [
                    "0x03"
                ],
                "gasLimit": "5,000,000"
            },
            "expect": {
                "out": [],
                "status": "0"
            }
        },
        {
            "step": "scQuery",
            "id": "",
            "tx": {
                "to": "bech32:erd1qqqqqqqqqqqqqpgqmauhsqd6zr7kt8pg80qhph2tw0ejed3pd8sszl98x7",
                "function": "getSum",
                "arguments": []
            },
            "expect": {
                "out": [
                    "0x03"
                ],
                "status": "0"
            }
        }
    ]
}
```

--------------------------------

### Verify Rust Toolchain and Target Installation

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/troubleshooting/rust-setup

This command checks the current Rust installation, displaying information about the default host, `rustup` home directory, installed toolchains (e.g., stable), and installed targets (e.g., `wasm32-unknown-unknown`). It helps confirm that the necessary components for MultiversX development are correctly set up.

```bash
rustup show
```

--------------------------------

### Build MultiversX Localnet Software

Source: https://docs.multiversx.com/developers/overview/developers/setup-local-testnet

Compiles the previously fetched software prerequisites for the MultiversX localnet. The actual build process occurs within the download folders, typically under `~/multiversx-sdk/localnet_software_remote`.

```bash
mxpy localnet build
```

--------------------------------

### Install MultiversX sdk-dapp without Optional UI

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-dapp

Instructions to install the MultiversX sdk-dapp library without its optional UI components, which can reduce dependencies, using npm or yarn.

```shell
npm install @multiversx/sdk-dapp --no-optional
```

```shell
yarn add @multiversx/sdk-dapp --no-optional
```

--------------------------------

### Full Example of mxpy Smart Contract Deployment

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/mxpy/mxpy-cli

This comprehensive example demonstrates deploying a smart contract with specific parameters. It includes specifying the bytecode path, proxy URL, initial arguments for contract initialization, gas limit for transaction execution, and the sender's PEM file for signing. It highlights the importance of matching the proxy and chain ID for successful transaction execution.

```shell
mxpy contract deploy --bytecode ~/contracts/adder/output/adder.wasm \n    --proxy=https://devnet-gateway.multiversx.com \n    --arguments 0 --gas-limit 5000000 \n    --pem=~/multiversx-sdk/testwallets/latest/users/alice.pem \n    --send
```

--------------------------------

### Build Sovereign Chain Node Executable

Source: https://docs.multiversx.com/developers/overview/sovereign/distributed-setup

Compiles the main Sovereign Chain node executable. The `-ldflags` option is used to embed a custom application version (`v0.0.1` in this example) into the binary, which is important for version tracking and deployment management.

```Bash
cd ..
cd cmd/sovereignnode/
go build -v -ldflags="-X main.appVersion=v0.0.1"
```

--------------------------------

### Inspect MultiversX Proxy Activity with journalctl

Source: https://docs.multiversx.com/developers/overview/integrators/observing-squad

The MultiversX Proxy does not offer a `termui` monitor. Instead, its activity can be inspected by viewing its logs in real-time using `journalctl` for the `elrond-proxy.service`.

```bash
journalctl -f -u elrond-proxy.service
```

--------------------------------

### Start MultiversX Sovereign Explorer (Testnet)

Source: https://docs.multiversx.com/developers/overview/sovereign/sovereign-explorer

These commands are used to install project dependencies (using 'yarn') and then launch the MultiversX Sovereign Explorer in testnet mode. Ensure that all necessary configurations in 'config.testnet.ts' have been updated to reflect your environment before executing these commands.

```Shell
yarn
npm run start-testnet
```

--------------------------------

### Granular Smart Contract Query Control in Python

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-py

This snippet provides a more granular approach to querying a smart contract compared to the combined `sc_controller.query` method. It demonstrates the initial setup for creating a `SmartContractController` with an ABI, allowing for separate steps for query creation, execution, and result parsing (though the latter two are not explicitly shown in this truncated example).

```python
from pathlib import Path

from multiversx_sdk import Address, DevnetEntrypoint
from multiversx_sdk.abi import Abi

abi = Abi.load(Path("contracts/adder.abi.json"))

contract_address = Address.new_from_bech32("erd1qqqqqqqqqqqqqpgq7cmfueefdqkjsnnjnwydw902v8pwjqy3d8ssd4meug")

sc_controller = DevnetEntrypoint().create_smart_contract_controller(abi=abi)
```

--------------------------------

### MultiversX Network Configuration API Response Example

Source: https://docs.multiversx.com/developers/overview/integrators/creating-transactions

Illustrates the JSON response structure from the MultiversX API's 'Get Network Configuration' endpoint, providing essential network parameters like chain ID, gas costs, and minimum limits.

```JSON
{
    "config": {
        "erd_chain_id": "1",
        "erd_gas_per_data_byte": 1500,
        "erd_min_gas_limit": 50000,
        "erd_min_gas_price": 1000000000,
        "erd_min_transaction_version": 1,
        "..."
    }
}
```

--------------------------------

### Clean MultiversX Testnet

Source: https://docs.multiversx.com/developers/overview/developers/setup-local-testnet-advanced

To remove all generated Testnet data and configurations, first stop the Testnet, then run the `clean.sh` command. This prepares the environment for a fresh Testnet setup.

```bash
./stop.sh
./clean.sh
```

--------------------------------

### Navigate to Sovereign Bridge Directory

Source: https://docs.multiversx.com/developers/overview/sovereign/local-setup

Changes the current working directory to the `sovereignBridge` folder, which is a necessary first step before running setup scripts.

```bash
cd sovereignBridge
```

--------------------------------

### Install MultiversX SDK with Ledger Support

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-py

This command installs the `multiversx-sdk` package along with necessary dependencies for Ledger device communication. It enables functionalities like transaction and message signing through a Ledger device.

```bash
pip install multiversx-sdk[ledger]
```

--------------------------------

### Clone MultiversX Ping-Pong Smart Contract Repository

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/your-first-dapp

Clones the official MultiversX Ping-Pong sample smart contract repository from GitHub into a 'contract' subfolder within the current project directory. This action provides all the necessary source files for the smart contract.

```bash
git clone https://github.com/multiversx/mx-ping-pong-sc contract
```

--------------------------------

### Example Output of Get Staking Position Query

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/staking-contract

Illustrative output showing the result of the `getStakingPosition` query. The value represents the total staked amount, including 1 EGLD plus a small additional amount.

```Plaintext
Result: 1000000000000000001
```

--------------------------------

### General Observing Squad Upgrade Procedure

Source: https://docs.multiversx.com/developers/overview/integrators/observing-squad

A standard sequence of commands to upgrade both the Observers and the Proxy components of the Observing Squad. It involves pulling the latest script updates, stopping services, upgrading, and then restarting.

```bash
$ cd ~/mx-chain-scripts
$ ./script.sh github_pull
$ ./script.sh stop
$ ./script.sh upgrade_squad
$ ./script.sh upgrade_proxy
$ ./script.sh start
```

--------------------------------

### Enable Node Log Saving

Source: https://docs.multiversx.com/developers/overview/integrators/observing-squad

Sets an additional flag (`-log-save`) for the node. This ensures that logs generated by the MultiversX node are saved persistently within its designated `logs` folder.

```bash
NODE_EXTRA_FLAGS="-log-save"
```

--------------------------------

### Migrate to New MultiversX Scripts (February 2023 Upgrade)

Source: https://docs.multiversx.com/developers/overview/integrators/observing-squad

Commands to clone the new `mx-chain-scripts` repository and migrate existing configurations from older scripts. This is a crucial step for users still on `elrond-go-scripts` to prepare for the February 2023 upgrade.

```bash
$ cd ~
$ git clone https://github.com/multiversx/mx-chain-scripts
$ cd mx-chain-scripts
$ ./script.sh migrate
```

--------------------------------

### Equivalent `sc-meta all` and `cargo run` Build Commands

Source: https://docs.multiversx.com/developers/overview/developers/meta/sc-meta-cli

These two code snippets demonstrate equivalent ways to build a smart contract project. The first uses the `sc-meta all` command from the parent directory, while the second navigates into the contract's `meta` subdirectory and uses `cargo run` directly.

```Shell
cd my-contract
sc-meta all build
```

```Shell
cd my-contract/meta
cargo run build
```

--------------------------------

### Combine NativeAuthGuard and NativeAuthAdminGuard for Admin Controllers

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-nestjs/sdk-nestjs-auth

This example demonstrates how to use both `NativeAuthGuard` and `NativeAuthAdminGuard` together on a NestJS controller. This setup ensures that requests are not only natively authenticated but also originate from predefined administrator addresses.

```TypeScript
 import { NativeAuthGuard, NativeAuthAdminGuard } from "@multiversx/sdk-nestjs-auth";

 @Controller('admin')
 @UseGuards(NativeAuthGuard, NativeAuthAdminGuard)
 export class AdminController {
   // your methods...
 }
```

--------------------------------

### Example MultiversX Localnet TOML Configuration

Source: https://docs.multiversx.com/developers/overview/developers/setup-local-testnet

Illustrates the structure and default values of the `localnet.toml` file. It includes general settings like rounds per epoch, shard configuration, networking ports, and remote archive URLs for software prerequisites.

```toml
[general]
...
rounds_per_epoch = 100
round_duration_milliseconds = 6000

[metashard]
...
num_validators = 1

[shards]
num_shards = 2
...

[networking]
...
port_proxy = 7950
port_first_validator_rest_api = 10200

[software.mx_chain_go]
resolution = "remote"
archive_url = "https://github.com/multiversx/mx-chain-go/archive/refs/heads/master.zip"
...

[software.mx_chain_proxy_go]
resolution = "remote"
archive_url = "https://github.com/multiversx/mx-chain-proxy-go/archive/refs/heads/master.zip"
...
```

--------------------------------

### Instantiate MultiversX Extension Provider

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-js/sdk-js-signing-providers

Demonstrates how to import the `ExtensionProvider` and obtain its singleton instance, which is essential for interacting with the MultiversX DeFi Wallet browser extension.

```javascript
import { ExtensionProvider } from "@multiversx/sdk-extension-provider";

const provider = ExtensionProvider.getInstance();
```

--------------------------------

### Use TestAddress for Parametric Testing (Rust)

Source: https://docs.multiversx.com/developers/overview/developers/transactions/tx-from

This Rust example demonstrates the use of `TestAddress` for parametric testing. It defines a constant `OWNER_ADDRESS` as a dummy address and uses it as the sender for a transaction, simplifying test setup.

```Rust
const OWNER_ADDRESS: TestAddress = TestAddress::new("owner");

fn add_one(&mut self) {
    self.world
        .tx()
        .from(OWNER_ADDRESS)
        .to(self.receiver)
        .typed(proxy::Proxy)
        .add(1u32)
        .run();
}
```

--------------------------------

### Rust Smart Contract `init` and `upgrade` Function Example

Source: https://docs.multiversx.com/developers/overview/developers/developer-reference/upgrading-smart-contracts

This Rust code snippet demonstrates the implementation of both `init` and `upgrade` functions in a MultiversX smart contract. It highlights how the `init` function is used for initial deployment setup (setting a value only if empty), while the new `upgrade` function is specifically designed to handle logic during contract upgrades (setting a new value directly). This example illustrates the behavioral change introduced in Sirius Mainnet v1.6.0, where `upgrade` takes precedence over `init` during subsequent upgrades.

```Rust
#[init]
fn init(&self, initial_value: u64) {
    // Save the initial value in storage only if it is empty.
    self.sum().set_if_empty(initial_value);
}

#[upgrade]
fn upgrade(&self, new_value: u64) {
    self.sum().set(new_value);
}
```

--------------------------------

### MultiversX ChangeOwnerAddress Event Structure and Example

Source: https://docs.multiversx.com/developers/overview/developers/event-logs/contract-deploy-events

Defines the structure and provides a concrete JSON example for the `ChangeOwnerAddress` event, detailing its fields like identifier, address, topics, and data.

```APIDOC
ChangeOwnerAddress Event Structure:
  identifier: string (Value: "ChangeOwnerAddress")
  address: string (Description: "the address of the contract")
  topics: array of string (Description: "`topics[0]` - the address bytes of the new contract owner base64 encoded")
  data: null (Description: "empty")
```

```json
{
    "address": "erd1qqqqqqqqqqqqqpgqnnl9nn0kuuckhg24g02hq2745n4jk2hp327qcay4nm",
    "identifier": "ChangeOwnerAddress",
    "topics": [
        "UKAg0hORMjk0oT6RalZp1w0Xulvvj0Wa/SSYstBepao="
    ],
    "data": null
}
```

--------------------------------

### Deploy MultiversX Smart Contract using Factory and Sign

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-js/sdk-js-cookbook

This comprehensive example demonstrates the full lifecycle of deploying a smart contract. It covers loading bytecode, preparing arguments, creating the deployment transaction, managing nonce, signing, broadcasting, and finally parsing the transaction outcome.

```JavaScript
{
    const entrypoint = new DevnetEntrypoint();
    const factory = entrypoint.createSmartContractTransactionsFactory();

    // load the contract bytecode
    const bytecode = await promises.readFile("../src/testData/adder.wasm");

    // For deploy arguments, use "TypedValue" objects if you haven't provided an ABI to the factory:
    let args: any[] = [new BigUIntValue(42)];
    // Or use simple, plain JavaScript values and objects if you have provided an ABI to the factory:
    args = [42];

    const filePath = path.join("../src", "testdata", "testwallets", "alice.pem");
    const alice = await Account.newFromPem(filePath);

    const deployTransaction = await factory.createTransactionForDeploy(alice.address, {
        bytecode: bytecode,
        gasLimit: 6000000n,
        arguments: args,
    });

    // the developer is responsible for managing the nonce
    alice.nonce = await entrypoint.recallAccountNonce(alice.address);

    // set the nonce
    deployTransaction.nonce = alice.nonce;

    // sign the transaction
    deployTransaction.signature = await alice.signTransaction(deployTransaction);

    // broadcasting the transaction
    const txHash = await entrypoint.sendTransaction(deployTransaction);

    // waiting for transaction to complete
    const transactionOnNetwork = await entrypoint.awaitCompletedTransaction(txHash);

    // parsing transaction
    const parser = new SmartContractTransactionsOutcomeParser();
    const parsedOutcome = parser.parseDeploy({ transactionOnNetwork });
    const contractAddress = parsedOutcome.contracts[0].address;

    console.log(contractAddress.toBech32());
}
```

--------------------------------

### Build MultiversX Smart Contract

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/staking-contract

This command builds all components of the MultiversX smart contract project. It must be executed from the contract's root directory to prepare the contract for deployment.

```shell
sc-meta all build
```

--------------------------------

### MultiversX Interactor System Test Example

Source: https://docs.multiversx.com/developers/overview/developers/transactions/tx-env

This snippet provides a basic system test setup using the `Interactor`. It defines a `tokio::test` function that calls the `example_scenario` (from the previous snippet) to interact with a smart contract and then prints the returned result, demonstrating how to integrate interactor-based scenarios into automated tests.

```Rust
#[cfg(test)]
pub mod system_test {
    use crate::example_scenario;
    use multiversx_sc_snippets::tokio;

    #[tokio::test]
    async fn test_full_farm_scenario() {
        let result = example_scenario().await;
        println!("result {:#?}", result);
    }
}
```

--------------------------------

### Run Ampd Verifier Process in Docker

Source: https://docs.multiversx.com/developers/overview/bridge/axelar

This command starts the `ampd` verifier process within a Docker container. Once running, the verifier will begin its operations, such as monitoring events, signing transactions, and participating in the Axelar network's consensus mechanisms.

```bash
docker run axelarnet/axelar-ampd:v1.3.1
```

--------------------------------

### Automated Rust and MultiversX SC-Meta Installation for CI/CD

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/troubleshooting/rust-setup

This script downloads and executes `rustup.sh` to install the stable Rust toolchain with the `wasm32-unknown-unknown` target, which is crucial for MultiversX smart contract development. It then installs the `multiversx-sc-meta` cargo package, ensuring a locked version for consistent builds in CI/CD pipelines.

```bash
wget -O rustup.sh https://sh.rustup.rs && \
    chmod +x rustup.sh && \
    ./rustup.sh --verbose --default-toolchain stable --target wasm32-unknown-unknown -y

cargo install multiversx-sc-meta --locked
```

--------------------------------

### Clone MultiversX Sovereign Go Repository

Source: https://docs.multiversx.com/developers/overview/sovereign/distributed-setup

Clones the `mx-chain-sovereign-go` GitHub repository, which contains the necessary source code for setting up a Sovereign Chain. This step requires a configured SSH key for GitHub authentication on the machine.

```Bash
git clone git@github.com:multiversx/mx-chain-sovereign-go.git
```

--------------------------------

### Expose Prometheus Metrics Endpoint in NestJS Controller

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-nestjs/sdk-nestjs-monitoring

This example illustrates how to create a NestJS controller that exposes the collected metrics for Prometheus. It injects `MetricsService` and provides a GET endpoint (`/metrics`) that returns the output of `metricsService.getMetrics()`.

```TypeScript
import { Controller, Get } from '@nestjs/common';
import { MetricsService } from '@multiversx/sdk-nestjs-monitoring';

@Controller('metrics')
export class MetricsController {
  constructor(
    private readonly metricsService: MetricsService
  ){}

  @Get()
  getMetrics(): string {
    return this.metricsService.getMetrics();
  }
}
```

--------------------------------

### Register MultiversX Smart Contract in Rust Blackbox Test Setup

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/crowdfunding-p1

Rust code snippet demonstrating the `world()` function, which initializes the test environment and registers the MultiversX smart contract for blackbox testing using its compiled JSON path.

```Rust
use crowdfunding::crowdfunding_proxy;
use multiversx_sc_scenario::imports::*;

const CODE_PATH: MxscPath = MxscPath::new("output/crowdfunding.mxsc.json");

fn world() -> ScenarioWorld {
    let mut blockchain = ScenarioWorld::new();

    blockchain.set_current_dir_from_workspace("crowdfunding");
    blockchain.register_contract(CODE_PATH, crowdfunding::ContractBuilder);
    blockchain
}
```

--------------------------------

### Get Current Block Round (MultiversX)

Source: https://docs.multiversx.com/developers/overview/developers/developer-reference/sc-api-functions

Returns the round number of the current block. Each epoch consists of a fixed number of rounds, and the round number resets to 1 at the start of every new epoch.

```APIDOC
get_block_round() -> u64
```

--------------------------------

### Upgrade Observing Squad via New Scripts (Post-Migration)

Source: https://docs.multiversx.com/developers/overview/integrators/observing-squad

The procedure to upgrade the Observing Squad to the newest version after successfully migrating to the `mx-chain-scripts`. This involves pulling updates, stopping services, upgrading components, and restarting the squad.

```bash
$ cd ~/mx-chain-scripts
$ ./script.sh github_pull
$ ./script.sh stop
$ ./script.sh upgrade_squad
$ ./script.sh upgrade_proxy
$ ./script.sh start
```

--------------------------------

### Get Transaction Process Status API

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/rest-api/transactions

Documents the API endpoint to query the process status of a transaction using its hash. It outlines the required path parameter and provides an example of a successful JSON response.

```APIDOC
GET /transaction/:txHash/process-status
Description: Query the process status of a transaction.
Path Parameters:
  txHash:
    Required: REQUIRED
    Type: string
    Description: The hash (identifier) of the Transaction.
Response:
  200 OK: Transaction status retrieved successfully.
```

```JSON
{
  "data": {
      "reason": "",
      "status": "success"
  },
  "error": "",
  "code": "successful"
}
```

--------------------------------

### Computing Smart Contract Address Pre-Deployment (Python)

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-py

This example demonstrates how to deterministically compute the future address of a smart contract before it is even deployed. By using the sender's address and the deployment nonce, the `AddressComputer` can predict the contract's address, which can be useful for pre-deployment setup or cross-contract interactions.

```Python
from multiversx_sdk import Address, AddressComputer

# we used Alice for deploying the contract, so we are using her address
alice = Address.new_from_bech32("erd1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssycr6th")

address_computer = AddressComputer()
contract_address = address_computer.compute_contract_address(
    deployer=alice,
    deployment_nonce=deploy_transaction.nonce  # the same nonce we set on the deploy transaction
)

print("Contract address:", contract_address.to_bech32())

```

--------------------------------

### Initialize MultiversX Staking Contract Test Environment

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/staking-contract

This Rust code defines the `ContractSetup` struct and its `new` method, which initializes a `ScenarioWorld` for testing a MultiversX staking contract. It registers the contract, sets up owner and user accounts with initial balances, and simulates the contract deployment.

```Rust
impl ContractSetup {
    pub fn new() -> Self {
        let mut world = ScenarioWorld::new();
        world.set_current_dir_from_workspace("staking-contract");
        world.register_contract(WASM_PATH, staking_contract::ContractBuilder);

        world.account(OWNER_ADDRESS).nonce(1).balance(0);
        world.account(USER_ADDRESS).nonce(1).balance(USER_BALANCE);

        // simulate deploy
        world
            .tx()
            .from(OWNER_ADDRESS)
            .typed(staking_contract_proxy::StakingContractProxy)
            .init(APY)
            .code(WASM_PATH)
            .new_address(STAKING_CONTRACT_ADDRESS)
            .run();

        ContractSetup { world }
    }
}
```

--------------------------------

### Check Single Account State in MultiversX Blackbox Test

Source: https://docs.multiversx.com/developers/overview/developers/testing/rust/sc-test setup

Shows how to verify the state of a single account using `CheckStateBuilder` via `ScenarioWorld.check_account()`. This example demonstrates checking an account's nonce and EGLD balance.

```Rust
    world
        .check_account(first) // CheckStateBuilder for `first`
        .nonce(3)
        .balance(100);
```

--------------------------------

### Execute MultiversX Node Management Script

Source: https://docs.multiversx.com/developers/overview/validators/nodes-scripts/install-update

This command runs the primary `script.sh` located in the `mx-chain-scripts` directory. It serves as the central interface for various node operations, including updating, upgrading, starting, and quitting. Users should follow the on-screen prompts for specific actions.

```bash
~/mx-chain-scripts/script.sh
```

--------------------------------

### Get Address Balance REST API Endpoint

Source: https://docs.multiversx.com/developers/overview/integrators/egld-integration-guide

Documents the REST API endpoint used to check the balance of a MultiversX address. This endpoint is crucial for integrators to perform pre-transaction safety checks or periodic balance verifications.

```APIDOC
Endpoint: /sdk-and-tools/rest-api/addresses#get-address-balance
Method: GET
Description: Retrieves the balance of a specific MultiversX address.
Parameters:
  address: string - The MultiversX address to query.
Returns:
  balance: string - The current balance of the address.
```

--------------------------------

### Source Deployment Script

Source: https://docs.multiversx.com/developers/overview/sovereign/local-setup

Executes `script.sh` in the current shell environment, making its functions and variables, specifically those related to deployment, available for subsequent commands.

```bash
source script.sh
```

--------------------------------

### Configure Sovereign Bridge Setup

Source: https://docs.multiversx.com/developers/overview/sovereign/local-setup

Updates the `config/configs.cfg` file with essential parameters for the MultiversX Sovereign Bridge. This includes paths for deployment outputs, the wallet location, main chain constants (Elasticsearch, Proxy, Chain ID), and native ESDT token details, crucial for connecting to a specific MultiversX network like testnet.

```ini
# Sovereign Paths
SOVEREIGN_DIRECTORY="~/sovereign"
TXS_OUTFILE_DIRECTORY="${SOVEREIGN_DIRECTORY}/txsOutput"
CONTRACTS_DIRECTORY="${SOVEREIGN_DIRECTORY}/contracts"

# Owner Configuration
WALLET="~/wallet.pem"

# Main Chain Constants
MAIN_CHAIN_ELASTIC=https://testnet-index.multiversx.com
PROXY = https://testnet-gateway.multiversx.com
CHAIN_ID = T

# Native token
NATIVE_ESDT_TICKER=SOV
NATIVE_ESDT_NAME=SovToken
```

--------------------------------

### Initiate Basic MultiversX Wallet Login

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-js/sdk-js-signing-providers

Demonstrates how to initiate a basic login flow with the MultiversX wallet provider, redirecting the user back to a specified callback URL upon completion.

```javascript
const callbackUrl = encodeURIComponent("http://my-dapp");
await provider.login({ callbackUrl });
```

--------------------------------

### Install Latest mxpy CLI with pipx

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/mxpy/installing-mxpy

This command installs the latest available version of the MultiversX SDK CLI (mxpy) using pipx. The `--force` flag ensures a clean installation or update.

```Shell
pipx install multiversx-sdk-cli --force
```

--------------------------------

### Deploying a Smart Contract with SmartContractController

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-js/sdk-js-cookbook

Illustrates the comprehensive process of deploying a smart contract using the `SmartContractController` from the MultiversX SDK. This example covers loading account details from a PEM file, fetching the account nonce, loading contract bytecode and ABI files, preparing deployment arguments (showing both `TypedValue` and plain JavaScript options), and broadcasting the transaction to the network.

```TypeScript
{
    const filePath = path.join("..", "src", "testdata", "testwallets", "alice.pem");
    const sender = await Account.newFromPem(filePath);
    const entrypoint = new DevnetEntrypoint();

    // the developer is responsible for managing the nonce
    sender.nonce = await entrypoint.recallAccountNonce(sender.address);

    // load the contract bytecode
    const bytecode = await promises.readFile("..", "src", "testData", "adder.wasm");
    // load the abi file
    const abi = await loadAbiRegistry("..", "src", "testdata", "adder.abi.json");

    const controller = entrypoint.createSmartContractController(abi);

    // For deploy arguments, use "TypedValue" objects if you haven't provided an ABI to the factory:
    let args: any[] = [new U32Value(42)];
    // Or use simple, plain JavaScript values and objects if you have provided an ABI to the factory:
    args = [42];

    const deployTransaction = await controller.createTransactionForDeploy(sender, sender.getNonceThenIncrement(), {
        bytecode: bytecode,
        gasLimit: 6000000n,
        arguments: args
    });

    // broadcasting the transaction
    const txHash = await entrypoint.sendTransaction(deployTransaction);
}
```

--------------------------------

### Clone MultiversX dApp Template Repository

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/your-first-dapp

These commands are used to clone a simple dApp template from GitHub, which includes pre-configured calls to interact with a deployed smart contract. After cloning, the user navigates into the newly created `dapp` directory.

```Shell
git clone https://github.com/multiversx/mx-template-dapp dapp
cd dapp
```

--------------------------------

### Install build dependencies for Rust and sc-meta on Ubuntu/WSL

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/troubleshooting/rust-setup

Installs essential system-level packages required for compiling Rust projects and the `sc-meta` tool on Ubuntu or Windows Subsystem for Linux environments.

```bash
sudo apt-get install build-essential pkg-config libssl-dev
```

--------------------------------

### Start MultiversX Sovereign Validator Node (Single Key)

Source: https://docs.multiversx.com/developers/overview/sovereign/distributed-setup

This command initiates a MultiversX sovereign validator node configured with a single validator key. It enables profile mode, saves logs, sets log level to INFO, includes logger name and correlation IDs, uses a health service, exposes a REST API on port 8080, and specifies the working directory.

```bash
./sovereignnode --validator-key-pem-file ./config/validatorKey.pem --profile-mode --log-save --log-level *:INFO --log-logger-name --log-correlation --use-health-service --rest-api-interface :8080 --working-directory ~/my_validator_node
```

--------------------------------

### Import Account Information Hooks from SDK-dapp

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-dapp

Example of importing hooks related to account information, such as `useGetAccountInfo`, `useGetAccountProvider`, and `useGetLoginInfo`, from the `@multiversx/sdk-dapp/hooks/accounts` module.

```javascript
import {
  useGetAccountInfo,
  useGetAccountProvider,
  useGetLoginInfo,
} from "@multiversx/sdk-dapp/hooks/accounts";
```

--------------------------------

### Get Transaction Shallow Status API

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/rest-api/transactions

Documents the API endpoint to query the shallow status of a transaction using its hash. It specifies path and optional query parameters, along with an example of a successful JSON response.

```APIDOC
GET /transaction/:txHash/status
Description: Query the shallow status of a transaction.
Path Parameters:
  txHash:
    Required: REQUIRED
    Type: string
    Description: The hash (identifier) of the Transaction.
Query Parameters:
  sender:
    Required: OPTIONAL
    Type: string
    Description: The Address of the sender - a hint to optimize the request. (Applicable to Proxy only)
Response:
  200 OK: Transaction status retrieved successfully.
```

```JSON
{
  "data": {
    "status": "success"
  },
  "error": "",
  "code": "successful"
}
```

--------------------------------

### Rust Integration Test Example with Rust Backend

Source: https://docs.multiversx.com/developers/overview/developers/testing/scenario/running-scenarios

Provides a Rust code example for integration tests using the native Rust backend. It shows how to initialize the `ScenarioWorld` and register the contract using `blockchain.register_contract()` for direct execution of Rust contract code.

```Rust
use multiversx_sc_scenario::*;

fn world() -> ScenarioWorld {
    let mut blockchain = ScenarioWorld::new();
    blockchain.register_contract("file:output/adder.wasm", adder::ContractBuilder);
    blockchain
}

#[test]
#[ignore]
fn adder_rs() {
    world().run("scenarios/adder.scen.json");
}

#[test]
fn interactor_trace_rs() {
    world().run("scenarios/interactor_trace.scen.json");
}
```

--------------------------------

### Create Network Entrypoint from API Network Provider

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-py

Demonstrates how to initialize a generic `NetworkEntrypoint` using an existing `ApiNetworkProvider` instance and a chain ID, allowing for more flexible network configurations beyond predefined entrypoints.

```Python
from multiversx_sdk import NetworkEntrypoint, ApiNetworkProvider

api = ApiNetworkProvider("https://devnet-api.multiversx.com")
entrypoint = NetworkEntrypoint.new_from_network_provider(network_provider=api, chain_id="D")
```

--------------------------------

### Start MultiversX Sovereign Observer Node

Source: https://docs.multiversx.com/developers/overview/sovereign/distributed-setup

This command launches a MultiversX sovereign observer node. It enables profile mode, saves logs, sets log level to INFO, includes logger name and correlation IDs, uses a health service, exposes a REST API on port 8080, and specifies the working directory. Observer nodes do not require a validator key.

```bash
./sovereignnode --profile-mode --log-save --log-level *:INFO --log-logger-name --log-correlation --use-health-service --rest-api-interface :8080 --working-directory ~/my_observer_node
```

--------------------------------

### Vote on Governance Proposal using MultiversX SDK Controller (Python)

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-py

This example illustrates how to cast a vote (YES/NO) on an existing governance proposal using the `GovernanceController` in the MultiversX SDK. It demonstrates account setup, controller initialization, creating a voting transaction, sending it to the network, and awaiting its completion to retrieve the vote outcome.

```Python
from multiversx_sdk import Account, ProxyNetworkProvider, GovernanceController, VoteType

alice = Account.new_from_pem(Path("../multiversx_sdk/testutils/testwallets/alice.pem"))
proxy = ProxyNetworkProvider("https://devnet-gateway.multiversx.com")
alice.nonce = proxy.get_account(alice.address).nonce

controller = GovernanceController(chain_id="D", network_provider=proxy)

transaction = controller.create_transaction_for_voting(
    sender=alice,
    nonce=alice.get_nonce_then_increment(),
    proposal_nonce=1,
    vote=VoteType.YES
)

# send the transaction
tx_hash = proxy.send_transaction(transaction)

# get vote outcome
[vote] = controller.await_completed_vote(tx_hash)
print(vote.proposal_nonce)
print(vote.vote)
print(vote.total_stake)
print(vote.total_voting_power)
```

--------------------------------

### Verify mxpy CLI Installation

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/mxpy/installing-mxpy

Run this command to check if mxpy has been successfully installed and to display its current version.

```Shell
mxpy --version
```

--------------------------------

### Issue Semi-Fungible Tokens via Factory (Python)

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-py

Provides a Python example for issuing a new semi-fungible token (SFT) on MultiversX using the `TokenManagementTransactionsFactory`. It details account setup, transaction construction with various token capabilities, signing the transaction, sending it to the network, and parsing the outcome to retrieve the token identifier.

```Python
from pathlib import Path
from multiversx_sdk import Account, DevnetEntrypoint, TokenManagementTransactionsOutcomeParser

# create the entrypoint and the token management transactions factory
entrypoint = DevnetEntrypoint()
factory = entrypoint.create_token_management_transactions_factory()

# create the issuer of the token
alice = Account.new_from_pem(Path("../multiversx_sdk/testutils/testwallets/alice.pem"))

transaction = factory.create_transaction_for_issuing_semi_fungible(
    sender=alice.address,
    token_name="NEWSEMI",
    token_ticker="SEMI",
    can_freeze=False,
    can_wipe=True,
    can_pause=False,
    can_transfer_nft_create_role=True,
    can_change_owner=True,
    can_upgrade=True,
    can_add_special_roles=True
)

# fetch the nonce of the network
alice.nonce = entrypoint.recall_account_nonce(alice.address)
transaction.nonce = alice.get_nonce_then_increment()

# sign the transaction
transaction.signature = alice.sign_transaction(transaction)

# sending the transaction
tx_hash = entrypoint.send_transaction(transaction)

# waits until the transaction is processed and fetches it from the network
transaction_on_network = entrypoint.await_transaction_completed(tx_hash)

# extract the token identifier
parser = TokenManagementTransactionsOutcomeParser()
outcome = parser.parse_issue_semi_fungible(transaction_on_network)

token_identifier = outcome[0].token_identifier
print(token_identifier)
```

--------------------------------

### Install MultiversX NestJS Monitoring SDK

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-nestjs/sdk-nestjs-monitoring

Command to install the `@multiversx/sdk-nestjs-monitoring` package using npm, making it available for use in a project. This is the first step to integrate the monitoring utilities into a NestJS application.

```npm
npm install @multiversx/sdk-nestjs-monitoring
```

--------------------------------

### Redelegate Earned Rewards on MultiversX (Python)

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-py

This snippet illustrates how to redelegate earned rewards back into the MultiversX delegation contract to compound earnings. It provides complete, runnable examples for both the delegation controller and the transactions factory, including necessary account and contract setup.

```python
from pathlib import Path
from multiversx_sdk import Account, Address, DevnetEntrypoint

# create the entrypoint and the delegation controller
entrypoint = DevnetEntrypoint()
controller = entrypoint.create_delegation_controller()

alice = Account.new_from_pem(Path("../multiversx_sdk/testutils/testwallets/alice.pem"))

# fetch the nonce of the network
alice.nonce = entrypoint.recall_account_nonce(alice.address)

# delegation contract
contract = Address.new_from_bech32("erd1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqf8llllswuedva")

transaction = controller.create_transaction_for_redelegating_rewards(
    sender=alice,
    nonce=alice.get_nonce_then_increment(),
    delegation_contract=contract
)

tx_hash = entrypoint.send_transaction(transaction)
```

```python
from pathlib import Path
from multiversx_sdk import Account, Address, DevnetEntrypoint

# create the entrypoint and the delegation transactions factory
entrypoint = DevnetEntrypoint()
factory = entrypoint.create_delegation_transactions_factory()

alice = Account.new_from_pem(Path("../multiversx_sdk/testutils/testwallets/alice.pem"))

# delegation contract (assuming it's defined or fetched)
contract = Address.new_from_bech32("erd1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqf8llllswuedva")

transaction = factory.create_transaction_for_redelegating_rewards(
    sender=alice.address,
    delegation_contract=contract
)

# fetch the nonce of the network
alice.nonce = entrypoint.recall_account_nonce(alice.address)

# set the nonce
transaction.nonce = alice.get_nonce_then_increment()

# sign the transaction
transaction.signature = alice.sign_transaction(transaction)

# send the transaction
tx_hash = entrypoint.send_transaction(transaction)
```

--------------------------------

### Rust Integration Test Example with Go Backend

Source: https://docs.multiversx.com/developers/overview/developers/testing/scenario/running-scenarios

Illustrates how to write Rust integration tests for MultiversX smart contracts using the Go backend. It demonstrates setting up the `ScenarioWorld` with `vm_go()` and running scenario files. It also shows the use of the `#[ignore]` attribute for skipping tests.

```Rust
use multiversx_sc_scenario::*;

fn world() -> ScenarioWorld {
    ScenarioWorld::vm_go()
}

#[test]
fn adder_go() {
    world().run("scenarios/adder.scen.json");
}

#[test]
#[ignore = "reason to ignore"]
fn ignored_test_go() {
    world().run("scenarios/ignored_test.scen.json");
}
```

--------------------------------

### Retrieve MultiversX Account Details via Gateway API

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/rest-api/addresses

Documents the `GET /address/:bech32Address` endpoint of the MultiversX Gateway REST API, providing details on how to query basic information for a given MultiversX account, including its structure, parameters, and an example successful response.

```APIDOC
GET /address/:bech32Address

Description: This endpoint allows one to retrieve basic information about an Address (Account).

Path Parameters:
  bech32Address:
    Type: string
    Required: REQUIRED
    Description: The Address to query.

Response (200 OK):
  Description: Address details retrieved successfully.
  Example:
    {
      "data": {
        "account": {
          "address": "erd1...",
          "nonce": 11,
          "balance": "100000000000000000000",
          "username": "",
          "code": "",
          "codeHash": null,
          "rootHash": "qBFvpFeF6...",
          "codeMetadata": null,
          "developerReward": "0",
          "ownerAddress": ""
        }
      },
      "blockInfo": {
        "nonce": 555,
        "hash": "f55fe00...",
        "rootHash": "294360..."
      },
      "error": "",
      "code": "successful"
    }
```

--------------------------------

### Start MultiversX localnet

Source: https://docs.multiversx.com/developers/overview/developers/setup-local-testnet

Initiates all necessary processes for the MultiversX localnet, including validator nodes, seednode, and the MultiversX Proxy. This command brings the local test network online, making it ready for development and testing.

```bash
mxpy localnet start
```

--------------------------------

### Install Python Dependencies from requirements.txt

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-py

This shell command uses pip to install all Python packages listed in the `requirements.txt` file. This ensures that all necessary project dependencies are installed in the active virtual environment.

```Shell
pip install -r requirements.txt
```

--------------------------------

### Rust Fixed-Point Percentage Calculation Example

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/staking-contract

Provides a concrete example of the fixed-point percentage calculation. It demonstrates how a 50.45% APY (represented as 50_45) applied to a user stake of 100 results in a reward of 50, illustrating the integer division behavior and the resulting precision.

```Rust
reward_amt = 100 * 50_45 / 100_00 = 5045_00 / 100_00 = 50
```

--------------------------------

### Rust Test Environment Setup for MultiversX SC

Source: https://docs.multiversx.com/developers/overview/developers/testing/rust/whitebox-legacy

This Rust code snippet demonstrates the initial setup for a MultiversX smart contract test file. It imports necessary modules from `multiversx_sc` and `multiversx_sc_scenario` and defines a `CrowdfundingSetup` struct to encapsulate common test environment components like blockchain state and contract wrappers, aiding in code de-duplication.

```Rust
use crowdfunding_esdt::*;
use multiversx_sc::{
    sc_error,
    types::{Address, SCResult},
};
use multiversx_sc_scenario::{
    managed_address, managed_biguint, managed_token_id, rust_biguint, whitebox::*,
    DebugApi,
};

const WASM_PATH: &'static str = "crowdfunding-esdt/output/crowdfunding-esdt.wasm";

struct CrowdfundingSetup<CrowdfundingObjBuilder>
where
    CrowdfundingObjBuilder:
        'static + Copy + Fn() -> crowdfunding_esdt::ContractObj<DebugApi>,
{
    pub blockchain_wrapper: BlockchainStateWrapper,
    pub owner_address: Address,
    pub first_user_address: Address,
    pub second_user_address: Address,
    pub cf_wrapper:
        ContractObjWrapper<crowdfunding_esdt::ContractObj<DebugApi>, CrowdfundingObjBuilder>,
}
```

--------------------------------

### Create and Navigate to a New Project Directory

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-py

This shell command sequence creates a new directory named 'hello-multiversx' and then changes the current working directory into it. This is a common first step when setting up a new project on the command line.

```Shell
mkdir hello-multiversx
cd hello-multiversx
```

--------------------------------

### Clone MultiversX Ping Pong Microservice Template

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/your-first-microservice

This command clones the official MultiversX ping-pong microservice template repository from GitHub. It's the first step to setting up the local development environment for the microservice.

```bash
git clone https://github.com/multiversx/mx-ping-pong-service
```

--------------------------------

### MultiversX Smart Contract Deploy Event Structure and Example

Source: https://docs.multiversx.com/developers/overview/developers/event-logs/contract-deploy-events

Details the structure and provides a JSON example of the SCDeploy event, generated upon successful deployment of a smart contract on MultiversX, without encountering errors.

```APIDOC
identifier: SCDeploy
address: the address of the deployed contract
topics:
  topics[0]: the address bytes of the deployed contract base64 encoded
  topics[1]: the address bytes of the deployer of the smart contract base64 encoded
  topics[2]: the code hash bytes of the deployer smart contract base64 encoded
data: empty
```

```JSON
{
    "address": "erd1qqqqqqqqqqqqqpgqnnl9nn0kuuckhg24g02hq2745n4jk2hp327qcay4nm",
    "identifier": "SCDeploy",
    "topics": [
        "AAAAAAAAAAAFAJz+Wc325zFroVVD1XAr1aTrKyrhirw=",
        "NRl7AwoM3hEPC0t9RTDy7gdJUSJvKC5dpJwLYaHLirw=",
        "bJtNdzjeaYecInf/NpHzSjHJEZ2l6hR/uJh0NkLIe+k="
    ],
    "data": null
}
```

--------------------------------

### Download MultiversX Node Installation Scripts

Source: https://docs.multiversx.com/developers/overview/validators/nodes-scripts/config-scripts

This command sequence navigates to the user's home directory and then clones the official MultiversX chain scripts repository from GitHub. These scripts are essential for installing and managing a MultiversX node.

```Bash
cd ~
git clone https://github.com/multiversx/mx-chain-scripts
```

--------------------------------

### Install MultiversX sc-meta and Wasm development tools

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/troubleshooting/rust-setup

Installs the `multiversx-sc-meta` smart contract management tool and then uses it to install the necessary `wasm32` target and optimization tools for Rust smart contract development, along with `twiggy` for analysis.

```bash
cargo install multiversx-sc-meta --locked
```

```bash
# Installs `wasm32`, `wasm-opt`, and others in one go:
sc-meta install all

cargo install twiggy
```

--------------------------------

### MultiversX Smart Contract Project Structure After Build

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/crowdfunding-p1

This snippet displays the typical directory layout of a MultiversX smart contract project following a successful build operation. It highlights the `output/` directory containing the compiled contract artifacts (ABI, imports, WASM) and the `src/` directory where the Rust source code resides, providing an overview of the project's organization.

```Shell
.
├── Cargo.lock
├── Cargo.toml
├── meta
│   ├── Cargo.toml
│   └── src
├── multiversx.json
├── output
│   ├── crowdfunding.abi.json
│   ├── crowdfunding.imports.json
│   ├── crowdfunding.mxsc.json
│   └── crowdfunding.wasm
├── src
│   └── crowdfunding.rs
├── target
│   ├── CACHEDIR.TAG
│   ├── debug
│   ├── release
│   ├── tmp
│   └── wasm32-unknown-unknown
├── tests
└── wasm
    ├── Cargo.lock
    ├── Cargo.toml
    └── src
```

--------------------------------

### Install MultiversX NestJS Cache SDK

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-nestjs/sdk-nestjs-cache

Command to install the `@multiversx/sdk-nestjs-cache` package using npm, which provides caching utilities for MultiversX NestJS microservices.

```bash
npm install @multiversx/sdk-nestjs-cache
```

--------------------------------

### Example MultiversX Keystore JSON Structure

Source: https://docs.multiversx.com/developers/overview/wallet/keystore

Illustrates the typical JSON structure of a MultiversX Keystore file, including cryptographic parameters for encryption and key derivation. This example shows a 'mnemonic' kind keystore.

```json
{
    "version": 4,
    "id": "5b448dbc-5c72-4d83-8038-938b1f8dff19",
    "kind": "mnemonic",
    "crypto": {
        "ciphertext": "6d70fbdceba874f56f15af4b1d060223799288cfc5d276d9ebb91732f5a38c3c59f83896fa7e7eb6a04c05475a6fe4d154de9b9441864c507abd0eb6987dac521b64c0c82783a3cd1e09270cd6cb5ae493f9af694b891253ac1f1ffded68b5ef39c972307e3c33a8354337540908acc795d4df72298dda1ca28ac920983e6a39a01e2bc988bd0b21f864c6de8b5356d11e4b77bc6f75ef",
        "cipherparams": {
            "iv": "2da5620906634972d9a623bc249d63d4"
        },
        "cipher": "aes-128-ctr",
        "kdf": "scrypt",
        "kdfparams": {
            "dklen": 32,
            "salt": "aa9e0ba6b188703071a582c10e5331f2756279feb0e2768f1ba0fd38ec77f035",
            "n": 4096,
            "r": 8,
            "p": 1
        },
        "mac": "5bc1b20b6d903b8ef3273eedf028112d65eaf85a5ef4215917c1209ec2df715a"
    }
}
```

--------------------------------

### Initialize MetamaskProxyProvider and Set Wallet URL

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-js/sdk-js-signing-providers

Explains the necessary steps to initialize the MetamaskProxyProvider and configure the MultiversX Snap Wallet URL before performing any operations.

```typescript
await provider.init();
provider.setWalletUrl("https://snap-wallet.multiversx.com");
```

--------------------------------

### Delegate EGLD to MultiversX Contract (Python)

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-py

This snippet demonstrates how to delegate EGLD tokens to a MultiversX delegation smart contract. It includes complete, runnable examples using both the delegation controller for direct interaction and the transactions factory for building and signing transactions, covering account setup and transaction submission.

```python
from pathlib import Path
from multiversx_sdk import Account, Address, DevnetEntrypoint

# create the entrypoint and the delegation controller
entrypoint = DevnetEntrypoint()
controller = entrypoint.create_delegation_controller()

alice = Account.new_from_pem(Path("../multiversx_sdk/testutils/testwallets/alice.pem"))

# fetch the nonce of the network
alice.nonce = entrypoint.recall_account_nonce(alice.address)

# delegation contract
contract = Address.new_from_bech32("erd1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqf8llllswuedva")

transaction = controller.create_transaction_for_delegating(
    sender=alice,
    nonce=alice.get_nonce_then_increment(),
    delegation_contract=contract,
    amount=5000000000000000000000  # 5000 EGLD
)

tx_hash = entrypoint.send_transaction(transaction)
```

```python
from pathlib import Path
from multiversx_sdk import Account, Address, DevnetEntrypoint

# create the entrypoint and the delegation transactions factory
entrypoint = DevnetEntrypoint()
factory = entrypoint.create_delegation_transactions_factory()

# create the account delegating funds
alice = Account.new_from_pem(Path("../multiversx_sdk/testutils/testwallets/alice.pem"))

# delegation contract (assuming it's defined or fetched)
contract = Address.new_from_bech32("erd1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqf8llllswuedva")

transaction = factory.create_transaction_for_delegating(
    sender=alice.address,
    delegation_contract=contract,
    amount=5000000000000000000000  # 5000 EGLD
)

# fetch the nonce of the network
alice.nonce = entrypoint.recall_account_nonce(alice.address)

# set the nonce
transaction.nonce = alice.get_nonce_then_increment()

# sign the transaction
transaction.signature = alice.sign_transaction(transaction)

# send the transaction
tx_hash = entrypoint.send_transaction(transaction)
```

--------------------------------

### GET MultiversX Network Shard Status API

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/rest-api/network

Documents the API endpoint for retrieving the status of a specific MultiversX blockchain shard. It details the required path parameters and provides an example of a successful JSON response, including various shard-related metrics.

```APIDOC
GET https://gateway.multiversx.com/network/status/:shardId
Description: This endpoint allows one to query the status of a given Shard.
Path Parameters:
  shardID:
    Required: true
    Type: number
    Description: The Shard ID. 0, 1, 2 etc. Use 4294967295 in order to query the Metachain.
```

```JSON
{
  "data": {
    "status": {
      "erd_current_round": 187068,
      "erd_epoch_number": 12,
      "erd_highest_final_nonce": 187019,
      "erd_nonce": 187023,
      "erd_nonce_at_epoch_start": 172770,
      "erd_nonces_passed_in_current_epoch": 14253,
      "erd_round_at_epoch_start": 172814,
      "erd_rounds_passed_in_current_epoch": 14254,
      "erd_rounds_per_epoch": 14400
    }
  },
  "error": "",
  "code": "successful"
}
```

--------------------------------

### Check Docker Container Logs for Sync Status

Source: https://docs.multiversx.com/developers/overview/integrators/observing-squad

To inspect the status inside a specific Docker container, execute a shell within it using `docker exec` and then view the relevant log file to check the last synchronized block nonce.

```bash
docker exec -it 'CONTAINER ID' /bin/bash
cat logs/mx-chain-.......log
```

--------------------------------

### Example Output of mxpy Configuration Dump

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/mxpy/mxpy-cli

An example of the JSON output returned when dumping the current `mxpy` configuration. This snippet illustrates the structure and content of the configuration data, specifically showing a dependency tag.

```JSON
{
  "dependencies.testwallets.tag": ""
}
```

--------------------------------

### Combine JwtAuthenticateGuard and JwtAdminGuard for Admin Controllers

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-nestjs/sdk-nestjs-auth

This example demonstrates how to use both `JwtAuthenticateGuard` and `JwtAdminGuard` together on a NestJS controller. This setup ensures that requests are authenticated via JWT and also originate from predefined administrator addresses, requiring an 'address' field in the JWT payload.

```TypeScript
 import { JwtAuthenticateGuard, JwtAdminGuard } from "@multiversx/sdk-nestjs-auth";

 @Controller('admin')
 @UseGuards(JwtAuthenticateGuard, JwtAdminGuard)
 export class AdminController {
   // your methods...
 }
```

--------------------------------

### Build and Generate MultiversX Contract Artifacts

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/staking-contract

These shell commands are used to build the MultiversX smart contract, generate necessary snippets (e.g., for ABI), and then navigate into the `interactor` directory, preparing for contract interaction.

```Shell
sc-meta all build
sc-meta all snippets
cd interactor/
```

--------------------------------

### Install Rust Build Dependencies on Ubuntu/WSL

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/troubleshooting/rust-setup

This command installs essential build tools and libraries like `build-essential`, `pkg-config`, and `libssl-dev` required for compiling Rust projects and `sc-meta` on Ubuntu or Windows Subsystem for Linux (WSL) environments.

```bash
sudo apt-get install build-essential pkg-config libssl-dev
```

--------------------------------

### Remove Previous mxpy Installation

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/mxpy/installing-mxpy

Before installing mxpy with pipx, it's recommended to remove any old mxpy shortcuts and virtual Python environments, especially if mxpy was previously installed using mxpy-up.

```Shell
rm ~/multiversx-sdk/mxpy
rm -rf ~/multiversx-sdk/mxpy-venv
```

--------------------------------

### Getting Help for mxpy Contract Deploy Command

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/mxpy/mxpy-cli

Use this command to display all available parameters and options for the `mxpy contract deploy` command. This is useful for understanding its full capabilities, required arguments, and optional flags.

```shell
mxpy contract deploy --help
```

--------------------------------

### Create Devnet Entrypoint

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-js/sdk-js-cookbook

Initializes a DevnetEntrypoint instance, providing a simplified client for common operations on the MultiversX Devnet.

```JavaScript
const entrypoint = new DevnetEntrypoint();
```

--------------------------------

### MultiversX JavaScript SDK (sdk-js) Overview

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/overview

Documentation for the MultiversX JavaScript SDK, `sdk-js`, providing high-level overviews, cookbooks for common tasks, extension guides, and integration details for signing providers. It also mentions xSuite, an external JavaScript toolkit for contract development.

```APIDOC
sdk-js - Javascript SDK:
  Description: High-level overview of the MultiversX JavaScript SDK.
  Related Resources:
    - Name: sdk-js (main overview)
      Description: High level overview about sdk-js.
      Link: /sdk-and-tools/sdk-js
    - Name: sdk-js cookbook
      Description: Learn how to handle common tasks by using sdk-js.
      Link: /sdk-and-tools/sdk-js/sdk-js-cookbook
    - Name: Extending sdk-js
      Description: How to extend and tailor certain modules of sdk-js.
      Link: /sdk-and-tools/sdk-js/extending-sdk-js
    - Name: Writing and testing sdk-js interactions
      Description: Write sdk-js interactions for Visual Studio Code.
      Link: /sdk-and-tools/sdk-js/writing-and-testing-sdk-js-interactions
    - Name: sdk-js signing providers
      Description: Integrate sdk-js signing providers.
      Link: /sdk-and-tools/sdk-js/sdk-js-signing-providers
  Additional Tool:
    - Name: xSuite
      Description: A toolkit to init, build, test, deploy contracts using JavaScript, made by the Arda team.
      Link: https://xsuite.dev
```

--------------------------------

### Install pip3 on macOS

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/mxpy/installing-mxpy

macOS users can install pip3 by running the `ensurepip` module via python3.

```Shell
python3 -m ensurepip
```

--------------------------------

### Navigate to Testnet Scripts Directory

Source: https://docs.multiversx.com/developers/overview/sovereign/distributed-setup

Changes the current working directory to the `scripts/testnet` subdirectory within the cloned `mx-chain-sovereign-go` repository. This directory contains scripts relevant for testnet deployments and further setup steps.

```Bash
cd mx-chain-sovereign-go/scripts/testnet
```

--------------------------------

### Import Hooks from Specific SDK-dapp Sub-modules

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-dapp

Example demonstrating more granular imports of hooks, like `useExtensionLogin` from `hooks/login` and `useGetAccountInfo` from `hooks/account`. This approach can be used for better tree-shaking and reduced bundle size.

```javascript
import { useExtensionLogin } from "@multiversx/sdk-dapp/hooks/login";
import { useGetAccountInfo } from "@multiversx/sdk-dapp/hooks/account";
```

--------------------------------

### Build a MultiversX smart contract

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/staking-contract

This command compiles the smart contract project using `sc-meta`, generating the necessary output files, including the WASM bytecode and ABI JSON. After execution, an 'output' directory will be created containing the compiled contract artifacts ready for deployment.

```Bash
sc-meta all build
```

--------------------------------

### Perform Custom MultiversX API/Proxy Calls (Generic GET)

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-js/sdk-js-cookbook

Details how to make custom API calls beyond the standard SDK methods using generic `doGetGeneric` and `doPostGeneric` methods. This is useful when specific API endpoints are not directly exposed. An example is provided for fetching transactions for a specific account and function call.

```javascript
{
    const entrypoint = new DevnetEntrypoint();
    const api = entrypoint.createNetworkProvider();

    const alice = Address.newFromBech32("erd1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssycr6th");
    const url = `transactions/${alice.toBech32()}?function=delegate`;

    const response = await api.doGetGeneric(url);
}
```

--------------------------------

### Generate MultiversX Localnet Configuration File

Source: https://docs.multiversx.com/developers/overview/developers/setup-local-testnet

Creates a new `localnet.toml` configuration file in the current directory with default settings for a MultiversX localnet. Users should inspect and modify this file before starting the localnet.

```bash
mxpy localnet new
```

--------------------------------

### Setup Ampd with Docker

Source: https://docs.multiversx.com/developers/overview/bridge/axelar

This command pulls the `ampd` Docker image, which is the core process for the Axelar Amplifier verifier. It prepares the environment for running the verifier and interacting with the Axelar network.

```bash
docker pull axelarnet/axelar-ampd:v1.3.1
```

--------------------------------

### Configure MultiversX Testnet Variables

Source: https://docs.multiversx.com/developers/overview/developers/setup-local-testnet-advanced

This snippet shows how to define core Testnet variables, such as the installation directory and shard count, within the `scripts/testnet/variables.sh` file. These variables dictate the fundamental structure of the Testnet environment.

```bash
export TESTNETDIR="$HOME/MultiversX/testnet"
export SHARDCOUNT=2
...
```

--------------------------------

### Create Devnet Entrypoint for Proxy Interaction

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-py

Illustrates how to configure a `DevnetEntrypoint` to interact with the proxy gateway instead of the default API, by specifying the `kind` parameter as 'proxy' along with the gateway URL.

```Python
from multiversx_sdk import DevnetEntrypoint

custom_entrypoint = DevnetEntrypoint(url="https://devnet-gateway.multiversx.com", kind="proxy")
```

--------------------------------

### MultiversX Crowdfunding Smart Contract API Design

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/crowdfunding-p1

Overview of the core methods for the crowdfunding smart contract, detailing their purpose, inputs, outputs, and behavior under different conditions.

```APIDOC
Crowdfunding Smart Contract Methods:
  init(target_amount_egld: u64, deadline_block_nonce: u64)
    description: Triggered on contract deployment. Initializes the crowdfunding campaign with a target EGLD amount and a deadline block nonce.
    parameters:
      target_amount_egld: The target amount of EGLD to raise.
      deadline_block_nonce: The block nonce representing the crowdfunding deadline.

  fund()
    description: Allows donors to contribute EGLD to the campaign. Records necessary details for potential refunds.
    receives: EGLD

  claim()
    description: Handles fund distribution or refunds after the deadline.
    behavior:
      - If called before deadline: Returns error.
      - If called by campaign creator after deadline:
        - If target met: Sends all raised EGLD to creator's account.
        - If target not met: Returns error.
      - If called by donor after deadline:
        - If target not met: Refunds donor's contribution.
        - If target met: Does nothing, returns error.
      - If called by anyone else: Does nothing, returns error.

  status()
    description: Provides real-time information about the campaign's progress.
    returns: Campaign activity status (active/completed), total EGLD raised.
```

--------------------------------

### Setup Crowdfunding Test Environment in Rust

Source: https://docs.multiversx.com/developers/overview/developers/testing/rust/whitebox-legacy

This Rust function, `setup_crowdfunding`, initializes a comprehensive test environment for a crowdfunding smart contract. It utilizes `BlockchainStateWrapper` to create mock owner and user accounts, deploys the smart contract, sets initial ESDT balances for users, and executes the contract's `init` function. The function returns a `CrowdfundingSetup` struct, encapsulating the blockchain state and all relevant account details for further testing.

```Rust
fn setup_crowdfunding<CrowdfundingObjBuilder>(
    cf_builder: CrowdfundingObjBuilder,
) -> CrowdfundingSetup<CrowdfundingObjBuilder>
where
    CrowdfundingObjBuilder: 'static + Copy + Fn() -> crowdfunding_esdt::ContractObj<DebugApi>,
{
    let rust_zero = rust_biguint!(0u64);
    let mut blockchain_wrapper = BlockchainStateWrapper::new();
    let owner_address = blockchain_wrapper.create_user_account(&rust_zero);
    let first_user_address = blockchain_wrapper.create_user_account(&rust_zero);
    let second_user_address = blockchain_wrapper.create_user_account(&rust_zero);
    let cf_wrapper = blockchain_wrapper.create_sc_account(
        &rust_zero,
        Some(&owner_address),
        cf_builder,
        WASM_PATH,
    );

    blockchain_wrapper.set_esdt_balance(&first_user_address, CF_TOKEN_ID, &rust_biguint!(1_000));
    blockchain_wrapper.set_esdt_balance(&second_user_address, CF_TOKEN_ID, &rust_biguint!(1_000));

    blockchain_wrapper
        .execute_tx(&owner_address, &cf_wrapper, &rust_zero, |sc| {
            let target = managed_biguint!(2_000);
            let token_id = managed_token_id!(CF_TOKEN_ID);

            sc.init(target, CF_DEADLINE, token_id);
        })
        .assert_ok();

    blockchain_wrapper.add_mandos_set_account(cf_wrapper.address_ref());

    CrowdfundingSetup {
        blockchain_wrapper,
        owner_address,
        first_user_address,
        second_user_address,
        cf_wrapper,
    }
}
```

--------------------------------

### Install argcomplete for Shell Completion

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/mxpy/installing-mxpy

This command installs the `argcomplete` package using pip3, which is required for enabling shell completion for mxpy.

```Shell
pip3 install argcomplete
```

--------------------------------

### Install mxpy CLI from GitHub Branch

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/mxpy/installing-mxpy

This command allows installing the mxpy CLI directly from a specific branch of its GitHub repository. Replace `branch_name` with the desired branch.

```Shell
pipx install git+https://github.com/multiversx/mx-sdk-py-cli@branch_name
```

--------------------------------

### Configure RabbitMQ for Event Subscription

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/notifier

This TOML configuration snippet details the setup for RabbitMQ in the MultiversX notifier service. It specifies the connection URL and defines exchanges for 'all_events' and 'revert_events', which are automatically created (if not existing) upon service start. RabbitMQ is recommended for scenarios where avoiding event loss is critical.

```TOML
[RabbitMQ]
    # The url used to connect to a rabbitMQ server
    Url = "amqp://guest:guest@localhost:5672"

    # The exchange which holds all logs and events
    [RabbitMQ.EventsExchange]
        Name = "all_events"
        Type = "fanout"

    # The exchange which holds revert events
    [RabbitMQ.RevertEventsExchange]
        Name = "revert_events"
        Type = "fanout"
```

--------------------------------

### Run MultiversX Node Migration Operation

Source: https://docs.multiversx.com/developers/overview/validators/nodes-scripts/install-update

After successfully cloning and configuring the new `mx-chain-scripts`, navigate into its directory and execute the `migrate` operation. This command facilitates the transition from previous node installations to the new script system, aiming to preserve validator keys, node installation, database, and logs.

```bash
cd ~/mx-chain-scripts
./script.sh migrate
```

--------------------------------

### Accessing Help for mxpy Dependency Management Commands

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/mxpy/mxpy-cli

Provides commands to view detailed help documentation for the `mxpy deps check` and `mxpy deps install` commands. This is useful for understanding their accepted positional arguments and available flags.

```Shell
mxpy deps check -h
mxpy deps install -h
```

--------------------------------

### Install pip3 on Linux

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/mxpy/installing-mxpy

For Linux users, this command installs the pip3 package manager using apt, if it's not already present.

```Shell
sudo apt install python3-pip
```

--------------------------------

### Import Login Hooks from SDK-dapp

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-dapp

Example of importing various authentication-related hooks, including `useExtensionLogin`, `useLedgerLogin`, `useWalletConnectLogin`, and `useWebWalletLogin`, from the `@multiversx/sdk-dapp/hooks/login` module.

```javascript
import {
  useExtensionLogin,
  useLedgerLogin,
  useWalletConnectLogin,
  useWebWalletLogin,
} from "@multiversx/sdk-dapp/hooks/login";
```

--------------------------------

### Send MultiversX Transaction using mxpy CLI

Source: https://docs.multiversx.com/developers/overview/developers/setup-local-testnet-advanced

This example shows how to send a simple transaction using the `mxpy` command-line tool. It includes parameters for recalling nonce, adding data, setting gas limits, specifying the receiver, providing PEM key details, and pointing to the local proxy.

```bash
mxpy tx new --recall-nonce --data="Hello, World" --gas-limit=70000 \
 --receiver=erd1... \
 --pem=./sandbox/node/config/walletKey.pem --pem-index=0 \
 --proxy=http://localhost:7950 \
 --send
```

--------------------------------

### Deploying Smart Contract with Controller (Python)

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-py

This snippet demonstrates how to deploy a smart contract using the `DevnetEntrypoint` and `SmartContractController` in Python. It covers account preparation, loading ABI and bytecode, handling deployment arguments (both typed and plain Python values), creating the deployment transaction, and broadcasting it to the network.

```Python
from pathlib import Path

from multiversx_sdk import Account, DevnetEntrypoint
from multiversx_sdk.abi import Abi, BigUIntValue

# prepare the account
account = Account.new_from_keystore(
    file_path=Path("../multiversx_sdk/testutils/testwallets/withDummyMnemonic.json"),
    password="password",
    address_index=0
)
# the developer is responsible for managing the nonce
account.nonce = entrypoint.recall_account_nonce(account.address)

# load the abi file
abi = Abi.load(Path("contracts/adder.abi.json"))

# get the smart contracts controller
entrypoint = DevnetEntrypoint()
controller = entrypoint.create_smart_contract_controller(abi=abi)

# load the contract bytecode
bytecode = Path("contracts/adder.wasm").read_bytes()

# For deploy arguments, use typed value objects if you haven't provided an ABI
args = [BigUIntValue(42)]
# Or use simple, plain Python values and objects if you have provided an ABI
args = [42]

deploy_transaction = controller.create_transaction_for_deploy(
    sender=account,
    nonce=account.get_nonce_then_increment(),
    bytecode=bytecode,
    gas_limit=5000000,
    arguments=args,
    is_upgradeable=True,
    is_readable=True,
    is_payable=True,
    is_payable_by_sc=True
)

# broadcasting the transaction
tx_hash = entrypoint.send_transaction(deploy_transaction)

```

--------------------------------

### Get Entire Transactions Pool API (Default)

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/rest-api/transactions

Documents the API endpoint to fetch the entire transaction pool, merging pools from each shard. This endpoint is specifically for local proxy instances with a particular configuration enabled. An example request URL and a default successful JSON response are provided.

```APIDOC
GET /transaction/pool
Description: Fetch the entire transactions pool, merging pools from each shard. (Local proxy instance only, with AllowEntireTxPoolFetch=true)
Example: http://local-proxy-instance/transaction/pool
Response:
  200 OK: Transaction status retrieved successfully.
```

```JSON
{
  "data": {
    "txPool": {
      "regularTransactions": [
        {
          "txFields": {
            "hash": "84bb8a..."
          }
        },
        {
          "txFields": {
            "hash": "4e2c43..."
          }
        }
      ],
      "smartContractResults": [],
      "rewards": []
    },
    "error": "",
    "code": "successful"
}
```

--------------------------------

### Install pipx and Configure Path

Source: https://docs.multiversx.com/developers/overview/sovereign/software-dependencies

Commands to install pipx, a tool for installing and managing Python applications in isolated environments, and ensure its executables are correctly added to the system's PATH for global access.

```Bash
sudo apt install pipx
pipx ensurepath
sudo pipx ensurepath --global
```

--------------------------------

### MultiversX Python SDK API Reference

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-py

Detailed API documentation for key classes and methods within the `multiversx_sdk` package, including constructors, parameters, return types, and descriptions for network entrypoints and account management.

```APIDOC
multiversx_sdk:
  DevnetEntrypoint:
    Description: Represents a network client for the MultiversX Devnet, providing access to common operations.
    __init__(self, url: str = None, kind: str = None)
      url: str = None
        The URL of the API or proxy to connect to. Defaults to the standard Devnet API if not provided.
      kind: str = None
        Specifies the type of endpoint, e.g., "proxy", to interact with the gateway instead of the API.
    create_account(self) -> Account
      Description: Creates a new network-agnostic account.
      Returns: Account
        A newly created Account object.
  NetworkEntrypoint:
    Description: A generic network client that can be configured with a specific network provider.
    new_from_network_provider(network_provider: ApiNetworkProvider, chain_id: str) -> NetworkEntrypoint
      Description: Creates a new NetworkEntrypoint instance from an existing API network provider.
      network_provider: ApiNetworkProvider
        An instance of an API network provider to use for network interactions.
      chain_id: str
        The chain ID of the network (e.g., "D" for Devnet, "T" for Testnet).
      Returns: NetworkEntrypoint
        A new NetworkEntrypoint configured with the specified provider and chain ID.
  ApiNetworkProvider:
    Description: Provides an interface to interact with a MultiversX API endpoint.
    __init__(self, url: str)
      url: str
        The base URL of the API endpoint.
  Account:
    Description: Represents a network-agnostic account. It is used for signing transactions and storing the account's nonce. Accounts can be saved to PEM or Keystore files for persistence.
```

--------------------------------

### Install wget on Linux

Source: https://docs.multiversx.com/developers/overview/sovereign/software-dependencies

Command to install wget, a command-line utility for retrieving content from web servers, on Linux systems.

```Bash
apt install wget
```

--------------------------------

### Load Wallet from Keystore Secret Key File

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-py

Provides an example of loading a secret key directly from an encrypted keystore file using UserWallet.load_secret_key. It then derives and prints the associated public address.

```python
from pathlib import Path
from multiversx_sdk import UserWallet

secret_key = UserWallet.load_secret_key(Path("walletWithSecretKey.json"), "password")
address = secret_key.generate_public_key().to_address("erd")

print("Secret key:", secret_key.hex())
print("Address:", address.to_bech32())
```

--------------------------------

### Create and navigate to localnet workspace

Source: https://docs.multiversx.com/developers/overview/developers/setup-local-testnet

This command creates a new directory named 'my-first-localnet' in the user's home directory if it doesn't already exist, and then changes the current working directory to this newly created folder. This workspace will house all localnet-related files.

```bash
mkdir -p ~/my-first-localnet && cd ~/my-first-localnet
```

--------------------------------

### Uninstall Rust from various installation sources

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/troubleshooting/rust-setup

Provides commands to remove existing Rust installations, covering common package managers (APT, Homebrew, Snap), `rustup`, and specific `mxpy` vendor directories.

```bash
# Ubuntu
sudo apt remove cargo
sudo apt remove rustc
sudo apt autoremove
```

```bash
rustup self uninstall
```

```bash
brew uninstall rust
```

```bash
snap remove rustup
```

```bash
rm -rf ~/multiversx-sdk/vendor-rust
```

--------------------------------

### Install Specific mxpy CLI Version with pipx

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/mxpy/installing-mxpy

To install a particular version of the MultiversX SDK CLI, specify the version number after the package name using `==`.

```Shell
pipx install multiversx-sdk-cli==9.5.1
```

--------------------------------

### Get Transactions Pool API (Custom Fields)

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/rest-api/transactions

Documents the API endpoint to fetch the transaction pool with custom fields or filtered by shard ID. It explains the 'fields' and 'shard-id' query parameters, provides an example request URL, and includes a successful JSON response demonstrating filtered data.

```APIDOC
GET /transaction/pool
Description: Fetch the transaction pool with custom fields or filtered by shard ID.
Query Parameters:
  fields:
    Required: OPTIONAL
    Type: string
    Description: A list of the fields to be included. Possible values: hash, nonce, sender, receiver, gaslimit, gasprice, receiverusername, data, value.
  shard-id:
    Required: OPTIONAL
    Type: string
    Description: A specific shard id (0, 1, 2 etc. or 4294967295 for Metachain).
Example: https://gateway.multiversx.com/transaction/pool?shard-id=0&fields=sender,receiver,value
Response:
  200 OK: Transaction status retrieved successfully.
```

```JSON
{
  "data": {
    "txPool": {
      "regularTransactions": [
        {
          "txFields": {
            "gasLimit": 10,
            "gasPrice": 1000,
            "receiver": "erd1...",
            "sender": "erd1...",
            "value": "10000000000000000000"
          }
        }
      ],
      "smartContractResults": [
        {
          "txFields": {
            "gasLimit": 10,
            "gasPrice": 1000,
            "receiver": "erd1...",
            "sender": "erd1...",
            "value": "10000000000000000000"
          }
        }
      ],
      "rewards": [
        {
          "txFields": {
            "gasLimit": 10,
            "gasPrice": 1000,
            "receiver": "erd1...",
            "sender": "erd1...",
            "value": "10000000000000000000"
          }
        }
      ]
    }
  },
  "error": "",
  "code": "successful"
}
```

--------------------------------

### Example MultiversX Contract Address in state.toml

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/interactors-guide

This snippet illustrates how a newly deployed MultiversX smart contract address is recorded in the `state.toml` file, which is automatically generated or updated after a successful deployment.

```TOML
contract_address = "erd1qqqqqqqqqqqqqpgqpsev0x4nufh240l44gf2t6qzkh9xvutqd8ssrnydzr"
```

--------------------------------

### Execute MultiversX Interactor Deploy Command

Source: https://docs.multiversx.com/developers/overview/developers/meta/interactor/interactors-example

This shell command demonstrates how to run the `deploy` command for the MultiversX interactor using `cargo run`. Executing this command in the `interactor` root folder will deploy the contract and generate a `state.toml` file containing the newly deployed address.

```Shell
interactor % cargo run deploy
```

--------------------------------

### MultiversX Multisig Contract Configuration Example

Source: https://docs.multiversx.com/developers/overview/developers/meta/sc-config

An example TOML configuration demonstrating how to set up a main multisig contract, an external view contract, and a full contract. It also shows how to use `labels-for-contracts` to map default and external view labels to specific contract IDs.

```TOML
[settings]
main = "multisig-main"

[contracts.multisig-main]
name = "multisig"

[contracts.view]
name = "multisig-view"
external-view = true

[contracts.full]
name = "multisig-full"

[labels-for-contracts]
default = ["multisig-main", "full"]
multisig-external-view = ["view", "full"]
```

--------------------------------

### Install MultiversX SDK Ledger Dependencies (npm)

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-js/sdk-js-cookbook

Provides the npm command to install the `@multiversx/sdk-hw-provider` package. This package is essential for enabling Ledger hardware wallet support within the MultiversX SDK, allowing secure transaction signing.

```npm
npm install @multiversx/sdk-hw-provider
```

--------------------------------

### Install MultiversX NestJS Auth SDK via npm

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-nestjs/sdk-nestjs-auth

This command installs the @multiversx/sdk-nestjs-auth package, a set of utilities for native authentication in MultiversX NestJS microservices, using the npm package manager.

```Bash
npm install @multiversx/sdk-nestjs-auth
```

--------------------------------

### Query MultiversX Smart Contract Results by Original Transaction Hash

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/indices/es-index-scresults

This example demonstrates how to fetch all smart contract results associated with a specific original transaction hash. It uses a `curl` command to perform a GET request against the MultiversX Elasticsearch API's `scresults` endpoint, filtering by the `originalTxHash` field.

```bash
curl --request GET \
  --url ${ES_URL}/scresults/_search \
  --header 'Content-Type: application/json' \
  --data '{
	"query": {
		"match": {
			"originalTxHash":"d6.."
		}
	}
}'
```

--------------------------------

### Build MultiversX Smart Contract using sc-meta CLI

Source: https://docs.multiversx.com/developers/overview/developers/meta/sc-build-reference

This command initiates the build process for a MultiversX smart contract. It leverages the `sc-meta` command-line tool to compile the contract, and should be executed from the root directory of the contract project. The `all build` arguments instruct the tool to perform a complete build.

```bash
sc-meta all build
```

--------------------------------

### MultiversX Sovereign Node Configuration Files

Source: https://docs.multiversx.com/developers/overview/sovereign/distributed-setup

Outlines the specific configuration files located in the `cmd/sovereignnode/config` directory, which are essential for a MultiversX sovereign chain setup.

```text
enableEpochs.toml
prefs.toml
sovereignConfig.toml
```

--------------------------------

### Activate Global Shell Completion

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/mxpy/installing-mxpy

After installing `argcomplete`, this command activates global shell completion for Python-based CLIs, including mxpy.

```Shell
activate-global-python-argcomplete
```

--------------------------------

### Fetch Latest 10 Blocks for All Shards using cURL

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/indices/es-index-blocks

This cURL command demonstrates how to query the MultiversX ElasticSearch index to retrieve the 10 most recent blocks across all shards. It sends a GET request to the /blocks/_search endpoint with a JSON payload that sorts results by timestamp in descending order and limits the size to 10.

```curl
curl --request GET \
  --url ${ES_URL}/blocks/_search \
  --header 'Content-Type: application/json' \
  --data '{
    "sort": [
        {
            "timestamp": {
                "order": "desc"
            }
        }
    ],
    "size":10
}'
```

--------------------------------

### Install MultiversX Smart Contract Meta Tool

Source: https://docs.multiversx.com/developers/overview/developers/meta/sc-meta

Installs the `multiversx-sc-meta` command-line interface (CLI) tool using Cargo, the Rust package manager. The `--locked` flag ensures that the exact versions specified in `Cargo.lock` are used, providing reproducible builds.

```Rust
cargo install multiversx-sc-meta --locked
```

--------------------------------

### Run Redis Server as a Daemon

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/your-first-microservice

This command starts the Redis server in the background as a daemon process. Running Redis as a daemon allows it to operate continuously without occupying the terminal, which is suitable for development environments.

```bash
redis-server --daemonize yes
```

--------------------------------

### Create Account from PEM File (JavaScript)

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-js/sdk-js-cookbook

Shows how to load an `Account` instance directly from a specified PEM file path using the static method `Account.newFromPem`. This method simplifies account loading from pre-existing PEM files.

```JavaScript
{
    const filePath = path.join("../src", "testdata", "testwallets", "alice.pem");
    const accountFromPem = Account.newFromPem(filePath);
}
```

--------------------------------

### MultiversX Smart Contract Token Transfer Endpoint in Rust

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/eth-to-mvx

Demonstrates a simplified token transfer within a MultiversX smart contract. This Rust example uses `#[payable]` and `#[endpoint]` attributes, retrieves payment details using `self.call_value().single_esdt()`, and constructs a direct transfer transaction using the `self.tx()` fluent API, highlighting the contract's ability to act as an account.

```Rust
#[payable("*")]
#[endpoint]
fn transfer(&self, to_address: ManagedAddress) {
   let payment= self.call_value().single_esdt();
   self.tx()
      .to(to_address)
      .single_esdt(&payment.token_identifier, payment.token_nonce, &payment.amount)
      .transfer();
}
```

--------------------------------

### MultiversX Testnet Generated Configuration Directory Structure

Source: https://docs.multiversx.com/developers/overview/developers/setup-local-testnet-advanced

This snippet illustrates the typical directory and file structure generated by the `config.sh` command. It shows where various configuration files, keys, and smart contracts are placed within the Testnet's working directory.

```text
$HOME/Desktop/mytestnet/sandbox
├── filegen
│   ├── filegen
│   └── output
│       ├── delegationWalletKey.pem
│       ├── delegators.pem
│       ├── genesis.json
│       ├── genesisSmartContracts.json
│       ├── nodesSetup.json
│       ├── validatorKey.pem
│       └── walletKey.pem
├── node
│   └── config
│       ├── api.toml
│       ├── config_observer.toml
│       ├── config_validator.toml
│       ├── delegationWalletKey.pem
│       ├── delegators.pem
│       ├── economics.toml
│       ├── external.toml
│       ├── gasSchedule.toml
│       ├── genesisContracts
│       │   ├── delegation.wasm
│       │   └── dns.wasm
│       ├── genesis.json
│       ├── genesisSmartContracts.json
│       ├── nodesSetup.json
│       ├── p2p.toml
│       ├── prefs.toml
│       ├── ratings.toml
│       ├── systemSmartContractsConfig.toml
│       ├── validatorKey.pem
│       └── walletKey.pem
├── node_working_dirs
├── proxy
│   └── config
│       ├── config.toml
│       ├── economics.toml
│       ├── external.toml
│       └── walletKey.pem
└── seednode
    └── config
        ├── config.toml
        └── p2p.toml
```

--------------------------------

### Install screen on Linux

Source: https://docs.multiversx.com/developers/overview/sovereign/software-dependencies

Command to install the 'screen' utility, another terminal multiplexer, on Linux systems.

```Bash
sudo apt install screen
```

--------------------------------

### Install MultiversX SDK via pip

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-py

This command installs the core MultiversX SDK package into the active Python virtual environment using pip. It's the standard way to add the SDK as a dependency to a Python project.

```Shell
pip install multiversx-sdk
```

--------------------------------

### Setup Tofnd with Docker

Source: https://docs.multiversx.com/developers/overview/bridge/axelar

This snippet provides Docker commands to pull and run the `tofnd` service, which is essential for cryptographic operations in the Axelar network. It configures `tofnd` to listen on port 50051 and uses auto-generated mnemonic with no password for simplicity in a development setup.

```bash
docker pull axelarnet/tofnd:v1.0.1
docker run -p 50051:50051 --env MNEMONIC_CMD=auto --env NOPASSWORD=true --env ADDRESS=0.0.0.0 -v tofnd:/.tofnd axelarnet/tofnd:v1.0.1
```

--------------------------------

### Displaying mxpy CLI Help Information

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/mxpy/mxpy-cli

Demonstrates how to access help documentation for the `mxpy` command-line tool. This includes general help for the main command and specific help for subcommands like `tx` and `tx new`, providing insights into their usage and available options.

```Shell
mxpy --help
mxpy tx --help
mxpy tx new --help
```

--------------------------------

### APIDOC: SetMapper Storage Structure Example

Source: https://docs.multiversx.com/developers/overview/developers/developer-reference/storage-mappers

Provides an example of the underlying storage structure for a `SetMapper` containing two elements. It shows how `info`, `node_id`, `node_links`, and `value` entries are organized to facilitate efficient O(1) lookups, albeit with higher storage entry count.

```APIDOC
"str:tokenWhitelist.info": "u32:2|u32:1|u32:2|u32:2",
"str:tokenWhitelist.node_idEGLD-123456": "2",
"str:tokenWhitelist.node_idETH-123456": "1",
"str:tokenWhitelist.node_links|u32:1": "u32:0|u32:2",
"str:tokenWhitelist.node_links|u32:2": "u32:1|u32:0",
"str:tokenWhitelist.value|u32:2": "str:EGLD-123456",
"str:tokenWhitelist.value|u32:1": "str:ETH-123456"
```

--------------------------------

### Run MultiversX Testnet Configuration Command

Source: https://docs.multiversx.com/developers/overview/developers/setup-local-testnet-advanced

After defining or overriding Testnet variables, execute the `config.sh` script. This command processes the variables and generates the necessary configuration files for the Testnet.

```bash
./config.sh
```

--------------------------------

### Deploy Multisig Smart Contract with MultiversX Factory (Python)

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-py

This example illustrates the deployment of a Multisig smart contract on MultiversX using the `MultisigTransactionsFactory` class. It shows how to configure the factory, create a deployment transaction, sign it with the sender's account, and broadcast it to the network.

```Python
from pathlib import Path
from multiversx_sdk import Account, Address, ApiNetworkProvider, MultisigTransactionsFactory, TransactionsFactoryConfig
from multiversx_sdk.abi import Abi

alice = Account.new_from_pem(Path("../multiversx_sdk/testutils/testwallets/alice.pem"))
api = ApiNetworkProvider(url="https://devnet-api.multiversx.com")
alice.nonce = api.get_account(alice.address).nonce

abi = Abi.load(Path("../multiversx_sdk/testutils/testdata/multisig-full.abi.json"))
config = TransactionsFactoryConfig(chain_id="D")
factory = MultisigTransactionsFactory(config=config, abi=abi)

transaction = factory.create_transaction_for_deploy(
    sender=alice.address,
    bytecode=Path("../multiversx_sdk/testutils/testdata/multisig-full.wasm"),
    quorum=2,
    board=[alice.address, Address.new_from_bech32("erd1spyavw0956vq68xj8y4tenjpq2wd5a9p2c6j8gsz7ztyrnpxrruqzu66jx")],
    gas_limit=100_000_000,
)
transaction.nonce = alice.get_nonce_then_increment()
transaction.signature = alice.sign_transaction(transaction)

tx_hash = api.send_transaction(transaction)

```

--------------------------------

### BLS Key Identities Mapping

Source: https://docs.multiversx.com/developers/overview/validators/key-management/multikey-nodes

This table provides a mapping of specific BLS keys to their corresponding node names and GitHub identities within a multikey setup. It illustrates how individual BLS keys are identified and named in the explorer after the multikey nodes are started, showing the relationship between the key, its assigned name (e.g., 'tsp-00'), and the overarching GitHub identity.

```APIDOC
Key | Name | Identity
--- | --- | ---
15eb03756... | tsp-00 | testing-staking-provider
ff12bc7f4... | tsp-01 | testing-staking-provider
3dec570c0... | tsp-02 | testing-staking-provider
38a93e3c0... | tsp-03 | testing-staking-provider
1fce426b6... | tsp-04 | testing-staking-provider
```

--------------------------------

### Configure MultiversX Observing Squad Environment Variables

Source: https://docs.multiversx.com/developers/overview/bridge/axelar

This snippet shows how to set environment variables in `config/variables.cfg` for a MultiversX Observing Squad setup, specifying the network (mainnet) and custom home directory/user. This file is edited before running setup scripts.

```toml
ENVIRONMENT="mainnet"
...
CUSTOM_HOME="/home/ubuntu"
CUSTOM_USER="ubuntu"
```

--------------------------------

### Initialize MultiversX Extension Provider

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-js/sdk-js-signing-providers

Initializes the `ExtensionProvider` instance. This step is crucial and must be completed before any operations like login or signing can be performed.

```javascript
await provider.init();
```

--------------------------------

### Deploy MultiversX Crowdfunding Smart Contract (Rust)

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/crowdfunding-p1

This Rust code snippet demonstrates how to deploy a MultiversX smart contract in a test environment. It initializes a `TestSCAddress` for the contract, uses the `world.tx()` builder to set the transaction sender, initial arguments, and the contract's code path, finally returning the new address.

```Rust
const CROWDFUNDING_ADDRESS: TestSCAddress = TestSCAddress::new("crowdfunding");

#[test]
fn crowdfunding_deploy_test() {
    /*
        Set up account
    */

    let crowdfunding_address = world
        .tx()
        .from(OWNER)
        .typed(crowdfunding_proxy::CrowdfundingProxy)
        .init(500_000_000_000u64)
        .code(CODE_PATH)
        .new_address(CROWDFUNDING_ADDRESS)
        .returns(ReturnsNewAddress)
        .run();
}
```

--------------------------------

### Hardware Wallet (Ledger): Initialize Provider

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-js/sdk-js-signing-providers

Demonstrates the necessary initialization step for the `HWProvider` before performing any operations. The MultiversX application must be open on the Ledger device.

```javascript
await provider.init();
```

--------------------------------

### Load Smart Contract ABI from File

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-py

This example demonstrates the straightforward process of loading a Smart Contract Application Binary Interface (ABI) definition from a local JSON file using the `Abi.load()` method. This is useful for interacting with contracts when their ABI is provided as a file.

```python
from pathlib import Path
from multiversx_sdk.abi import Abi

abi = Abi.load(Path("./contracts/adder.abi.json"))
```

--------------------------------

### Verify mxpy CLI Installation

Source: https://docs.multiversx.com/developers/overview/validators/staking

Checks if the mxpy command-line tool is installed on your system and displays its current version. This command is a crucial prerequisite for performing staking operations directly via the CLI.

```Shell
mxpy --version

```

--------------------------------

### MultiversX Wallet Connect: Sign Message Example

Source: https://docs.multiversx.com/developers/overview/integrators/walletconnect-json-rpc-methods

Illustrates the JSON RPC request and result for the `mvx_signMessage` method. The example shows how to request a signature for a given message and MultiversX address, and the resulting signature.

```json
// Request
{
    "id": 1,
    "jsonrpc": "2.0",
    "method": "mvx_signMessage",
    "params": {
        "message": "food for cats",
        "address": "erd1uapegx64zk6yxa9kxd2ujskkykdnvzlla47uawh7sh0rhwx6y60sv68me9"
    }
}

// Result
{
    "id": 1,
    "jsonrpc": "2.0",
    "result": {
        "signature": "513fb2fa5ac39282ffc3aa90a89024b77057ac4542199673b05601302668bdda36c1076952f4c7445f4c6487a4263d51f72dff325012ab3f236594546ef54408"
    }
}
```

--------------------------------

### Configure MultiversX Localnet Directories

Source: https://docs.multiversx.com/developers/overview/developers/setup-local-testnet

Initializes and creates the necessary subfolders and file structures for the MultiversX localnet. This command sets up directories for proxy, seednode, and validator instances.

```bash
mxpy localnet config
```

--------------------------------

### Example MultiversX Contract Codehash File Content

Source: https://docs.multiversx.com/developers/overview/developers/reproducible-contract-builds

This snippet displays an example of the content found within a `*.codehash.txt` file, which is generated during the build process. This file contains the computed codehash of the smart contract, essential for verifying the contract's integrity and ensuring it matches a known version.

```text
adder.codehash.txt: 384b680df7a95ebceca02ffb3e760a2fc288dea1b802685ef15df22ae88ba15b
```

--------------------------------

### Start MultiversX Deep-history Squad Command

Source: https://docs.multiversx.com/developers/overview/integrators/deep-history-squad

This command is used to start both the deep-history squad and its associated proxy. It executes a shell script located in the user's home directory, which handles the initialization process. Users should ensure the script has executable permissions and is correctly configured.

```bash
~/mx-chain-scripts/script.sh start
```

--------------------------------

### Get CrossWindowProvider Singleton Instance

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-js/sdk-js-signing-providers

Shows how to acquire the singleton instance of the CrossWindowProvider, which facilitates interaction with the MultiversX Web Wallet via cross-window communication.

```typescript
import { CrossWindowProvider } from "@multiversx/sdk-web-wallet-cross-window-provider";

const provider = CrossWindowProvider.getInstance();
```

--------------------------------

### Fetch Smart Contract Results by Transaction Hash

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/indices/es-index-operations

This snippet shows how to query the MultiversX Elasticsearch operations index to find all smart contract results that were generated by a specific original transaction hash. It uses a `curl` command to send a GET request to the Elasticsearch `_search` endpoint, filtering by `originalTxHash` and `type` (specifically "unsigned").

```bash
curl --request GET \
  --url ${ES_URL}/operations/_search \
  --header 'Content-Type: application/json' \
  --data '{
	"query": {
		"bool": {
			"must": [
				{
					"match": {
						"originalTxHash": "d6.."
					}
				},
				{
					"match": {
						"type": "unsigned"
					}
				}
			]
		}
	}
}'
```

--------------------------------

### Create Default Devnet Entrypoint with MultiversX Python SDK

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-py

Demonstrates how to instantiate a default `DevnetEntrypoint` client, which provides easy access to common operations on the MultiversX Devnet using its standard API.

```Python
from multiversx_sdk import DevnetEntrypoint

entrypoint = DevnetEntrypoint()
```

--------------------------------

### Example Network Parameters

Source: https://docs.multiversx.com/developers/overview/economics/staking-providers-apr

Defines the key network-wide parameters used in the APR calculation example, including total supply, inflation rate, node counts, and various reward factors.

```Text
genesisTotalSupply = 20M EGLD
inflationRate = 9.7% (year 2)
p = 2M EGLD
totalNodes = 3200
eligibleCumulatedTopUp = 2.6M
totalCumulatedTopUp = 5.2M
protocolSustainabilityRewards = 10%
numDaysInAYear = 365
topUpFactor = 0.5
```

--------------------------------

### Install Python3 on Linux

Source: https://docs.multiversx.com/developers/overview/sovereign/software-dependencies

Command to install Python3, a core dependency for MultiversX Sovereign Chains, using the apt package manager on Linux systems.

```Bash
sudo apt install python3
```

--------------------------------

### Fetch Latest Operations of an Address

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/indices/es-index-operations

This snippet demonstrates how to query the MultiversX Elasticsearch operations index to retrieve the latest operations (transactions, smart contract calls) associated with a specific address. It uses a `curl` command to send a GET request to the Elasticsearch `_search` endpoint, filtering by `sender`, `receiver`, or `receivers` fields and sorting by timestamp in descending order.

```bash
ADDRESS="erd1..."

curl --request GET \
  --url ${ES_URL}/operations/_search \
  --header 'Content-Type: application/json' \
  --data '{
	"query": {
		"bool": {
			"should": [
				{
					"match": {
						"sender": "${ADDRESS}"
					}
				},
				{
					"match": {
						"receiver": "${ADDRESS}"
					}
				},
				{
					"match": {
						"receivers": "${ADDRESS}"
					}
				}
			]
		}
	},
	 "sort": [
        {
            "timestamp": {
                "order": "desc"
            }
        }
    ]
}'
```

--------------------------------

### Initialize CrossWindowProvider and Set Wallet URL

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-js/sdk-js-signing-providers

Explains the necessary steps to initialize the CrossWindowProvider and configure the MultiversX Web Wallet URL before performing any operations like login or signing.

```typescript
await provider.init();
provider.setWalletUrl("https://wallet.multiversx.com");
```

--------------------------------

### Deploy `adder` Smart Contract in Test Environment

Source: https://docs.multiversx.com/developers/overview/developers/testing/rust/sc-blackbox-example

Demonstrates how to deploy the `adder` smart contract within the testing framework. It uses a transaction builder pattern to specify the sender, contract proxy, initialization arguments, code path, and the expected new address, asserting the deployment success.

```Rust
    let new_address = world
        .tx()
        .from(OWNER_ADDRESS)
        .typed(adder_proxy::AdderProxy)
        .init(5u32)
        .code(CODE_PATH)
        .new_address(ADDER_ADDRESS)
        .returns(ReturnsNewAddress)
        .run();

    assert_eq!(new_address, ADDER_ADDRESS.to_address());

```

--------------------------------

### Install MultiversX SDK for Python

Source: https://docs.multiversx.com/developers/overview/sovereign/software-dependencies

Command to install the 'multiversx-sdk' Python package using pip, which is a required dependency for MultiversX Sovereign Chains.

```Bash
pip install multiversx-sdk
```

--------------------------------

### Get MetamaskProxyProvider Singleton Instance

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-js/sdk-js-signing-providers

Shows how to acquire the singleton instance of the MetamaskProxyProvider, which enables dApps to interact with Metamask via the MultiversX Web Wallet as an iframe proxy.

```typescript
import { MetamaskProxyProvider } from "@multiversx/sdk-metamask-proxy-provider";

const provider = MetamaskProxyProvider.getInstance();
```

--------------------------------

### Example MultiversX Transaction for Serialization

Source: https://docs.multiversx.com/developers/overview/developers/signing-transactions

An example of a MultiversX transaction object before serialization, showing various fields like nonce, value, receiver, sender, gasPrice, gasLimit, data, chainID, and version. This represents the initial state of a transaction.

```Generic
nonce = 7
value = "10000000000000000000"  # 10 EGLD
receiver = "erd1cux02zersde0l7hhklzhywcxk4u9n4py5tdxyx7vrvhnza2r4gmq4vw35r"
sender = "erd1l453hd0gt5gzdp7czpuall8ggt2dcv5zwmfdf3sd3lguxseux2fsmsgldz"
gasPrice = 1000000000
gasLimit = 70000
data = "for the book"
chainID = "1"
version = 1
```

--------------------------------

### Sign Arbitrary Messages with MultiversX SDK

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-js/sdk-js-signing-providers

This example illustrates how to sign an arbitrary message using the `SignableMessage` class from the MultiversX SDK. It shows how to create a message, sign it with a `provider`, and then log its JSON representation.

```JavaScript
import { SignableMessage } from "@multiversx/sdk-core";

const message = new SignableMessage({
    message: Buffer.from("hello")
});

await provider.signMessage(message);

console.log(message.toJSON());
```

--------------------------------

### MultiversX Example Unjail Single Validator Data Field Content

Source: https://docs.multiversx.com/developers/overview/validators/staking/unjailing

Provides a concrete example of the 'Data' field content for unjailing a single MultiversX validator. This illustrates how the 'unJail@' prefix is combined with an actual BLS public key. This example helps users understand the exact string format required for their transactions.

```Data Format
unJail@b617d8bc442bda59510f77e04a1680e8b2d3293c8c4083d94260db96a4d732deaaf9855fa0cef2273f5a67b4f442c725efc06a5d366b9f15a66da9eb8208a09c9ab4066b6b3d38c3cf1ea7fab6489a90713b3b56d87de68c6558c80d7533bf27
```

--------------------------------

### Install tmux on Linux

Source: https://docs.multiversx.com/developers/overview/sovereign/software-dependencies

Command to install tmux, a terminal multiplexer, which is recommended for managing multiple terminal sessions in Sovereign Chain deployments.

```Bash
sudo apt install tmux
```

--------------------------------

### Reference `adder` Contract Files

Source: https://docs.multiversx.com/developers/overview/developers/testing/rust/sc-blackbox-example

Imports the `adder` contract files, specifically to gain access to `adder_proxy.rs`, which is crucial for interacting with the contract within the testing environment.

```Rust
use adder::*;

```

--------------------------------

### Example MultiversX Token Role Assignment for TKN-001122

Source: https://docs.multiversx.com/developers/overview/bridge/whitelist-requirements

Provides a concrete example of the `RolesAssigningTransaction` for whitelisting the token `TKN-001122` on the Ethereum bridge. This example illustrates the specific hexadecimal values for the token identifier and the MINT/BURN roles, demonstrating how to apply the general structure.

```MultiversX Transaction Format
RolesAssigningTransaction {
    Sender: <address of the ESDT owner>
    Receiver: erd1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqzllls8a5w6u
    Value: 0
    GasLimit: 60000000
    Data: "setSpecialRole" +
          "@544b4e2d303031313232" +
          "@000000000000000005004ab1cd3d291159a38df7d2a1c498c9d7a7e3047ccc48" +
          "@45534454526f6c654c6f63616c4d696e74" +
          "@45534454526f6c654c6f63616c4275726e"
}
```

--------------------------------

### MultiversX Smart Contract Upgrade Event Structure and Example

Source: https://docs.multiversx.com/developers/overview/developers/event-logs/contract-deploy-events

Details the structure and provides a JSON example of the SCUpgrade event, generated when a transaction involving an upgrade to an existing smart contract is successfully executed.

```APIDOC
identifier: SCUpgrade
address: the address of the deployed contract
topics:
  topics[0]: the address bytes of the upgraded contract base64 encoded
  topics[1]: the address bytes of the upgrader of the smart contract base64 encoded
  topics[2]: the code hash bytes of the upgraded smart contract base64 encoded
data: empty
```

```JSON
{
    "address": "erd1qqqqqqqqqqqqqpgqnnl9nn0kuuckhg24g02hq2745n4jk2hp327qcay4nm",
    "identifier": "SCUpgrade",
    "topics": [
        "AAAAAAAAAAAFAJz+Wc325zFroVVD1XAr1aTrKyrhirw=",
        "NRl7AwoM3hEPC0t9RTDy7gdJUSJvKC5dpJwLYaHLirw=",
        "kUVJtdwvHG2sCTi9l2uneSONUVonWfgHCK69gdB+52o="
    ]
}
```

--------------------------------

### Example Staking Provider Parameters

Source: https://docs.multiversx.com/developers/overview/economics/staking-providers-apr

Specifies the parameters specific to a hypothetical staking provider used in the APR calculation example, such as node count, base and top-up stake amounts, and the fee percentage.

```Text
stakingProviderNumberOfNodes = 10
stakingProviderBaseStake = 25,000 EGLD
stakingProviderTopUpAmount = 6,472 EGLD
stakingProviderTotalStake = 31,472 EGLD
fee = 2%
```

--------------------------------

### Rust: Full Crowdfunding Smart Contract Structure

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/crowdfunding-p1

This comprehensive Rust code block presents the complete structure of a MultiversX Crowdfunding smart contract. It includes the `init` method for setting the target, an `upgrade` method, and a `view` method for accessing the stored target, demonstrating essential contract components and attributes.

```Rust
#!no_std]

#[allow(unused_imports)]
use multiversx_sc::imports::*;

#[multiversx_sc::contract]
pub trait Crowdfunding {
    #[init]
    fn init(&self, target: BigUint) {
        self.target().set(&target);
    }

    #[upgrade]
    fn upgrade() {}

    #[view]
    #[storage_mapper("target")]
    fn target(&self) -> SingleValueMapper<BigUint>;

}
```

--------------------------------

### Stop and Clean Local Sovereign Chain

Source: https://docs.multiversx.com/developers/overview/sovereign/local-setup

Executes a command to halt all running sovereign services and remove the local Sovereign Chain environment, preparing it for a fresh setup or complete shutdown.

```bash
stopAndCleanSovereign
```

--------------------------------

### MultiversX Smart Contract Build and Proxy Generation Commands

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/staking-contract

These shell commands are used to compile the MultiversX smart contract and generate the necessary proxy interfaces. `sc-meta all build` compiles the contract, and `sc-meta all proxy` creates the proxy files for interaction.

```Shell
sc-meta all build
sc-meta all proxy
```

--------------------------------

### Example Data Field for Unjailing Two Nodes

Source: https://docs.multiversx.com/developers/overview/validators/staking/unjailing

This example demonstrates a concrete 'Data' field string for unjailing two MultiversX validator nodes, using actual (example) BLS public keys. This string would be used in a transaction to initiate the unjailing process for the specified nodes.

```Text
unJail@b617d8bc442bda59510f77e04a1680e8b2d3293c8c4083d94260db96a4d732deaaf9855fa0cef2273f5a67b4f442c725efc06a5d366b9f15a66da9eb8208a09c9ab4066b6b3d38c3cf1ea7fab6489a90713b3b56d87de68c6558c80d7533bf27@f921a0f76ed70e8a806c6f9119f87b12700f96f732e6070b675e0aec10cb0723803202a4c40194847c38195db07b1001f6d50c81a82b949e438cd6dd945c2eb99b32c79465aefb9144c8668af67e2d01f71b81842d9b94e4543a12616cb5897d
```

--------------------------------

### Delegate Funds to Contract using DelegationController (Python)

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-py

Demonstrates the initial steps for delegating funds to an existing delegation contract using the `DelegationController`. It sets up the controller and loads the delegating account, preparing for the delegation transaction.

```Python
from pathlib import Path
from multiversx_sdk import Account, Address, DevnetEntrypoint

# create the entrypoint and the delegation controller
entrypoint = DevnetEntrypoint()
controller = entrypoint.create_delegation_controller()

# create the account delegating funds
alice = Account.new_from_pem(Path("../multiversx_sdk/testutils/testwallets/alice.pem"))

# fetch the nonce of the network
alice.nonce = entrypoint.recall_account_nonce(alice.address)
```

--------------------------------

### MultiversX mvx_signTransactions API JSON-RPC Example

Source: https://docs.multiversx.com/developers/overview/integrators/walletconnect-json-rpc-methods

A complete JSON-RPC example demonstrating how to call the `mvx_signTransactions` method to sign multiple transactions. It includes the request payload with two transaction objects and the corresponding successful response containing their generated signatures.

```JSON
// Request
{
    "id": 1,
    "jsonrpc": "2.0",
    "method": "mvx_signTransactions",
    "params": {
        "transactions": [
            {
                "nonce": 42,
                "value": "100000000000000000",
                "receiver": "erd1cux02zersde0l7hhklzhywcxk4u9n4py5tdxyx7vrvhnza2r4gmq4vw35r",
                "sender": "erd1uapegx64zk6yxa9kxd2ujskkykdnvzlla47uawh7sh0rhwx6y60sv68me9",
                "gasPrice": 1000000000,
                "gasLimit": 70000,
                "data": "Zm9vZCBmb3IgY2F0cw==", // base64 representation of "food for cats"
                "chainID": "1",
                "version": 1
            },
            {
                "nonce": 43,
                "value": "300000000000000000",
                "receiver": "erd1ylzm22ngxl2tspgvwm0yth2myr6dx9avtx83zpxpu7rhxw4qltzs9tmjm9",
                "sender": "erd1uapegx64zk6yxa9kxd2ujskkykdnvzlla47uawh7sh0rhwx6y60sv68me9",
                "gasPrice": 1000000000,
                "gasLimit": 70000,
                "data": "Zm9vZCBmb3IgZG9ncw==", // base64 representation of "food for dogs"
                "chainID": "1",
                "version": 1
            }
        ]
    }
}

// Result
{
    "id": 1,
    "jsonrpc": "2.0",
    "result": {
        "signatures": [
            {
                "signature": "1aa6cdd9f614e2a1cedcc207e6e7c574674c9b05e98f31035cac89fcca2673ca9273c48823418cf44696f64a2c535ab3784f680a0c6d6e84b960c33e586cb30b"
            },
            {
                "signature": "43127c0ac3d5b124ced9c15e884940fb3c1256c463a74db33c1842fa323971e1f43725eea62225c6b2f9b2634edf68ad2e315241df734d60c41b920dec85b60a"
            }
        ]
    }
}
```

--------------------------------

### Example: Multi-ESDT/NFT Transfer with Method Call

Source: https://docs.multiversx.com/developers/overview/tokens/fungible-tokens

Illustrates a concrete example of the `MultiTokensTransferWithCallTransaction` structure. This example demonstrates transferring two different tokens (ALC-6258d2 and SFT-1q4r8i) to a smart contract and calling its 'transfer' method with a specific address as an argument, showcasing the hexadecimal encoding of all data fields.

```APIDOC
MultiTokensTransferWithCallTransaction {
    Sender: erd1sg4u62lzvgkeu4grnlwn7h2s92rqf8a64z48pl9c7us37ajv9u8qj9w8xg
    Receiver: erd1sg4u62lzvgkeu4grnlwn7h2s92rqf8a64z48pl9c7us37ajv9u8qj9w8xg
    Value: 0
    GasLimit: 8_200_000
    Data: "MultiESDTNFTTransfer" +
          "@0000000000000000050032a3dc7511d6062c6a3b90ac02d8c3f474ef71c65008" + // smart contract address: erd1qqqqqqqqqqqqqpgqx23acag36crzc63mjzkq9kxr736w7uwx2qyqcmq7ar
          "@02" +  // 2 tokens to transfer
          "@414c432d363235386432" +   // ALC-6258d2
          "@00" +  // 0 -> the nonce is 0 for regular ESDT tokens
          "@0c" +  // 12 -> value to transfer
          "@5346542d317134723869" +  // SFT-1q4r8i
          "@01" +  // 1 -> the nonce of the SFT
          "@03" +  // 3 -> the quantity to transfer
          "@7472616e73666572" + // method name is 'transfer'
          "@f69adc800dca9e3ba3328d17ded25f3a8f328aa1e0e8a347f34ce5ea3aac5008" // there is one argument, the address: 'erd176ddeqqde20rhgej35taa5jl828n9z4pur52x3lnfnj75w4v2qyqa230vx'
}
```

--------------------------------

### Start MultiversX Metachain Observer Node

Source: https://docs.multiversx.com/developers/overview/validators/node-cli

This command initializes a MultiversX node as an observer for the Metachain. It configures the REST API interface to 'localhost:8080', enables log viewing and saving, sets the log level to DEBUG for all components, and specifies the validator key file 'observerMetachain.pem'. The node will start in the current epoch.

```Shell
./node --rest-api-interface=localhost:8080 \
 --use-log-view --log-save --log-level=*:DEBUG --log-logger-name \
 --destination-shard-as-observer=metachain --start-in-epoch\
 --validator-key-pem-file=observerMetachain.pem
```

--------------------------------

### Import Hooks from SDK-dapp Main Hooks Module

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-dapp

Example of importing multiple hooks, such as `useExtensionLogin` and `useGetAccountInfo`, from the main `@multiversx/sdk-dapp/hooks` module. This is a common way to import frequently used hooks.

```javascript
import {
  useExtensionLogin,
  useGetAccountInfo,
} from "@multiversx/sdk-dapp/hooks";
```

--------------------------------

### Example MultiversX Staking Command for Two Nodes

Source: https://docs.multiversx.com/developers/overview/validators/staking

This example demonstrates the `mxpy` staking command for two validator nodes. The `value` parameter is adjusted to `5000000000000000000000` (5000 EGLD) to reflect the increased stake for two nodes.

```Shell
mxpy --verbose validator stake --pem=walletKey.pem --value="5000000000000000000000" --validators-file=my-validators.json --proxy=https://gateway.multiversx.com --estimate-gas --recall-nonce
```

--------------------------------

### Import `multiversx_sc_scenario` for Integration Tests

Source: https://docs.multiversx.com/developers/overview/developers/testing/rust/sc-blackbox-example

Imports all necessary tools, data types, and methods from the `multiversx_sc_scenario` crate, which is essential for writing comprehensive integration tests for MultiversX smart contracts.

```Rust
use multiversx_sc_scenario::imports::*;

```

--------------------------------

### Upgrade MultiversX mxpy CLI with pipx

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/mxpy/installing-mxpy

This command utilizes pipx to upgrade the 'multiversx-sdk-cli' package to its latest available version. Running this command ensures that your mxpy installation is up-to-date with the newest features, improvements, and bug fixes.

```shell
pipx upgrade multiversx-sdk-cli
```

--------------------------------

### Generate Interactor Code Snippets

Source: https://docs.multiversx.com/developers/overview/developers/meta/interactor/interactors-example

Executing this command in the root directory of the `adder` contract generates the necessary interactor code. It creates a new `interactor` project and updates the `sc-config.toml` file with the new proxy path.

```Shell
sc-meta all snippets
```

--------------------------------

### Execute MultiversX Smart Contract Proxy Generation Command

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/crowdfunding-p1

The terminal command `sc-meta all proxy` used to trigger the generation of the Rust proxy for a MultiversX smart contract, based on the `sc-config.toml` configuration.

```Shell
sc-meta all proxy
```

--------------------------------

### Instantiate MultiversX Transaction Controllers and Factories

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-js/sdk-js-cookbook

Describes two methods for creating transaction controllers and factories in the MultiversX SDK: obtaining them from an `Entrypoint` or instantiating them manually. Controllers are suitable for quick scripts, while factories offer a more granular, lower-level approach for DApps.

```javascript
{
    const entrypoint = new DevnetEntrypoint();

    // getting the controller and the factory from the entrypoint
    const transfersController = entrypoint.createTransfersController();
    const transfersFactory = entrypoint.createTransfersTransactionsFactory();

    // manually instantiating the controller and the factory
    const controller = new TransfersController({ chainID: "D" });

    const config = new TransactionsFactoryConfig({ chainID: "D" });
    const factory = new TransferTransactionsFactory({ config });
}
```

--------------------------------

### APIDOC: get Function for Mappers

Source: https://docs.multiversx.com/developers/overview/developers/developer-reference/storage-mappers

Describes the `get` function, which retrieves a value at a specified index. If the entry is empty, the index itself is returned, adhering to the mapper's property.

```APIDOC
fn get(index: usize) -> usize
```

--------------------------------

### Build MultiversX Ping-Pong Smart Contract

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/your-first-dapp

Navigates into the smart contract's source directory and compiles the Rust source code into a WebAssembly (WASM) binary. The resulting WASM file, located at `output/ping-pong.wasm`, contains the bytecode ready for deployment on the MultiversX blockchain.

```bash
cd contract/ping-pong
sc-meta all build
```

--------------------------------

### Delegate Funds to Contract Using Factory

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-js/sdk-js-cookbook

This example demonstrates delegating funds to an existing delegation contract using the `DelegationTransactionsFactory`. It outlines the steps for loading an account, specifying the target contract and delegation amount, manually constructing and signing the transaction, and finally sending it to the network.

```javascript
{
    // create the entrypoint and the delegation factory
    const entrypoint = new DevnetEntrypoint();
    const factory = entrypoint.createDelegationTransactionsFactory();

    const filePath = path.join("../src", "testdata", "testwallets", "alice.pem");
    const alice = await Account.newFromPem(filePath);

    const contract = Address.newFromBech32("erd1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqf8llllswuedva");

    const transaction = await factory.createTransactionForDelegating(alice.address, {
        delegationContract: contract,
        amount: 5000000000000000000000n,
    });
    // fetch the nonce of the network
    alice.nonce = await entrypoint.recallAccountNonce(alice.address);

    // set the nonce
    transaction.nonce = alice.getNonceThenIncrement();

    // sign the transaction
    transaction.signature = await alice.signTransaction(transaction);

    // sending the transaction
    const txHash = await entrypoint.sendTransaction(transaction);
}
```

--------------------------------

### Checking mxpy Dependency Installation Status

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/mxpy/mxpy-cli

Illustrates the command used to verify if a specific dependency is already installed within the `mxpy` environment. The dependency name is provided as a required positional argument.

```Shell
mxpy deps check <dependency-name>
```

--------------------------------

### Execute full_scenario CLI Command and Observe Output

Source: https://docs.multiversx.com/developers/overview/developers/meta/interactor/interactors-example

This snippet shows the console output when executing the `full` command via `cargo run`. It demonstrates the compilation process, the execution of the `full_scenario`, and the resulting transaction hashes and contract addresses for deployment and subsequent calls, along with the final `Result`.

```Shell
interactor % cargo run full
   Compiling rust-interact v0.0.0 (/Users/calin/Documents/work/MultiversX/adder/interactor)
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 1.69s
     Running `/Users/calin/Documents/work/MultiversX/adder/target/debug/rust-interact full`
sender's recalled nonce: 1427
-- tx nonce: 1427
sc deploy tx hash: bf5122ea02e48d02f1107d494ceb3e75097d8ffd12ed050a0f3074ec5293c573
deploy address: erd1qqqqqqqqqqqqqpgqmauhsqd6zr7kt8pg80qhph2tw0ejed3pd8sszl98x7
new address: erd1qqqqqqqqqqqqqpgqmauhsqd6zr7kt8pg80qhph2tw0ejed3pd8sszl98x7
sender's recalled nonce: 1428
-- tx nonce: 1428
sc call tx hash: 7f5ca4106aa0101e0712d8a582609bcfd6db80b299dae26ac25ae5a77995afbe
Result: ()
Result: 3
```

--------------------------------

### Initialize MultiversX Web Wallet Provider for Devnet

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-js/sdk-js-signing-providers

This JavaScript code demonstrates how to create an instance of the `WalletProvider` for the MultiversX Web Wallet. It imports the necessary `WalletProvider` class and `WALLET_PROVIDER_DEVNET` constant from the `@multiversx/sdk-web-wallet-provider` package to configure the provider for the Devnet environment.

```JavaScript
import { WalletProvider, WALLET_PROVIDER_DEVNET } from "@multiversx/sdk-web-wallet-provider";

const provider = new WalletProvider(WALLET_PROVIDER_DEVNET);
```

--------------------------------

### Build MultiversX Smart Contract

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/interactors-guide

This shell command navigates into the `my-contract` directory and uses `sc-meta all build` to compile the MultiversX smart contract. This process generates essential files like `my-contract.wasm` and `my-contract.mxsc.json` in the `output` folder, which are required for deployment and testing.

```Shell
cd my-contract
sc-meta all build
```

--------------------------------

### Example MultiversX Validator Key PEM Format

Source: https://docs.multiversx.com/developers/overview/validators/key-management/validator-keys

An example of the content found within a `validatorKey.pem` file, illustrating the standard PEM (Privacy-Enhanced Mail) block structure. It shows the BEGIN/END markers, the embedded public key, and the base64-encoded private key.

```plaintext
-----BEGIN PRIVATE KEY for *45e7131ba37e05c5de3f8862b4d8294812f004a5b660abb793e89b65816dbff2b02f54c25f139359c9c98be0fa657d0bf1ae4115dcf6fdbf5f3a470f1d251f769610b48fe34eeab59e82ac1cc0336d1d9109a14b768b97ccb4db4c2431629688*-----

**YmRiNmViOGYzMmQ3OWY0YjE4ODJjMzE1ODA4YjQyZmZjODhiZDQxNzMwNmE5MTRiZjQ4OTAyNjM0MTcyNjMzMw==**

-----END PRIVATE KEY for *45e7131ba37e05c5de3f8862b4d8294812f004a5b660abb793e89b65816dbff2b02f54c25f139359c9c98be0fa657d0bf1ae4115dcf6fdbf5f3a470f1d251f769610b48fe34eeab59e82ac1cc0336d1d9109a14b768b97ccb4db4c2431629688*-----
```

--------------------------------

### Example Instance of a Custom Rust Struct

Source: https://docs.multiversx.com/developers/overview/developers/data/custom-types

Provides a concrete example of an instantiated `Struct` with specific values. This demonstrates the data structure that will be serialized and subsequently encoded for contract interaction.

```Rust
Struct {
		int: 0x42,
		seq: vec![0x1, 0x2, 0x3, 0x4, 0x5],
		another_byte: 0x6,
		uint_32: 0x12345,
		uint_64: 0x123456789,
}
```

--------------------------------

### Deploy Multisig Smart Contract with MultiversX Controller (Python)

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-py

This snippet demonstrates how to deploy a Multisig smart contract on the MultiversX blockchain using the `MultisigController` class from the Python SDK. It covers account setup, ABI loading, transaction creation for deployment, signing, and sending the transaction to the network.

```Python
from pathlib import Path
from multiversx_sdk import Account, Address, ApiNetworkProvider, MultisigController
from multiversx_sdk.abi import Abi

alice = Account.new_from_pem(Path("../multiversx_sdk/testutils/testwallets/alice.pem"))
api = ApiNetworkProvider(url="https://devnet-api.multiversx.com")
alice.nonce = api.get_account(alice.address).nonce

abi = Abi.load(Path("../multiversx_sdk/testutils/testdata/multisig-full.abi.json"))
controller = MultisigController(chain_id="D", network_provider=api, abi=abi)

transaction = controller.create_transaction_for_deploy(
    sender=alice,
    nonce=alice.get_nonce_then_increment(),
    bytecode=Path("../multiversx_sdk/testutils/testdata/multisig-full.wasm"),
    quorum=2,
    board=[alice.address, Address.new_from_bech32("erd1spyavw0956vq68xj8y4tenjpq2wd5a9p2c6j8gsz7ztyrnpxrruqzu66jx")],
    gas_limit=100_000_000,
)

transaction.signature = alice.sign_transaction(transaction)
tx_hash = api.send_transaction(transaction)

```

--------------------------------

### Example MultiversX Transaction with Empty Data Field

Source: https://docs.multiversx.com/developers/overview/developers/signing-transactions

An example of a MultiversX transaction object where the 'data' field is empty. This demonstrates how the serialization process handles the absence of a data payload.

```Generic
nonce = 8
value = "10000000000000000000"  # 10 ERD
receiver = "erd1cux02zersde0l7hhklzhywcxk4u9n4py5tdxyx7vrvhnza2r4gmq4vw35r"
sender = "erd1l453hd0gt5gzdp7czpuall8ggt2dcv5zwmfdf3sd3lguxseux2fsmsgldz"
gasPrice = 1000000000
gasLimit = 50000
data = ""
chainID = "1"
version = 1
```

--------------------------------

### Install Yarn via npm

Source: https://docs.multiversx.com/developers/overview/sovereign/services

This command installs the Yarn package manager globally on your system using Node Package Manager (npm). Yarn is a crucial dependency for managing project packages within the MultiversX ecosystem.

```Shell
npm install --global yarn
```

--------------------------------

### Run All MultiversX Smart Contract Tests

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/staking-contract

This command executes all tests defined within the current MultiversX smart contract project directory, typically `staking-contract/`. It's a convenient way to validate the entire test suite.

```Shell
sc-meta test

```

--------------------------------

### Public Gateway Deep History Availability Example

Source: https://docs.multiversx.com/developers/overview/integrators/deep-history-squad

Provides a concrete example of deep history availability for the public MultiversX Gateway, detailing the accessible epochs relative to the current epoch, considering the default 'NumEpochsToKeep' value.

```text
...                 deep history not available
CurrentEpoch - 5:   deep history not available
CurrentEpoch - 4    deep history not available
CurrentEpoch - 3:   deep history partially available
CurrentEpoch - 2:   deep history available
CurrentEpoch - 1:   deep history available
CurrentEpoch:       deep history available
```

--------------------------------

### Rust Scenario Runner Setup for MultiversX Multi-Contract Testing

Source: https://docs.multiversx.com/developers/overview/developers/meta/sc-config

This Rust function, `world()`, demonstrates the setup for a `ScenarioWorld` in the MultiversX Rust scenario runner. It shows how to register both single contracts and multi-contract outputs using `register_contract` and `register_partial_contract`, providing ABI providers and contract builders to simulate on-chain behavior for complex contract configurations.

```Rust
fn world() -> ScenarioWorld {
    // Initialize the blockchain mock, the same as for a regular test.
    let mut blockchain = ScenarioWorld::new();

    // Contracts that have no multi-contract config are provided the same as before.
    blockchain.register_contract("file:test-contracts/adder.wasm", adder::ContractBuilder);

    // For multi-contract outputs we need to provide:
    // - the ABI, via the generated AbiProvider type
    // - a scenario expression to bind to, same as for simple contracts
    // - a contract builder, same as for simple contracts
    // - the contract name, as specified in multicontract.toml
    blockchain.register_partial_contract::<multisig::AbiProvider, _>(
        "file:output/multisig.wasm",
        multisig::ContractBuilder,
        "multisig",
    );

    // The same goes for the external view contract.
    // There is no need to specify here that it is an external view,
    // the framework gets all the data from multicontract.toml.
    blockchain.register_partial_contract::<multisig::AbiProvider, _>(
        "file:output/multisig-view.wasm",
        multisig::ContractBuilder,
        "multisig-view",
    );

    blockchain
}
```

--------------------------------

### Deploy Sovereign Chain with Cross-Chain Contracts

Source: https://docs.multiversx.com/developers/overview/sovereign/local-setup

Initiates the deployment of all main chain smart contracts, updates sovereign configurations, and deploys sovereign nodes along with the main chain observer. The 'sov' argument sets the prefix for ESDT tokens within the sovereign chain.

```bash
deploySovereignWithCrossChainContracts sov
```

--------------------------------

### Example MultiversX Staking Command for One Node

Source: https://docs.multiversx.com/developers/overview/validators/staking

A concrete example of the `mxpy` staking command for a single validator node. The `value` parameter is set to `2500000000000000000000` (2500 EGLD, considering denomination) and `my-validators.json` is used as the validator file.

```Shell
mxpy --verbose validator stake --pem=walletKey.pem --value="2500000000000000000000" --validators-file=my-validators.json --proxy=https://gateway.multiversx.com --estimate-gas --recall-nonce
```

--------------------------------

### Generate MultiversX Validator Key with Existing Node Installation

Source: https://docs.multiversx.com/developers/overview/validators/key-management/validator-keys

This snippet provides an alternative method for generating a validator key, assuming a MultiversX node is already installed on the host and the `keygenerator` tool is accessible within the `elrond-utils` directory.

```Shell
cd ~/elrond-utils/
./keygenerator --key-type validator
```

--------------------------------

### Blackbox Test Example for Contract Deployment

Source: https://docs.multiversx.com/developers/overview/developers/transactions/tx-data

Provides a comprehensive example of a blackbox test function for contract deployment. It demonstrates chaining `raw_deploy`, `argument`, `code`, and `new_address` to simulate a full deployment scenario within a testing environment.

```MultiversX
fn deploy(&mut self) {
    self.world
        .tx()
        .from(OWNER_ADDRESS)
        .raw_deploy()
        .argument(5u32)
        .code(CODE_PATH)
        .new_address(ADDER_ADDRESS)
        .run();
}
```

--------------------------------

### Integrate LedgerLoginContainer for Hardware Wallet Login

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-dapp

Example of using `LedgerLoginContainer` for integrating Ledger hardware wallet login. It provides essential props such as `callbackRoute`, `className`, `wrapContentInsideModal`, and `onClose` to manage the login process and modal behavior.

```React
<LedgerLoginContainer
  callbackRoute={callbackRoute}
  className="ledger-login-modal"
  wrapContentInsideModal={wrapContentInsideModal}
  redirectAfterLogin={redirectAfterLogin}
  token={token}
  onClose={onClose}
  onLoginRedirect={onLoginRedirect}
/>
```

--------------------------------

### Start MultiversX Observer Node in Shard 0

Source: https://docs.multiversx.com/developers/overview/validators/node-cli

This command initializes a MultiversX node as an observer for Shard 0. It configures the REST API interface to 'localhost:8080', enables log saving, sets the log level to DEBUG for all components, and specifies the validator key file 'observer0.pem'. The node will start in the current epoch.

```Shell
./node --rest-api-interface=localhost:8080 \
 --log-save --log-level=*:DEBUG --log-logger-name \
 --destination-shard-as-observer=0 --start-in-epoch\
 --validator-key-pem-file=observer0.pem
```

--------------------------------

### Example MultiversX Gateway API Response for Proposal Query

Source: https://docs.multiversx.com/developers/overview/governance/governance-interaction

An illustrative example of the JSON response received from the MultiversX `vm-values/query` API, showing decoded values for each base64-encoded field within the `returnData` array, providing a concrete instance of a proposal's status.

```JSON
{
  "returnData": [
    "NjXJrcXeoAAA",
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABg==",
    "AQ==",
    "aj88GtqHy9ibm5ePPQlG4aqLhpgqsQWygoTppckLa4M=",
    "bQ==",
    "bg==",
    "ntGU2xmyOMAAAA==",
    "",
    "",
    "ntGU2xmyOMAAAA==",
    "",
    "dHJ1ZQ==",
    "ZmFsc2U="
  ]
}
```

--------------------------------

### Load Account for Native Token Transfers with MultiversX Controller

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-py

Demonstrates how to load an account from a keystore file using `Account.new_from_keystore` to prepare for signing and performing native token (EGLD) transfers via a MultiversX controller.

```Python
from pathlib import Path
from multiversx_sdk import Account, DevnetEntrypoint

entrypoint = DevnetEntrypoint()

account = Account.new_from_keystore(
    file_path=Path("../multiversx_sdk/testutils/testwallets/withDummyMnemonic.json"),
    password="password",
    address_index=0
)
```

--------------------------------

### Basic Usage of ExtensionLoginButton

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-dapp

Example of using the `ExtensionLoginButton` component for simple login integration. It accepts `callbackRoute` for post-login redirection, `buttonClassName` for styling, and `loginButtonText` for display.

```React
<ExtensionLoginButton
  callbackRoute="/dashboard"
  buttonClassName="extension-login"
  loginButtonText="Extension login"
/>
```

--------------------------------

### Archive and Backup Validator Key

Source: https://docs.multiversx.com/developers/overview/validators/nodes-scripts/install-update

This snippet first zips the `validatorKey.pem` file, creating an archive (e.g., `node-0.zip`), and then moves this zipped backup to the designated `VALIDATOR_KEYS` folder. This ensures a secure and organized backup of the critical validator key for future use, especially during node upgrades.

```Bash
zip node-0.zip validatorKey.pem
mv node-0.zip $HOME/VALIDATOR_KEYS/
```

--------------------------------

### Example Calculation of gasToLockForCallback for MultiversX

Source: https://docs.multiversx.com/developers/overview/developers/gas-and-fees/user-defined-smart-contracts

This snippet provides a concrete example of calculating `gasToLockForCallback` based on specific cost values (as of February 2022) and a contract size of 453 bytes. It demonstrates the application of the gas lock formula with numerical values.

```text
gasToLockForCallback = 100000 + 4000000 + 100 * 453 = 4145300
```

--------------------------------

### Example JSON Response for Delegation Contract View Function Query

Source: https://docs.multiversx.com/developers/overview/validators/delegation-manager

An example of a successful JSON response returned when querying the delegation contract's view functions via the '/vm-values/query' endpoint. It shows the structure of the 'returnData' field and other status indicators for a successful query.

```JSON
{
  "data": {
    "data": {
      "returnData": [],
      "returnCode": "ok",
      "returnMessage": "",
      "gasRemaining": 0,
      "gasRefund": 0,
      "outputAccounts": null,
      "deletedAccounts": null,
      "touchedAccounts": null,
      "logs": []
    }
  },
  "error": "",
  "code": "successful"
}
```

--------------------------------

### MultiversX Smart Contract Cargo.toml Configuration

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/crowdfunding-p1

Configuration file for a Rust-based MultiversX smart contract project, defining package metadata, library path, dependencies (including MultiversX-specific crates), and workspace settings. This file is crucial for project compilation and dependency management.

```toml
[package]
name = "crowdfunding"
version = "0.0.0"
publish = false
edition = "2021"
authors = ["you"]

[lib]
path = "src/crowdfunding.rs"

[dependencies.multiversx-sc]
version = "0.57.0"

[dev-dependencies]
num-bigint = "0.4"

[dev-dependencies.multiversx-sc-scenario]
version = "0.57.0"

[workspace]
members = [
    ".",
    "meta",
]
```

--------------------------------

### Initialize MultiversX Localnet Workspace

Source: https://docs.multiversx.com/developers/overview/developers/setup-local-testnet

This command sequence creates a new directory for a MultiversX localnet instance and initializes a new localnet workspace within it. This is a foundational step before configuring the localnet for specific purposes like sharding or building from local source.

```bash
mkdir -p ~/my-multiversx-localnet && cd ~/my-multiversx-localnet
mxpy localnet new
```

--------------------------------

### Minimal MultiversX Smart Contract ABI Structure Example

Source: https://docs.multiversx.com/developers/overview/developers/data/abi

An example of a minimal MultiversX Smart Contract ABI (Application Binary Interface) structure, detailing its build information, documentation, contract name, constructor, and endpoint definitions. This JSON representation provides a blueprint for how smart contract interfaces are described.

```JSON
{
    "buildInfo": {
        "rustc": {
            "version": "1.71.0-nightly",
            "commitHash": "a2b1646c597329d0a25efa3889b66650f65de1de",
            "commitDate": "2023-05-25",
            "channel": "Nightly",
            "short": "rustc 1.71.0-nightly (a2b1646c5 2023-05-25)"
        },
        "contractCrate": {
            "name": "adder",
            "version": "0.0.0",
            "gitVersion": "v0.43.2-5-gfe62c37d2"
        },
        "framework": {
            "name": "multiversx-sc",
            "version": "0.43.2"
        }
    },
    "docs": [
        "One of the simplest smart contracts possible,",
        "it holds a single variable in storage, which anyone can increment."
    ],
    "name": "Adder",
    "constructor": {
        "inputs": [
            {
                "name": "initial_value",
                "type": "BigUint"
            }
        ],
        "outputs": []
    },
    "endpoints": [
        {
            "name": "getSum",
            "mutability": "readonly",
            "inputs": [],
            "outputs": [
                {
                    "type": "BigUint"
                }
            ]
        },
        {
            "docs": [
                "Add desired amount to the storage variable."
            ],
            "name": "add",
            "mutability": "mutable",
            "inputs": [
                {
                    "name": "value",
                    "type": "BigUint"
                }
            ],
            "outputs": []
        }
    ],
    "events": [],
    "esdtAttributes": [],
    "hasCallback": false,
    "types": {}
}
```

--------------------------------

### Configure Owner Account with Initial Nonce

Source: https://docs.multiversx.com/developers/overview/developers/testing/rust/sc-blackbox-example

Initializes a `SetStateBuilder` which helps set the owner account at a custom address (`OWNER_ADDRESS`) and assigns it a nonce of 1, making it ready for sending transactions within the test environment.

```Rust
    world.account(OWNER_ADDRESS).nonce(1);

```

--------------------------------

### MultiversX Smart Contract: Example with ESDT Attribute

Source: https://docs.multiversx.com/developers/overview/developers/meta/sc-meta-cli

A simple Rust smart contract example demonstrating the use of `#[multiversx_sc::contract]` and `#[esdt_attribute]` to define a contract with an ESDT attribute, which influences ABI generation.

```Rust
#[multiversx_sc::contract]
#[esdt_attribute("myTicker", u64)]
pub trait SomeContract {
    #[init]
    fn init(&self) {}
}

```

--------------------------------

### Rust Blackbox Testing Example for MultiversX Smart Contracts

Source: https://docs.multiversx.com/developers/overview/developers/testing/rust/sc-blackbox-example

This Rust code snippet illustrates a blackbox test for a MultiversX smart contract. It sets up a `ScenarioWorld` blockchain environment, registers an 'adder' contract, initializes it with a value, performs an 'add' transaction, and then queries the contract's state to assert the sum. It also checks account balances and contract storage, and writes a scenario trace.

```Rust
use multiversx_sc_scenario::imports::*;

use adder::*;

const OWNER_ADDRESS: TestAddress = TestAddress::new("owner");
const ADDER_ADDRESS: TestSCAddress = TestSCAddress::new("adder");
const CODE_PATH: MxscPath = MxscPath::new("output/adder.mxsc.json");

fn world() -> ScenarioWorld {
    let mut blockchain = ScenarioWorld::new();
    blockchain.register_contract(CODE_PATH, adder::ContractBuilder);
    blockchain
}

#[test]
fn adder_blackbox() {
    let mut world = world();

    world.start_trace();

    world.account(OWNER_ADDRESS).nonce(1);

    let new_address = world
        .tx()
        .from(OWNER_ADDRESS)
        .typed(adder_proxy::AdderProxy)
        .init(5u32)
        .code(CODE_PATH)
        .new_address(ADDER_ADDRESS)
        .returns(ReturnsNewAddress)
        .run();

    assert_eq!(new_address, ADDER_ADDRESS.to_address());

    world
        .query()
        .to(ADDER_ADDRESS)
        .typed(adder_proxy::AdderProxy)
        .sum()
        .returns(ExpectValue(5u32))
        .run();

    world
        .tx()
        .from(OWNER_ADDRESS)
        .to(ADDER_ADDRESS)
        .typed(adder_proxy::AdderProxy)
        .add(1u32)
        .run();

    world
        .query()
        .to(ADDER_ADDRESS)
        .typed(adder_proxy::AdderProxy)
        .sum()
        .returns(ExpectValue(6u32))
        .run();

    world.check_account(OWNER_ADDRESS);

    world
        .check_account(ADDER_ADDRESS)
        .check_storage("str:sum", "6");

    world.write_scenario_trace("trace1.scen.json");
}
```

--------------------------------

### Initial MultiversX Rust Smart Contract Template

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/crowdfunding-p1

This Rust code snippet defines the foundational structure for a MultiversX smart contract. It includes essential attributes like `no_std` for a lean binary, necessary `multiversx_sc` imports, and the `#[init]` and `#[upgrade]` functions, which serve as the contract's constructor and upgrade entry points, respectively. It's designed as a minimal template for new contract development.

```Rust
#![no_std]                      //  [1]

use multiversx_sc::imports::*;  //  [2]
#[allow(unused_imports)]        //  [3]

/// An empty contract. To be used as a template when starting a new contract from scratch.
#[multiversx_sc::contract]      //  [4]
pub trait Crowdfunding {        //  [5]
    #[init]                     //  [6]
    fn init(&self) {}           //  [7]

    #[upgrade]                  //  [8]
    fn upgrade(&self) {}        //  [9]
}
```

--------------------------------

### Activate Guardian with Controller (MultiversX)

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-js/sdk-js-cookbook

This example illustrates the process of activating a previously set guardian for a MultiversX account using the `AccountController`. It involves initializing the controller, loading the account, fetching and incrementing the nonce, creating the activation transaction, and sending it to the network.

```javascript
{
    // create the entrypoint and the account controller
    const entrypoint = new DevnetEntrypoint();
    const controller = entrypoint.createAccountController();

    // create the account to guard
    const filePath = path.join("../src", "testdata", "testwallets", "alice.pem");
    const alice = await Account.newFromPem(filePath);

    // fetch the nonce of the network
    alice.nonce = await entrypoint.recallAccountNonce(alice.address);

    const transaction = await controller.createTransactionForGuardingAccount(
        alice,
        alice.getNonceThenIncrement(),
        {},
    );

    // sending the transaction
    const txHash = await entrypoint.sendTransaction(transaction);
}
```

--------------------------------

### Generate PEM Wallet for MultiversX Testing

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/your-first-dapp

Creates a 'wallet' subfolder within the project and generates a new PEM-formatted wallet file named 'wallet-owner.pem' inside it. This wallet is recommended for simplicity and ease of testing, particularly for deploying smart contracts.

```bash
mkdir -p wallet
sc-meta wallet new --format pem --outfile ./wallet/wallet-owner.pem
```

--------------------------------

### Create New MultiversX Wallet

Source: https://docs.multiversx.com/developers/overview/sovereign/local-setup

Generates a new MultiversX wallet in PEM format and saves it to `~/wallet.pem`. This wallet will serve as the owner for cross-chain smart contracts and is utilized by the sovereign bridge service.

```bash
mxpy wallet new --format pem --outfile ~/wallet.pem
```

--------------------------------

### Parse MultiversX Contract Deployment Transaction in Two Steps

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-js/sdk-js-cookbook

This example illustrates a two-step approach for parsing a smart contract deployment transaction. It first waits for the transaction to complete on the network and then separately parses its outcome using the `SmartContractController`.

```JavaScript
{
    // We use the transaction hash we got when broadcasting the transaction
    // If we want to wait for transaction completion and parse the result in two different steps, we can do as follows:

    const entrypoint = new DevnetEntrypoint();
    const controller = entrypoint.createSmartContractController();
    const networkProvider = entrypoint.createNetworkProvider();
    const transactionOnNetwork = await networkProvider.awaitTransactionCompleted("txHash");

    // parsing the transaction
    const outcome = await controller.parseDeploy(transactionOnNetwork);
}
```

--------------------------------

### Example Data Field for SetMetadataTransaction

Source: https://docs.multiversx.com/developers/overview/validators/delegation-manager

Provides a concrete example of the 'Data' field's content for a 'SetMetadataTransaction', demonstrating how to encode the staking provider's name, website, and GitHub identifier into hexadecimal strings for the transaction's data payload.

```APIDOC
"setMetaData" +
    "@54657374204d782050726f7669646572" // Test Mx Provider
    "@746573746d782e70726f7669646572" //  testmx.provider
    "@746573746d7870726f7669646572"   // testmxprovider
```

--------------------------------

### Configure MultiversX Localnet for Local Source Builds

Source: https://docs.multiversx.com/developers/overview/developers/setup-local-testnet

This TOML configuration snippet instructs the MultiversX localnet to build the `mx_chain_go` (node) and `mx_chain_proxy_go` components from local source code. It specifies `resolution = "local"` and provides the `local_path` to the respective repositories.

```toml
[software.mx_chain_go]
resolution = "local"
local_path = "~/Desktop/workspace/mx-chain-go"

[software.mx_chain_proxy_go]
resolution = "local"
local_path = "~/Desktop/workspace/mx-chain-proxy-go"
```

--------------------------------

### MultiversX Smart Contract Upgrade Example

Source: https://docs.multiversx.com/developers/overview/developers/transactions/tx-legacy-calls

Demonstrates how to upgrade a MultiversX smart contract using the `ContractDeploy` object, specifying the recipient address and initiating the upgrade with EGLD transfer.

```Rust
self.callee_contract_proxy()
	.contract(calee_contract_address)
	.init(123, 456)
	.with_egld_transfer(payment)
	.upgrade_contract(code, code_metadata);
```

--------------------------------

### Create and Initialize New Localnet for Chronology Alteration

Source: https://docs.multiversx.com/developers/overview/developers/setup-local-testnet

Sets up a new workspace and generates a default `localnet.toml` file, specifically for demonstrating how to modify chronology parameters before starting the localnet. This allows for custom epoch and round durations.

```bash
mkdir -p ~/my-localnet-with-altered-chronology && cd ~/my-localnet-with-altered-chronology
mxpy localnet new
```

--------------------------------

### Create New Delegation Contract using DelegationController (Python)

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-py

Illustrates how to deploy a new delegation smart contract on the MultiversX blockchain using the `DelegationController`. It covers initializing the controller, loading an account, setting contract parameters like cap and fee, and awaiting transaction completion to get the contract address.

```Python
from pathlib import Path
from multiversx_sdk import Account, DevnetEntrypoint

# create the entrypoint and the delegation controller
entrypoint = DevnetEntrypoint()
controller = entrypoint.create_delegation_controller()

# the owner of the contract
alice = Account.new_from_pem(Path("../multiversx_sdk/testutils/testwallets/alice.pem"))

# fetch the nonce of the network
alice.nonce = entrypoint.recall_account_nonce(alice.address)

transaction = controller.create_transaction_for_new_delegation_contract(
    sender=alice,
    nonce=alice.get_nonce_then_increment(),
    total_delegation_cap=0,  # uncapped,
    service_fee=0,
    amount=1250000000000000000000  # 1250 EGLD
)

tx_hash = entrypoint.send_transaction(transaction)

# wait for transaction completion, extract delegation contract's address
outcome = controller.await_completed_create_new_delegation_contract(tx_hash)

contract_address = outcome[0].contract_address
```

--------------------------------

### MultiversX Account Storage: Gas Calculation Example Breakdown

Source: https://docs.multiversx.com/developers/overview/developers/account-storage

Illustrates a concrete example of gas cost calculation for a `SaveKeyValue` transaction with specific key-value data (`SaveKeyValue@6b657930@76616c756530`). It breaks down the total `271000` gas units into individual cost components based on current MultiversX protocol values.

```Pseudocode
required_gas =  100000    + // save key value function cost
                50000     + // move balance cost
                1500 * 34 + // cost_per_byte * length(txData)
                1000 * 4 + // persist_per_byte * length(key)
                1000 * 6 + // persist_per_byte * length(value)
                10000 * 6 + // store_per_byte * length(value)

             =  271000
```

--------------------------------

### Mainnet Deep History Squad Storage Requirements Example

Source: https://docs.multiversx.com/developers/overview/integrators/deep-history-squad

Displays an example of disk space usage for a mainnet deep-history squad configured for a long historical interval (July 2020 - January 2024), showing the storage consumed by different node components (metachain, shards).

```shell
307G    ./node-metachain
1.4T    ./node-0
3.9T    ./node-1
2.0T    ./node-2
```

--------------------------------

### Query `sum` Endpoint of Deployed `adder` Contract

Source: https://docs.multiversx.com/developers/overview/developers/testing/rust/sc-blackbox-example

Illustrates how to query a smart contract's endpoint (`sum`) after deployment. It uses a query builder pattern to specify the target address, contract proxy, and the expected return value, validating the contract's state.

```Rust
    world
        .query()
        .to(ADDER_ADDRESS)
        .typed(adder_proxy::AdderProxy)
        .sum()
        .returns(ExpectValue(5u32))
        .run();

```

--------------------------------

### Summarized MultiversX Contract Build Bash Script

Source: https://docs.multiversx.com/developers/overview/developers/reproducible-contract-builds

This comprehensive bash script provides a quick summary of the contract build process. It first downloads the necessary build wrapper, then sets environment variables for the project path, output directory, and the Docker image tag, before executing the build command.

```bash
wget https://raw.githubusercontent.com/multiversx/mx-sdk-build-contract/main/build_with_docker.py

export PROJECT=~/contracts/mx-contracts-rs
export BUILD_OUTPUT=~/contracts/output-from-docker
# Below, the image tag is just an example:
export IMAGE=multiversx/sdk-rust-contract-builder:v1.2.3

python3 ./build_with_docker.py --image=${IMAGE} \
    --project=${PROJECT} \
    --output=${BUILD_OUTPUT}
```

--------------------------------

### MultiversX NFT Field Encoding Example

Source: https://docs.multiversx.com/developers/overview/tokens/nft-tokens

This example table demonstrates the plain text values and their required hexadecimal encoded counterparts for various NFT fields. It illustrates how properties like NFT Name, Quantity, Royalties, Hash, Attributes, and URI are transformed for transaction building on the MultiversX network, using a song NFT as a specific use case.

```APIDOC
Property | Plain value | Encoded value
--- | --- | ---
**NFT Name** | Beautiful song | 42656175746966756c20736f6e67
**Quantity** | 1 | 01
**Royalties** | 7500 *=75%* | 1d4c
**Hash** | 00 | 00
**Attributes** | metadata:*ipfsCID/song.json*;tags:song,beautiful,music | 6d657461646174613a697066734349442f736f6e672e6a736f6e3b746167733a736f6e672c62656175746966756c2c6d75736963
**URI** | *URL_to_decentralized_storage/song.mp3* | 55524c5f746f5f646563656e7472616c697a65645f73746f726167652f736f6e672e6d7033
```

--------------------------------

### Simulate Simple Token Transfer using mxpy CLI

Source: https://docs.multiversx.com/developers/overview/developers/setup-local-testnet

This `mxpy` command simulates a new transaction. It recalls the sender's nonce, includes 'Hello, World' as transaction data, sets a gas limit, specifies the receiver address, uses a PEM file for authentication, targets a localnet, and connects via a local proxy. The `--simulate` flag ensures the transaction is not broadcasted but only simulated for testing.

```Shell
mxpy tx new --recall-nonce --data="Hello, World" --gas-limit=70000 \
 --receiver=erd1spyavw0956vq68xj8y4tenjpq2wd5a9p2c6j8gsz7ztyrnpxrruqzu66jx \
 --pem=~/multiversx-sdk/testwallets/latest/users/alice.pem \
 --chain=localnet --proxy=http://localhost:7950 \
 --simulate
```

--------------------------------

### Example Gas Limit Range for MultiversX Asynchronous Calls

Source: https://docs.multiversx.com/developers/overview/developers/gas-and-fees/user-defined-smart-contracts

This snippet applies the gas limit inequality to a specific example, showing the numerical range for `gasLimit` based on a `simulatedCost` of 3473900 and a `gasToLockForCallback` of 4145300. This provides a practical boundary for gas limit optimization.

```text
3473900 < gasLimit < 7619200
```

--------------------------------

### Hardware Wallet (Ledger): Instantiate Provider

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-js/sdk-js-signing-providers

Illustrates how to create a new instance of the `HWProvider` for interacting with a Ledger hardware wallet. Requires importing `HWProvider` from `@multiversx/sdk-hw-provider`.

```javascript
import { HWProvider } from "@multiversx/sdk-hw-provider";

const provider = new HWProvider();
```

--------------------------------

### Initiate MultiversX Wallet Login with Native Authentication

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-js/sdk-js-signing-providers

Demonstrates how to set up and initialize the NativeAuthClient to generate the initial part of the native authentication token, which is then passed to the login method for enhanced security and reliable off-chain identity assignment.

```javascript
import { NativeAuthClient } from "@multiversx/sdk-native-auth-client";

const nativeAuthClient = new NativeAuthClient({ ... });
const nativeAuthInitialPart = await nativeAuthClient.initialize();

const callbackUrl = encodeURIComponent("https://my-dapp/on-wallet-login");
await provider.login({ callbackUrl, token: nativeAuthInitialPart });
```

--------------------------------

### Simulating MultiversX Smart Contract Call via CLI

Source: https://docs.multiversx.com/developers/overview/developers/gas-and-fees/user-defined-smart-contracts

This command-line example demonstrates how to simulate a smart contract function call on the MultiversX network. It specifies the PEM file for authentication, the target function, a gas limit, and arguments. This simulation helps in pre-execution analysis and debugging, especially for gas consumption issues like 'out of gas' errors.

```bash
--pem=~/multiversx-sdk/testwallets/latest/users/alice.pem \
--function=foo\
--recall-nonce --gas-limit=6000000\
--arguments ${hexAddressOfB}\
--simulate
```

--------------------------------

### MultiversX Smart Contract Build Configuration Example

Source: https://docs.multiversx.com/developers/overview/developers/meta/sc-config

This configuration snippet defines how a single MultiversX smart contract is built, including its name, features, and various compilation settings. It also specifies profiling options and proxy configurations for the contract.

```TOML
[settings]
main = "main"

[contracts.main]
name = "my-contract"
add-unlabelled = true
panic-message = true
ei = "1.3"
allocator = "leaking"
stack-size = "3 pages"
features = ["example_feature_1", "example_feature_2"]
kill-legacy-callback = true

[contracts.main.profile]
codegen-units = 1
opt-level = "z"
lto = true
debug = false
panic = "abort"
overflow-checks = false

[[proxy]]
path = "src/main_proxy.rs"
override-import = "use new::override::path"
add-unlabelled=false
add-labels=["label_one"]
add-endpoints=["endpoint_one"]
[[proxy.path-rename]]
from = "main"
to = "new::main"
```

--------------------------------

### Deploy MultiversX Smart Contract

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-py

This snippet demonstrates the full process of deploying a smart contract on the MultiversX devnet. It covers loading the ABI and bytecode, preparing deployment arguments, creating a deploy transaction, signing it with a loaded account, broadcasting the transaction, and finally parsing the transaction outcome to retrieve the deployed contract's address.

```Python
# load the abi file
abi = Abi.load(Path("contracts/adder.abi.json"))

# get the smart contracts controller
entrypoint = DevnetEntrypoint()
factory = entrypoint.create_smart_contract_transactions_factory(abi=abi)

# load the contract bytecode
bytecode = Path("contracts/adder.wasm").read_bytes()

# For deploy arguments, use typed value objects if you haven't provided an ABI to the factory:
args = [BigUIntValue(42)]
# Or use simple, plain Python values and objects if you have provided an ABI to the factory:
args = [42]

alice_address = Address.new_from_bech32("erd1qyu5wthldzr8wx5c9ucg8kjagg0jfs53s8nr3zpz3hypefsdd8ssycr6th")

deploy_transaction = factory.create_transaction_for_deploy(
    sender=alice_address,
    bytecode=bytecode,
    gas_limit=5000000,
    arguments=args,
    is_upgradeable=True,
    is_readable=True,
    is_payable=True,
    is_payable_by_sc=True
)

# load the account
alice = Account.new_from_keystore(
    file_path=Path("../multiversx_sdk/testutils/testwallets/withDummyMnemonic.json"),
    password="password",
    address_index=0
)
# the developer is responsible for managing the nonce
alice.nonce = entrypoint.recall_account_nonce(alice.address)

# set the nonce
deploy_transaction.nonce = alice.nonce

# sign transaction
deploy_transaction.signature = alice.sign_transaction(deploy_transaction)

# broadcasting the transaction
tx_hash = entrypoint.send_transaction(deploy_transaction)
print(tx_hash.hex())

# waiting for transaction to complete
transaction_on_network = entrypoint.await_transaction_completed(tx_hash)

# parsing transaction
parser = SmartContractTransactionsOutcomeParser(abi)
contract_deploy_outcome = parser.parse_deploy(transaction_on_network)

contract_address = contract_deploy_outcome.contracts[0].address
print(contract_address.to_bech32())
```

--------------------------------

### Solidity Basic Address to Balance Mapping

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/eth-to-mvx

Illustrates a fundamental `mapping` in Solidity, used to associate an Ethereum address with a `uint` value, typically representing a balance.

```Solidity
mapping(address => uint) public balances
```

--------------------------------

### MultiversX API: Get NFT Data Request Parameters

Source: https://docs.multiversx.com/developers/overview/tokens/nft-tokens

Describes the required parameters for the 'Get NFT data for an address' API endpoint, including their types and descriptions. These parameters are essential for constructing a valid request to fetch NFT information.

```APIDOC
Param | Required | Type | Description
--- | --- | --- | ---
bech32Address | REQUIRED | `string` | The Address to query in bech32 format.
tokenIdentifier | REQUIRED | `string` | The token identifier.
nonce | REQUIRED | `numeric` | The nonce after the NFT creation.
```

--------------------------------

### Deploy MultiversX Smart Contract via CLI

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/interactors-guide

This command navigates into the `interactor` directory and executes the `deploy` command using `cargo run`, initiating the deployment of a MultiversX smart contract to the blockchain.

```Shell
cd interactor
cargo run deploy
```

--------------------------------

### Initiate Untyped Contract Deployment with Argument

Source: https://docs.multiversx.com/developers/overview/developers/transactions/tx-data

Illustrates how to start an untyped contract deployment using `.raw_deploy()` and add an argument with `.argument()`. This is similar to function call arguments but for deployment.

```MultiversX
tx().raw_deploy().argument(&argument)
```

--------------------------------

### Example HTTP Request to Send Multiple MultiversX Transactions

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/rest-api/transactions

An example demonstrating the structure of an HTTP POST request to the `send-multiple` endpoint, including the `Content-Type` header and a JSON array containing two sample transaction objects with their respective parameters.

```HTTP
POST https://gateway.multiversx.com/transaction/send-multiple HTTP/1.1
Content-Type: application/json

[
    {
        "nonce": 42,
        "value": "100000000000000000",
        "receiver": "erd1cux02zersde0l7hhklzhywcxk4u9n4py5tdxyx7vrvhnza2r4gmq4vw35r",
        "sender": "erd1njqj2zggfup4nl83x0nfgqjkjserm7mjyxdx5vzkm8k0gkh40ezqtfz9lg",
        "gasPrice": 1000000000,
        "gasLimit": 70000,
        "data": "Zm9vZCBmb3IgY2F0cw==",
        "signature": "93207c579bf57be03add632b0e1624a73576eeda8a1687e0fa286f03eb1a17ffb125ccdb008a264c402f074a360442c7a034e237679322f62268b614e926d10f",
        "chainId": "1",
        "version": 1
},
    {
        "nonce": 43,
        "value": "100000000000000000",
        "receiver": "erd1cux02zersde0l7hhklzhywcxk4u9n4py5tdxyx7vrvhnza2r4gmq4vw35r",
        "sender": "erd1rhp4q3qlydyrrjt7dgpfzxk8n4f7yrat4wc6hmkmcnmj0vgc543s8h7hyl",
        "gasPrice": 1000000000,
        "gasLimit": 70000,
        "data": "YnVzIHRpY2tldHM=",
        "signature": "01535fd1d40d98b7178ccfd1729b3f526ee4542482eb9f591d83433f9df97ce7b91db07298b1d14308e020bba80dbe4bba8617a96dd7743f91ee4b03d7f43e00",
        "chainID": "1",
        "version": 1
    }
]
```

--------------------------------

### JSON Example: Request Body for Sending Transaction

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/rest-api/transactions

A complete example of the JSON payload used to send a signed transaction via the MultiversX Gateway API, demonstrating the structure and typical values for parameters such as `nonce`, `value`, `sender`, `receiver`, `gasLimit`, `data`, and `signature`.

```JSON
{
    "nonce": 42,
    "value": "100000000000000000",
    "receiver": "erd1cux02zersde0l7hhklzhywcxk4u9n4py5tdxyx7vrvhnza2r4gmq4vw35r",
    "sender": "erd1njqj2zggfup4nl83x0nfgqjkjserm7mjyxdx5vzkm8k0gkh40ezqtfz9lg",
    "gasPrice": 1000000000,
    "gasLimit": 70000,
    "data": "Zm9vZCBmb3IgY2F0cw==",
    "signature": "93207c579bf57be03add632b0e1624a73576eeda8a1687e0fa286f03eb1a17ffb125ccdb008a264c402f074a360442c7a034e237679322f62268b614e926d10f",
    "chainId": "1",
    "version": 1
}
```

--------------------------------

### Create Network Provider from Devnet Entrypoint

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-py

Shows how to obtain an API network provider instance by creating a `DevnetEntrypoint` and calling its `create_network_provider` method. This provider facilitates interaction with the MultiversX network, abstracting underlying API calls.

```python
from multiversx_sdk import DevnetEntrypoint

entrypoint = DevnetEntrypoint()
api = entrypoint.create_network_provider()
```

--------------------------------

### Create Test Function for Contract Initialization in Rust

Source: https://docs.multiversx.com/developers/overview/developers/testing/rust/whitebox-legacy

This Rust test function, `init_test`, orchestrates the execution of the `setup_crowdfunding` function to prepare the test environment. Subsequently, it writes the generated test scenario to a JSON file named `_generated_init.scen.json`. This process facilitates automated testing and the generation of reproducible scenarios for the smart contract's initialization phase.

```Rust
#[test]
fn init_test() {
    let cf_setup = setup_crowdfunding(crowdfunding_esdt::contract_obj);
    cf_setup
        .blockchain_wrapper
        .write_mandos_output("_generated_init.scen.json");
}
```

--------------------------------

### MultiversX API Response Example for Address with No Votes

Source: https://docs.multiversx.com/developers/overview/governance/governance-interaction

This example demonstrates the API response for an address that has not cast any votes on proposals. The `returnData` array clearly shows base64-encoded zero counts for both delegated and direct nonces, indicating no voting activity.

```APIDOC
{
  "returnData": [
    "AA==", (number of delegated nonces: 0)
    "AA==", (number of direct nonces: 0)
  ]
}
```

--------------------------------

### Generate New MultiversX Smart Contract from Template

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/interactors-guide

This command uses `sc-meta` to generate a new smart contract project from a specified template. The `code` command (optional) opens the generated project in VSCode for further development. This provides a starting point for MultiversX smart contract development.

```Shell
sc-meta new --template empty --name my-contract
code my-contract # opens the contract in VSCode (optional)
```

--------------------------------

### Fetch MultiversX Block using ApiNetworkProvider

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-js/sdk-js-cookbook

Provides examples for fetching a specific block by hash and the latest block from the MultiversX network using the `ApiNetworkProvider`.

```TypeScript
{
    const api = new ApiNetworkProvider("https://devnet-api.multiversx.com");
    const blockHash = "1147e111ce8dd860ae43a0f0d403da193a940bfd30b7d7f600701dd5e02f347a";
    const block = await api.getBlock(blockHash);
}
```

```TypeScript
{
    const api = new ApiNetworkProvider("https://devnet-api.multiversx.com");
    const latestBlock = await api.getLatestBlock();
}
```

--------------------------------

### Rust: Manual Storage Mapper Key Construction

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/staking-contract

This snippet demonstrates the manual construction of a storage key for a MultiversX smart contract mapper. It shows how a base string is combined with an address to form the complete key, illustrating the underlying operations that are optimized by reusing mapper instances.

```Rust
let mut key = ManagedBuffer::new_from_bytes(b"stakingPosition");
key.append(addr.as_managed_buffer());
```

--------------------------------

### Navigate to Scripts Directory and Execute Main Script

Source: https://docs.multiversx.com/developers/overview/validators/nodes-scripts/install-update

This snippet shows how to change the current directory to the `mx-chain-scripts` folder and then execute the main `script.sh` to begin node management operations. It serves as the initial entry point for interacting with the MultiversX validator tools.

```Bash
cd ~/mx-chain-scripts
./script.sh
```

--------------------------------

### Import Autogenerated Proxy in MultiversX Rust Contract

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/crowdfunding-p1

Illustrates the necessary Rust code modification to import the autogenerated `crowdfunding_proxy` module into the main smart contract's source, enabling its use for testing.

```Rust
#![no_std]

#[allow(unused_imports)]
use multiversx_sc::imports::*;

pub mod crowdfunding_proxy;

#[multiversx_sc::contract]
pub trait Crowdfunding {
    // Here is the implementation of the crowdfunding contract
}
```

--------------------------------

### Import Constants from SDK-dapp Constants Module

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-dapp

Example of importing various constants, such as `GAS_PRICE_MODIFIER`, `DECIMALS`, and `mnemonicWords`, from the `@multiversx/sdk-dapp/constants` module. These constants are essential for interacting with the MultiversX blockchain.

```javascript
import {
  GAS_PRICE_MODIFIER,
  GAS_PER_DATA_BYTE,
  GAS_LIMIT,
  GAS_PRICE,
  DECIMALS,
  DIGITS,
  mnemonicWords,
  ledgerErrorCodes,
  fallbackNetworkConfigurations,
} from "@multiversx/sdk-dapp/constants";
```

--------------------------------

### Deploy MultiversX Smart Contract to Devnet

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/staking-contract

This command navigates into the interactor directory and then executes the deployment of the smart contract to the MultiversX Devnet. This is the final step in the contract deployment process.

```shell
cd interactor/
cargo run deploy
```

--------------------------------

### Deploy MyAdder Contract on MultiversX Chain Simulator (Rust)

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/chain-simulator-adder

This snippet demonstrates the initial deployment of the MyAdder smart contract on the MultiversX Chain Simulator. The contract is initialized with a sum of zero, setting up the environment for subsequent interactions.

```Rust
use basic_interactor::{Config, MyAdderInteract};

#[tokio::test]
#[cfg_attr(not(feature = "chain-simulator-tests"), ignore)]
async fn simulator_adder_test() {
    let mut basic_interact = MyAdderInteract::init(Config::chain_simulator_config()).await;

    ///////////////////////1///////////////////////
    basic_interact.deploy().await;
}
```

--------------------------------

### MultiversX Wallet Connect: Sign Transaction Example

Source: https://docs.multiversx.com/developers/overview/integrators/walletconnect-json-rpc-methods

Demonstrates the JSON RPC request and corresponding result for the `mvx_signTransaction` method, used to sign a MultiversX blockchain transaction. The example includes a full transaction object with nonce, value, receiver, sender, gas details, data, chain ID, and version, along with the expected signature in the result.

```json
// Request
{
    "id": 1,
    "jsonrpc": "2.0",
    "method": "mvx_signTransaction",
    "params": {
        "transaction": {
            "nonce": 42,
            "value": "100000000000000000",
            "receiver": "erd1cux02zersde0l7hhklzhywcxk4u9n4py5tdxyx7vrvhnza2r4gmq4vw35r",
            "sender": "erd1ylzm22ngxl2tspgvwm0yth2myr6dx9avtx83zpxpu7rhxw4qltzs9tmjm9",
            "gasPrice": 1000000000,
            "gasLimit": 70000,
            "data": "Zm9vZCBmb3IgY2F0cw==", // base64 representation of "food for cats"
            "chainID": "1",
            "version": 1
        }
    }
}

// Result
{
    "id": 1,
    "jsonrpc": "2.0",
    "result": {
        "signature": "5845301de8ca3a8576166fb3b7dd25124868ce54b07eec7022ae3ffd8d4629540dbb7d0ceed9455a259695e2665db614828728d0f9b0fb1cc46c07dd669d2f0e"
    }
}
```

--------------------------------

### Claim MultiversX Rewards using the Factory

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-js/sdk-js-cookbook

This example shows how to claim rewards using the 'Delegation Transactions Factory'. It involves creating the claim transaction, manually assigning the nonce, signing the transaction, and then broadcasting it to the network.

```javascript
{
    // create the entrypoint and the delegation factory
    const entrypoint = new DevnetEntrypoint();
    const factory = entrypoint.createDelegationTransactionsFactory();

    const filePath = path.join("../src", "testdata", "testwallets", "alice.pem");
    const alice = await Account.newFromPem(filePath);

    const contract = Address.newFromBech32("erd1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqf8llllswuedva");

    const transaction = await factory.createTransactionForClaimingRewards(alice.address, {
        delegationContract: contract,
    });
    // fetch the nonce of the network
    alice.nonce = await entrypoint.recallAccountNonce(alice.address);

    // set the nonce
    transaction.nonce = alice.getNonceThenIncrement();

    // sign the transaction
    transaction.signature = await alice.signTransaction(transaction);

    // sending the transaction
    const txHash = await entrypoint.sendTransaction(transaction);
}
```

--------------------------------

### Example MultiversX `setState` Configuration for Blockchain Mock

Source: https://docs.multiversx.com/developers/overview/developers/testing/scenario/structure-json

This JSON snippet illustrates how to configure the `setState` step within a MultiversX blockchain mock. It demonstrates setting up multiple accounts, including user and smart contract accounts, with detailed specifications for EGLD balances, various ESDT token types (fungible, semi-fungible, NFTs), account storage, and block information. The example highlights the flexibility in defining initial states for testing scenarios.

```JSON
{
    "steps": [
        {
            "step": "setState",
            "comment": "not much to comment here, but we can",
            "accounts": {
                "address:user_account": {
                    "comment": "we can comment on individual account initializations",
                    "nonce": "0",
                    "balance": "123,000,000,000",
                    "esdt": {
                        "str:MYFUNGIBLE-0001": "400,000,000,000",
                        "str:MYSFT-123456": {
                            "instances": [
                                {
                                    "nonce": "24",
                                    "balance": "1"
                                },
                                {
                                    "nonce": "25",
                                    "balance": "1",
                                    "creator": "address:other_creator_address",
                                    "royalties": "5000",
                                    "hash": "keccak256:str:other_nft_hash",
                                    "uri": [
                                        "str:www.something.com/funny.jpeg"
                                    ],
                                    "attributes": "str:other_attributes"
                                }
                            ],
                            "lastNonce": "7",
                            "roles": [
                                "ESDTRoleLocalMint",
                                "ESDTRoleLocalBurn",
                                "ESDTRoleNFTCreate",
                                "ESDTRoleNFTAddQuantity",
                                "ESDTRoleNFTBurn"
                            ],
                            "frozen": "false"
                        }
                    },
                    "username": "str:myusername.x",
                    "storage": {},
                    "code": ""
                },
                "sc:smart_contract_address": {
                    "nonce": "0",
                    "balance": "23,000",
                    "esdt": {
                        "str:MYFUNGIBLE-0001": "100,000,000,000"
                    },
                    "storage": {
                        "str:storage-key-1": "-5",
                        "str:storage-key-2|u32:4": ["u32:1", "u32:2", "u32:3"]
                    },
                    "code": "file:smart-contract.wasm"
                }
            },
            "newAddresses": [
                {
                    "creatorAddress": "address:creator",
                    "creatorNonce": "1234",
                    "newAddress": "sc:future_sc"
                }
            ]
        },
        {
            "step": "setState",
            "comment": "only set block info this time",
            "previousBlockInfo": {
                "blockNonce": "222",
                "blockRound": "333",
                "blockEpoch": "444"
            },
            "currentBlockInfo": {
                "blockTimestamp": "511",
                "blockNonce": "522",
                "blockRound": "533",
                "blockEpoch": "544"
            }
        }
    ]
}
```

--------------------------------

### Query MultiversX Smart Contract State with mxpy

Source: https://docs.multiversx.com/developers/overview/developers/setup-local-testnet-advanced

Performs a read-only query on a deployed MultiversX smart contract to retrieve its current state. This `mxpy` command requires the contract address and the specific function to query (e.g., `get`), interacting with the local proxy.

```Shell
Query
mxpy --verbose contract query erd1qqqqqqqqqqqqqpgqlq... \
 --function=get \
 --proxy=http://localhost:7950
```

--------------------------------

### EGLD Transfer Gas Limit and Fee Calculation Examples

Source: https://docs.multiversx.com/developers/overview/developers/gas-and-fees/egld-transfers

These examples demonstrate the application of the gas limit formula and subsequent fee calculation for EGLD transfers. They show how gas limits and fees vary based on the presence and length of transaction data, using specific network configuration values.

```Pseudocode
networkConfig.erd_min_gas_limit is 50000
networkConfig.erd_gas_per_data_byte is 1500
networkConfig.erd_min_gas_price is 1000000000

tx1.data = ""
tx1.gasPrice = networkConfig.erd_min_gas_price

tx2.data = "Hello world!"
tx2.gasPrice = networkConfig.erd_min_gas_price

tx1.gasLimit = 50000

tx2.gasLimit
    = 50000 + 1500 * len("Hello world!")
    = 68000

fee(tx1)
    = tx1.gasLimit * tx1.gasPrice
    = 50000 * 1000000000
    = 50000000000000 atoms of EGLD
    = 0.00005 EGLD

fee(tx2)
    = tx2.gasLimit * tx2.gasPrice
    = 68000 * 1000000000
    = 68000000000000 atoms of EGLD
    = 0.000068 EGLD
```

--------------------------------

### Upgrade Deployed MultiversX Smart Contract

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/staking-contract

Instructions to build and then upgrade a previously deployed MultiversX smart contract. This command ensures that new functionality is applied while preserving existing storage, emphasizing the need for backwards compatibility in storage changes.

```Rust
cargo run upgrade
```

--------------------------------

### Cargo.toml Configuration for Chain Simulator Tests

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/chain-simulator-adder

Provides an example `Cargo.toml` file, demonstrating the inclusion of the `chain-simulator-tests` feature flag. This feature is essential for enabling and running tests specifically designed for the MultiversX Chain Simulator environment.

```TOML
[package]
name = "my-adder"
version = "0.0.0"
publish = false
edition = "2021"
authors = ["you"]

[lib]
path = "src/my_adder.rs"

[dependencies.multiversx-sc]
version = "0.54.0"

[dev-dependencies.multiversx-sc-scenario]
version = "0.54.0"

[workspace]
members = [
    ".",
    "meta",
    "interactor",
]

[features]
chain-simulator-tests = []
```

--------------------------------

### MultiversX General Developer Topics Overview

Source: https://docs.multiversx.com/developers/overview/developers/overview

Provides an overview of additional developer-related topics and resources available for MultiversX, covering fundamental aspects like network constants, protocol-side functions, data storage, transaction handling, and environment setup.

```APIDOC
OtherDeveloperTopics:
  Constants: A list of useful constants that governs the MultiversX Mainnet.
  Built in functions: Built-in functions - protocol-side functions.
  Account storage: How the data is stored under an an account + how to query and change it.
  Relayed/meta transactions: How to prepare transactions whose fee is not paid by the user, but by a relayer.
  Setup local testnet: How to set up a localnet (local testnet) - basic solution.
  Setup local testnet advanced: How to set up a localnet (local testnet) - advanced solution.
  Creating wallets: Examples on creating wallets.
  Reproducible builds: How to perform reproducible contract builds.
  Contract API limits: Limits that a smart contract must abide when calling external (node-related) functions.
```

--------------------------------

### Create Account from Keystore File (JavaScript)

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-js/sdk-js-cookbook

Illustrates how to create an `Account` object by loading it from a keystore JSON file. This method requires both the file path and a password for decryption, offering enhanced security for stored accounts.

```JavaScript
{
    const keystorePath = path.join("../src", "testdata", "testwallets", "alice.json");
    const accountFromKeystore = Account.newFromKeystore(keystorePath, "password");
}
```

--------------------------------

### Interact with MultiversX Chain Simulator

Source: https://docs.multiversx.com/developers/overview/developers/meta/sc-meta-cli

This command initiates interaction with the MultiversX chain simulator. It provides subcommands to manage the simulator, such as pulling the Docker image, starting, and stopping the simulator, facilitating local contract testing.

```CLI
cargo run cs
```

```CLI
sc-meta cs
```

--------------------------------

### MultiversX ESDT Transfer Fee Example

Source: https://docs.multiversx.com/developers/overview/tokens/fungible-tokens

This example illustrates the calculation of the ESDT transfer fee using the provided formula. It includes a sample `TransferTransaction` structure, demonstrating how gas price, data length, and constants are used to derive the final fee in EGLD.

```Formula
TransferTransaction {
    ...
    gasPrice: 1000000000
    data: ESDTTransfer@4d45582d343535633537@043c33c1937564800000
}

ESDT_TRANSFER_FEE = gas_price * gas_cost
                  = 1000000000    * [ MIN_GAS_LIMIT + (data_length * GAS_PER_DATA_BYTE) + (ESDT_TRANSFER_FUNCTION_COST * GAS_PRICE_MODIFIER)]
                  = 1,000,000,000 * [    50,000     + (     54     *      1500        ) + (         200,000            *        0.01       )]
                  = 133000000000000
                  = 0.000133 EGLD
```

--------------------------------

### Create MultiversX Devnet Wallet PEM File

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/staking-contract

This command sequence creates a new directory for wallets and then generates a new wallet file in PEM format. This wallet will be used for signing transactions and deploying contracts on the MultiversX Devnet.

```shell
mkdir -p ~/MyTestWallets
sc-meta wallet new --format pem --outfile ~/MyTestWallets/tutorialKey.pem
```

--------------------------------

### MultiversX Node Binary Location

Source: https://docs.multiversx.com/developers/overview/validators/import-db

Specifies the typical installation path for the MultiversX node executable, which is essential for running the node and its associated commands.

```Filesystem
~/mx-chain-go/cmd/node
```

--------------------------------

### Example of a Single ESDT Attribute ABI JSON File

Source: https://docs.multiversx.com/developers/overview/developers/data/abi

This JSON snippet provides an example of the content found within a generated `.esdt-abi.json` file for a specific ESDT attribute, such as `testOption`. It details the `ticker` and `type` of the attribute as defined in the smart contract.

```JSON
{
    "esdtAttribute": {
        "ticker": "testOption",
        "type": "Option<TokenIdentifier>"
    }
}
```

--------------------------------

### Create UserSigner from PEM File (JavaScript)

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-js/sdk-js-cookbook-v13

Shows how to initialize a UserSigner instance directly from the content of a PEM file. This method provides an alternative to using a JSON wallet for signer creation, suitable for environments where PEM files are preferred.

```JavaScript
const pemText = await promises.readFile("../testwallets/alice.pem", { encoding: "utf8" });
signer = UserSigner.fromPem(pemText);
```

--------------------------------

### Create Local Backup Directory for Validator Keys

Source: https://docs.multiversx.com/developers/overview/validators/nodes-scripts/install-update

This snippet demonstrates how to navigate to the home directory and create a new folder named `VALIDATOR_KEYS`. This directory is designated for securely storing backups of the validator's private keys, which are crucial for node recovery and upgrades.

```Bash
cd ~
mkdir -p ~/VALIDATOR_KEYS
```

--------------------------------

### Format Token Amounts

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-js/sdk-js-cookbook-v13

Demonstrates how to format raw token amounts (e.g., from smart contracts) into human-readable numbers with a specified number of decimals and digits. Examples are provided for both `@multiversx/sdk-dapp` and `bignumber.js`.

```JavaScript
import { formatAmount } from '@multiversx/sdk-dapp/utils/operations';

console.log("Format using sdk-dapp:", formatAmount({
    input: "1500000000000000000",
    decimals: 18,
    digits: 4
}));
```

```JavaScript
import BigNumber from "bignumber.js";

BigNumber.config({ ROUNDING_MODE: BigNumber.ROUND_FLOOR });

console.log("Format using bignumber.js:", new BigNumber("1500000000000000000").shiftedBy(-18).toFixed(4));
```

--------------------------------

### Example MultiversX Transaction for Delegation Contract Creation

Source: https://docs.multiversx.com/developers/overview/validators/delegation-manager

A concrete example demonstrating how to construct a NewDelegationContractTransaction to create a delegation contract with a total delegation cap of 7231.941 EGLD and a service fee of 37.45%. This transaction also funds the new contract with 1250 EGLD upon creation.

```MultiversX Transaction
NewDelegationContractTransaction {
    Sender: <account address of the node operator>
    Receiver: erd1qqqqqqqqqqqqqqqpqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqylllslmq6y6
    Value: 1250000000000000000000
    GasLimit: 60000000
    Data: "createNewDelegationContract" +
          "@01880b57b708cf408000" +
          "@0ea1"
}
```

--------------------------------

### MultiversX Node Configuration Files Structure

Source: https://docs.multiversx.com/developers/overview/sovereign/distributed-setup

Lists the standard configuration files and folders found within the `cmd/node/config` directory for a MultiversX node, indicating which files are discussed in detail later.

```text
gasSchedules folder
genesisContracts folder
genesis.json*
genesisSmartContracts.json
nodesSetup.json*
api.toml
config.toml
economics.toml
enableEpochs.toml
enableRounds.toml
external.toml
fullArchiveP2P.toml
p2p.toml
prefs.toml
ratings.toml
systemSmartContractsConfig.toml
```

--------------------------------

### Example Unjailing Command for Two Validators

Source: https://docs.multiversx.com/developers/overview/validators/staking/unjailing

This example illustrates the `mxpy` command for unjailing two MultiversX validators simultaneously. It shows how to provide multiple BLS public keys, separated by a comma without spaces. The `value` parameter reflects the total EGLD required for both validators, emphasizing the importance of accounting for denomination.

```bash
mxpy --verbose validator unjail --pem=walletKey.pem --value="5000000000000000000000" --nodes-public-keys="b617d8bc442bda59510f77e04a1680e8b2d3293c8c4083d94260db96a4d732deaaf9855fa0cef2273f5a67b4f442c725efc06a5d366b9f15a66da9eb8208a09c9ab4066b6b3d38c3cf1ea7fab6489a90713b3b56d87de68c6558c80d7533bf27,f921a0f76ed70e8a806c6f9119f87b12700f96f732e6070b675e0aec10cb0723803202a4c40194847c38195db07b1001f6d50c81a82b949e438cd6dd945c2eb99b32c79465aefb9144c8668af67e2d01f71b81842d9b94e4543a12616cb5897d" --proxy=https://gateway.multiversx.com --estimate-gas --recall-nonce
```

--------------------------------

### Create New Delegation Contract Using Controller

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-js/sdk-js-cookbook

This code demonstrates how to deploy a new delegation smart contract on the MultiversX network using the `DevnetEntrypoint` and `DelegationController`. It covers account setup, nonce management, transaction creation with initial delegation parameters (cap, fee, amount), transaction submission, and awaiting the outcome to retrieve the newly deployed contract's address.

```javascript
{
    // create the entrypoint and the delegation controller
    const entrypoint = new DevnetEntrypoint();
    const controller = entrypoint.createDelegationController();

    const filePath = path.join("../src", "testdata", "testwallets", "alice.pem");
    const alice = await Account.newFromPem(filePath);

    // fetch the nonce of the network
    alice.nonce = await entrypoint.recallAccountNonce(alice.address);

    const transaction = await controller.createTransactionForNewDelegationContract(
        alice,
        alice.getNonceThenIncrement(),
        {
            totalDelegationCap: 0n,
            serviceFee: 10n,
            amount: 1250000000000000000000n,
        },
    );

    // sending the transaction
    const txHash = await entrypoint.sendTransaction(transaction);

    // wait for transaction completion, extract delegation contract's address
    const outcome = await controller.awaitCompletedCreateNewDelegationContract(txHash);

    const contractAddress = outcome[0].contractAddress;
}
```

--------------------------------

### Import Operations Utility Functions from MultiversX SDK Dapp

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-dapp

This snippet imports utility functions from `@multiversx/sdk-dapp/utils/operations` for calculating fee limits, formatting amounts, nominating, and getting USD values.

```javascript
import {
  calculateFeeLimit,
  formatAmount,
  nominate,
  getUsdValue,
} from "@multiversx/sdk-dapp/utils/operations";
```

--------------------------------

### Example of Overriding config.toml Values in prefs.toml

Source: https://docs.multiversx.com/developers/overview/validators/node-configuration

This code example demonstrates how to use the `OverridableConfigTomlValues` array within `prefs.toml` to set custom values for specific paths in `config.toml`. This feature, introduced in `v1.4.x`, allows node operators to preserve their preferred settings, such as `StoragePruning.NumEpochsToKeep` or `MiniBlocksStorage.Cache.Name`, even after node upgrades.

```TOML
   OverridableConfigTomlValues = [
     { Path = "StoragePruning.NumEpochsToKeep", Value = "4" },
     { Path = "MiniBlocksStorage.Cache.Name", Value = "MiniBlocksStorage" }
   ]
```

--------------------------------

### Log In with MetamaskProxyProvider

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-js/sdk-js-signing-providers

Demonstrates how to initiate a user login flow using the MetamaskProxyProvider. Upon successful login, the user's address and account details become available.

```typescript
const address = await provider.login();

console.log(address);
console.log(provider.account);
```

--------------------------------

### Microservice Devnet Configuration File Path

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/your-first-microservice

This snippet indicates the typical path to the devnet configuration file for the ping-pong microservice. This YAML file is where settings like Redis server URL and smart contract addresses are defined.

```text
~ping-pong/microservice/config/config.devnet.yaml
```

--------------------------------

### MultiversX dApp SDK (sdk-dapp) Overview

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/overview

Documentation for `sdk-dapp`, a React library designed to simplify dApp development on the MultiversX Network. It abstracts boilerplate for logging in, signing transactions or messages, and offers helper functions for common tasks, streamlining the creation of decentralized applications.

```APIDOC
sdk-dapp - core functional logic of a dApp:
  Description: React library aimed to help developers create dApps based on MultiversX Network. It abstracts away all the boilerplate for logging in, signing transactions or messages, and also offers helper functions for common tasks.
  Link: /sdk-and-tools/sdk-dapp
```

--------------------------------

### Generate MultiversX Native Auth Access Token

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-py

This example illustrates the process of generating a native authentication token using the NativeAuthClient. It involves initializing the client, obtaining a token for signing, signing it with an account from a keystore, and finally retrieving the access token.

```python
from pathlib import Path

from multiversx_sdk import Account, Message, NativeAuthClient, NativeAuthClientConfig

config = NativeAuthClientConfig(origin="https://devnet-api.multiversx.com", api_url="https://devnet-api.multiversx.com")
client = NativeAuthClient(config)

account = Account.new_from_keystore(
    file_path=Path("../multiversx_sdk/testutils/testwallets/withDummyMnemonic.json"),
    password="password",
    address_index=0
)

init_token = client.initialize()
token_for_signing = client.get_token_for_signing(account.address, init_token)
signature = account.sign_message(Message(token_for_signing))
access_token = client.get_token(address=account.address, token=init_token, signature=signature.hex())

print(access_token)
```

--------------------------------

### Log In with CrossWindowProvider

Source: https://docs.multiversx.com/developers/overview/sdk-and-tools/sdk-js/sdk-js-signing-providers

Demonstrates how to initiate a user login flow using the CrossWindowProvider. Upon successful login, the user's address and account details become available.

```typescript
const address = await provider.login();

console.log(address);
console.log(provider.account);
```

--------------------------------

### Build MultiversX Rust Smart Contract with sc-meta

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/crowdfunding-p1

This shell command triggers the build process for a MultiversX Rust smart contract using the `sc-meta` tool. It compiles the contract and generates necessary output artifacts such as the ABI, imports, and the WASM bytecode, which are crucial for deployment on the MultiversX blockchain.

```Shell
sc-meta all build
```

--------------------------------

### MultiversX Smart Contract Proxy Generation Configuration (TOML)

Source: https://docs.multiversx.com/developers/overview/developers/tutorials/crowdfunding-p1

Defines the `sc-config.toml` file used to specify the output path for the autogenerated Rust proxy of a MultiversX smart contract, essential for interacting with contract endpoints in tests.

```TOML
[settings]

[[proxy]]
path = "src/crowdfunding_proxy.rs"
```