#!/bin/bash
# Build and deploy all transpiled contracts
# Usage: ./build_and_deploy_all.sh

set -e

MXPY="/Users/kaan/Library/Python/3.9/bin/mxpy"
WALLET_PEM="/Users/kaan/.multiversx/wallet.pem"
PROXY_URL="https://devnet-gateway.multiversx.com"
GAS_LIMIT=50000000

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Contract list (excluding SimpleStorage as it's already deployed)
CONTRACTS=("ERC20Token" "Voting" "Crowdfunding" "NFTMarketplace")

echo -e "${BLUE}=== Building and Deploying Contracts ===${NC}\n"

for CONTRACT_NAME in "${CONTRACTS[@]}"; do
    echo -e "${YELLOW}=== Processing ${CONTRACT_NAME} ===${NC}"
    
    CONTRACT_NAME_LOWER=$(echo "${CONTRACT_NAME}" | tr '[:upper:]' '[:lower:]')
    DEMO_DIR="demo/${CONTRACT_NAME_LOWER}"
    RUST_SOURCE="test_cases/expected/${CONTRACT_NAME}.rs"
    OUTPUT_DIR="${DEMO_DIR}/output"
    
    # Create directory structure
    mkdir -p "${DEMO_DIR}/src"
    mkdir -p "${DEMO_DIR}/meta/src"
    mkdir -p "${OUTPUT_DIR}"
    
    # Copy Rust source
    cp "${RUST_SOURCE}" "${DEMO_DIR}/src/lib.rs"
    echo -e "${GREEN}✓ Copied Rust source${NC}"
    
    # Create Cargo.toml
    cat > "${DEMO_DIR}/Cargo.toml" << EOF
[package]
name = "${CONTRACT_NAME_LOWER}"
version = "0.1.0"
edition = "2021"

[lib]
path = "src/lib.rs"

[dependencies]
multiversx-sc = "0.57.0"

[dev-dependencies]
multiversx-sc-scenario = "0.57.0"
num-bigint = "0.4"
EOF
    
    # Create multiversx.json
    cat > "${DEMO_DIR}/multiversx.json" << EOF
{
  "language": "rust"
}
EOF
    
    # Create meta/Cargo.toml
    cat > "${DEMO_DIR}/meta/Cargo.toml" << EOF
[package]
name = "${CONTRACT_NAME_LOWER}-meta"
version = "0.0.0"
edition = "2021"
publish = false

[dependencies.${CONTRACT_NAME_LOWER}]
path = ".."

[dependencies.multiversx-sc-meta-lib]
version = "0.57.0"
default-features = false
EOF
    
    # Create meta/src/main.rs
    cat > "${DEMO_DIR}/meta/src/main.rs" << EOF
fn main() {
    multiversx_sc_meta_lib::cli_main::<${CONTRACT_NAME_LOWER}::AbiProvider>();
}
EOF
    
    echo -e "${GREEN}✓ Created project structure${NC}"
    
    # Build contract
    echo -e "${BLUE}Building ${CONTRACT_NAME}...${NC}"
    cd "${DEMO_DIR}"
    if sc-meta all build > build.log 2>&1; then
        echo -e "${GREEN}✓ Build successful${NC}"
        cd ../..
    else
        echo -e "${RED}✗ Build failed${NC}"
        echo "Build log:"
        cat build.log
        cd ../..
        continue
    fi
    
    # Deploy contract
    WASM_FILE="${OUTPUT_DIR}/${CONTRACT_NAME_LOWER}.wasm"
    if [ ! -f "$WASM_FILE" ]; then
        echo -e "${RED}✗ WASM file not found at ${WASM_FILE}${NC}"
        continue
    fi
    
    echo -e "${BLUE}Deploying ${CONTRACT_NAME} to devnet...${NC}"
    DEPLOY_OUTPUT=$(${MXPY} contract deploy \
        --bytecode "${WASM_FILE}" \
        --proxy="${PROXY_URL}" \
        --gas-limit ${GAS_LIMIT} \
        --pem="${WALLET_PEM}" \
        --send 2>&1)
    
    # Extract contract address
    CONTRACT_ADDRESS=$(echo "$DEPLOY_OUTPUT" | grep -o '"contractAddress":\s*"[^"]*"' | grep -o 'erd1[^"]*' || echo "")
    if [ -z "$CONTRACT_ADDRESS" ]; then
        CONTRACT_ADDRESS=$(echo "$DEPLOY_OUTPUT" | grep -o 'erd1[a-z0-9]*' | head -1 || echo "")
    fi
    
    # Extract transaction hash
    TX_HASH=$(echo "$DEPLOY_OUTPUT" | grep -o '"emittedTransactionHash":\s*"[^"]*"' | grep -o '[a-f0-9]*' | head -1 || echo "")
    if [ -z "$TX_HASH" ]; then
        TX_HASH=$(echo "$DEPLOY_OUTPUT" | grep -o 'tx hash:[[:space:]]*[a-f0-9]*' | grep -o '[a-f0-9]*' | head -1 || echo "")
    fi
    
    # Save deployment info
    if [ -n "$CONTRACT_ADDRESS" ]; then
        echo -e "${GREEN}✓ Deployment successful!${NC}"
        echo -e "${GREEN}  Contract Address: ${CONTRACT_ADDRESS}${NC}"
        echo "$CONTRACT_ADDRESS" > "${OUTPUT_DIR}/.deployed_address"
        if [ -n "$TX_HASH" ]; then
            echo -e "${GREEN}  Transaction Hash: ${TX_HASH}${NC}"
            echo -e "${BLUE}  Explorer: https://devnet-explorer.multiversx.com/transactions/${TX_HASH}${NC}"
            echo "$TX_HASH" > "${OUTPUT_DIR}/.deployed_tx_hash"
            echo "https://devnet-explorer.multiversx.com/transactions/${TX_HASH}" > "${OUTPUT_DIR}/.explorer_link"
        fi
        echo ""
    else
        echo -e "${RED}✗ Deployment failed${NC}"
        echo "$DEPLOY_OUTPUT"
        continue
    fi
done

echo -e "${BLUE}=== All done! ===${NC}"

