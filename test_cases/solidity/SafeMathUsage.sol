// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SafeMathUsage {
    using SafeMath for uint256;

    uint256 public total;

    function addValues(uint256 a, uint256 b) public {
        total = a.add(b);
    }

    function subValues(uint256 a, uint256 b) public {
        total = a.sub(b);
    }
}
