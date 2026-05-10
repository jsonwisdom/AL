// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title MigrationRelayerReputationOracle
/// @notice Receipt-bound relayer reputation oracle following REPUTATION_CORRECTION_DOCTRINE_V1
/// and ECONOMY_REPAIR_COST_DOCTRINE_V1.
/// @dev Money can support review costs. Money cannot restore relay authority.
contract MigrationRelayerReputationOracle {
    bytes32 public constant REJECT_TARGET_CONFIDENCE_PROMOTION =
        keccak256("TARGET_CONFIDENCE_PROMOTION");
    bytes32 public constant REJECT_RESTRAINT_FLAG_STRIPPED =
        keccak256("RESTRAINT_FLAG_STRIPPED");
    bytes32 public constant REJECT_RECEIPT_INTEGRITY_MISMATCH =
        keccak256("RECEIPT_INTEGRITY_MISMATCH");
    bytes32 public constant REJECT_CONCEALMENT_ESCALATION =
        keccak256("CONCEALMENT_ESCALATION");

    uint64 public constant DEFAULT_CHALLENGE_WINDOW = 48 hours;
    uint64 public constant DEFAULT_INTEGRITY_COOLDOWN = 7 days;
    uint64 public constant DEFAULT_CONCEALMENT_COOLDOWN = 30 days;

    address public immutable auditCommittee;

    enum PenaltyState {
        NONE,
        NEUTRAL_PENDING_REPLAY,
        REPAIR_SUBMITTED,
        REPAIR_REPLAYED,
        REPAIR_VERIFIED,
        REPAIR_REJECTED,
        CONCEALMENT_CONFIRMED
    }

    struct RelayerRecord {
        uint256 promotionAttempts;
        uint256 integrityViolations;
        uint256 concealedViolations;
        uint64 suspendedUntil;
        bytes32 latestPenaltyId;
    }

    struct PenaltyReceipt {
        bytes32 sourceWitnessHash;
        bytes32 rejectCode;
        address relayer;
        uint64 observedAt;
        uint64 challengeWindowEndsAt;
        uint64 suspensionEndsAt;
        bytes32 repairProofHash;
        bytes32 replayProofHash;
        uint256 stake;
        PenaltyState state;
        bool stakeSlashed;
    }

    mapping(address => RelayerRecord) public relayers;
    mapping(bytes32 => PenaltyReceipt) public penalties;
    mapping(bytes32 => uint256) public stakes;

    event PenaltyRecorded(
        bytes32 indexed penaltyId,
        address indexed relayer,
        bytes32 indexed rejectCode,
        bytes32 sourceWitnessHash
    );
    event RepairSubmitted(bytes32 indexed penaltyId, address indexed relayer, bytes32 indexed proofHash);
    event ReplayProofSubmitted(bytes32 indexed penaltyId, address indexed relayer, bytes32 indexed replayProofHash);
    event RepairVerified(bytes32 indexed penaltyId, address indexed relayer, bytes32 indexed replayProofHash);
    event RepairRejected(bytes32 indexed penaltyId, address indexed relayer, bytes32 reasonHash);
    event RelayerSuspended(address indexed relayer, bytes32 indexed reason, uint64 untilTimestamp);
    event StakeDeposited(bytes32 indexed penaltyId, address indexed relayer, uint256 amount);
    event StakeRefunded(bytes32 indexed penaltyId, address indexed relayer, uint256 amount);
    event StakeSlashed(bytes32 indexed penaltyId, address indexed relayer, uint256 amount);

    error Unauthorized();
    error ZeroAuditCommittee();
    error UnknownPenalty();
    error WrongRelayer();
    error ProofMismatch();
    error ReplayProofRequired();
    error AlreadyVerified();
    error InvalidState();
    error TransferFailed();

    modifier onlyAuditCommittee() {
        if (msg.sender != auditCommittee) revert Unauthorized();
        _;
    }

    constructor(address auditCommittee_) {
        if (auditCommittee_ == address(0)) revert ZeroAuditCommittee();
        auditCommittee = auditCommittee_;
    }

    function ingestFailClosed(
        bytes32 sourceWitnessHash,
        bytes32 rejectCode,
        address relayer
    ) external returns (bytes32 penaltyId) {
        penaltyId = keccak256(abi.encodePacked(
            sourceWitnessHash,
            rejectCode,
            relayer,
            block.chainid,
            address(this),
            block.timestamp
        ));

        PenaltyReceipt storage p = penalties[penaltyId];
        p.sourceWitnessHash = sourceWitnessHash;
        p.rejectCode = rejectCode;
        p.relayer = relayer;
        p.observedAt = uint64(block.timestamp);
        p.challengeWindowEndsAt = uint64(block.timestamp) + DEFAULT_CHALLENGE_WINDOW;
        p.state = PenaltyState.NEUTRAL_PENDING_REPLAY;

        RelayerRecord storage r = relayers[relayer];
        r.latestPenaltyId = penaltyId;

        if (rejectCode == REJECT_TARGET_CONFIDENCE_PROMOTION) {
            r.promotionAttempts++;
            p.suspensionEndsAt = uint64(block.timestamp) + DEFAULT_INTEGRITY_COOLDOWN;
            r.suspendedUntil = _max64(r.suspendedUntil, p.suspensionEndsAt);
            emit RelayerSuspended(relayer, rejectCode, p.suspensionEndsAt);
        } else if (
            rejectCode == REJECT_RESTRAINT_FLAG_STRIPPED ||
            rejectCode == REJECT_RECEIPT_INTEGRITY_MISMATCH
        ) {
            r.integrityViolations++;
            if (r.integrityViolations >= 2) {
                p.suspensionEndsAt = uint64(block.timestamp) + DEFAULT_INTEGRITY_COOLDOWN;
                r.suspendedUntil = _max64(r.suspendedUntil, p.suspensionEndsAt);
                emit RelayerSuspended(relayer, rejectCode, p.suspensionEndsAt);
            }
        }

        emit PenaltyRecorded(penaltyId, relayer, rejectCode, sourceWitnessHash);
    }

    /// @notice Optional stake/bond for external review cost. This never restores authority.
    function depositStake(bytes32 penaltyId) external payable {
        PenaltyReceipt storage p = penalties[penaltyId];
        if (p.relayer == address(0)) revert UnknownPenalty();
        if (p.relayer != msg.sender) revert WrongRelayer();
        if (p.stakeSlashed) revert InvalidState();

        p.stake += msg.value;
        stakes[penaltyId] += msg.value;
        emit StakeDeposited(penaltyId, msg.sender, msg.value);
    }

    function submitRepair(bytes32 penaltyId, bytes32 repairProofHash, bytes32 replayProofHash) external {
        PenaltyReceipt storage p = penalties[penaltyId];
        if (p.relayer == address(0)) revert UnknownPenalty();
        if (p.relayer != msg.sender) revert WrongRelayer();
        if (p.state == PenaltyState.REPAIR_VERIFIED) revert AlreadyVerified();
        if (replayProofHash == bytes32(0)) revert ReplayProofRequired();

        p.repairProofHash = repairProofHash;
        p.replayProofHash = replayProofHash;
        p.state = PenaltyState.REPAIR_REPLAYED;

        emit RepairSubmitted(penaltyId, msg.sender, repairProofHash);
        emit ReplayProofSubmitted(penaltyId, msg.sender, replayProofHash);
    }

    /// @notice Only replay-verified repair can restore role capability.
    function verifyRepair(bytes32 penaltyId, bytes32 repairProofHash, bytes32 replayProofHash)
        external
        onlyAuditCommittee
    {
        PenaltyReceipt storage p = penalties[penaltyId];
        if (p.relayer == address(0)) revert UnknownPenalty();
        if (p.state == PenaltyState.REPAIR_VERIFIED) revert AlreadyVerified();
        if (replayProofHash == bytes32(0)) revert ReplayProofRequired();
        if (p.repairProofHash != repairProofHash) revert ProofMismatch();
        if (p.replayProofHash != replayProofHash) revert ProofMismatch();

        p.state = PenaltyState.REPAIR_VERIFIED;
        p.suspensionEndsAt = uint64(block.timestamp);

        RelayerRecord storage r = relayers[p.relayer];
        if (r.suspendedUntil <= block.timestamp + DEFAULT_INTEGRITY_COOLDOWN) {
            r.suspendedUntil = uint64(block.timestamp);
        }

        emit RepairVerified(penaltyId, p.relayer, replayProofHash);
    }

    function rejectRepair(bytes32 penaltyId, bytes32 reasonHash) external onlyAuditCommittee {
        PenaltyReceipt storage p = penalties[penaltyId];
        if (p.relayer == address(0)) revert UnknownPenalty();
        p.state = PenaltyState.REPAIR_REJECTED;
        emit RepairRejected(penaltyId, p.relayer, reasonHash);
    }

    function reportConcealment(bytes32 penaltyId, uint256 concealedCount) external onlyAuditCommittee {
        PenaltyReceipt storage p = penalties[penaltyId];
        if (p.relayer == address(0)) revert UnknownPenalty();

        RelayerRecord storage r = relayers[p.relayer];
        r.concealedViolations += concealedCount;
        p.state = PenaltyState.CONCEALMENT_CONFIRMED;

        uint64 untilTimestamp = uint64(block.timestamp) + DEFAULT_CONCEALMENT_COOLDOWN;
        p.suspensionEndsAt = untilTimestamp;
        r.suspendedUntil = _max64(r.suspendedUntil, untilTimestamp);

        if (p.stake > 0 && !p.stakeSlashed) {
            uint256 amount = p.stake;
            p.stake = 0;
            stakes[penaltyId] = 0;
            p.stakeSlashed = true;
            emit StakeSlashed(penaltyId, p.relayer, amount);
        }

        emit RelayerSuspended(p.relayer, REJECT_CONCEALMENT_ESCALATION, untilTimestamp);
    }

    function refundStake(bytes32 penaltyId) external onlyAuditCommittee {
        PenaltyReceipt storage p = penalties[penaltyId];
        if (p.relayer == address(0)) revert UnknownPenalty();
        if (p.stakeSlashed || p.stake == 0) revert InvalidState();
        if (p.state != PenaltyState.REPAIR_VERIFIED) revert InvalidState();

        uint256 amount = p.stake;
        p.stake = 0;
        stakes[penaltyId] = 0;

        (bool ok, ) = p.relayer.call{value: amount}("");
        if (!ok) revert TransferFailed();

        emit StakeRefunded(penaltyId, p.relayer, amount);
    }

    /// @notice There is intentionally no payToRestoreRole function.
    function canRelay(address relayer) external view returns (bool) {
        return block.timestamp >= relayers[relayer].suspendedUntil;
    }

    function _max64(uint64 a, uint64 b) internal pure returns (uint64) {
        return a >= b ? a : b;
    }
}
