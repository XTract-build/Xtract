#![no_std]

use multiversx_sc::imports::*;

#[multiversx_sc::contract]
pub trait AbiEncoding {
    #[init]
    fn init(&self) {}

    #[endpoint]
    fn encode_two(&self, a: BigUint<Self::Api>, b: BigUint<Self::Api>) -> bytes {
        return {
            let mut __buf = ManagedBuffer::new();
            codec::top_encode_to_managed_buffer(&a, &mut __buf);
            codec::top_encode_to_managed_buffer(&b, &mut __buf);
            __buf
        };
    }

    #[endpoint]
    fn encode_packed_two(&self, a: BigUint<Self::Api>, b: BigUint<Self::Api>) -> bytes {
        return {
            let mut __buf = ManagedBuffer::new();
            __buf.append(&ManagedBuffer::from(&a.to_bytes_be_buffer()));
            __buf.append(&ManagedBuffer::from(&b.to_bytes_be_buffer()));
            __buf
        };
    }

    #[endpoint]
    fn decode_hint(&self, data: BigUint<Self::Api>) -> BigUint<Self::Api> {
        return todo!(/* abi.decode: use codec::top_decode_from_managed_buffer */);
    }

}
