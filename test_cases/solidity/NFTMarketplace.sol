// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract NFTMarketplace {
    uint256 public currentTokenId;
    address public currentOwner;
    uint256 public currentPrice;
    bool public currentForSale;
    uint256 public nextTokenId;
    address public previousOwner;
    
    event NFTCreated(uint256 indexed tokenId, address indexed owner);
    event NFTListed(uint256 indexed tokenId, uint256 price);
    event NFTSold(uint256 indexed tokenId, address indexed from, address indexed to, uint256 price);
    
    function createNFT() public returns (uint256) {
        nextTokenId = nextTokenId + 1;
        currentTokenId = nextTokenId - 1;
        currentOwner = msg.sender;
        currentPrice = 0;
        currentForSale = false;
        emit NFTCreated(currentTokenId, msg.sender);
        return currentTokenId;
    }
    
    function listNFTForSale(uint256 price) public {
        require(currentOwner == msg.sender);
        currentPrice = price;
        currentForSale = true;
        emit NFTListed(currentTokenId, price);
    }
    
    function buyNFT() public {
        require(currentForSale == true);
        previousOwner = currentOwner;
        currentOwner = msg.sender;
        currentForSale = false;
        emit NFTSold(currentTokenId, previousOwner, msg.sender, currentPrice);
    }
    
    function getCurrentOwner() public view returns (address) {
        return currentOwner;
    }
    
    function getCurrentPrice() public view returns (uint256) {
        return currentPrice;
    }
    
    function getCurrentForSale() public view returns (bool) {
        return currentForSale;
    }
}
