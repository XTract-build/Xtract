#![no_std]

use multiversx_sc::imports::*;

#[multiversx_sc::contract]
pub trait SafeMathUsage {
    #[storage_mapper("total")]
    fn total(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[init]
    fn init(&self) {}

    #[endpoint]
    fn add_values(&self, a: BigUint<Self::Api>, b: BigUint<Self::Api>) {
        self.total().set(&(a + b));
    }

    #[endpoint]
    fn sub_values(&self, a: BigUint<Self::Api>, b: BigUint<Self::Api>) {
        self.total().set(&(a - b));
    }

}