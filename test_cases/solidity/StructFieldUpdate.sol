// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract StructFieldUpdate {
    struct Listing {
        uint256 price;
        bool active;
    }

    mapping(address => Listing) public listings;

    function activate(address seller) public {
        listings[seller].active = true;
    }

    function setPrice(address seller, uint256 newPrice) public {
        listings[seller].price = newPrice;
    }
}
