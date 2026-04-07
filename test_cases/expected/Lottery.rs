#![no_std]

use multiversx_sc::imports::*;

#[multiversx_sc::contract]
pub trait Lottery {
    #[storage_mapper("owner")]
    fn owner(&self) -> SingleValueMapper<ManagedAddress<Self::Api>>;

    #[storage_mapper("ticketPrice")]
    fn ticket_price(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("ticketCount")]
    fn ticket_count(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("prizePool")]
    fn prize_pool(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("lotteryOpen")]
    fn lottery_open(&self) -> SingleValueMapper<bool>;

    #[event("TicketPurchased")]
    fn ticket_purchased_event(&self, #[indexed] buyer: &ManagedAddress<Self::Api>, ticketId: &BigUint<Self::Api>);

    #[event("WinnerSelected")]
    fn winner_selected_event(&self, #[indexed] winner: &ManagedAddress<Self::Api>, prize: &BigUint<Self::Api>);

    #[event("LotteryOpened")]
    fn lottery_opened_event(&self, ticketPrice: &BigUint<Self::Api>);

    #[event("LotteryClosed")]
    fn lottery_closed_event(&self);

    #[init]
    fn init(&self) {
        self.owner().set(&(self.blockchain().get_caller()));
        self.ticket_price().set(&(BigUint::zero()));
        self.ticket_count().set(&(BigUint::zero()));
        self.prize_pool().set(&(BigUint::zero()));
        self.lottery_open().set(&false);
    }

    #[endpoint]
    fn open_lottery(&self, price: BigUint<Self::Api>) {
        require!(self.blockchain().get_caller() == self.owner().get(), "Not owner");
        require!(!self.lottery_open().get(), "Already open");
        self.ticket_price().set(&price);
        self.lottery_open().set(&true);
        self.lottery_opened_event(&price.clone());
    }

    #[endpoint]
    fn buy_ticket(&self) {
        require!(self.lottery_open().get(), "Lottery closed");
        self.ticket_count().set(&(self.ticket_count().get() + BigUint::from(1u32)));
        self.prize_pool().set(&(self.prize_pool().get() + self.ticket_price().get()));
        self.ticket_purchased_event(&self.blockchain().get_caller(), &self.ticket_count().get());
    }

    #[endpoint]
    fn close_lottery(&self) {
        require!(self.blockchain().get_caller() == self.owner().get(), "Not owner");
        require!(self.lottery_open().get(), "Already closed");
        self.lottery_open().set(&false);
        self.lottery_closed_event();
    }

    #[view(getPrizePool)]
    fn get_prize_pool(&self) -> BigUint<Self::Api> {
        return self.prize_pool().get();
    }

}