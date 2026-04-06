#![no_std]

use multiversx_sc::imports::*;

#[multiversx_sc::contract]
pub trait Badge {
    #[storage_mapper("admin")]
    fn admin(&self) -> SingleValueMapper<ManagedAddress<Self::Api>>;

    #[storage_mapper("badgeCount")]
    fn badge_count(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("hasBadge")]
    fn has_badge(&self, key1: &ManagedAddress<Self::Api>, key2: &BigUint<Self::Api>) -> SingleValueMapper<bool>;

    #[storage_mapper("badgeName")]
    fn badge_name(&self, key: &BigUint<Self::Api>) -> SingleValueMapper<ManagedBuffer<Self::Api>>;

    #[storage_mapper("badgeCountPerUser")]
    fn badge_count_per_user(&self, key: &ManagedAddress<Self::Api>) -> SingleValueMapper<BigUint<Self::Api>>;

    #[event("BadgeCreated")]
    fn badge_created_event(&self, #[indexed] badgeId: &BigUint<Self::Api>, name: &ManagedBuffer<Self::Api>);

    #[event("BadgeAwarded")]
    fn badge_awarded_event(&self, #[indexed] user: &ManagedAddress<Self::Api>, #[indexed] badgeId: &BigUint<Self::Api>);

    #[event("BadgeRevoked")]
    fn badge_revoked_event(&self, #[indexed] user: &ManagedAddress<Self::Api>, #[indexed] badgeId: &BigUint<Self::Api>);

    #[init]
    fn init(&self) {
        self.admin().set(&(self.blockchain().get_caller()));
        self.badge_count().set(&(BigUint::zero()));
    }

    #[endpoint]
    fn create_badge(&self, memory: ManagedBuffer<Self::Api>) {
        require!(self.blockchain().get_caller() == self.admin().get(), "Not admin");
        self.badge_count().set(&(self.badge_count().get() + BigUint::from(1u32)));
        self.badge_name(&self.badge_count().get()).set(name);
        self.badge_created_event(&self.badge_count().get(), &name);
    }

    #[endpoint]
    fn award_badge(&self, user: ManagedAddress<Self::Api>, badgeId: BigUint<Self::Api>) {
        require!(self.blockchain().get_caller() == self.admin().get(), "Not admin");
        require!(!self.has_badge(&user, &badgeId).get(), "Already has badge");
        self.has_badge(&user, &badgeId).set(true);
        self.badge_count_per_user(&user).set(self.badge_count_per_user(&user).get() + BigUint::from(1u32));
        self.badge_awarded_event(&user, &badgeId);
    }

    #[endpoint]
    fn revoke_badge(&self, user: ManagedAddress<Self::Api>, badgeId: BigUint<Self::Api>) {
        require!(self.blockchain().get_caller() == self.admin().get(), "Not admin");
        require!(self.has_badge(&user, &badgeId).get(), "Does not have badge");
        self.has_badge(&user, &badgeId).set(false);
        self.badge_count_per_user(&user).set(self.badge_count_per_user(&user).get() - BigUint::from(1u32));
        self.badge_revoked_event(&user, &badgeId);
    }

    #[view(checkBadge)]
    fn check_badge(&self, user: ManagedAddress<Self::Api>, badgeId: BigUint<Self::Api>) -> bool {
        return self.has_badge(&user, &badgeId).get();
    }

}