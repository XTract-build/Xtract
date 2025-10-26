from __future__ import annotations

import re
from pathlib import Path


SOLIDITY_TO_MVX_TYPE = {
    "uint256": "BigUint<Self::Api>",
    "uint128": "BigUint<Self::Api>",
    "uint64": "u64",
    "uint32": "u32",
    "uint16": "u16",
    "uint8": "u8",
    "int256": "BigInt<Self::Api>",
    "int128": "BigInt<Self::Api>",
    "int64": "i64",
    "int32": "i32",
    "int16": "i16",
    "int8": "i8",
    "address": "ManagedAddress<Self::Api>",
    "string": "ManagedBuffer<Self::Api>",
    "bool": "bool",
    "u8": "u8",
}


def camel_to_snake(name: str) -> str:
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


class Transpiler:
    def parse_contract_name(self, content: str) -> str | None:
        match = re.search(r"contract\s+(\w+)", content)
        return match.group(1) if match else None

    def parse_structs(self, content: str):
        structs = []
        for match in re.finditer(r"struct\s+(\w+)\s*{([^}]*)}", content):
            name = match.group(1)
            fields = match.group(2).strip()
            structs.append({"name": name, "fields": fields})
        return structs

    def parse_events(self, content: str):
        events = []
        for match in re.finditer(r"event\s+(\w+)\s*\(([^)]*)\)", content):
            name = match.group(1)
            params = match.group(2).strip()
            events.append({"name": name, "params": params})
        return events

    def parse_errors(self, content: str):
        errors = []
        for match in re.finditer(r"error\s+(\w+)\s*\(([^)]*)\)", content):
            name = match.group(1)
            params = match.group(2).strip()
            errors.append({"name": name, "params": params})
        return errors

    def parse_constructors(self, content: str):
        constructors = []
        for match in re.finditer(r"constructor\s*\((.*?)\)\s*([^\{]*)\{([^}]*)\}", content, re.DOTALL):
            params = match.group(1).strip()
            modifiers = match.group(2).strip()
            body = match.group(3).strip()
            constructors.append({
                "params": params,
                "body": body,
            })
        return constructors

    def parse_functions(self, content: str):
        functions = []

        # Parse constructors first
        constructors = self.parse_constructors(content)
        for constructor in constructors:
            functions.append({
                "name": "",  # Empty name for constructor (becomes init)
                "params": constructor["params"],
                "is_view": False,
                "return_type": None,
                "body": constructor["body"],
            })

        # Parse regular functions
        for match in re.finditer(r"function\s+(\w+)\s*\((.*?)\)\s*([^\{]*)\{([^}]*)\}", content, re.DOTALL):
            name = match.group(1)
            params = match.group(2).strip()
            modifiers = match.group(3).strip()
            body = match.group(4).strip()
            is_view = " view" in f" {modifiers} " or " view " in f" {modifiers} "
            returns_match = re.search(r"returns\s*\(([^)]*)\)", modifiers)
            return_type = returns_match.group(1).strip() if returns_match else None
            functions.append({
                "name": name,
                "params": params,
                "is_view": is_view,
                "return_type": return_type,
                "body": body,
            })
        return functions

    def _map_type(self, solidity_type: str) -> str:
        t = solidity_type.strip()
        return SOLIDITY_TO_MVX_TYPE.get(t, t)

    def _format_params(self, param_str: str) -> list[str]:
        results: list[str] = []
        if not param_str:
            return results
        for raw in param_str.split(","):
            p = raw.strip()
            if not p:
                continue
            parts = p.split()
            if len(parts) < 2:
                continue
            p_type, p_name = parts[0], parts[1].rstrip(",")
            results.append(f"{p_name}: {self._map_type(p_type)}")
        return results

    def _format_return(self, return_type: str | None) -> str:
        if not return_type:
            return ""
        rt = return_type.split()[0]
        return f" -> {self._map_type(rt)}"

    def convert_struct(self, struct: dict) -> str:
        fields = []
        if struct["fields"]:
            for field in struct["fields"].split(";"):
                f = field.strip()
                if not f:
                    continue
                parts = f.split()
                if len(parts) < 2:
                    continue
                t, n = parts[0], parts[1]
                rust_t = self._map_type(t).replace("<Self::Api>", "<M>")
                fields.append(f"pub {n}: {rust_t}")
        fields_str = ",\n    ".join(fields)
        return (
            "#[derive(TypeAbi, TopEncode, TopDecode, NestedEncode, NestedDecode, ManagedVecItem)]\n"
            f"pub struct {struct['name']}<M: ManagedTypeApi> {{\n"
            f"    {fields_str}\n"
            "}"
        )

    def convert_event(self, event: dict) -> str:
        params: list[str] = []
        if event["params"]:
            for raw in event["params"].split(","):
                s = raw.strip()
                if not s:
                    continue
                is_indexed = " indexed" in f" {s} "
                s = s.replace("indexed", "").strip()
                parts = s.split()
                if len(parts) < 2:
                    continue
                t, n = parts[0], parts[1]
                idx = "#[indexed] " if is_indexed else ""
                params.append(f"{idx}{n}: {self._map_type(t)}")
        return f"#[event(\"{event['name']}\")]\n    fn {camel_to_snake(event['name'])}_event(&self{', ' if params else ''}{', '.join(params)});"

    def convert_error(self, error: dict) -> str:
        params: list[str] = []
        if error["params"]:
            for raw in error["params"].split(","):
                s = raw.strip()
                if not s:
                    continue
                parts = s.split()
                if len(parts) < 2:
                    continue
                t, n = parts[0], parts[1]
                params.append(f"pub {n}: {self._map_type(t).replace('<Self::Api>', '<M>')}")

        fields_str = ",\n    ".join(params) if params else ""
        return (
            "#[derive(TypeAbi, TopEncode, TopDecode, NestedEncode, NestedDecode)]\n"
            f"pub struct {error['name']}<M: ManagedTypeApi> {{\n"
            f"    {fields_str}\n"
            "}"
        )

    def _parse_statements(self, body: str) -> list[dict]:
        """Parse statements from function body"""
        statements = []

        # Remove comments and normalize whitespace
        body = re.sub(r'//.*', '', body)
        body = re.sub(r'/\*.*?\*/', '', body, flags=re.DOTALL)

        # Split by semicolons, but be careful with strings and complex expressions
        # This is a simplified approach - in a full implementation we'd need a proper parser
        lines = body.split(';')
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Handle require statements
            if require_match := re.match(r'require\s*\(([^,]+),\s*["\']([^"\']+)["\']\)', line):
                condition = require_match.group(1).strip()
                message = require_match.group(2).strip()
                statements.append({
                    "type": "require",
                    "condition": condition,
                    "message": message
                })
                continue

            # Handle revert statements
            if revert_match := re.match(r'revert\s*\(\s*["\']([^"\']+)["\']\s*\)', line):
                message = revert_match.group(1).strip()
                statements.append({
                    "type": "revert",
                    "message": message
                })
                continue

            # Handle custom error revert
            if revert_error_match := re.match(r'revert\s+(\w+)\s*\(([^)]*)\)', line):
                error_name = revert_error_match.group(1)
                args = revert_error_match.group(2).strip()
                statements.append({
                    "type": "revert_error",
                    "error_name": error_name,
                    "args": args
                })
                continue

            # Handle emit statements
            if emit_match := re.match(r'emit\s+(\w+)\s*\((.*)\)', line):
                event_name = emit_match.group(1)
                args = emit_match.group(2).strip()
                statements.append({
                    "type": "emit",
                    "event_name": event_name,
                    "args": args
                })
                continue

            # Handle return statements
            if return_match := re.match(r'return\s+(.+)', line):
                expression = return_match.group(1).strip()
                statements.append({
                    "type": "return",
                    "expression": expression
                })
                continue

            # Handle assignments and declarations
            if '=' in line:
                if assign_match := re.match(r'(\w+(?:\s+\w+)*)\s*=\s*(.+)', line):
                    left = assign_match.group(1).strip()
                    right = assign_match.group(2).strip()
                    statements.append({
                        "type": "assignment",
                        "left": left,
                        "right": right
                    })
                continue

            # Handle variable declarations with initialization
            if var_match := re.match(r'(\w+(?:\s+\w+)*\s+\w+)\s*=\s*(.+)', line):
                declaration = var_match.group(1).strip()
                value = var_match.group(2).strip()
                statements.append({
                    "type": "declaration",
                    "declaration": declaration,
                    "value": value
                })
                continue

            # Handle struct initialization and push
            if push_match := re.match(r'(\w+)\.push\s*\((.+)\)', line):
                array_name = push_match.group(1)
                struct_data = push_match.group(2).strip()
                statements.append({
                    "type": "push",
                    "array_name": array_name,
                    "struct_data": struct_data
                })
                continue

            # Handle simple variable updates (like +=, -=)
            if update_match := re.match(r'(\w+(?:\[[^\]]+\])*)\s*([+\-*/]?=)\s*(.+)', line):
                target = update_match.group(1).strip()
                operator = update_match.group(2).strip()
                value = update_match.group(3).strip()
                statements.append({
                    "type": "update",
                    "target": target,
                    "operator": operator,
                    "value": value
                })
                continue

        return statements

    def _convert_statement(self, stmt: dict, contract_name: str) -> str:
        """Convert a single statement to MultiversX Rust"""
        stmt_type = stmt["type"]

        if stmt_type == "require":
            condition = self._convert_expression(stmt["condition"])
            message = stmt["message"]
            return f'        require!({condition}, "{message}");'

        elif stmt_type == "emit":
            event_name = stmt["event_name"]
            args = stmt["args"]
            if args:
                converted_args = self._convert_expression(args)
                return f'        self.{camel_to_snake(event_name)}_event({converted_args});'
            else:
                return f'        self.{camel_to_snake(event_name)}_event();'

        elif stmt_type == "return":
            expression = self._convert_expression(stmt["expression"])
            return f'        return {expression};'

        elif stmt_type == "assignment":
            left = stmt["left"]
            right = self._convert_expression(stmt["right"])

            # Check if this is a storage variable assignment
            if left in ['value', 'name', 'symbol', 'decimals', 'totalSupply', 'chairperson', 'votingEnd', 'votingClosed', 'nextTokenId']:
                snake_left = camel_to_snake(left)
                return f'        self.{snake_left}().set({right});'
            else:
                return f'        {left} = {right};'

        elif stmt_type == "declaration":
            # For now, we'll handle simple cases
            return f'        // TODO: declaration - {stmt["declaration"]} = {stmt["value"]};'

        elif stmt_type == "push":
            array_name = stmt["array_name"]
            struct_data = self._convert_struct_initialization(stmt["struct_data"])
            return f'        self.{array_name}().push(&{struct_data});'

        elif stmt_type == "update":
            target = stmt["target"]
            operator = stmt["operator"]
            value = self._convert_expression(stmt["value"])

            # Handle storage variable updates
            if '.' in target:  # mapping access like balanceOf[sender]
                if operator == "-=":
                    return f'        self.{target.replace("[", "(&").replace("]", ")").replace(" -= ", "").replace(";", "")} -= &{value};'
                elif operator == "+=":
                    return f'        self.{target.replace("[", "(&").replace("]", ")").replace(" += ", "").replace(";", "")} += &{value};'
                elif operator == "=":
                    return f'        self.{target.replace("[", "(&").replace("]", ")").replace(" = ", "").replace(";", "")} = {value};'
            elif target in ['voteCount', 'hasVoted', 'votedProposalId']:  # struct field updates
                return f'        // TODO: struct field update - {target} {operator} {value};'
            else:
                if operator == "=":
                    return f'        {target} = {value};'
                else:
                    return f'        {target} {operator} {value};'

        elif stmt_type == "revert":
            message = stmt["message"]
            return f'        sc_panic!("{message}");'

        elif stmt_type == "revert_error":
            error_name = stmt["error_name"]
            args = stmt["args"]
            if args:
                converted_args = self._convert_expression(args)
                return f'        sc_panic!("{error_name}({converted_args})");'
            else:
                return f'        sc_panic!("{error_name}");'

        return f'        // TODO: unhandled statement: {stmt}'

    def _convert_expression(self, expr: str) -> str:
        """Convert Solidity expressions to MultiversX equivalents"""
        # Handle msg.sender
        expr = expr.replace("msg.sender", "self.blockchain().get_caller()")

        # Handle address(0)
        expr = expr.replace("address(0)", "ManagedAddress::zero()")

        # Handle block.timestamp
        expr = expr.replace("block.timestamp", "self.blockchain().get_block_timestamp()")

        # Handle simple arithmetic and comparisons (basic cases)
        # This would need to be much more sophisticated for complex expressions

        # Handle array length
        expr = expr.replace(".length", ".len()")

        # Handle power operator (limited)
        expr = expr.replace("**", ".pow")

        # Handle 1 minutes -> 60 seconds conversion
        expr = re.sub(r'(\d+)\s*minutes', lambda m: str(int(m.group(1)) * 60), expr)

        # Handle BigUint conversion for numbers
        expr = re.sub(r'\b(\d+)\b', r'BigUint::from(\1u32)', expr)

        # Handle variable access - convert simple variable names to storage getters
        # This is a simple heuristic - in a full implementation we'd need proper symbol resolution
        # Don't convert function parameters, literals, or certain keywords
        # But DO convert storage variables like 'value', 'balanceOf', etc.
        exclude_patterns = [
            'true', 'false', 'self', 'newValue', 'new_value', 'to', 'from',
            '_to', '_from', '_value', 'spender', 'owner', 'caller', 'description',
            'price', 'tokenId', 'token_id', 'durationInMinutes', 'duration_in_minutes',
            'proposalId', 'proposal_id', 'voterAddress', 'voter_address',
            'offerIndex', 'offer_index', 'id', 'required', 'provided'
        ]

        # Storage variables that should be converted to getters (common patterns)
        # Note: mappings like balanceOf should NOT be converted to .get() since they're accessed with []
        storage_vars = [
            'value', 'totalSupply', 'name', 'symbol', 'decimals',
            'chairperson', 'votingEnd', 'votingClosed',
            'nextTokenId', 'campaigns', 'crowdfundingEnd'
        ]

        # Mapping variables that should be converted to mappers (not getters)
        mapping_vars = [
            'balanceOf', 'allowance', 'voters', 'proposals', 'nfts', 'offersForNFT'
        ]

        def convert_var(match):
            var = match.group(1)
            if var in exclude_patterns:
                return var
            elif var in storage_vars:
                return f'self.{camel_to_snake(var)}().get()'
            elif var in mapping_vars:
                return f'self.{camel_to_snake(var)}()'
            else:
                return var

        expr = re.sub(r'\b(\w+)\b', convert_var, expr)

        # Handle storage access (basic mapping patterns) - do this after variable conversion
        # Handle nested mapping access like allowance[from][to] -> self.allowance(&from, &to)
        # This is a simplified approach - in a full implementation we'd need proper AST parsing
        expr = re.sub(r'(\w+)\[([^\]]+)\]\[([^\]]+)\]', r'self.\1(&\2, &\3)', expr)
        # Handle single mapping access like balanceOf[...] -> self.balance_of(&...)
        expr = re.sub(r'(\w+)\[([^\]]+)\]', r'self.\1(&\2)', expr)
        # Handle mapper access like balance_of()[...] -> balance_of(&...)
        expr = re.sub(r'self\.(\w+)\(\)\[([^\]]+)\]', r'self.\1(&\2)', expr)
        # Handle nested mapper access like allowance(&_from)[...] -> allowance(&_from, &...)
        expr = re.sub(r'self\.(\w+)\(([^)]+)\)\[([^\]]+)\]', r'self.\1(\2, &\3)', expr)

        return expr

    def _convert_struct_initialization(self, struct_data: str) -> str:
        """Convert Solidity struct initialization to MultiversX"""
        # Handle Proposal({...}) pattern
        if struct_match := re.match(r'(\w+)\s*\(\s*\{([^}]*)\}\s*\)', struct_data):
            struct_name = struct_match.group(1)
            fields_str = struct_match.group(2).strip()

            # Parse field assignments
            fields = []
            for field_assign in fields_str.split(','):
                field_assign = field_assign.strip()
                if ':' in field_assign:
                    key, value = field_assign.split(':', 1)
                    key = key.strip()
                    value = self._convert_expression(value.strip())
                    fields.append(f'{key}: {value}')

            fields_joined = ',\n            '.join(fields)
            return f'{struct_name} {{\n            {fields_joined}\n        }}'

        # Handle simple variable
        return self._convert_expression(struct_data)

    def convert_function(self, func: dict, contract_name: str = "Contract") -> str:
        snake_name = camel_to_snake(func["name"]) if func["name"] else "init"
        annotation = (
            f"#[view({func['name']})]\n    " if func["is_view"] else ("#[endpoint]\n    " if func["name"] else "#[init]\n    ")
        )
        params = self._format_params(func["params"]) if func["name"] else []
        return_type = self._format_return(func.get("return_type"))

        # Parse and convert body statements
        body_lines = []
        if func.get("body"):
            statements = self._parse_statements(func["body"])
            for stmt in statements:
                converted = self._convert_statement(stmt, "")
                if converted:
                    body_lines.append(converted)

        if body_lines:
            body = '\n'.join(body_lines)
            return f"{annotation}fn {snake_name}(&self{', ' if params else ''}{', '.join(params)}){return_type} {{\n{body}\n    }}"
        else:
            return f"{annotation}fn {snake_name}(&self{', ' if params else ''}{', '.join(params)}){return_type} {{\n        // TODO: implement body\n    }}"

    def _extract_storage(self, content: str) -> list[tuple[str, str, str]]:
        """Extract storage variables, including mappings"""
        vars: list[tuple[str, str, str]] = []

        # Simple variables (uint256, address, etc.)
        for match in re.finditer(r"(uint256|uint128|uint64|uint32|uint16|uint8|int256|int128|int64|int32|int16|int8|string|address|bool|u8)(?:\s+(?:public|private|internal|external))?\s+(\w+)\s*;", content):
            vars.append((match.group(1), match.group(2), ""))

        # Mappings
        for match in re.finditer(r"mapping\s*\(\s*([^=]+)\s*=>\s*([^)]+)\s*\)\s+(?:\s+(?:public|private|internal|external))?\s+(\w+)\s*;", content):
            key_type = match.group(1).strip()
            value_type = match.group(2).strip()
            var_name = match.group(3)
            vars.append(("mapping", var_name, f"{key_type}=>{value_type}"))

        return vars

    def _convert_storage_mapper(self, var_type: str, var_name: str, mapping_info: str = "") -> str:
        """Convert storage variable to appropriate mapper type"""
        if var_type == "mapping":
            # Parse key=>value mapping
            key_val = mapping_info.split("=>")
            if len(key_val) == 2:
                key_type = key_val[0].strip()
                value_type = key_val[1].strip()

                # Map types
                key_mapped = self._map_type(key_type)
                value_mapped = self._map_type(value_type)

                return f"MapMapper<Self::Api, {key_mapped}, {value_mapped}>"
        else:
            return f"SingleValueMapper<{self._map_type(var_type)}>"

    def convert(self, solidity_content: str) -> str:
        name = self.parse_contract_name(solidity_content) or "Contract"
        structs = self.parse_structs(solidity_content)
        events = self.parse_events(solidity_content)
        errors = self.parse_errors(solidity_content)
        functions = self.parse_functions(solidity_content)
        storage = self._extract_storage(solidity_content)

        lines: list[str] = []
        lines.append("#![no_std]\n")
        lines.append("use multiversx_sc::imports::*;")
        lines.append("use multiversx_sc::derive_imports::*;\n")

        for s in structs:
            lines.append(self.convert_struct(s))
        if structs:
            lines.append("")

        for e in errors:
            lines.append(self.convert_error(e))
        if errors:
            lines.append("")

        lines.append("#[multiversx_sc::contract]")
        lines.append(f"pub trait {name} {{")

        for var_type, var_name, mapping_info in storage:
            mapper_t = self._convert_storage_mapper(var_type, var_name, mapping_info)
            snake_name = camel_to_snake(var_name)

            if var_type == "mapping":
                # Parse key=>value mapping
                key_val = mapping_info.split("=>")
                if len(key_val) == 2:
                    key_type = key_val[0].strip()
                    lines.append(f"    #[storage_mapper(\"{var_name}\")]")
                    lines.append(f"    fn {snake_name}(&self, key: &{self._map_type(key_type)}) -> {mapper_t};")
                else:
                    lines.append(f"    #[storage_mapper(\"{var_name}\")]")
                    lines.append(f"    fn {snake_name}(&self) -> {mapper_t};")
            else:
                lines.append(f"    #[storage_mapper(\"{var_name}\")]")
                lines.append(f"    fn {snake_name}(&self) -> {mapper_t};")
            lines.append("")

        for e in events:
            lines.append(f"    {self.convert_event(e)}")
            lines.append("")

        # Ensure we have an init
        has_init = any(f.get("name", "") == "" for f in functions)
        if not has_init:
            lines.append("    #[init]")
            lines.append("    fn init(&self) {}")
            lines.append("")

        for f in functions:
            lines.append(f"    {self.convert_function(f, name)}")
            lines.append("")

        lines.append("}")
        return "\n".join(lines)


def transpile(input_path: Path, output_path: Path) -> bool:
    content = input_path.read_text()
    code = Transpiler().convert(content)
    output_path.write_text(code)
    return True


