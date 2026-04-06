#![no_std]

use multiversx_sc::imports::*;

#[multiversx_sc::contract]
pub trait Claimer {
    #[storage_mapper("owner")]
    fn owner(&self) -> SingleValueMapper<ManagedAddress<Self::Api>>;

    #[storage_mapper("claimAmount")]
    fn claim_amount(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("totalClaimed")]
    fn total_claimed(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("hasClaimed")]
    fn has_claimed(&self, key: &ManagedAddress<Self::Api>) -> SingleValueMapper<bool>;

    #[storage_mapper("claimedAt")]
    fn claimed_at(&self, key: &ManagedAddress<Self::Api>) -> SingleValueMapper<BigUint<Self::Api>>;

    #[event("Claimed")]
    fn claimed_event(&self, #[indexed] user: &ManagedAddress<Self::Api>, amount: &BigUint<Self::Api>, #[indexed] timestamp: &BigUint<Self::Api>);

    #[event("ClaimAmountUpdated")]
    fn claim_amount_updated_event(&self, #[indexed] oldAmount: &BigUint<Self::Api>, #[indexed] newAmount: &BigUint<Self::Api>);

    #[init]
    fn init(&self) {
        self.owner().set(&(self.blockchain().get_caller()));
        self.claim_amount().set(&(BigUint::from(100u32)));
        self.total_claimed().set(&(BigUint::zero()));
    }

    #[endpoint]
    fn claim(&self) {
        require!(!self.has_claimed(&self.blockchain().get_caller()), "Already claimed");
        self.has_claimed(&self.blockchain().get_caller()).set(true);
        self.claimed_at(&self.blockchain().get_caller()).set(self.blockchain().get_block_timestamp());
        self.total_claimed().set(&(self.total_claimed().get() + self.claim_amount().get()));
        self.claimed_event(&self.blockchain().get_caller(), &self.claim_amount().get(), &self.blockchain().get_block_timestamp());
    }

    #[endpoint]
    fn set_claim_amount(&self, newAmount: BigUint<Self::Api>) {
        require!(self.blockchain().get_caller() == owner, "Not owner");
        self.claim_amount_updated_event(&self.claim_amount().get(), &newAmount);
        self.claim_amount().set(&newAmount);
    }

    #[view(checkClaimed)]
    fn check_claimed(&self, user: ManagedAddress<Self::Api>) -> bool {
        return self.has_claimed(&user).get();
    }

    #[view(getTotalClaimed)]
    fn get_total_claimed(&self) -> BigUint<Self::Api> {
        return self.total_claimed().get();
    }

}