#![no_std]

use multiversx_sc::imports::*;

#[multiversx_sc::contract]
pub trait Poll {
    #[storage_mapper("creator")]
    fn creator(&self) -> SingleValueMapper<ManagedAddress<Self::Api>>;

    #[storage_mapper("optionCount")]
    fn option_count(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("pollActive")]
    fn poll_active(&self) -> SingleValueMapper<bool>;

    #[storage_mapper("votes")]
    fn votes(&self, key: &BigUint<Self::Api>) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("hasVoted")]
    fn has_voted(&self, key: &ManagedAddress<Self::Api>) -> SingleValueMapper<bool>;

    #[event("PollCreated")]
    fn poll_created_event(&self, #[indexed] creator: &ManagedAddress<Self::Api>, options: &BigUint<Self::Api>);

    #[event("VoteCast")]
    fn vote_cast_event(&self, #[indexed] voter: &ManagedAddress<Self::Api>, option: &BigUint<Self::Api>);

    #[event("PollClosed")]
    fn poll_closed_event(&self, winningOption: &BigUint<Self::Api>);

    #[init]
    fn init(&self) {
        self.creator().set(&(self.blockchain().get_caller()));
        self.option_count().set(&(BigUint::from(0u32)));
        self.poll_active().set(&false);
    }

    #[endpoint]
    fn create_poll(&self, options: BigUint<Self::Api>) {
        require!(self.blockchain().get_caller() == self.creator().get(), "Not creator");
        require!(!self.poll_active().get(), "Poll already active");
        self.option_count().set(&options);
        self.poll_active().set(&true);
        self.poll_created_event(&self.blockchain().get_caller(), &options);
    }

    #[endpoint]
    fn cast_vote(&self, option: BigUint<Self::Api>) {
        require!(self.poll_active().get(), "Poll not active");
        require!(!self.has_voted(&self.blockchain().get_caller()), "Already voted");
        require!(option < self.option_count().get(), "Invalid option");
        self.vote_cast_event(&self.blockchain().get_caller(), &option);
    }

    #[endpoint]
    fn close_poll(&self) {
        require!(self.blockchain().get_caller() == self.creator().get(), "Not creator");
        require!(self.poll_active().get(), "Poll not active");
        self.poll_active().set(&false);
        self.poll_closed_event(&BigUint::from(0u32));
    }

    #[view(getVotes)]
    fn get_votes(&self, option: BigUint<Self::Api>) -> BigUint<Self::Api> {
        return self.votes(&option);
    }

}