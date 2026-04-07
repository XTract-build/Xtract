#![no_std]

use multiversx_sc::imports::*;

#[multiversx_sc::contract]
pub trait Proxy {
    #[storage_mapper("admin")]
    fn admin(&self) -> SingleValueMapper<ManagedAddress<Self::Api>>;

    #[storage_mapper("implementation")]
    fn implementation(&self) -> SingleValueMapper<ManagedAddress<Self::Api>>;

    #[storage_mapper("initialized")]
    fn initialized(&self) -> SingleValueMapper<bool>;

    #[event("ImplementationUpdated")]
    fn implementation_updated_event(&self, #[indexed] oldImpl: &ManagedAddress<Self::Api>, #[indexed] newImpl: &ManagedAddress<Self::Api>);

    #[event("AdminChanged")]
    fn admin_changed_event(&self, #[indexed] oldAdmin: &ManagedAddress<Self::Api>, #[indexed] newAdmin: &ManagedAddress<Self::Api>);

    #[event("Initialized")]
    fn initialized_event(&self);

    #[init]
    fn init(&self) {
        self.admin().set(&(self.blockchain().get_caller()));
        self.initialized().set(&false);
    }

    #[endpoint]
    fn initialize(&self, impl: ManagedAddress<Self::Api>) {
        require!(self.blockchain().get_caller() == self.admin().get(), "Not admin");
        require!(!self.initialized().get(), "Already initialized");
        require!(impl != ManagedAddress::zero(), "Invalid implementation");
        self.implementation().set(&impl);
        self.initialized().set(&true);
        self.initialized_event();
    }

    #[endpoint]
    fn upgrade_to(&self, newImpl: ManagedAddress<Self::Api>) {
        require!(self.blockchain().get_caller() == self.admin().get(), "Not admin");
        require!(newImpl != ManagedAddress::zero(), "Invalid implementation");
        self.implementation_updated_event(&self.implementation().get(), &newImpl);
        self.implementation().set(&newImpl);
    }

    #[endpoint]
    fn change_admin(&self, newAdmin: ManagedAddress<Self::Api>) {
        require!(self.blockchain().get_caller() == self.admin().get(), "Not admin");
        require!(newAdmin != ManagedAddress::zero(), "Invalid admin");
        self.admin_changed_event(&self.admin().get(), &newAdmin);
        self.admin().set(&newAdmin);
    }

    #[view(getImplementation)]
    fn get_implementation(&self) -> ManagedAddress<Self::Api> {
        return self.implementation().get();
    }

}