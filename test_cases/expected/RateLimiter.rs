#![no_std]

use multiversx_sc::imports::*;

#[multiversx_sc::contract]
pub trait RateLimiter {
    #[storage_mapper("owner")]
    fn owner(&self) -> SingleValueMapper<ManagedAddress<Self::Api>>;

    #[storage_mapper("limit")]
    fn limit(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("window")]
    fn window(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("lastAction")]
    fn last_action(&self, key: &ManagedAddress<Self::Api>) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("actionCount")]
    fn action_count(&self, key: &ManagedAddress<Self::Api>) -> SingleValueMapper<BigUint<Self::Api>>;

    #[event("ActionPerformed")]
    fn action_performed_event(&self, #[indexed] user: &ManagedAddress<Self::Api>, count: &BigUint<Self::Api>);

    #[event("LimitUpdated")]
    fn limit_updated_event(&self, #[indexed] oldLimit: &BigUint<Self::Api>, #[indexed] newLimit: &BigUint<Self::Api>);

    #[event("WindowUpdated")]
    fn window_updated_event(&self, #[indexed] oldWindow: &BigUint<Self::Api>, #[indexed] newWindow: &BigUint<Self::Api>);

    #[init]
    fn init(&self) {
        self.owner().set(&(self.blockchain().get_caller()));
        self.limit().set(&(BigUint::from(10u32)));
        self.window().set(&(BigUint::from(3600u32)));
    }

    #[endpoint]
    fn perform_action(&self) {
        require!(self.action_count(&self.blockchain().get_caller()) < self.limit().get(), "Rate limit exceeded");
        self.action_count(&self.blockchain().get_caller()).set(self.action_count(&self.blockchain().get_caller()) + BigUint::from(1u32));
        self.last_action(&self.blockchain().get_caller()).set(self.blockchain().get_block_timestamp());
        self.action_performed_event(&self.blockchain().get_caller(), &self.action_count(&self.blockchain().get_caller()));
    }

    #[endpoint]
    fn reset_limit(&self, user: ManagedAddress<Self::Api>) {
        require!(self.blockchain().get_caller() == owner, "Not owner");
        self.action_count(&user).set(BigUint::zero());
    }

    #[endpoint]
    fn set_limit(&self, newLimit: BigUint<Self::Api>) {
        require!(self.blockchain().get_caller() == owner, "Not owner");
        self.limit_updated_event(&self.limit().get(), &newLimit);
        self.limit().set(&newLimit);
    }

    #[endpoint]
    fn set_window(&self, newWindow: BigUint<Self::Api>) {
        require!(self.blockchain().get_caller() == owner, "Not owner");
        self.window_updated_event(&self.window().get(), &newWindow);
        self.window().set(&newWindow);
    }

    #[view(getActionCount)]
    fn get_action_count(&self, user: ManagedAddress<Self::Api>) -> BigUint<Self::Api> {
        return self.action_count(&user).get();
    }

}