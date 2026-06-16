// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract MockReceiptEmitter {
    event ReceiptEmitted(
        uint256 indexed receiptId,
        bytes32 indexed merkleRoot,
        bytes manifest
    );

    mapping(uint256 => bytes32) public receiptRoot;

    function emitReceipt(
        uint256 receiptId,
        bytes32 merkleRoot,
        bytes calldata manifest
    ) external {
        receiptRoot[receiptId] = merkleRoot;
        emit ReceiptEmitted(receiptId, merkleRoot, manifest);
    }

    function verifyReceipt(
        uint256 receiptId,
        bytes32[] calldata proof,
        bytes32 leaf
    ) external view returns (bool) {
        if (proof.length != 0) return false;
        return receiptRoot[receiptId] == leaf;
    }
}
