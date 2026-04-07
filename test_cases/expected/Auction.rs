#![no_std]

use multiversx_sc::imports::*;

#[multiversx_sc::contract]
pub trait Auction {
    #[storage_mapper("owner")]
    fn owner(&self) -> SingleValueMapper<ManagedAddress<Self::Api>>;

    #[storage_mapper("highestBidder")]
    fn highest_bidder(&self) -> SingleValueMapper<ManagedAddress<Self::Api>>;

    #[storage_mapper("highestBid")]
    fn highest_bid(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("auctionEndTime")]
    fn auction_end_time(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("ended")]
    fn ended(&self) -> SingleValueMapper<bool>;

    #[event("BidPlaced")]
    fn bid_placed_event(&self, #[indexed] bidder: &ManagedAddress<Self::Api>, amount: &BigUint<Self::Api>);

    #[event("AuctionEnded")]
    fn auction_ended_event(&self, #[indexed] winner: &ManagedAddress<Self::Api>, amount: &BigUint<Self::Api>);

    #[init]
    fn init(&self) {
        self.owner().set(&(self.blockchain().get_caller()));
        self.highest_bid().set(&(BigUint::zero()));
        self.ended().set(&false);
    }

    #[endpoint]
    fn start_auction(&self, duration: BigUint<Self::Api>) {
        require!(self.blockchain().get_caller() == self.owner().get(), "Not owner");
        require!(!self.ended().get(), "Auction ended");
        self.auction_end_time().set(&(self.blockchain().get_block_timestamp() + duration));
    }

    #[endpoint]
    fn bid(&self, amount: BigUint<Self::Api>) {
        require!(!self.ended().get(), "Auction ended");
        require!(amount > self.highest_bid().get(), "Bid too low");
        self.highest_bidder().set(&(self.blockchain().get_caller()));
        self.highest_bid().set(&amount);
        self.bid_placed_event(&self.blockchain().get_caller(), &amount.clone());
    }

    #[endpoint]
    fn end_auction(&self) {
        require!(self.blockchain().get_caller() == self.owner().get(), "Not owner");
        require!(!self.ended().get(), "Already ended");
        self.ended().set(&true);
        self.auction_ended_event(&self.highest_bidder().get(), &self.highest_bid().get());
    }

    #[view(getHighestBid)]
    fn get_highest_bid(&self) -> BigUint<Self::Api> {
        return self.highest_bid().get();
    }

}