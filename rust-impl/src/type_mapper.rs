use solang_parser::pt::Type;
use anyhow::{Result, anyhow};

pub fn map_type(ty: &Type) -> Result<String> {
    match ty {
        Type::Bool => Ok("bool".to_string()),
        Type::Address => Ok("ManagedAddress<Self::Api>".to_string()),
        Type::AddressPayable => Ok("ManagedAddress<Self::Api>".to_string()),
        Type::Payable => Ok("ManagedAddress<Self::Api>".to_string()),
        Type::String => Ok("ManagedBuffer<Self::Api>".to_string()),
        Type::Int(size) => {
            let size_val = *size;
            match size_val {
                8 => Ok("i8".to_string()),
                16 => Ok("i16".to_string()),
                32 => Ok("i32".to_string()),
                64 => Ok("i64".to_string()),
                128 => Ok("BigInt<Self::Api>".to_string()),
                256 => Ok("BigInt<Self::Api>".to_string()),
                _ => Ok("BigInt<Self::Api>".to_string()), // Default to BigInt
            }
        },
        Type::Uint(size) => {
            let size_val = *size;
            match size_val {
                8 => Ok("u8".to_string()),
                16 => Ok("u16".to_string()), 
                32 => Ok("u32".to_string()),
                64 => Ok("u64".to_string()),
                128 => Ok("BigUint<Self::Api>".to_string()),
                256 => Ok("BigUint<Self::Api>".to_string()),
                _ => Ok("BigUint<Self::Api>".to_string()), // Default to BigUint
            }
        },
        Type::Bytes(size) => {
            let size_val = *size;
            if size_val <= 32 {
                Ok(format!("[u8; {}]", size_val))
            } else {
                Ok("ManagedBuffer<Self::Api>".to_string())
            }
        },
        Type::DynamicBytes => Ok("ManagedBuffer<Self::Api>".to_string()),
        // Note: These type variants may not exist in the version of solang-parser being used
        // They are handled in a catch-all at the end
        // Uncomment and fix if your version supports them:
        /*
        Type::Mapping { key_ty, value_ty, .. } => {
            // Extract the key type
            let key_type = match &**key_ty {
                Type::Address | Type::AddressPayable | Type::Payable => 
                    Ok("ManagedAddress<Self::Api>".to_string()),
                Type::Uint(size) => {
                    let size_val = *size;
                    match size_val {
                        8 => Ok("u8".to_string()),
                        16 => Ok("u16".to_string()),
                        32 => Ok("u32".to_string()),
                        64 => Ok("u64".to_string()),
                        _ => Ok("BigUint<Self::Api>".to_string()),
                    }
                },
                Type::String => Ok("ManagedBuffer<Self::Api>".to_string()),
                _ => Err(anyhow!("Unsupported mapping key type: {:?}", key_ty)),
            }?;

            // Extract the value type
            let value_type = map_type(&**value_ty)?;
            
            // For simple key types, use MapMapper
            match key_type.as_str() {
                "u8" | "u16" | "u32" | "u64" | "ManagedAddress<Self::Api>" => {
                    Ok(format!("MapMapper<Self::Api, {}, {}>", key_type, value_type))
                },
                _ => {
                    // For more complex keys, use UnorderedMapMapper
                    Ok(format!("UnorderedMapMapper<Self::Api, {}, {}>", key_type, value_type))
                }
            }
        },
        */
        // Add any other variants as needed
        _ => Err(anyhow!("Unsupported type: {:?}", ty)),
    }
}