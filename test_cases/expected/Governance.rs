#![no_std]

use multiversx_sc::imports::*;

#[multiversx_sc::contract]
pub trait Governance {
    #[storage_mapper("governor")]
    fn governor(&self) -> SingleValueMapper<ManagedAddress<Self::Api>>;

    #[storage_mapper("proposalCount")]
    fn proposal_count(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("votingPeriod")]
    fn voting_period(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("proposalVotes")]
    fn proposal_votes(&self, key: &BigUint<Self::Api>) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("hasVoted")]
    fn has_voted(&self, key: &ManagedAddress<Self::Api>) -> SingleValueMapper<bool>;

    #[event("ProposalCreated")]
    fn proposal_created_event(&self, #[indexed] proposalId: &BigUint<Self::Api>, #[indexed] proposer: &ManagedAddress<Self::Api>);

    #[event("Voted")]
    fn voted_event(&self, #[indexed] proposalId: &BigUint<Self::Api>, #[indexed] voter: &ManagedAddress<Self::Api>, support: &bool);

    #[event("ProposalExecuted")]
    fn proposal_executed_event(&self, #[indexed] proposalId: &BigUint<Self::Api>);

    #[init]
    fn init(&self) {
        self.governor().set(&(self.blockchain().get_caller()));
        self.proposal_count().set(&(BigUint::zero()));
        self.voting_period().set(&(BigUint::from(86400u32)));
    }

    #[endpoint]
    fn create_proposal(&self) {
        self.proposal_count().set(&(self.proposal_count().get() + BigUint::from(1u32)));
        self.proposal_created_event(&self.proposal_count().get(), &self.blockchain().get_caller());
    }

    #[endpoint]
    fn vote(&self, proposalId: BigUint<Self::Api>, support: bool) {
        require!(!self.has_voted(&self.blockchain().get_caller()), "Already voted");
        self.has_voted(&self.blockchain().get_caller()).set(true);
        self.proposal_votes(&proposalId).set(self.proposal_votes(&proposalId.clone()).get() + BigUint::from(1u32));
        self.voted_event(&proposalId.clone(), &self.blockchain().get_caller(), &support);
    }

    #[endpoint]
    fn execute(&self, proposalId: BigUint<Self::Api>) {
        require!(self.blockchain().get_caller() == self.governor().get(), "Not governor");
        self.proposal_executed_event(&proposalId.clone());
    }

    #[view(getVotes)]
    fn get_votes(&self, proposalId: BigUint<Self::Api>) -> BigUint<Self::Api> {
        return self.proposal_votes(&proposalId).get();
    }

}