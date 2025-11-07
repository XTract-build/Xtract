#![no_std]

use multiversx_sc::imports::*;

#[multiversx_sc::contract]
pub trait Crowdfunding {
    #[storage_mapper("campaignCreator")]
    fn campaign_creator(&self) -> SingleValueMapper<ManagedAddress<Self::Api>>;

    #[storage_mapper("campaignGoal")]
    fn campaign_goal(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("campaignPledged")]
    fn campaign_pledged(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("campaignClaimed")]
    fn campaign_claimed(&self) -> SingleValueMapper<bool>;

    #[storage_mapper("count")]
    fn count(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[event("CampaignCreated")]
    fn campaign_created_event(&self, #[indexed] id: &BigUint<Self::Api>, #[indexed] creator: &ManagedAddress<Self::Api>, goal: &BigUint<Self::Api>);

    #[event("PledgeCreated")]
    fn pledge_created_event(&self, #[indexed] id: &BigUint<Self::Api>, #[indexed] pledger: &ManagedAddress<Self::Api>, amount: &BigUint<Self::Api>);

    #[event("Claimed")]
    fn claimed_event(&self, #[indexed] id: &BigUint<Self::Api>, creator: &ManagedAddress<Self::Api>, #[indexed] amount: &BigUint<Self::Api>);

    #[init]
    fn init(&self) {}

    #[endpoint]
    fn create_campaign(&self, goal: BigUint<Self::Api>) -> BigUint<Self::Api> {
        self.count().set(&(self.count().get() + BigUint::from(1u32)));
        self.campaign_creator().set(&(self.blockchain().get_caller()));
        self.campaign_goal().set(&goal);
        self.campaign_pledged().set(&(BigUint::from(0u32)));
        self.campaign_claimed().set(&false);
        self.campaign_created_event(&(self.count().get() - BigUint::from(1u32)), &self.blockchain().get_caller(), &goal.clone());
        return self.count().get() - BigUint::from(1u32);
    }

    #[endpoint]
    fn pledge(&self, amount: BigUint<Self::Api>) {
        require!(self.campaign_claimed().get() == false, "Requirement not met");
        self.campaign_pledged().set(&(self.campaign_pledged().get() + amount.clone()));
        self.pledge_created_event(&(self.count().get() - BigUint::from(1u32)), &self.blockchain().get_caller(), &amount.clone());
    }

    #[endpoint]
    fn claim(&self) {
        require!(self.campaign_creator().get() == self.blockchain().get_caller(), "Requirement not met");
        require!(self.campaign_pledged().get() >= self.campaign_goal().get(), "Requirement not met");
        require!(self.campaign_claimed().get() == false, "Requirement not met");
        self.campaign_claimed().set(&true);
        self.claimed_event(&(self.count().get() - BigUint::from(1u32)), &self.campaign_creator().get(), &self.campaign_pledged().get());
    }

    #[view(getCampaignCreator)]
    fn get_campaign_creator(&self) -> ManagedAddress<Self::Api> {
        return self.campaign_creator().get();
    }

    #[view(getCampaignGoal)]
    fn get_campaign_goal(&self) -> BigUint<Self::Api> {
        return self.campaign_goal().get();
    }

    #[view(getCampaignPledged)]
    fn get_campaign_pledged(&self) -> BigUint<Self::Api> {
        return self.campaign_pledged().get();
    }

    #[view(getCampaignClaimed)]
    fn get_campaign_claimed(&self) -> bool {
        return self.campaign_claimed().get();
    }

}