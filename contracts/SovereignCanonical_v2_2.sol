// SPDX-License-Identifier: Maxwell-Tribunal-Core
pragma solidity ^0.8.25;

import "@openzeppelin/contracts/utils/cryptography/EIP712.sol";
import "@openzeppelin/contracts/utils/cryptography/ECDSA.sol";

contract SovereignCanonical is EIP712 {
    using ECDSA for bytes32;

    address public canonMarshal;
    mapping(address => bool) public vetoCommittee;

    enum Tier { SUPERSEDED, FULLY_DETERMINISTIC, PARTIAL_DETERMINISTIC, VETOED }

    struct Build {
        bytes32 circuitSourceHash;
        bytes32 receiptHash;
        bytes32 envHash;
        bytes32 auditSchemaHash;
        uint64  timestamp;
        Tier    tier;
        bool    vetoTriggered;
    }

    mapping(bytes32 => Build) public canonicalBuilds;
    mapping(bytes32 => Build[]) public history;

    event BuildPromoted(bytes32 indexed circuitSourceHash, bytes32 indexed receiptHash, bytes32 envHash, string tier, bool vetoTriggered, bytes32 auditSchemaHash, uint256 stabilityIndex, uint256 timestamp);
    event BuildSuperseded(bytes32 indexed circuitSourceHash, bytes32 receiptHash, uint256 indexed indexInHistory);
    event VaultStateRoot(bytes32 indexed walletId, bytes32 merkleRoot, string schemaVersion, bytes32 schemaHash, uint256 timestamp);

    error NotCanonMarshal();
    error NotVetoCommittee();

    constructor(address _marshal) EIP712("SovereignCanonical", "2") {
        require(_marshal != address(0), "invalid marshal");
        canonMarshal = _marshal;
    }

    modifier onlyCanonMarshal() { require(msg.sender == canonMarshal, "NOT_CANON_MARSHAL"); _; }

    function addVetoMember(address member) external onlyCanonMarshal { vetoCommittee[member] = true; }
    function removeVetoMember(address member) external onlyCanonMarshal { delete vetoCommittee[member]; }

    function promoteBuild(bytes32 _circuitSourceHash, bytes32 _receiptHash, bytes32 _envHash, string memory _tier, bytes32 _auditSchemaHash, uint256 _stabilityIndex, bytes memory _vetoSignature) external onlyCanonMarshal returns (bool) {
        bool veto = (_stabilityIndex == 0);
        Tier tier = veto ? Tier.VETOED : _parseTier(_tier);
        bytes32 structHash = keccak256(abi.encode(keccak256("BuildPromotion(bytes32 circuitSourceHash,bytes32 receiptHash,bool vetoTriggered)"), _circuitSourceHash, _receiptHash, veto));
        bytes32 digest = _hashTypedDataV4(structHash);
        address signer = ECDSA.recover(digest, _vetoSignature);
        require(signer != address(0), "Invalid veto signature");
        require(vetoCommittee[signer], "Signer not on veto committee");
        if (veto) {
            history[_circuitSourceHash].push(Build(_circuitSourceHash, _receiptHash, _envHash, _auditSchemaHash, uint64(block.timestamp), Tier.VETOED, true));
            emit BuildPromoted(_circuitSourceHash, _receiptHash, _envHash, "VETOED", true, _auditSchemaHash, 0, block.timestamp);
            return false;
        }
        Build storage prev = canonicalBuilds[_circuitSourceHash];
        if (prev.timestamp != 0) {
            prev.tier = Tier.SUPERSEDED;
            history[_circuitSourceHash].push(prev);
            emit BuildSuperseded(_circuitSourceHash, prev.receiptHash, history[_circuitSourceHash].length - 1);
        }
        canonicalBuilds[_circuitSourceHash] = Build(_circuitSourceHash, _receiptHash, _envHash, _auditSchemaHash, uint64(block.timestamp), tier, false);
        history[_circuitSourceHash].push(canonicalBuilds[_circuitSourceHash]);
        emit BuildPromoted(_circuitSourceHash, _receiptHash, _envHash, _tier, false, _auditSchemaHash, _stabilityIndex, block.timestamp);
        return true;
    }

    function getCanonicalBuild(bytes32 _circuitSourceHash) external view returns (Build memory) { require(canonicalBuilds[_circuitSourceHash].timestamp != 0, "no build"); return canonicalBuilds[_circuitSourceHash]; }
    function getHistory(bytes32 _circuitSourceHash) external view returns (Build[] memory) { return history[_circuitSourceHash]; }
    function getAuditSchemaHash() external pure returns (bytes32) { return keccak256(abi.encodePacked("veto-schema-v1.0")); }
    function _parseTier(string memory _tier) internal pure returns (Tier) {
        if (keccak256(bytes(_tier)) == keccak256("FULLY_DETERMINISTIC")) return Tier.FULLY_DETERMINISTIC;
        if (keccak256(bytes(_tier)) == keccak256("PARTIAL_DETERMINISTIC")) return Tier.PARTIAL_DETERMINISTIC;
        revert("invalid tier");
    }
}
