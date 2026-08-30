// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract NodeBUptime {
    struct Attest { bytes32 root; uint256 start; uint256 end; uint256 outages; }
    mapping(uint256 => Attest) public epochs;
    event Attested(uint256 indexed month, bytes32 root, uint256 outages);

    function attestMonth(
        uint256 month,
        bytes32 root,
        uint256 startTs,
        uint256 endTs,
        uint256 outagesMinutes
    ) external {
        require(epochs[month].root == bytes32(0), "already set");
        epochs[month] = Attest(root, startTs, endTs, outagesMinutes);
        emit Attested(month, root, outagesMinutes);
    }
}
