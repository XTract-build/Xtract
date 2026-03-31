#![no_std]

use multiversx_sc::imports::*;

#[multiversx_sc::contract]
pub trait UsingForDirective {
    #[storage_mapper("result")]
    fn result(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[init]
    fn init(&self) {}

    #[endpoint]
    fn compute(&self, a: BigUint<Self::Api>, b: BigUint<Self::Api>) {
        self.result().set(&(a + b));
    }

}