#![no_std]

use multiversx_sc::imports::*;

#[multiversx_sc::contract]
pub trait SimpleStorage {
    #[storage_mapper("value")]
    fn value(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[init]
    fn init(&self) {}

    #[event("ValueChanged")]
    fn value_changed(&self, #[indexed] new_value: &BigUint<Self::Api>);
    #[endpoint(setValue)]
    fn set_value(&self, newValue: BigUint<Self::Api>) {
        self.value().set(&newValue);
        self.value_changed(&newValue)
    }
    #[view(getValue)]
    fn get_value(&self) -> BigUint<Self::Api> {
        self.value().get()
    }
}

