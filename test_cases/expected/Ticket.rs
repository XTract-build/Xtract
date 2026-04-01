#![no_std]

use multiversx_sc::imports::*;

#[multiversx_sc::contract]
pub trait Ticket {
    #[storage_mapper("owner")]
    fn owner(&self) -> SingleValueMapper<ManagedAddress<Self::Api>>;

    #[storage_mapper("ticketPrice")]
    fn ticket_price(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("totalTickets")]
    fn total_tickets(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("soldTickets")]
    fn sold_tickets(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("ticketBalance")]
    fn ticket_balance(&self, key: &ManagedAddress<Self::Api>) -> SingleValueMapper<BigUint<Self::Api>>;

    #[event("TicketPurchased")]
    fn ticket_purchased_event(&self, #[indexed] buyer: &ManagedAddress<Self::Api>, quantity: &BigUint<Self::Api>);

    #[event("TicketTransferred")]
    fn ticket_transferred_event(&self, #[indexed] from: &ManagedAddress<Self::Api>, #[indexed] to: &ManagedAddress<Self::Api>, quantity: &BigUint<Self::Api>);

    #[event("TicketUsed")]
    fn ticket_used_event(&self, #[indexed] holder: &ManagedAddress<Self::Api>, quantity: &BigUint<Self::Api>);

    #[init]
    fn init(&self) {
        self.owner().set(&(self.blockchain().get_caller()));
        self.ticket_price().set(&(BigUint::from(100u32)));
        self.total_tickets().set(&(BigUint::from(1000u32)));
        self.sold_tickets().set(&(BigUint::from(0u32)));
    }

    #[endpoint]
    fn buy_ticket(&self, quantity: BigUint<Self::Api>) {
        require!(self.sold_tickets().get() + quantity <= self.total_tickets().get(), "Not enough tickets");
        self.ticket_balance(&self.blockchain().get_caller()).set(self.ticket_balance(&self.blockchain().get_caller()) + quantity);
        self.sold_tickets().set(&(self.sold_tickets().get() + quantity));
        self.ticket_purchased_event(&self.blockchain().get_caller(), &quantity);
    }

    #[endpoint]
    fn transfer_ticket(&self, to: ManagedAddress<Self::Api>, quantity: BigUint<Self::Api>) {
        require!(self.ticket_balance(&self.blockchain().get_caller()) >= quantity, "Insufficient tickets");
        self.ticket_balance(&self.blockchain().get_caller()).set(self.ticket_balance(&self.blockchain().get_caller()) - quantity);
        self.ticket_balance(&to).set(self.ticket_balance(&to) + quantity);
        self.ticket_transferred_event(&self.blockchain().get_caller(), &to, &quantity);
    }

    #[endpoint]
    fn use_ticket(&self, quantity: BigUint<Self::Api>) {
        require!(self.ticket_balance(&self.blockchain().get_caller()) >= quantity, "Insufficient tickets");
        self.ticket_balance(&self.blockchain().get_caller()).set(self.ticket_balance(&self.blockchain().get_caller()) - quantity);
        self.ticket_used_event(&self.blockchain().get_caller(), &quantity);
    }

    #[view(getBalance)]
    fn get_balance(&self, holder: ManagedAddress<Self::Api>) -> BigUint<Self::Api> {
        return self.ticket_balance(&holder);
    }

}