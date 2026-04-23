// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract SoulboundReceipt is ERC721, Ownable {
    address public proofEngine;
    uint256 private _tokenIdCounter;

    struct ReceiptData {
        uint256 claimId;
        uint8 status;
        uint8 latencyTier;
        uint256 mintedAt;
        uint256 updatedAt;
    }

    mapping(uint256 => ReceiptData) public receipts;
    mapping(uint256 => uint256) public claimToToken;
    mapping(uint256 => string) private _tokenURIs;

    event ReceiptMinted(uint256 indexed tokenId, uint256 indexed claimId, address indexed issuer, uint8 status, uint8 latencyTier);
    event ReceiptUpdated(uint256 indexed tokenId, uint8 oldStatus, uint8 newStatus);
    event MetadataUpdated(uint256 indexed tokenId, string newURI);

    modifier onlyProofEngine() {
        require(msg.sender == proofEngine, "Only proof engine");
        _;
    }

    constructor() ERC721("Alabama Machine Speed Proof", "AMSP") Ownable(msg.sender) {}

    function setProofEngine(address _proofEngine) external onlyOwner {
        require(_proofEngine != address(0), "Zero address");
        proofEngine = _proofEngine;
    }

    function mintReceipt(address issuer, uint256 claimId, uint8 status, uint8 latencyTier) external onlyProofEngine returns (uint256 tokenId) {
        if (claimToToken[claimId] != 0) {
            tokenId = claimToToken[claimId];
            _updateReceiptInternal(tokenId, status);
            return tokenId;
        }

        _tokenIdCounter++;
        tokenId = _tokenIdCounter;
        claimToToken[claimId] = tokenId;

        receipts[tokenId] = ReceiptData({
            claimId: claimId,
            status: status,
            latencyTier: latencyTier,
            mintedAt: block.timestamp,
            updatedAt: block.timestamp
        });

        _tokenURIs[tokenId] = "";
        _safeMint(issuer, tokenId);
        emit ReceiptMinted(tokenId, claimId, issuer, status, latencyTier);
    }

    function updateReceiptStatus(uint256 claimId, uint8 newStatus) external onlyProofEngine {
        uint256 tokenId = claimToToken[claimId];
        require(tokenId != 0, "Receipt not found");
        _updateReceiptInternal(tokenId, newStatus);
    }

    function _updateReceiptInternal(uint256 tokenId, uint8 newStatus) private {
        ReceiptData storage data = receipts[tokenId];
        uint8 oldStatus = data.status;
        data.status = newStatus;
        data.updatedAt = block.timestamp;
        emit ReceiptUpdated(tokenId, oldStatus, newStatus);
    }

    function setTokenURI(uint256 tokenId, string calldata uri) external {
        require(msg.sender == proofEngine || msg.sender == owner(), "Not authorized");
        _tokenURIs[tokenId] = uri;
        emit MetadataUpdated(tokenId, uri);
    }

    function tokenURI(uint256 tokenId) public view override returns (string memory) {
        string memory customURI = _tokenURIs[tokenId];
        if (bytes(customURI).length > 0) return customURI;
        return super.tokenURI(tokenId);
    }

    function transferFrom(address, address, uint256) public pure override {
        revert("Soulbound: non-transferable");
    }

    function safeTransferFrom(address, address, uint256, bytes memory) public pure override {
        revert("Soulbound: non-transferable");
    }

    function approve(address, uint256) public pure override {
        revert("Soulbound: non-transferable");
    }

    function setApprovalForAll(address, bool) public pure override {
        revert("Soulbound: non-transferable");
    }

    function getReceiptByClaim(uint256 claimId) external view returns (ReceiptData memory) {
        uint256 tokenId = claimToToken[claimId];
        require(tokenId != 0, "Receipt not found");
        return receipts[tokenId];
    }

    function getReceipt(uint256 tokenId) external view returns (ReceiptData memory) {
        return receipts[tokenId];
    }

    function burn(uint256 tokenId) external {
        require(ownerOf(tokenId) == msg.sender || msg.sender == proofEngine || msg.sender == owner(), "Not authorized");
        uint256 claimId = receipts[tokenId].claimId;
        _burn(tokenId);
        delete claimToToken[claimId];
        delete receipts[tokenId];
    }
}
