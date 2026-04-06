#![no_std]

use multiversx_sc::imports::*;

#[multiversx_sc::contract]
pub trait Vesting {
    #[storage_mapper("beneficiary")]
    fn beneficiary(&self) -> SingleValueMapper<ManagedAddress<Self::Api>>;

    #[storage_mapper("startTime")]
    fn start_time(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("duration")]
    fn duration(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("totalAmount")]
    fn total_amount(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("released")]
    fn released(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[event("TokensReleased")]
    fn tokens_released_event(&self, #[indexed] beneficiary: &ManagedAddress<Self::Api>, amount: &BigUint<Self::Api>);

    #[event("VestingScheduleCreated")]
    fn vesting_schedule_created_event(&self, #[indexed] beneficiary: &ManagedAddress<Self::Api>, amount: &BigUint<Self::Api>, #[indexed] duration: &BigUint<Self::Api>);

    #[init]
    fn init(&self) {
        self.beneficiary().set(&(self.blockchain().get_caller()));
        self.released().set(&(BigUint::zero()));
    }

    #[endpoint]
    fn create_schedule(&self, _beneficiary: ManagedAddress<Self::Api>, _amount: BigUint<Self::Api>, _duration: BigUint<Self::Api>) {
        require!(_beneficiary != address(BigUint::zero(), "Requirement not met");
        require!(_amount > BigUint::zero(), "Invalid amount");
        require!(_duration > BigUint::zero(), "Invalid duration");
        self.beneficiary().set(&_beneficiary);
        self.total_amount().set(&_amount);
        self.duration().set(&_duration);
        self.start_time().set(&(self.blockchain().get_block_timestamp()));
        self.vesting_schedule_created_event(&_beneficiary, &_amount.clone(), &_duration);
    }

    #[endpoint]
    fn release(&self) {
        require!(self.blockchain().get_caller() == self.beneficiary().get(), "Not beneficiary");
        let mut releasable: BigUint<Self::Api> = self.total_amount().get() - self.released().get();
        require!(releasable > BigUint::zero(), "Nothing to release");
        self.released().set(&(self.released().get() + releasable));
        self.tokens_released_event(&self.beneficiary().get(), &releasable);
    }

    #[view(getVestedAmount)]
    fn get_vested_amount(&self) -> BigUint<Self::Api> {
        return self.released().get();
    }

    #[view(getRemainingAmount)]
    fn get_remaining_amount(&self) -> BigUint<Self::Api> {
        return self.total_amount().get() - self.released().get();
    }

}