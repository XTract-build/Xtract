#![no_std]

use multiversx_sc::imports::*;

#[derive(TypeAbi, TopEncode, TopDecode, NestedEncode, NestedDecode, ManagedVecItem)]
pub struct Listing<M: ManagedTypeApi> {
    pub price: BigUint<M>,
    pub active: bool
}

#[multiversx_sc::contract]
pub trait StructFieldUpdate {
    #[storage_mapper("listings")]
    fn listings(&self, key: &ManagedAddress<Self::Api>) -> SingleValueMapper<Listing>;

    #[init]
    fn init(&self) {}

    #[endpoint]
    fn activate(&self, seller: ManagedAddress<Self::Api>) {
        let mut s = self.listings(&seller).get();
        s.active = true;
        self.listings(&seller).set(&s);
    }

    #[endpoint]
    fn set_price(&self, seller: ManagedAddress<Self::Api>, newPrice: BigUint<Self::Api>) {
        let mut s = self.listings(&seller).get();
        s.price = newPrice;
        self.listings(&seller).set(&s);
    }

}