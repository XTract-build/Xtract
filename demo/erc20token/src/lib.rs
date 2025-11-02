#![no_std]

use multiversx_sc::imports::*;

#[multiversx_sc::contract]
pub trait ERC20Token {
    #[storage_mapper("totalSupply")]
    fn total_supply(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("balance")]
    fn balance(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[event("Transfer")]
    fn transfer_event(&self, #[indexed] from: &ManagedAddress<Self::Api>, #[indexed] to: &ManagedAddress<Self::Api>, value: &BigUint<Self::Api>);

    #[init]
    fn init(&self) {
        self.total_supply().set(&(BigUint::from(10u32).pow(24)));
        self.balance().set(&(self.total_supply().get()));
    }

    #[endpoint]
    fn transfer(&self, _to: ManagedAddress<Self::Api>, _value: BigUint<Self::Api>) -> bool {
        require!(self.balance().get() >= _value, "Requirement not met");
        self.balance().set(&(self.balance().get() - _value.clone()));
        self.transfer_event(&self.blockchain().get_caller(), &_to.clone(), &_value.clone());
        true
    }

}