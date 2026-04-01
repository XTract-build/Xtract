// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

/**
 * @title Subscription
 * @notice Recurring-payment / SaaS subscription contract.
 *
 * Services register themselves and define Plans (price + duration).
 * Users subscribe to a plan by paying the plan price; they can renew before
 * or after expiry and cancel at any time (no refund).  Service owners
 * accumulate payments on-chain and withdraw at will.
 *
 * block.timestamp is used for expiry arithmetic — maps cleanly to
 * MultiversX's get_block_timestamp() call.
 */
contract Subscription {
    address public owner;

    // ── Data structures ────────────────────────────────────────────────────────

    struct Plan {
        uint256 price;      // required EGLD/token amount
        uint256 duration;   // seconds a single payment covers
        bool active;        // owner can deactivate without deleting
    }

    struct SubscriptionRecord {
        uint256 expiresAt;  // Unix timestamp
        uint256 planId;     // index into servicePlans[service]
        bool cancelled;     // once cancelled, cannot be renewed
    }

    // ── Storage ────────────────────────────────────────────────────────────────

    // service address → ordered list of Plans
    mapping(address => Plan[]) public servicePlans;
    // user → service → active subscription
    mapping(address => mapping(address => SubscriptionRecord)) public subscriptions;
    // service → total unclaimed payments
    mapping(address => uint256) public serviceBalance;
    // service → its registered owner (set at registerService time)
    mapping(address => address) public serviceOwner;

    // ── Events ─────────────────────────────────────────────────────────────────

    event Subscribed(address indexed user, address indexed service, uint256 planId, uint256 expiresAt);
    event Renewed(address indexed user, address indexed service, uint256 newExpiresAt);
    event Cancelled(address indexed user, address indexed service);
    event Withdrawn(address indexed service, address indexed serviceOwner, uint256 amount);

    // ── Modifiers ──────────────────────────────────────────────────────────────

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    modifier onlyServiceOwner(address service) {
        require(msg.sender == serviceOwner[service], "Not service owner");
        _;
    }

    // ── Constructor ────────────────────────────────────────────────────────────

    constructor() {
        owner = msg.sender;
    }

    // ── Service management ─────────────────────────────────────────────────────

    /**
     * @notice Register a new service.  The caller becomes the service owner.
     */
    function registerService(address service) public {
        require(serviceOwner[service] == address(0), "Service already registered");
        serviceOwner[service] = msg.sender;
    }

    /**
     * @notice Add a subscription plan to a service.
     * @param service   The service address (must be registered by caller).
     * @param price     Amount users must pay to subscribe (in wei).
     * @param duration  How long the subscription lasts (in seconds).
     */
    function addPlan(address service, uint256 price, uint256 duration) public onlyServiceOwner(service) {
        require(price > 0, "Price must be positive");
        require(duration > 0, "Duration must be positive");
        servicePlans[service].push(Plan({ price: price, duration: duration, active: true }));
    }

    /**
     * @notice Deactivate a plan so no new subscriptions can be created for it.
     */
    function deactivatePlan(address service, uint256 planId) public onlyServiceOwner(service) {
        require(planId < servicePlans[service].length, "Invalid plan");
        servicePlans[service][planId].active = false;
    }

    // ── Subscription lifecycle ─────────────────────────────────────────────────

    /**
     * @notice Subscribe to a plan.  Caller must send exactly plan.price in ETH.
     * @param service  Service address.
     * @param planId   Plan index within servicePlans[service].
     */
    function subscribe(address service, uint256 planId) public payable {
        require(planId < servicePlans[service].length, "Invalid plan");
        Plan storage plan = servicePlans[service][planId];
        require(plan.active, "Plan not active");
        require(msg.value >= plan.price, "Insufficient payment");

        uint256 expiresAt = block.timestamp + plan.duration;
        subscriptions[msg.sender][service] = SubscriptionRecord({
            expiresAt: expiresAt,
            planId: planId,
            cancelled: false
        });
        serviceBalance[service] = serviceBalance[service] + msg.value;
        emit Subscribed(msg.sender, service, planId, expiresAt);
    }

    /**
     * @notice Renew an existing subscription.
     * If the current subscription has not expired, the new expiry extends from
     * the current expiresAt; otherwise it extends from block.timestamp.
     */
    function renew(address service) public payable {
        SubscriptionRecord storage sub = subscriptions[msg.sender][service];
        require(!sub.cancelled, "Subscription cancelled");
        Plan storage plan = servicePlans[service][sub.planId];
        require(plan.active, "Plan not active");
        require(msg.value >= plan.price, "Insufficient payment");

        uint256 base = sub.expiresAt > block.timestamp ? sub.expiresAt : block.timestamp;
        sub.expiresAt = base + plan.duration;
        serviceBalance[service] = serviceBalance[service] + msg.value;
        emit Renewed(msg.sender, service, sub.expiresAt);
    }

    /**
     * @notice Cancel subscription immediately.  No refund is issued.
     */
    function cancel(address service) public {
        SubscriptionRecord storage sub = subscriptions[msg.sender][service];
        require(!sub.cancelled, "Already cancelled");
        sub.cancelled = true;
        emit Cancelled(msg.sender, service);
    }

    // ── Views ──────────────────────────────────────────────────────────────────

    /**
     * @notice Returns true if `user` has an active (non-cancelled, non-expired)
     * subscription to `service`.
     */
    function isActive(address user, address service) public view returns (bool) {
        SubscriptionRecord storage sub = subscriptions[user][service];
        return !sub.cancelled && sub.expiresAt > block.timestamp;
    }

    /**
     * @notice Returns the number of plans registered for a service.
     */
    function planCount(address service) public view returns (uint256) {
        return servicePlans[service].length;
    }

    // ── Withdrawal ─────────────────────────────────────────────────────────────

    /**
     * @notice Service owner withdraws all accumulated subscription payments.
     */
    function withdraw(address service) public onlyServiceOwner(service) {
        uint256 amount = serviceBalance[service];
        require(amount > 0, "Nothing to withdraw");
        serviceBalance[service] = 0;
        emit Withdrawn(service, msg.sender, amount);
    }
}
