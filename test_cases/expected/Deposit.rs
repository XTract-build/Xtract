#![no_std]

use multiversx_sc::imports::*;

#[multiversx_sc::contract]
pub trait Deposit {
    #[storage_mapper("owner")]
    fn owner(&self) -> SingleValueMapper<ManagedAddress<Self::Api>>;

    #[storage_mapper("minDeposit")]
    fn min_deposit(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("maxDeposit")]
    fn max_deposit(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("totalDeposits")]
    fn total_deposits(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("userDeposits")]
    fn user_deposits(&self, key: &ManagedAddress<Self::Api>) -> SingleValueMapper<BigUint<Self::Api>>;

    #[event("DepositMade")]
    fn deposit_made_event(&self, #[indexed] user: &ManagedAddress<Self::Api>, amount: &BigUint<Self::Api>);

    #[event("WithdrawalMade")]
    fn withdrawal_made_event(&self, #[indexed] user: &ManagedAddress<Self::Api>, amount: &BigUint<Self::Api>);

    #[event("LimitsUpdated")]
    fn limits_updated_event(&self, minDeposit: &BigUint<Self::Api>, #[indexed] maxDeposit: &BigUint<Self::Api>);

    #[init]
    fn init(&self) {
        self.owner().set(&(self.blockchain().get_caller()));
        self.min_deposit().set(&(BigUint::from(100u32)));
        self.max_deposit().set(&(BigUint::from(10000u32)));
        self.total_deposits().set(&(BigUint::from(0u32)));
    }

    #[endpoint]
    fn deposit(&self, amount: BigUint<Self::Api>) {
        require!(amount >= self.min_deposit().get(), "Below minimum");
        require!(amount <= self.max_deposit().get(), "Above maximum");
        self.user_deposits(&self.blockchain().get_caller()).set(self.user_deposits(&self.blockchain().get_caller()) + amount.clone());
        self.total_deposits().set(&(self.total_deposits().get() + amount.clone()));
        self.deposit_made_event(&self.blockchain().get_caller(), &amount.clone());
    }

    #[endpoint]
    fn withdraw(&self, amount: BigUint<Self::Api>) {
        require!(self.user_deposits(&self.blockchain().get_caller()) >= amount, "Insufficient balance");
        self.user_deposits(&self.blockchain().get_caller()).set(self.user_deposits(&self.blockchain().get_caller()) - amount.clone());
        self.total_deposits().set(&(self.total_deposits().get() - amount.clone()));
        self.withdrawal_made_event(&self.blockchain().get_caller(), &amount.clone());
    }

    #[endpoint]
    fn set_limits(&self, newMin: BigUint<Self::Api>, newMax: BigUint<Self::Api>) {
        require!(self.blockchain().get_caller() == owner, "Not owner");
        require!(newMin <= newMax, "Invalid limits");
        self.min_deposit().set(&newMin);
        self.max_deposit().set(&newMax);
        self.limits_updated_event(&newMin, &newMax);
    }

    #[view(getDeposit)]
    fn get_deposit(&self, user: ManagedAddress<Self::Api>) -> BigUint<Self::Api> {
        return self.user_deposits(&user).get();
    }

}