#![no_std]

use multiversx_sc::imports::*;

#[multiversx_sc::contract]
pub trait DeleteOp {
    #[storage_mapper("counter")]
    fn counter(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("allowance")]
    fn allowance(&self, key1: &ManagedAddress<Self::Api>, key2: &ManagedAddress<Self::Api>) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("balances")]
    fn balances(&self, key: &ManagedAddress<Self::Api>) -> SingleValueMapper<BigUint<Self::Api>>;

    #[init]
    fn init(&self) {}

    #[endpoint]
    fn reset_counter(&self) {
        self.counter().clear();
    }

    #[endpoint]
    fn reset_balance(&self, user: ManagedAddress<Self::Api>) {
        self.balances(&user).clear();
    }

    #[endpoint]
    fn reset_allowance(&self, owner: ManagedAddress<Self::Api>, spender: ManagedAddress<Self::Api>) {
        self.allowance(&owner, &spender).clear();
    }

}