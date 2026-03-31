#![no_std]

use multiversx_sc::imports::*;

#[multiversx_sc::contract]
pub trait Config {
    #[storage_mapper("owner")]
    fn owner(&self) -> SingleValueMapper<ManagedAddress<Self::Api>>;

    #[storage_mapper("uintConfig")]
    fn uint_config(&self, key: &ManagedBuffer<Self::Api>) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("boolConfig")]
    fn bool_config(&self, key: &ManagedBuffer<Self::Api>) -> SingleValueMapper<bool>;

    #[storage_mapper("addressConfig")]
    fn address_config(&self, key: &ManagedBuffer<Self::Api>) -> SingleValueMapper<ManagedAddress<Self::Api>>;

    #[event("UintConfigSet")]
    fn uint_config_set_event(&self, #[indexed] key: &ManagedBuffer<Self::Api>, value: &BigUint<Self::Api>);

    #[event("BoolConfigSet")]
    fn bool_config_set_event(&self, #[indexed] key: &ManagedBuffer<Self::Api>, value: &bool);

    #[event("AddressConfigSet")]
    fn address_config_set_event(&self, #[indexed] key: &ManagedBuffer<Self::Api>, value: &ManagedAddress<Self::Api>);

    #[init]
    fn init(&self) {
        self.owner().set(&(self.blockchain().get_caller()));
    }

    #[endpoint]
    fn set_uint(&self, memory: ManagedBuffer<Self::Api>, value: BigUint<Self::Api>) {
        require!(self.blockchain().get_caller() == owner, "Not owner");
        self.uint_config_set_event(&key, &value);
    }

    #[endpoint]
    fn set_bool(&self, memory: ManagedBuffer<Self::Api>, value: bool) {
        require!(self.blockchain().get_caller() == owner, "Not owner");
        self.bool_config_set_event(&key, &value);
    }

    #[endpoint]
    fn set_address(&self, memory: ManagedBuffer<Self::Api>, value: ManagedAddress<Self::Api>) {
        require!(self.blockchain().get_caller() == owner, "Not owner");
        self.address_config_set_event(&key, &value);
    }

    #[view(getUint)]
    fn get_uint(&self, memory: ManagedBuffer<Self::Api>) -> BigUint<Self::Api> {
        return self.uint_config(&key);
    }

    #[view(getBool)]
    fn get_bool(&self, memory: ManagedBuffer<Self::Api>) -> bool {
        return self.bool_config(&key);
    }

    #[view(getAddress)]
    fn get_address(&self, memory: ManagedBuffer<Self::Api>) -> ManagedAddress<Self::Api> {
        return self.address_config(&key);
    }

}