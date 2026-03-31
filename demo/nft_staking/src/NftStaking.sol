// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title NftStaking
 * @notice Time-locked NFT staking with ESDT reward accumulation.
 *
 * MultiversX mapping notes:
 *   - NFT payments:   #[payable('*')] with EsdtTokenPayment
 *   - Token return:   self.send().direct_esdt(caller, token_id, nonce, &BigUint::from(1u32))
 *   - Reward token:   custom ESDT; minted via self.send().esdt_local_mint(...)
 *   - block.timestamp → self.blockchain().get_block_timestamp()
 *
 * Each ERC-721 tokenId is globally unique, so we key the stake mapping by
 * tokenId alone (no nesting needed).  Ownership is verified on-chain via the
 * NFT payment itself.
 */
contract NftStaking {
    address public owner;
    uint256 public rewardRate;
    uint256 public lockPeriod;
    uint256 public totalStaked;

    // Struct stored per tokenId
    struct StakeInfo {
        address owner;
        uint256 stakedAt;
        bool active;
    }

    // tokenId => StakeInfo  (single-key mapping — NFT token IDs are globally unique)
    mapping(uint256 => StakeInfo) stakes;

    event Staked(address indexed user, uint256 indexed tokenId, uint256 timestamp);
    event Unstaked(address indexed user, uint256 indexed tokenId, uint256 timestamp);
    event RewardsClaimed(address indexed user, uint256 indexed tokenId, uint256 amount);

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    constructor() {
        owner = msg.sender;
        rewardRate = 100;
        lockPeriod = 86400;
        totalStaked = 0;
    }

    /**
     * @notice Stake an NFT.
     *
     * MultiversX: annotate with #[payable("*")] and read the NFT token/nonce
     * from self.call_value().single_esdt() instead of a uint256 tokenId param.
     */
    function stake(uint256 tokenId) public payable {
        require(tokenId > 0, "Invalid token ID");
        require(!stakes[tokenId].active, "Already staked");
        stakes[tokenId].owner = msg.sender;
        stakes[tokenId].stakedAt = block.timestamp;
        stakes[tokenId].active = true;
        totalStaked = totalStaked + 1;
        emit Staked(msg.sender, tokenId, block.timestamp);
    }

    /**
     * @notice Unstake an NFT after the lock period has elapsed.
     *
     * MultiversX: return the NFT via
     *   self.send().direct_esdt(&caller, &token_id, nonce, &BigUint::from(1u32))
     */
    function unstake(uint256 tokenId) public {
        require(stakes[tokenId].active, "Not staked");
        require(stakes[tokenId].owner == msg.sender, "Not your NFT");
        require(
            block.timestamp >= stakes[tokenId].stakedAt + lockPeriod,
            "Lock period not elapsed"
        );
        stakes[tokenId].active = false;
        totalStaked = totalStaked - 1;
        emit Unstaked(msg.sender, tokenId, block.timestamp);
    }

    /**
     * @notice Claim accumulated rewards.
     *         rewards = rewardRate * timeElapsed / 1 day
     *
     * MultiversX: mint reward ESDT via
     *   self.send().esdt_local_mint(&reward_token_id, 0, &rewards)
     *   self.send().direct_esdt(&caller, &reward_token_id, 0, &rewards)
     */
    function claimRewards(uint256 tokenId) public {
        require(stakes[tokenId].active, "Not staked");
        require(stakes[tokenId].owner == msg.sender, "Not your NFT");
        uint256 elapsed = block.timestamp - stakes[tokenId].stakedAt;
        uint256 rewards = rewardRate * elapsed / 86400;
        require(rewards > 0, "No rewards yet");
        stakes[tokenId].stakedAt = block.timestamp;
        emit RewardsClaimed(msg.sender, tokenId, rewards);
    }

    /**
     * @notice Returns the full StakeInfo for a given tokenId.
     */
    function getStakeInfo(uint256 tokenId) public view returns (bool active, uint256 stakedAt) {
        return (stakes[tokenId].active, stakes[tokenId].stakedAt);
    }

    /**
     * @notice Returns whether a given tokenId is currently staked.
     */
    function isStaked(uint256 tokenId) public view returns (bool) {
        return stakes[tokenId].active;
    }

    /**
     * @notice Update the per-day reward rate (owner only).
     */
    function setRewardRate(uint256 newRate) public onlyOwner {
        require(newRate > 0, "Rate must be positive");
        rewardRate = newRate;
    }

    /**
     * @notice Update the lock period in seconds (owner only).
     */
    function setLockPeriod(uint256 newPeriod) public onlyOwner {
        require(newPeriod > 0, "Period must be positive");
        lockPeriod = newPeriod;
    }
}
