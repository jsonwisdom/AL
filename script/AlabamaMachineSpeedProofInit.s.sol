// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

import "forge-std/Script.sol";
import "../src/AlabamaMachineSpeedProof.sol";

contract AlabamaMachineSpeedProofInit is Script {
    function run() external {
        uint256 key = vm.envUint("DEPLOYER_PRIVATE_KEY");
        vm.startBroadcast(key);

        AlabamaMachineSpeedProof proof = new AlabamaMachineSpeedProof(address(0));

        vm.stopBroadcast();
    }
}
