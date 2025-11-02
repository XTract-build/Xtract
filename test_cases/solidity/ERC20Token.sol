// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract ERC20Token {
    uint256 public totalSupply;
    uint256 public balance;
    
    event Transfer(address indexed from, address indexed to, uint256 value);
    
    constructor() {
        totalSupply = 1000000000000000000000000;
        balance = totalSupply;
    }
    
    function transfer(address _to, uint256 _value) public returns (bool success) {
        require(balance >= _value);
        
        balance = balance - _value;
        
        emit Transfer(msg.sender, _to, _value);
        return true;
    }
}
