// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title DaoGovernance
 * @notice On-chain proposal voting with quorum enforcement and time-lock execution.
 *
 * MultiversX notes:
 *   - string params map to ManagedBuffer (UTF-8 encoded on MultiversX)
 *   - bytes calldata → ManagedBuffer; cross-contract execute → typed contract call
 *   - block.timestamp → self.blockchain().get_block_timestamp()
 *   - Nested mapping hasVoted stored as two-key SingleValueMapper (A2 dynamic detection)
 *   - Struct field updates use A5 load-mutate-store pattern
 */
contract DaoGovernance {
    address public owner;
    uint256 public proposalCount;
    uint256 public quorum;
    uint256 public votingDuration;

    struct Proposal {
        uint256 id;
        string description;
        uint256 voteCount;
        uint256 against;
        bool executed;
        uint256 deadline;
    }

    // proposalId => Proposal  (A5 struct-field-update pattern)
    mapping(uint256 => Proposal) proposals;

    // proposalId => voter => voted  (A2 nested-mapping; two-key SingleValueMapper)
    mapping(uint256 => mapping(address => bool)) hasVoted;

    event ProposalCreated(uint256 indexed id, address indexed proposer, uint256 deadline);
    event VoteCast(uint256 indexed proposalId, address indexed voter, bool support);
    event ProposalExecuted(uint256 indexed proposalId);

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    modifier onlyAfterDeadline(uint256 proposalId) {
        require(block.timestamp > proposals[proposalId].deadline, "Voting still open");
        _;
    }

    constructor() {
        owner = msg.sender;
        proposalCount = 0;
        quorum = 3;
        votingDuration = 86400;
    }

    /**
     * @notice Create a new governance proposal.
     * @param description  Human-readable description (maps to ManagedBuffer on MultiversX).
     * @return id          Unique proposal ID.
     *
     * Note: Solidity uses `string memory description` for storage location; the
     * transpiler reads type=string, name=description when the memory keyword is omitted.
     */
    function createProposal(string description) public returns (uint256) {
        proposalCount = proposalCount + 1;
        uint256 id = proposalCount;
        uint256 deadline = block.timestamp + votingDuration;
        proposals[id].id = id;
        proposals[id].voteCount = 0;
        proposals[id].against = 0;
        proposals[id].executed = false;
        proposals[id].deadline = deadline;
        emit ProposalCreated(id, msg.sender, deadline);
        return id;
    }

    /**
     * @notice Cast a vote for or against a proposal.
     *
     * Pattern tested:
     *   proposals[proposalId].voteCount = proposals[proposalId].voteCount + 1
     *   → A5 load-mutate-store for struct field inside mapping
     *
     *   hasVoted[proposalId][msg.sender] = true
     *   → two-key mapping write (stored as nested SingleValueMapper on MultiversX)
     */
    function vote(uint256 proposalId, bool support) public {
        require(proposalId > 0, "Invalid proposal");
        require(block.timestamp <= proposals[proposalId].deadline, "Voting closed");
        require(!hasVoted[proposalId][msg.sender], "Already voted");
        hasVoted[proposalId][msg.sender] = true;
        if (support) {
            proposals[proposalId].voteCount = proposals[proposalId].voteCount + 1;
        } else {
            proposals[proposalId].against = proposals[proposalId].against + 1;
        }
        emit VoteCast(proposalId, msg.sender, support);
    }

    /**
     * @notice Execute an approved proposal after its deadline.
     *         On MultiversX replace the low-level call with a typed contract call.
     */
    function execute(uint256 proposalId) public onlyAfterDeadline(proposalId) {
        require(!proposals[proposalId].executed, "Already executed");
        require(proposals[proposalId].voteCount >= quorum, "Quorum not reached");
        proposals[proposalId].executed = true;
        emit ProposalExecuted(proposalId);
    }

    /**
     * @notice Returns the vote counts and execution status of a proposal.
     */
    function getVoteCount(uint256 id) public view returns (uint256) {
        return proposals[id].voteCount;
    }

    /**
     * @notice Returns the full deadline timestamp for a proposal.
     */
    function getDeadline(uint256 id) public view returns (uint256) {
        return proposals[id].deadline;
    }

    /**
     * @notice Returns whether a voter has already voted on a proposal.
     */
    function didVote(uint256 proposalId, address voter) public view returns (bool) {
        return hasVoted[proposalId][voter];
    }

    /**
     * @notice Update the quorum threshold (owner only).
     */
    function setQuorum(uint256 newQuorum) public onlyOwner {
        require(newQuorum > 0, "Quorum must be positive");
        quorum = newQuorum;
    }
}
