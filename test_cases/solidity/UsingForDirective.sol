// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract UsingForDirective {
    uint256 public result;

    function compute(uint256 a, uint256 b) public {
        result = SafeMath.add(a, b);
    }
}
