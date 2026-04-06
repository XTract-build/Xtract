#![no_std]

use multiversx_sc::imports::*;

#[multiversx_sc::contract]
pub trait Certificate {
    #[storage_mapper("issuer")]
    fn issuer(&self) -> SingleValueMapper<ManagedAddress<Self::Api>>;

    #[storage_mapper("certificateCount")]
    fn certificate_count(&self) -> SingleValueMapper<BigUint<Self::Api>>;

    #[storage_mapper("certificateOwner")]
    fn certificate_owner(&self, key: &BigUint<Self::Api>) -> SingleValueMapper<ManagedAddress<Self::Api>>;

    #[storage_mapper("certificateValid")]
    fn certificate_valid(&self, key: &BigUint<Self::Api>) -> SingleValueMapper<bool>;

    #[storage_mapper("ownerCertificateCount")]
    fn owner_certificate_count(&self, key: &ManagedAddress<Self::Api>) -> SingleValueMapper<BigUint<Self::Api>>;

    #[event("CertificateIssued")]
    fn certificate_issued_event(&self, #[indexed] certId: &BigUint<Self::Api>, #[indexed] recipient: &ManagedAddress<Self::Api>);

    #[event("CertificateRevoked")]
    fn certificate_revoked_event(&self, #[indexed] certId: &BigUint<Self::Api>);

    #[event("CertificateTransferred")]
    fn certificate_transferred_event(&self, #[indexed] certId: &BigUint<Self::Api>, #[indexed] from: &ManagedAddress<Self::Api>, #[indexed] to: &ManagedAddress<Self::Api>);

    #[init]
    fn init(&self) {
        self.issuer().set(&(self.blockchain().get_caller()));
        self.certificate_count().set(&(BigUint::zero()));
    }

    #[endpoint]
    fn issue_certificate(&self, recipient: ManagedAddress<Self::Api>) {
        require!(self.blockchain().get_caller() == self.issuer().get(), "Not issuer");
        require!(recipient != address(BigUint::zero(), "Requirement not met");
        self.certificate_count().set(&(self.certificate_count().get() + BigUint::from(1u32)));
        self.certificate_owner(&self.certificate_count().get()).set(recipient);
        self.certificate_valid(&self.certificate_count().get()).set(true);
        self.owner_certificate_count(&recipient).set(self.owner_certificate_count(&recipient).get() + BigUint::from(1u32));
        self.certificate_issued_event(&self.certificate_count().get(), &recipient);
    }

    #[endpoint]
    fn revoke_certificate(&self, certId: BigUint<Self::Api>) {
        require!(self.blockchain().get_caller() == self.issuer().get(), "Not issuer");
        require!(self.certificate_valid(&certId).get(), "Not valid");
        self.certificate_valid(&certId).set(false);
        self.certificate_revoked_event(&certId);
    }

    #[endpoint]
    fn transfer_certificate(&self, certId: BigUint<Self::Api>, to: ManagedAddress<Self::Api>) {
        require!(self.certificate_owner(&certId).get() == self.blockchain().get_caller(), "Not owner");
        require!(self.certificate_valid(&certId).get(), "Not valid");
        self.owner_certificate_count(&self.blockchain().get_caller()).set(self.owner_certificate_count(&self.blockchain().get_caller()) - BigUint::from(1u32));
        self.owner_certificate_count(&to).set(self.owner_certificate_count(&to).get() + BigUint::from(1u32));
        self.certificate_owner(&certId).set(to);
        self.certificate_transferred_event(&certId, &self.blockchain().get_caller(), &to);
    }

    #[view(isValid)]
    fn is_valid(&self, certId: BigUint<Self::Api>) -> bool {
        return self.certificate_valid(&certId).get();
    }

}