#![no_std]

use multiversx_sc::imports::*;
use multiversx_sc::derive_imports::*;

#[multiversx_sc::contract]
pub trait SimpleStorage {
    #[storage_mapper("value")]
    fn value(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[event("ValueChanged")]
    fn value_changed_event(&self, #[indexed] newValue: BigUint<Self::Api>);

    #[init]
    fn init(&self) {}

    #[endpoint]
    fn set_value(&self, newValue: BigUint<Self::Api>) {
        self.value().set(newValue);
        self.value_changed_event(newValue);
    }

    #[view(getValue)]
    fn get_value(&self) -> BigUint<Self::Api> {
        return self.value().get();
    }

}