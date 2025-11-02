// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Voting {
    address public chairperson;
    bool public hasVoted;
    uint256 public votedProposalId;
    uint256 public proposalVoteCount;
    uint256 public proposalCount;
    
    event ProposalCreated(uint256 indexed proposalId);
    event VoteCast(address indexed voter, uint256 indexed proposalId);
    
    constructor() {
        chairperson = msg.sender;
    }
    
    function addProposal() public {
        require(msg.sender == chairperson);
        proposalCount = proposalCount + 1;
        emit ProposalCreated(proposalCount - 1);
    }
    
    function vote(uint256 proposalId) public {
        require(proposalId < proposalCount);
        require(hasVoted == false);
        hasVoted = true;
        votedProposalId = proposalId;
        proposalVoteCount = proposalVoteCount + 1;
        emit VoteCast(msg.sender, proposalId);
    }
    
    function getProposalVoteCount() public view returns (uint256) {
        return proposalVoteCount;
    }
    
    function getProposalCount() public view returns (uint256) {
        return proposalCount;
    }
}
