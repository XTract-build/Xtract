use crate::helper_functions::convert_expression_to_type;
use crate::parser::ParsedContract;
use crate::rust_ast::{RustExpression, RustNode, RustParameter, RustVisibility};
use crate::statement::{statements_contains_return, transform_statements, snake_to_camel_case};
use crate::type_mapper::map_type;
use anyhow::{anyhow, Result};
use inflector::Inflector;
use solang_parser::pt;


pub fn transform_with_attributes(parsed: ParsedContract) -> Result<String> {
    let mut output = String::new();

    // Add header
    output.push_str("#![no_std]\n\n");
    output.push_str("use multiversx_sc::imports::*;\n\n");


    for part in parsed.solidity_ast.0 {
        if let pt::SourceUnitPart::ContractDefinition(contract) = part {
            let contract_name = contract
                .name
                .as_ref()
                .map(|name| name.name.clone())
                .unwrap_or_default();

            // Generate trait for storage mappers
            output.push_str(&format!(
                "#[multiversx_sc::contract]\npub trait {} {{\n",
                contract_name
            ));
            let rust_body = transform_contract_with_attributes(&contract)?;

            // First, add storage mappers to the trait
            for node in &rust_body {
                if let RustNode::StorageDefinition {
                    name, type_name, ..
                } = node
                {
                    output.push_str(&format!(
                        "    #[storage_mapper(\"{}\")]\n    fn {}(&self) -> SingleValueMapper<{}>;\n",
                        name,
                        name.to_snake_case(),
                        type_name
                    ));
                }
            }

            // Check if there's an init function
            let has_init = rust_body.iter().any(|node| {
                if let RustNode::Function { name, .. } = node {
                    name.is_empty()
                } else {
                    false
                }
            });

            // Add empty init if there's no constructor
            if !has_init {
                output.push_str("\n    #[init]\n");
                output.push_str("    fn init(&self) {}\n");
            }

            // Add events to the trait
            for node in &rust_body {
                if let RustNode::EventDefinition { name, params } = node {
                    let params_str = params
                        .iter()
                        .map(|param| {
                            // Make parameter types references for events
                            let ref_type = if param.type_name.starts_with("&") {
                                param.type_name.clone()
                            } else {
                                format!("&{}", param.type_name)
                            };
                            // Add #[indexed] if the parameter is indexed
                            let indexed_attr = if param.indexed {
                                "#[indexed] "
                            } else {
                                ""
                            };
                            format!("{}{}: {}", indexed_attr, param.name.to_snake_case(), ref_type)
                        })
                        .collect::<Vec<_>>()
                        .join(", ");

                    // Add _event suffix to avoid conflict with function names
                    let event_fn_name = format!("{}_event", name.to_snake_case());
                    output.push_str(&format!(
                        "\n    #[event(\"{}\")]\n    fn {}(&self{});\n",
                        name,
                        event_fn_name,
                        if params_str.is_empty() { "".to_string() } else { format!(", {}", params_str) }
                    ));
                }
            }

            // Add all functions (endpoints and views) to the trait
            for node in rust_body {
                match node {
                    // Handle function definitions
                    RustNode::Function {
                        name,
                        params,
                        body,
                        is_endpoint,
                        is_view,
                        visibility,
                        returns,
                        ..
                    } => {
                        let annotation_name = snake_to_camel_case(&name);

                        let annotation = if is_endpoint {
                            format!("    #[endpoint({})]\n", annotation_name)
                        } else if is_view {
                            format!("    #[view({})]\n", annotation_name)
                        } else if name.is_empty() {
                            "    #[init]\n".to_string()
                        } else {
                            String::new()
                        };
                        output.push_str(&annotation);

                        // Add function signature
                        let function_name =
                            if name.is_empty() { "init" } else { &name.to_snake_case() };
                        // In trait, functions don't need pub - they're public by default in traits
                        let function_visibility = "";

                        let params_str = params
                            .iter()
                            .map(|p| format!("{}: {}", p.name, p.type_name))
                            .collect::<Vec<_>>()
                            .join(", ");

                        // Generate the return type
                        let return_type = if let Some(return_params) = returns {
                            if !return_params.is_empty() {
                                format!(" -> {}", return_params[0].type_name)
                            } else {
                                String::new()
                            }
                        } else {
                            String::new()
                        };

                        output.push_str(&format!(
                            "    {}fn {}(&self{}){} {{\n",
                            function_visibility,
                            function_name,
                            if params_str.is_empty() {
                                String::new()
                            } else {
                                format!(", {}", params_str)
                            },
                            return_type
                        ));

                        // Add function body
                        for stmt in body {
                            output.push_str(&format!(
                                "        {}\n",
                                transform_rust_node_to_code(&stmt)?
                            ));
                        }

                        output.push_str("    }\n");
                    }

                    // Events are already handled above, skip here
                    RustNode::EventDefinition { .. } => {}
                    RustNode::StorageDefinition { .. } => {}
                    _ => {}
                }
            }

            output.push_str("}\n");
        }
    }

    Ok(output)
}

