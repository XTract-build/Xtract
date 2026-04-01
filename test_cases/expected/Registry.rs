#![no_std]

use multiversx_sc::imports::*;

#[multiversx_sc::contract]
pub trait Registry {
    #[storage_mapper("owner")]
    fn owner(&self) -> SingleValueMapper<ManagedAddress<Self::Api>>;

    #[storage_mapper("registry")]
    fn registry(&self, key: &ManagedBuffer<Self::Api>) -> SingleValueMapper<ManagedAddress<Self::Api>>;

    #[event("Registered")]
    fn registered_event(&self, #[indexed] name: &ManagedBuffer<Self::Api>, #[indexed] addr: &ManagedAddress<Self::Api>);

    #[event("Unregistered")]
    fn unregistered_event(&self, #[indexed] name: &ManagedBuffer<Self::Api>);

    #[init]
    fn init(&self) {
        self.owner().set(&(self.blockchain().get_caller()));
    }

    #[endpoint]
    fn register(&self, memory: ManagedBuffer<Self::Api>, addr: ManagedAddress<Self::Api>) {
        require!(self.blockchain().get_caller() == owner, "Not owner");
        require!(addr != address(BigUint::from(0u32), "Requirement not met");
        self.registry(&name).set(addr);
        self.registered_event(&name, &addr);
    }

    #[endpoint]
    fn unregister(&self, memory: ManagedBuffer<Self::Api>) {
        require!(self.blockchain().get_caller() == owner, "Not owner");
        self.registry(&name).set(ManagedAddress::zero());
        self.unregistered_event(&name);
    }

    #[view(lookup)]
    fn lookup(&self, memory: ManagedBuffer<Self::Api>) -> ManagedAddress<Self::Api> {
        return self.registry(&name);
    }

}