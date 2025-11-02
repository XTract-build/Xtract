#!/bin/bash
# Universal deployment script for MultiversX smart contracts
# Usage: ./deploy_all_contracts.sh [contract_name]

set -e

CONTRACT_NAME="${1:-simple_storage}"
MXPY="/Users/kaan/Library/Python/3.9/bin/mxpy"
WALLET_PEM="/Users/kaan/.multiversx/wallet.pem"
PROXY_URL="https://devnet-gateway.multiversx.com"
GAS_LIMIT=5000000
OUTPUT_DIR="demo/${CONTRACT_NAME}/output"
WASM_FILE="${OUTPUT_DIR}/${CONTRACT_NAME}.wasm"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}Deploying ${CONTRACT_NAME} contract...${NC}"

# Check if WASM file exists
if [ ! -f "$WASM_FILE" ]; then
    echo -e "${RED}Error: WASM file not found at ${WASM_FILE}${NC}"
    echo "Please build the contract first using: sc-meta all build"
    exit 1
fi

# Deploy contract
echo -e "${BLUE}Deploying to devnet...${NC}"
DEPLOY_OUTPUT=$($MXPY contract deploy \
    --bytecode "$WASM_FILE" \
    --proxy="$PROXY_URL" \
    --gas-limit $GAS_LIMIT \
    --pem="$WALLET_PEM" \
    --send 2>&1)

# Extract contract address from output
CONTRACT_ADDRESS=$(echo "$DEPLOY_OUTPUT" | grep -o '"contractAddress":\s*"[^"]*"' | grep -o 'erd1[^"]*' || echo "")

if [ -z "$CONTRACT_ADDRESS" ]; then
    # Try alternative pattern
    CONTRACT_ADDRESS=$(echo "$DEPLOY_OUTPUT" | grep -o 'erd1[a-z0-9]*' | head -1 || echo "")
fi

# Extract transaction hash
TX_HASH=$(echo "$DEPLOY_OUTPUT" | grep -o '"emittedTransactionHash":\s*"[^"]*"' | grep -o '[a-f0-9]*' | head -1 || echo "")

if [ -z "$TX_HASH" ]; then
    TX_HASH=$(echo "$DEPLOY_OUTPUT" | grep -o 'tx hash:[[:space:]]*[a-f0-9]*' | grep -o '[a-f0-9]*' | head -1 || echo "")
fi

# Display results
if [ -n "$CONTRACT_ADDRESS" ]; then
    echo -e "${GREEN}✓ Deployment successful!${NC}"
    echo -e "${GREEN}Contract Address: ${CONTRACT_ADDRESS}${NC}"
    if [ -n "$TX_HASH" ]; then
        echo -e "${GREEN}Transaction Hash: ${TX_HASH}${NC}"
        echo -e "${BLUE}Explorer: https://devnet-explorer.multiversx.com/transactions/${TX_HASH}${NC}"
    fi
    echo ""
    echo "$CONTRACT_ADDRESS" > "${OUTPUT_DIR}/.deployed_address"
    echo "$TX_HASH" > "${OUTPUT_DIR}/.deployed_tx_hash"
else
    echo -e "${RED}Error: Could not extract contract address from deployment output${NC}"
    echo "$DEPLOY_OUTPUT"
    exit 1
fi

