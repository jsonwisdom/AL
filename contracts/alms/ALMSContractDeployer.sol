// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/// @title ALMS Contract Deployer Registry
/// @notice Tracks verified contract deployments and external domain anchors (e.g., SAM.gov)
contract ALMSContractDeployer {

    struct Deployment {
        address deployer;
        address contractAddress;
        uint256 chainId;
        bytes32 sourceHash; // hash of GitHub commit or manifest
        string domain; // e.g., "sam.gov"
        string externalId; // SAM.gov entity ID or similar
        uint256 timestamp;
    }

    mapping(bytes32 => Deployment) public deployments; // key = keccak(txHash)

    event ContractRegistered(
        bytes32 indexed txKey,
        address indexed contractAddress,
        address indexed deployer,
        uint256 chainId,
        string domain
    );

    function registerDeployment(
        bytes32 txKey,
        address contractAddress,
        uint256 chainId,
        bytes32 sourceHash,
        string calldata domain,
        string calldata externalId
    ) external {
        require(deployments[txKey].contractAddress == address(0), "already registered");

        deployments[txKey] = Deployment({
            deployer: msg.sender,
            contractAddress: contractAddress,
            chainId: chainId,
            sourceHash: sourceHash,
            domain: domain,
            externalId: externalId,
            timestamp: block.timestamp
        });

        emit ContractRegistered(txKey, contractAddress, msg.sender, chainId, domain);
    }
}
