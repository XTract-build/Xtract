// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AbiEncoding {
    function encodeTwo(uint256 a, uint256 b) public pure returns (bytes memory) {
        return abi.encode(a, b);
    }

    function encodePackedTwo(uint256 a, uint256 b) public pure returns (bytes memory) {
        return abi.encodePacked(a, b);
    }

    function decodeHint(uint256 data) public pure returns (uint256) {
        return abi.decode(data, (uint256));
    }
}
