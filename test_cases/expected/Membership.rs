#![no_std]

use multiversx_sc::imports::*;

#[multiversx_sc::contract]
pub trait Membership {
    #[storage_mapper("owner")]
    fn owner(&self) -> SingleValueMapper<ManagedAddress<Self::Api>>;

    #[storage_mapper("membershipFee")]
    fn membership_fee(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("memberCount")]
    fn member_count(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("isMember")]
    fn is_member(&self, key: &ManagedAddress<Self::Api>) -> SingleValueMapper<bool>;

    #[storage_mapper("memberSince")]
    fn member_since(&self, key: &ManagedAddress<Self::Api>) -> SingleValueMapper<BigUint<Self::Api>>;

    #[event("MemberJoined")]
    fn member_joined_event(&self, #[indexed] member: &ManagedAddress<Self::Api>, timestamp: &BigUint<Self::Api>);

    #[event("MemberLeft")]
    fn member_left_event(&self, #[indexed] member: &ManagedAddress<Self::Api>);

    #[event("FeeUpdated")]
    fn fee_updated_event(&self, #[indexed] oldFee: &BigUint<Self::Api>, #[indexed] newFee: &BigUint<Self::Api>);

    #[init]
    fn init(&self) {
        self.owner().set(&(self.blockchain().get_caller()));
        self.membership_fee().set(&(BigUint::from(100u32)));
        self.member_count().set(&(BigUint::zero()));
    }

    #[endpoint]
    fn join(&self) {
        require!(!self.is_member(&self.blockchain().get_caller()), "Already a member");
        self.is_member(&self.blockchain().get_caller()).set(true);
        self.member_since(&self.blockchain().get_caller()).set(self.blockchain().get_block_timestamp());
        self.member_count().set(&(self.member_count().get() + BigUint::from(1u32)));
        self.member_joined_event(&self.blockchain().get_caller(), &self.blockchain().get_block_timestamp());
    }

    #[endpoint]
    fn leave(&self) {
        require!(self.is_member(&self.blockchain().get_caller()), "Not a member");
        self.is_member(&self.blockchain().get_caller()).set(false);
        self.member_count().set(&(self.member_count().get() - BigUint::from(1u32)));
        self.member_left_event(&self.blockchain().get_caller());
    }

    #[endpoint]
    fn set_fee(&self, newFee: BigUint<Self::Api>) {
        require!(self.blockchain().get_caller() == owner, "Not owner");
        self.fee_updated_event(&self.membership_fee().get(), &newFee);
        self.membership_fee().set(&newFee);
    }

    #[view(checkMembership)]
    fn check_membership(&self, account: ManagedAddress<Self::Api>) -> bool {
        return self.is_member(&account).get();
    }

}