fn transform_rust_node_to_code(node: &RustNode) -> Result<String> {
    match node {
        RustNode::Expression(RustExpression::FunctionCall {
            function,
            arguments,
        }) => {
            if let RustExpression::MemberAccess { expression, member } = *function.clone() {
                // Handle `increment` and `decrement` operations
                if member == "increment" || member == "decrement" {
                    let operation = if member == "increment" { "+" } else { "-" };

                    if let Some(arg) = arguments.first() {
                        let argument_code =
                            transform_rust_node_to_code(&RustNode::Expression(arg.clone()))?;

                        return Ok(format!(
                            "let current_value = self.{}().get();\n        self.{}().set(&(current_value {} 1u32.into()));",
                            argument_code, argument_code, operation
                        ));
                    }
                // Handle `pre_increment` and `pre_decrement` operations
                } else if member == "pre_increment" || member == "pre_decrement" {
                    let operation = if member == "pre_increment" { "+" } else { "-" };

                    if let Some(arg) = arguments.first() {
                        let argument_code =
                            transform_rust_node_to_code(&RustNode::Expression(arg.clone()))?;

                        return Ok(format!(
                            "let current_value = self.{}().get() {} 1u32.into();\n        self.{}().set(&current_value);",
                            argument_code, operation, argument_code
                        ));
                    }
                // Handle `set` calls on storage mappers
                } else if member == "set" {
                    if let Some(arg) = arguments.first() {
                        let storage_variable = transform_rust_node_to_code(&RustNode::Expression(
                            *expression.clone(),
                        ))?;
                        let argument_code =
                            transform_rust_node_to_code(&RustNode::Expression(arg.clone()))?;

                        return Ok(format!(
                            "self.{}().set(&{});",
                            storage_variable, argument_code
                        ));
                    }
                }
            }

            // Fallback to default function call handling for other cases
            let func_code = transform_rust_node_to_code(&RustNode::Expression(*function.clone()))?;
            
            // Check if this is an event call (starts with "self." and doesn't contain "()")
            // Events are called as self.event_name(...) while storage mappers are self.variable()
            // For event calls, arguments should be passed as references
            let func_code_str = func_code.clone();
            let is_event_call = func_code_str.starts_with("self.") && !func_code_str.contains("()");
            
            let args_code = if is_event_call {
                // For events, pass arguments as references
                arguments
                    .iter()
                    .map(|arg| {
                        let arg_code = transform_rust_node_to_code(&RustNode::Expression(arg.clone()))?;
                        // Always pass as reference for event calls
                        Ok(format!("&{}", arg_code))
                    })
                    .collect::<Result<Vec<_>>>()?
                    .join(", ")
            } else {
                arguments
                    .iter()
                    .map(|arg| transform_rust_node_to_code(&RustNode::Expression(arg.clone())))
                    .collect::<Result<Vec<_>>>()?
                    .join(", ")
            };
            Ok(format!("{}({})", func_code, args_code))
        }

        // Handle arithmetic operations
        RustNode::Expression(RustExpression::BinaryOperation {
            left,
            operator,
            right,
        }) => {
            let left_code = transform_rust_node_to_code(&RustNode::Expression(*left.clone()))?;
            let right_code = transform_rust_node_to_code(&RustNode::Expression(*right.clone()))?;
            // Wrap binary operations in parentheses for safety
            Ok(format!("({} {} {})", left_code, operator, right_code))
        }

        // Handle variable identifiers
        RustNode::Expression(RustExpression::Identifier(name)) => Ok(name.clone()),

        // Handle number literals
        RustNode::Expression(RustExpression::NumberLiteral(value)) => Ok(value.clone()),
        
        // Handle bool literals
        RustNode::Expression(RustExpression::BoolLiteral(value)) => Ok(value.to_string()),

        // Handle block nodes
        RustNode::Function { name, body, .. } if name == "block" => {
            let body_code = body
                .iter()
                .map(transform_rust_node_to_code)
                .collect::<Result<Vec<_>>>()?
                .join("\n        ");
            Ok(body_code)
        }

        // Handle assignments
        RustNode::Assignment { target, value } => {
            let target_code = transform_rust_node_to_code(&RustNode::Expression(*target.clone()))?;
            // Transform value - if it contains storage variable access, convert to get()
            let value_code = transform_value_with_storage_access(&RustNode::Expression(*value.clone()))?;
            Ok(format!("self.{}().set(&{});", target_code, value_code))
        }

        // Handle return statements
        RustNode::Return(Some(expression)) => {
            if let RustExpression::Identifier(name) = expression.clone() {
                // Check if it's a storage variable - if so, return get() call
                Ok(format!("self.{}().get()", name.to_snake_case()))
            } else if let RustExpression::BoolLiteral(value) = expression.clone() {
                // Return bool literal without "return" keyword
                Ok(value.to_string())
            } else {
                let return_value =
                    transform_rust_node_to_code(&RustNode::Expression(expression.clone()))?;
                // Return expression value without "return" keyword (MultiversX style)
                Ok(return_value)
            }
        }

        RustNode::Return(None) => Ok("return;".to_string()),

        // Handle function definitions
        RustNode::Function {
            name,
            params,
            body,
            visibility,
            ..
        } => {
            let visibility_str = if *visibility == RustVisibility::Public {
                "pub "
            } else {
                ""
            };

            let params_str = params
                .iter()
                .map(|param| format!("{}: {}", param.name, param.type_name))
                .collect::<Vec<_>>()
                .join(", ");

            let body_code = body
                .iter()
                .map(transform_rust_node_to_code)
                .collect::<Result<Vec<_>>>()?
                .join("\n        ");

            Ok(format!(
                "    {}fn {}(&self{}) {{\n        {}\n    }}",
                visibility_str,
                name,
                if params_str.is_empty() {
                    "".to_string()
                } else {
                    format!(", {}", params_str)
                },
                body_code
            ))
        }

        // Handle require statements
        RustNode::Require { condition, message } => {
            let condition_code = transform_rust_node_to_code(&RustNode::Expression(condition.clone()))?;
            if let Some(msg) = message {
                let msg_code = transform_rust_node_to_code(&RustNode::Expression(msg.clone()))?;
                Ok(format!("require!({}, {});", condition_code, msg_code))
            } else {
                Ok(format!("require!({});", condition_code))
            }
        }

        // Unsupported cases
        _ => Err(anyhow!("Unsupported RustNode type: {:?}", node)),
    }
}

