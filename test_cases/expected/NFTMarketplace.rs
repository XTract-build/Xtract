#![no_std]

use multiversx_sc::imports::*;

#[multiversx_sc::contract]
pub trait NFTMarketplace {
    #[storage_mapper("currentTokenId")]
    fn current_token_id(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("currentOwner")]
    fn current_owner(&self) -> SingleValueMapper<ManagedAddress<Self::Api>>;

    #[storage_mapper("currentPrice")]
    fn current_price(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("currentForSale")]
    fn current_for_sale(&self) -> SingleValueMapper<bool>;

    #[storage_mapper("nextTokenId")]
    fn next_token_id(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("previousOwner")]
    fn previous_owner(&self) -> SingleValueMapper<ManagedAddress<Self::Api>>;

    #[event("NFTCreated")]
    fn nft_created_event(&self, #[indexed] tokenId: &BigUint<Self::Api>, #[indexed] owner: &ManagedAddress<Self::Api>);

    #[event("NFTListed")]
    fn nft_listed_event(&self, #[indexed] tokenId: &BigUint<Self::Api>, price: &BigUint<Self::Api>);

    #[event("NFTSold")]
    fn nft_sold_event(&self, #[indexed] tokenId: &BigUint<Self::Api>, #[indexed] from: &ManagedAddress<Self::Api>, #[indexed] to: &ManagedAddress<Self::Api>, price: &BigUint<Self::Api>);

    #[init]
    fn init(&self) {}

    #[endpoint]
    fn create_nft(&self) -> BigUint<Self::Api> {
        self.next_token_id().set(&(self.next_token_id().get() + BigUint::from(1u32)));
        self.current_token_id().set(&(self.next_token_id().get() - BigUint::from(1u32)));
        self.current_owner().set(&(self.blockchain().get_caller()));
        self.current_price().set(&(BigUint::from(0u32)));
        self.current_for_sale().set(&false);
        self.nft_created_event(&self.current_token_id().get(), &self.blockchain().get_caller());
        return self.current_token_id().get();
    }

    #[endpoint]
    fn list_nft_for_sale(&self, price: BigUint<Self::Api>) {
        require!(self.current_owner().get() == self.blockchain().get_caller(), "Requirement not met");
        self.current_price().set(&price);
        self.current_for_sale().set(&true);
        self.nft_listed_event(&self.current_token_id().get(), &price.clone());
    }

    #[endpoint]
    fn buy_nft(&self) {
        require!(self.current_for_sale().get() == true, "Requirement not met");
        self.previous_owner().set(&(self.current_owner().get()));
        self.current_owner().set(&(self.blockchain().get_caller()));
        self.current_for_sale().set(&false);
        self.nft_sold_event(&self.current_token_id().get(), &self.previous_owner().get(), &self.blockchain().get_caller(), &self.current_price().get());
    }

    #[view(getCurrentOwner)]
    fn get_current_owner(&self) -> ManagedAddress<Self::Api> {
        return self.current_owner().get();
    }

    #[view(getCurrentPrice)]
    fn get_current_price(&self) -> BigUint<Self::Api> {
        return self.current_price().get();
    }

    #[view(getCurrentForSale)]
    fn get_current_for_sale(&self) -> bool {
        return self.current_for_sale().get();
    }

}