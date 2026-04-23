// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

interface ISoulboundReceipt {
    function mintReceipt(address,uint256,uint8,uint8) external returns (uint256);
    function updateReceiptStatus(uint256,uint8) external;
}

contract AlabamaMachineSpeedProof {
    enum Status { None, Pending, Matched, Mismatched, Contested, HearingRequired }
    enum NodeClass { None, Government, Infrastructure, Civilian }
    enum LatencyTier { None, Green, Yellow, Orange, Red }

    struct Claim {
        bytes32 claimHash;
        address issuer;
        string metadataCID;
        uint64 issuedAt;
        Status status;
        LatencyTier latencyTier;
        bool issuerVerified;
        bool selmaValidated;
        uint64 lastReportAt;
        uint64 correctionDeadline;
        bool hearingTriggered;
        uint64 hearingBy;
    }

    struct ConsensusAccumulator {
        uint256 weightedMatches;
        uint256 totalWeight;
        bool govPresent;
        bool infraPresent;
        bool civilPresent;
        uint8 totalReports;
        bool finalized;
    }

    uint256 public claimCounter;
    mapping(uint256 => Claim) public claims;
    mapping(uint256 => ConsensusAccumulator) private accumulators;
    mapping(uint256 => mapping(address => bool)) public hasReported;
    mapping(bytes32 => bool) public claimHashUsed;

    mapping(address => NodeClass) public nodeClass;
    mapping(address => uint256) public nodeReliability;
    mapping(address => bool) public isIssuer;
    mapping(address => bool) public isNode;
    address public admin;
    address[] public selmaMirrors;

    ISoulboundReceipt public receiptContract;

    constructor(address _receiptContract) {
        admin = msg.sender;
        receiptContract = ISoulboundReceipt(_receiptContract);
    }

    modifier onlyAdmin() { require(msg.sender == admin); _; }
    modifier onlyNode() { require(isNode[msg.sender]); _; }
    modifier onlyIssuer() { require(isIssuer[msg.sender]); _; }

    function addIssuer(address issuer) external onlyAdmin { isIssuer[issuer]=true; }

    function addNode(address node, NodeClass c, uint256 r) external onlyAdmin {
        isNode[node]=true; nodeClass[node]=c; nodeReliability[node]=r;
    }

    function registerClaim(bytes32 claimHash, bytes calldata, bytes calldata, string calldata cid)
        external onlyIssuer returns (uint256 id)
    {
        require(!claimHashUsed[claimHash]);
        claimHashUsed[claimHash]=true;
        id = ++claimCounter;
        claims[id] = Claim(claimHash,msg.sender,cid,uint64(block.timestamp),Status.Pending,LatencyTier.None,true,false,0,0,false,0);
    }

    function submitBelowReport(uint256 id, NodeClass, bool isMatch, uint256, bytes calldata) external onlyNode {
        Claim storage c = claims[id];
        require(c.status==Status.Pending || c.status==Status.Contested);
        require(!hasReported[id][msg.sender]);

        hasReported[id][msg.sender]=true;
        ConsensusAccumulator storage acc = accumulators[id];

        uint256 w = nodeReliability[msg.sender];
        acc.totalWeight += w;
        if(isMatch) acc.weightedMatches += w;

        NodeClass cls = nodeClass[msg.sender];
        if(cls==NodeClass.Government) acc.govPresent=true;
        if(cls==NodeClass.Infrastructure) acc.infraPresent=true;
        if(cls==NodeClass.Civilian) acc.civilPresent=true;

        acc.totalReports++;

        if(acc.govPresent && acc.infraPresent && acc.civilPresent) {
            _tryFinalize(id);
        }
    }

    function _tryFinalize(uint256 id) internal {
        ConsensusAccumulator storage acc = accumulators[id];
        Claim storage c = claims[id];
        if(acc.finalized) return;

        uint256 score = acc.totalWeight==0 ? 0 : (acc.weightedMatches*10000)/acc.totalWeight;

        if(score>=8000) _finalize(id, Status.Matched);
        else if(score<=2000) _finalize(id, Status.Mismatched);
        else c.status = Status.Contested;
    }

    function _finalize(uint256 id, Status s) internal {
        Claim storage c = claims[id];
        accumulators[id].finalized = true;

        c.status = s;
        c.selmaValidated = true;

        uint64 e = uint64(block.timestamp)-c.issuedAt;
        if(e<=1 days) c.latencyTier=LatencyTier.Green;
        else if(e<=3 days) c.latencyTier=LatencyTier.Yellow;
        else if(e<=7 days) c.latencyTier=LatencyTier.Orange;
        else c.latencyTier=LatencyTier.Red;

        if(s==Status.Mismatched && c.latencyTier==LatencyTier.Red) {
            c.status = Status.HearingRequired;
            receiptContract.mintReceipt(c.issuer,id,uint8(Status.HearingRequired),uint8(c.latencyTier));
        } else {
            receiptContract.mintReceipt(c.issuer,id,uint8(s),uint8(c.latencyTier));
        }
    }
}
