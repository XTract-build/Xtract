#![no_std]

use multiversx_sc::imports::*;

#[multiversx_sc::contract]
pub trait Escrow {
    #[storage_mapper("buyer")]
    fn buyer(&self) -> SingleValueMapper<ManagedAddress<Self::Api>>;

    #[storage_mapper("seller")]
    fn seller(&self) -> SingleValueMapper<ManagedAddress<Self::Api>>;

    #[storage_mapper("arbiter")]
    fn arbiter(&self) -> SingleValueMapper<ManagedAddress<Self::Api>>;

    #[storage_mapper("amount")]
    fn amount(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("released")]
    fn released(&self) -> SingleValueMapper<bool>;

    #[storage_mapper("refunded")]
    fn refunded(&self) -> SingleValueMapper<bool>;

    #[event("Deposited")]
    fn deposited_event(&self, #[indexed] buyer: &ManagedAddress<Self::Api>, amount: &BigUint<Self::Api>);

    #[event("Released")]
    fn released_event(&self, #[indexed] seller: &ManagedAddress<Self::Api>, amount: &BigUint<Self::Api>);

    #[event("Refunded")]
    fn refunded_event(&self, #[indexed] buyer: &ManagedAddress<Self::Api>, amount: &BigUint<Self::Api>);

    #[init]
    fn init(&self) {
        self.buyer().set(&(self.blockchain().get_caller()));
        self.released().set(&false);
        self.refunded().set(&false);
    }

    #[endpoint]
    fn set_seller(&self, _seller: ManagedAddress<Self::Api>) {
        require!(self.blockchain().get_caller() == self.buyer().get(), "Only buyer");
        self.seller().set(&_seller);
    }

    #[endpoint]
    fn set_arbiter(&self, _arbiter: ManagedAddress<Self::Api>) {
        require!(self.blockchain().get_caller() == self.buyer().get(), "Only buyer");
        self.arbiter().set(&_arbiter);
    }

    #[endpoint]
    fn deposit(&self, _amount: BigUint<Self::Api>) {
        require!(self.blockchain().get_caller() == self.buyer().get(), "Only buyer");
        require!(!self.released().get(), "Already released");
        require!(!self.refunded().get(), "Already refunded");
        self.amount().set(&_amount);
        self.deposited_event(&self.buyer().get(), &_amount.clone());
    }

    #[endpoint]
    fn release(&self) {
        require!(self.blockchain().get_caller() == self.buyer().get(), "Only buyer");
        require!(!self.released().get(), "Already released");
        require!(!self.refunded().get(), "Already refunded");
        self.released().set(&true);
        self.released_event(&self.seller().get(), &self.amount().get());
    }

    #[endpoint]
    fn refund(&self) {
        require!(self.blockchain().get_caller() == self.arbiter().get(), "Only arbiter");
        require!(!self.released().get(), "Already released");
        require!(!self.refunded().get(), "Already refunded");
        self.refunded().set(&true);
        self.refunded_event(&self.buyer().get(), &self.amount().get());
    }

}