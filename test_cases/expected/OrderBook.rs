#![no_std]

use multiversx_sc::imports::*;

#[multiversx_sc::contract]
pub trait OrderBook {
    #[storage_mapper("owner")]
    fn owner(&self) -> SingleValueMapper<ManagedAddress<Self::Api>>;

    #[storage_mapper("orderCount")]
    fn order_count(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("orderOwner")]
    fn order_owner(&self, key: &BigUint<Self::Api>) -> SingleValueMapper<ManagedAddress<Self::Api>>;

    #[storage_mapper("orderAmount")]
    fn order_amount(&self, key: &BigUint<Self::Api>) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("orderActive")]
    fn order_active(&self, key: &BigUint<Self::Api>) -> SingleValueMapper<bool>;

    #[event("OrderCreated")]
    fn order_created_event(&self, #[indexed] orderId: &BigUint<Self::Api>, #[indexed] creator: &ManagedAddress<Self::Api>, amount: &BigUint<Self::Api>);

    #[event("OrderCancelled")]
    fn order_cancelled_event(&self, #[indexed] orderId: &BigUint<Self::Api>);

    #[event("OrderFilled")]
    fn order_filled_event(&self, #[indexed] orderId: &BigUint<Self::Api>, #[indexed] filler: &ManagedAddress<Self::Api>);

    #[init]
    fn init(&self) {
        self.owner().set(&(self.blockchain().get_caller()));
        self.order_count().set(&(BigUint::zero()));
    }

    #[endpoint]
    fn create_order(&self, amount: BigUint<Self::Api>) {
        require!(amount > BigUint::zero(), "Invalid amount");
        self.order_count().set(&(self.order_count().get() + BigUint::from(1u32)));
        self.order_owner(&self.order_count().get()).set(self.blockchain().get_caller());
        self.order_amount(&self.order_count().get()).set(amount);
        self.order_active(&self.order_count().get()).set(true);
        self.order_created_event(&self.order_count().get(), &self.blockchain().get_caller(), &amount.clone());
    }

    #[endpoint]
    fn cancel_order(&self, orderId: BigUint<Self::Api>) {
        require!(self.order_owner(&orderId).get() == self.blockchain().get_caller(), "Not order owner");
        require!(self.order_active(&orderId).get(), "Order not active");
        self.order_active(&orderId).set(false);
        self.order_cancelled_event(&orderId);
    }

    #[endpoint]
    fn fill_order(&self, orderId: BigUint<Self::Api>) {
        require!(self.order_active(&orderId).get(), "Order not active");
        self.order_active(&orderId).set(false);
        self.order_filled_event(&orderId, &self.blockchain().get_caller());
    }

    #[view(getOrderAmount)]
    fn get_order_amount(&self, orderId: BigUint<Self::Api>) -> BigUint<Self::Api> {
        return self.order_amount(&orderId).get();
    }

}