// Helper function to transform value expressions, handling storage variable access
fn transform_value_with_storage_access(node: &RustNode) -> Result<String> {
    match node {
        RustNode::Expression(RustExpression::Identifier(name)) => {
            // Check if this is a storage variable - if so, use get()
            Ok(format!("self.{}().get()", name.to_snake_case()))
        }
        RustNode::Expression(RustExpression::BinaryOperation { left, operator, right }) => {
            let left_code = transform_value_with_storage_access(&RustNode::Expression(*left.clone()))?;
            let right_code = transform_value_with_storage_access(&RustNode::Expression(*right.clone()))?;
            Ok(format!("({} {} {})", left_code, operator, right_code))
        }
        _ => transform_rust_node_to_code(node),
    }
}

fn transform_contract_with_attributes(contract: &pt::ContractDefinition) -> Result<Vec<RustNode>> {
    let mut rust_nodes = Vec::new();

    for part in &contract.parts {
        match part {
            pt::ContractPart::VariableDefinition(var) => {
                let name = var
                    .name
                    .as_ref()
                    .map(|id| id.name.clone())
                    .unwrap_or_default();
                let type_name = map_type(&convert_expression_to_type(&var.ty)?)?;
                rust_nodes.push(RustNode::StorageDefinition { name, type_name });
            }
            pt::ContractPart::FunctionDefinition(func) => {
                rust_nodes.push(transform_function_with_attributes(func)?);
            }
            pt::ContractPart::EnumDefinition(enum_def) => {
                let name = enum_def
                    .name
                    .as_ref()
                    .map(|id| id.name.clone())
                    .unwrap_or_default();
                let variants = enum_def
                    .values
                    .iter()
                    .map(|variant| {
                        variant
                            .as_ref()
                            .map(|id| id.name.clone())
                            .unwrap_or_default()
                    })
                    .collect();
                rust_nodes.push(RustNode::EnumDefinition { name, variants });
            }
            pt::ContractPart::StructDefinition(struct_def) => {
                let name = struct_def
                    .name
                    .as_ref()
                    .map(|id| id.name.clone())
                    .unwrap_or_default();
                let fields = struct_def
                    .fields
                    .iter()
                    .map(|field| {
                        let field_name = field
                            .name
                            .as_ref()
                            .map(|id| id.name.clone())
                            .unwrap_or_default();
                        let field_type = map_type(&convert_expression_to_type(&field.ty)?)?;
                        Ok(RustParameter {
                            name: field_name,
                            type_name: field_type,
                            indexed: false,
                        })
                    })
                    .collect::<Result<Vec<_>>>()?;
                rust_nodes.push(RustNode::StructDefinition { name, fields });
            }
            pt::ContractPart::EventDefinition(event_def) => {
                let name = event_def
                    .name
                    .as_ref()
                    .map(|id| id.name.clone())
                    .unwrap_or_default();
            
                let params = event_def
                    .fields
                    .iter()
                    .map(|param| {
                        let param_name = param
                            .name
                            .as_ref()
                            .map(|id| id.name.clone())
                            .unwrap_or_default();
                        
                        let param_type = map_type(&convert_expression_to_type(&param.ty)?)?;
                        
                        // For events, parameters should be references
                        let ref_type = format!("&{}", param_type);
            
                        // Check if the parameter is indexed
                        let indexed = param.indexed;
            
                        Ok((param_name, ref_type, indexed))
                    })
                    .collect::<Result<Vec<(String, String, bool)>>>()?;
            
                rust_nodes.push(RustNode::EventDefinition {
                    name,
                    params: params
                        .into_iter()
                        .map(|(param_name, param_type, indexed)| RustParameter {
                            name: param_name,
                            type_name: param_type,
                            indexed,
                        })
                        .collect(),
                });
            }
            _ => {
                // Log unsupported parts for debugging
                println!("Unsupported contract part: {:?}", part);
            }
        }
    }

    Ok(rust_nodes)
}

