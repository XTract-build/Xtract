// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title DexTokenSwap
 * @notice Constant-product AMM DEX (x*y=k) with deposit/swap/withdraw.
 *
 * SafeMath note: Solidity 0.8+ has built-in overflow checks, so arithmetic
 * operators are safe by default (A6 library-inlining not required here).
 *
 * ReentrancyGuard: implemented via a `locked` boolean storage flag; the
 * nonReentrant modifier maps cleanly to MultiversX's sequential execution model.
 */
contract DexTokenSwap {
    address public owner;
    bool public locked;

    // Token reserves: token address => total deposited liquidity
    mapping(address => uint256) public reserves;
    // LP positions: token => provider => deposited amount
    mapping(address => mapping(address => uint256)) public balances;

    // ── Events ────────────────────────────────────────────────────────────────
    event Deposit(
        address indexed token,
        address indexed provider,
        uint256 amount
    );
    event Swap(
        address indexed tokenIn,
        address indexed tokenOut,
        address indexed trader,
        uint256 amountIn,
        uint256 amountOut
    );
    event Withdraw(
        address indexed token,
        address indexed provider,
        uint256 amount
    );

    // ── Modifiers ─────────────────────────────────────────────────────────────
    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    modifier nonReentrant() {
        require(!locked, "Reentrant call");
        locked = true;
        _;
        locked = false;
    }

    // ── Constructor ───────────────────────────────────────────────────────────
    constructor() {
        owner = msg.sender;
        locked = false;
    }

    // ── Liquidity ─────────────────────────────────────────────────────────────

    /**
     * @notice Deposit `amount` units of `token` into the pool.
     * On MultiversX this becomes a #[payable] ESDT endpoint.
     */
    function deposit(address token, uint256 amount) public nonReentrant {
        require(amount > 0, "Amount must be positive");
        reserves[token] = reserves[token] + amount;
        balances[token][msg.sender] = balances[token][msg.sender] + amount;
        emit Deposit(token, msg.sender, amount);
    }

    /**
     * @notice Remove `amount` units of `token` from the pool.
     * On MultiversX this becomes a #[payable] ESDT endpoint.
     */
    function withdraw(address token, uint256 amount) public nonReentrant {
        require(amount > 0, "Amount must be positive");
        require(balances[token][msg.sender] >= amount, "Insufficient balance");
        require(reserves[token] >= amount, "Insufficient reserve");
        balances[token][msg.sender] = balances[token][msg.sender] - amount;
        reserves[token] = reserves[token] - amount;
        emit Withdraw(token, msg.sender, amount);
    }

    // ── Swap ──────────────────────────────────────────────────────────────────

    /**
     * @notice Swap `amountIn` of `tokenIn` for `tokenOut` using x*y=k formula.
     * amountOut = (amountIn * reserveOut) / (reserveIn + amountIn)
     */
    function swap(
        address tokenIn,
        uint256 amountIn,
        address tokenOut
    ) public nonReentrant {
        require(amountIn > 0, "Invalid input amount");
        require(reserves[tokenIn] > 0, "No liquidity for tokenIn");
        require(reserves[tokenOut] > 0, "No liquidity for tokenOut");
        uint256 amountOut = (amountIn * reserves[tokenOut]) / (reserves[tokenIn] + amountIn);
        require(amountOut > 0, "Insufficient output amount");
        reserves[tokenIn] = reserves[tokenIn] + amountIn;
        reserves[tokenOut] = reserves[tokenOut] - amountOut;
        emit Swap(tokenIn, tokenOut, msg.sender, amountIn, amountOut);
    }

    // ── View ──────────────────────────────────────────────────────────────────

    /**
     * @notice Returns the spot price of tokenIn in terms of tokenOut, scaled by 1e18.
     * price = reserveOut * 1e18 / reserveIn
     */
    function getPrice(
        address tokenIn,
        address tokenOut
    ) public view returns (uint256) {
        require(reserves[tokenIn] > 0, "No liquidity for tokenIn");
        require(reserves[tokenOut] > 0, "No liquidity for tokenOut");
        return (reserves[tokenOut] * 1000000000000000000) / reserves[tokenIn];
    }

    /**
     * @notice Returns the reserve balance for a given token.
     */
    function getReserve(address token) public view returns (uint256) {
        return reserves[token];
    }
}
