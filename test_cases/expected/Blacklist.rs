#![no_std]

use multiversx_sc::imports::*;

#[multiversx_sc::contract]
pub trait Blacklist {
    #[storage_mapper("owner")]
    fn owner(&self) -> SingleValueMapper<ManagedAddress<Self::Api>>;

    #[storage_mapper("blacklistCount")]
    fn blacklist_count(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("blacklisted")]
    fn blacklisted(&self, key: &ManagedAddress<Self::Api>) -> SingleValueMapper<bool>;

    #[event("Blacklisted")]
    fn blacklisted_event(&self, #[indexed] account: &ManagedAddress<Self::Api>);

    #[event("Unblacklisted")]
    fn unblacklisted_event(&self, #[indexed] account: &ManagedAddress<Self::Api>);

    #[init]
    fn init(&self) {
        self.owner().set(&(self.blockchain().get_caller()));
        self.blacklist_count().set(&(BigUint::from(0u32)));
    }

    #[endpoint]
    fn add_to_blacklist(&self, account: ManagedAddress<Self::Api>) {
        require!(self.blockchain().get_caller() == owner, "Not owner");
        require!(!self.blacklisted(&account), "Already blacklisted");
        self.blacklisted(&account).set(true);
        self.blacklist_count().set(&(self.blacklist_count().get() + BigUint::from(1u32)));
        self.blacklisted_event(&account);
    }

    #[endpoint]
    fn remove_from_blacklist(&self, account: ManagedAddress<Self::Api>) {
        require!(self.blockchain().get_caller() == owner, "Not owner");
        require!(self.blacklisted(&account), "Not blacklisted");
        self.blacklisted(&account).set(false);
        self.blacklist_count().set(&(self.blacklist_count().get() - BigUint::from(1u32)));
        self.unblacklisted_event(&account);
    }

    #[view(isBlacklisted)]
    fn is_blacklisted(&self, account: ManagedAddress<Self::Api>) -> bool {
        return self.blacklisted(&account);
    }

    #[view(getBlacklistCount)]
    fn get_blacklist_count(&self) -> BigUint<Self::Api> {
        return self.blacklist_count().get();
    }

}