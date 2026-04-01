// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ContractFactory {
    address public lastDeployed;

    function createChild(uint256 initialValue) public {
        Child instance = new Child(initialValue);
    }
}
