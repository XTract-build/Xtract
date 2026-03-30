#![no_std]

use multiversx_sc::imports::*;

#[multiversx_sc::contract]
pub trait Timer {
    #[storage_mapper("owner")]
    fn owner(&self) -> SingleValueMapper<ManagedAddress<Self::Api>>;

    #[storage_mapper("startTime")]
    fn start_time(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("duration")]
    fn duration(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("active")]
    fn active(&self) -> SingleValueMapper<bool>;

    #[event("TimerStarted")]
    fn timer_started_event(&self, startTime: &BigUint<Self::Api>, #[indexed] duration: &BigUint<Self::Api>);

    #[event("TimerStopped")]
    fn timer_stopped_event(&self, timestamp: &BigUint<Self::Api>);

    #[event("TimerReset")]
    fn timer_reset_event(&self);

    #[init]
    fn init(&self) {
        self.owner().set(&(self.blockchain().get_caller()));
        self.active().set(&false);
    }

    #[endpoint]
    fn start(&self, _duration: BigUint<Self::Api>) {
        require!(self.blockchain().get_caller() == owner, "Not owner");
        require!(!self.active().get(), "Already active");
        self.start_time().set(&(self.blockchain().get_block_timestamp()));
        self.duration().set(&_duration);
        self.active().set(&true);
        self.timer_started_event(&self.start_time().get(), &self.duration().get());
    }

    #[endpoint]
    fn stop(&self) {
        require!(self.blockchain().get_caller() == owner, "Not owner");
        require!(self.active().get(), "Not active");
        self.active().set(&false);
        self.timer_stopped_event(&self.blockchain().get_block_timestamp());
    }

    #[endpoint]
    fn reset(&self) {
        require!(self.blockchain().get_caller() == owner, "Not owner");
        self.start_time().set(&(BigUint::from(0u32)));
        self.duration().set(&(BigUint::from(0u32)));
        self.active().set(&false);
        self.timer_reset_event();
    }

    #[view(isExpired)]
    fn is_expired(&self) -> bool {
        return self.active().get();
    }

    #[view(getTimeRemaining)]
    fn get_time_remaining(&self) -> BigUint<Self::Api> {
        return self.duration().get();
    }

}