fn transform_function_with_attributes(func: &pt::FunctionDefinition) -> Result<RustNode> {
    let params = func
        .params
        .iter()
        .filter_map(|(_, param)| param.as_ref())
        .map(|p| {
            let type_name = convert_expression_to_type(&p.ty)?;
            Ok(RustParameter {
                name: p
                    .name
                    .as_ref()
                    .map(|id| id.name.clone())
                    .unwrap_or_default(),
                type_name: map_type(&type_name)?,
                indexed: false,
            })
        })
        .collect::<Result<Vec<_>>>()?;

    let returns = if func.returns.is_empty() {
        None
    } else {
        Some(
            func.returns
                .iter()
                .filter_map(|(_, param)| param.as_ref())
                .map(|p| {
                    let type_name = convert_expression_to_type(&p.ty)?;
                    Ok(RustParameter {
                        name: p
                            .name
                            .as_ref()
                            .map(|id| id.name.clone())
                            .unwrap_or_default(),
                        type_name: map_type(&type_name)?,
                        indexed: false,
                    })
                })
                .collect::<Result<Vec<_>>>()?,
        )
    };

    // Determine visibility
    let visibility = func
        .attributes
        .iter()
        .find_map(|attr| {
            if let pt::FunctionAttribute::Visibility(vis) = attr {
                match vis {
                    pt::Visibility::Public(_) => Some(RustVisibility::Public),
                    pt::Visibility::Internal(_) | pt::Visibility::Private(_) => {
                        Some(RustVisibility::Private)
                    }
                    pt::Visibility::External(_) => Some(RustVisibility::Public),
                }
            } else {
                None
            }
        })
        .unwrap_or(RustVisibility::Private);

    // Check for return statement and determine body type
    let body_contains_return = match &func.body {
        Some(statements) => statements_contains_return(&[statements.clone()]),
        None => false,
    };

    let is_view = func
        .name
        .as_ref()
        .map(|id| id.name.contains("get"))
        .unwrap_or(false);
    let _ = &&body_contains_return;

    let is_endpoint = !is_view
        && !func
            .name
            .as_ref()
            .map(|id| id.name.is_empty())
            .unwrap_or(true);

    let body = match &func.body {
        Some(statements) => transform_statements(&[statements.clone()])?,
        None => Vec::new(),
    };

    Ok(RustNode::Function {
        name: func
            .name
            .as_ref()
            .map(|id| id.name.clone())
            .unwrap_or_default(),
        params,
        returns,
        body,
        visibility,
        is_endpoint,
        is_view,
    })
}


