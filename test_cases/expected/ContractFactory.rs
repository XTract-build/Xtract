#![no_std]

use multiversx_sc::imports::*;

#[multiversx_sc::contract]
pub trait ContractFactory {
    #[storage_mapper("lastDeployed")]
    fn last_deployed(&self) -> SingleValueMapper<ManagedAddress<Self::Api>>;

    #[init]
    fn init(&self) {}

    #[endpoint]
    fn create_child(&self, initialValue: BigUint<Self::Api>) {
        // TODO: deploy Child — use ContractDeploy via self.send().contract_call(...)
        // Args: initialValue
        let instance: ManagedAddress<Self::Api> = ManagedAddress::zero();
    }

}