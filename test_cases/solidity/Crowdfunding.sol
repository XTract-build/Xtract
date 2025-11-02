// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Crowdfunding {
    address public campaignCreator;
    uint256 public campaignGoal;
    uint256 public campaignPledged;
    bool public campaignClaimed;
    uint256 public count;
    
    event CampaignCreated(uint256 indexed id, address indexed creator, uint256 goal);
    event PledgeCreated(uint256 indexed id, address indexed pledger, uint256 amount);
    event Claimed(uint256 indexed id, address creator, uint256 amount);
    
    function createCampaign(uint256 goal) external returns (uint256) {
        count = count + 1;
        campaignCreator = msg.sender;
        campaignGoal = goal;
        campaignPledged = 0;
        campaignClaimed = false;
        emit CampaignCreated(count - 1, msg.sender, goal);
        return count - 1;
    }
    
    function pledge(uint256 amount) external {
        require(campaignClaimed == false);
        campaignPledged = campaignPledged + amount;
        emit PledgeCreated(count - 1, msg.sender, amount);
    }
    
    function claim() external {
        require(campaignCreator == msg.sender);
        require(campaignPledged >= campaignGoal);
        require(campaignClaimed == false);
        campaignClaimed = true;
        emit Claimed(count - 1, campaignCreator, campaignPledged);
    }
    
    function getCampaignCreator() external view returns (address) {
        return campaignCreator;
    }
    
    function getCampaignGoal() external view returns (uint256) {
        return campaignGoal;
    }
    
    function getCampaignPledged() external view returns (uint256) {
        return campaignPledged;
    }
    
    function getCampaignClaimed() external view returns (bool) {
        return campaignClaimed;
    }
}
