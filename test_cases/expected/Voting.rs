#![no_std]

use multiversx_sc::imports::*;

#[multiversx_sc::contract]
pub trait Voting {
    #[storage_mapper("chairperson")]
    fn chairperson(&self) -> SingleValueMapper<ManagedAddress<Self::Api>>;

    #[storage_mapper("hasVoted")]
    fn has_voted(&self) -> SingleValueMapper<bool>;

    #[storage_mapper("votedProposalId")]
    fn voted_proposal_id(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("proposalVoteCount")]
    fn proposal_vote_count(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("proposalCount")]
    fn proposal_count(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[event("ProposalCreated")]
    fn proposal_created_event(&self, #[indexed] proposalId: &BigUint<Self::Api>);

    #[event("VoteCast")]
    fn vote_cast_event(&self, #[indexed] voter: &ManagedAddress<Self::Api>, #[indexed] proposalId: &BigUint<Self::Api>);

    #[init]
    fn init(&self) {
        self.chairperson().set(&(self.blockchain().get_caller()));
    }

    #[endpoint]
    fn add_proposal(&self) {
        require!(self.blockchain().get_caller() == self.chairperson().get(), "Requirement not met");
        self.proposal_count().set(&(self.proposal_count().get() + BigUint::from(1u32)));
        self.proposal_created_event(&(self.proposal_count().get() - BigUint::from(1u32)));
    }

    #[endpoint]
    fn vote(&self, proposalId: BigUint<Self::Api>) {
        require!(proposalId < self.proposal_count().get(), "Requirement not met");
        require!(self.has_voted().get() == false, "Requirement not met");
        self.has_voted().set(&true);
        self.voted_proposal_id().set(&proposalId);
        self.proposal_vote_count().set(&(self.proposal_vote_count().get() + BigUint::from(1u32)));
        self.vote_cast_event(&self.blockchain().get_caller(), &proposalId.clone());
    }

    #[view(getProposalVoteCount)]
    fn get_proposal_vote_count(&self) -> BigUint<Self::Api> {
        return self.proposal_vote_count().get();
    }

    #[view(getProposalCount)]
    fn get_proposal_count(&self) -> BigUint<Self::Api> {
        return self.proposal_count().get();
    }

}