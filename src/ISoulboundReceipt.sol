// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface ISoulboundReceipt {
    function mintReceipt(
        address issuer,
        uint256 claimId,
        uint8 status,
        uint8 latencyTier
    ) external returns (uint256 tokenId);

    function updateReceiptStatus(uint256 claimId, uint8 newStatus) external;

    function ownerOf(uint256 tokenId) external view returns (address);
    function receiptData(uint256 tokenId) external view returns (
        uint256 claimId,
        uint8 status,
        uint8 latencyTier,
        uint256 mintedAt
    );
}
