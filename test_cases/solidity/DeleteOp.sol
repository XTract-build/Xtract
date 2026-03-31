// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract DeleteOp {
    uint256 public counter;
    mapping(address => uint256) public balances;
    mapping(address => mapping(address => uint256)) public allowance;

    function resetCounter() public {
        delete counter;
    }

    function resetBalance(address user) public {
        delete balances[user];
    }

    function resetAllowance(address owner, address spender) public {
        delete allowance[owner][spender];
    }
}
