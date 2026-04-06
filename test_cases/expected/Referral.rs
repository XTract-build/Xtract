#![no_std]

use multiversx_sc::imports::*;

#[multiversx_sc::contract]
pub trait Referral {
    #[storage_mapper("owner")]
    fn owner(&self) -> SingleValueMapper<ManagedAddress<Self::Api>>;

    #[storage_mapper("referralBonus")]
    fn referral_bonus(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("referrers")]
    fn referrers(&self, key: &ManagedAddress<Self::Api>) -> SingleValueMapper<ManagedAddress<Self::Api>>;

    #[storage_mapper("referralCount")]
    fn referral_count(&self, key: &ManagedAddress<Self::Api>) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("earnings")]
    fn earnings(&self, key: &ManagedAddress<Self::Api>) -> SingleValueMapper<BigUint<Self::Api>>;

    #[event("ReferralRegistered")]
    fn referral_registered_event(&self, #[indexed] user: &ManagedAddress<Self::Api>, #[indexed] referrer: &ManagedAddress<Self::Api>);

    #[event("BonusPaid")]
    fn bonus_paid_event(&self, #[indexed] referrer: &ManagedAddress<Self::Api>, amount: &BigUint<Self::Api>);

    #[init]
    fn init(&self) {
        self.owner().set(&(self.blockchain().get_caller()));
        self.referral_bonus().set(&(BigUint::from(100u32)));
    }

    #[endpoint]
    fn register(&self, referrer: ManagedAddress<Self::Api>) {
        require!(referrer != self.blockchain().get_caller(), "Cannot refer self");
        require!(self.referrers(&self.blockchain().get_caller()) == address(BigUint::zero(), "Requirement not met");
        self.referrers(&self.blockchain().get_caller()).set(referrer);
        self.referral_count(&referrer).set(self.referral_count(&referrer).get() + BigUint::from(1u32));
        self.referral_registered_event(&self.blockchain().get_caller(), &referrer);
    }

    #[endpoint]
    fn pay_bonus(&self, referrer: ManagedAddress<Self::Api>) {
        require!(self.blockchain().get_caller() == owner, "Not owner");
        let mut bonus: BigUint<Self::Api> = self.referral_bonus().get();
        self.earnings(&referrer).set(self.earnings(&referrer).get() + bonus);
        self.bonus_paid_event(&referrer, &bonus);
    }

    #[endpoint]
    fn set_bonus(&self, newBonus: BigUint<Self::Api>) {
        require!(self.blockchain().get_caller() == owner, "Not owner");
        self.referral_bonus().set(&newBonus);
    }

    #[view(getReferralCount)]
    fn get_referral_count(&self, referrer: ManagedAddress<Self::Api>) -> BigUint<Self::Api> {
        return self.referral_count(&referrer).get();
    }

}