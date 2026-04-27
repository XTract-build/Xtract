from __future__ import annotations

import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class TranspilationWarning:
    """Represents a warning during transpilation"""
    message: str
    line: Optional[int] = None
    severity: str = "warning"  # warning, info, error


@dataclass
class TranspilationResult:
    """Result of transpilation with diagnostics"""
    code: str
    success: bool = True
    warnings: list[TranspilationWarning] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def add_warning(self, message: str, line: Optional[int] = None, severity: str = "warning"):
        self.warnings.append(TranspilationWarning(message, line, severity))

    def add_error(self, message: str):
        self.errors.append(message)
        self.success = False


LIBRARY_FUNCTION_MAP = {
    # (library_name, method_name): (num_args, transform_fn)
    # transform_fn receives a list of already-split argument strings
    ("SafeMath", "add"): (2, lambda args: f"{args[0]} + {args[1]}"),
    ("SafeMath", "sub"): (2, lambda args: f"{args[0]} - {args[1]}"),
    ("SafeMath", "mul"): (2, lambda args: f"{args[0]} * {args[1]}"),
    ("SafeMath", "div"): (2, lambda args: f"{args[0]} / {args[1]}"),
    ("SafeMath", "mod"): (2, lambda args: f"{args[0]} % {args[1]}"),
    ("Math",     "max"): (2, lambda args: f"std::cmp::max({args[0]}, {args[1]})"),
    ("Math",     "min"): (2, lambda args: f"std::cmp::min({args[0]}, {args[1]})"),
    ("Strings",  "toString"): (1, lambda args: f"/* TODO: Strings.toString({args[0]}) — use ManagedBuffer */"),
    ("Address",  "isContract"): (1, lambda args: f"!{args[0]}.is_zero()"),
}

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
    def __init__(self):
        # Populated by convert() from _extract_storage() before any expression conversion
        self._storage_var_names: set[str] = set()
        self._storage_var_types: dict[str, str] = {}
        self._current_var_types: dict[str, str] = {}
        self._mapping_var_names: dict[str, int] = {}  # name → number of keys
        self._array_var_names: set[str] = set()  # VecMapper array variables
        self._using_for: dict[str, str] = {}   # type_name -> library_name
        self._warnings: list[TranspilationWarning] = []

    def parse_contract_name(self, content: str) -> str | None:
        # Match contract definition at beginning of line (not in comments)
        # Remove single-line comments first
        content_no_comments = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        # Remove multi-line comments
        content_no_comments = re.sub(r'/\*.*?\*/', '', content_no_comments, flags=re.DOTALL)

        # Now search for contract definition
        match = re.search(r'\bcontract\s+(\w+)', content_no_comments)
        return match.group(1) if match else None

    def parse_inheritance(self, content: str) -> list[str]:
        """Parse inherited contracts from Solidity code (contract A is B, C)"""
        # Remove comments first
        content_no_comments = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        content_no_comments = re.sub(r'/\*.*?\*/', '', content_no_comments, flags=re.DOTALL)

        parents = []
        # Match: contract Name is Parent1, Parent2, ...
        match = re.search(r"contract\s+\w+\s+is\s+([^{]+)\s*\{", content_no_comments)
        if match:
            parents_str = match.group(1).strip()
            # Split by comma and clean up
            # Use a more robust split that doesn't split on commas inside parentheses
            parts = []
            current_part = []
            paren_depth = 0
            for char in parents_str:
                if char == '(':
                    paren_depth += 1
                elif char == ')':
                    paren_depth -= 1

                if char == ',' and paren_depth == 0:
                    parts.append("".join(current_part))
                    current_part = []
                else:
                    current_part.append(char)
            parts.append("".join(current_part))

            for parent in parts:
                parent_name = parent.strip()
                # Handle constructor arguments in inheritance: Parent(arg1, arg2)
                # Use a more robust regex or loop to handle nested parentheses
                while re.search(r'\([^()]*\)', parent_name):
                    parent_name = re.sub(r'\([^()]*\)', '', parent_name).strip()
                if parent_name:
                    parents.append(parent_name)
        return parents

    def parse_abstract_contract(self, content: str) -> bool:
        """Check if contract is abstract"""
        return bool(re.search(r"abstract\s+contract\s+\w+", content))

    def parse_interface(self, content: str) -> str | None:
        """Parse interface name from Solidity code"""
        match = re.search(r"interface\s+(\w+)", content)
        return match.group(1) if match else None

    def validate_and_diagnose(self, content: str) -> TranspilationResult:
        """Validate Solidity code and generate diagnostics for unsupported features"""
        result = TranspilationResult(code="")

        # Check for unsupported features
        unsupported_patterns = [
            # Loops and if/else are now supported
            (r'\btry\s*\{', "Try-catch blocks are not supported - use require/revert instead"),
            (r'\bcatch\s*\{', "Try-catch blocks are not supported - use require/revert instead"),
            (r'\bassembly\s*\{', "Inline assembly is not supported"),
            # delete and unchecked are now handled — no warnings needed
            (r'\.call\s*\{', "Low-level calls are not supported - use direct contract calls"),
            (r'\.delegatecall\s*\(', "Delegatecall is not supported on MultiversX"),
            (r'\.staticcall\s*\(', "Staticcall is not supported - use view functions"),
            (r'\bselfdestruct\s*\(', "Selfdestruct is not supported on MultiversX"),
            (r'abi\.encodeWithSelector', "abi.encodeWithSelector has no MultiversX equivalent — stub emitted"),
            (r'abi\.decode', "abi.decode requires manual conversion — use codec::top_decode_from_managed_buffer"),
            (r'\blibrary\s+\w+', "Libraries require manual flattening"),
        ]

        for pattern, message in unsupported_patterns:
            if re.search(pattern, content):
                result.add_warning(message)

        # Payable functions are now automatically handled - no warning needed

        # Check for complex inheritance
        parents = self.parse_inheritance(content)
        if len(parents) > 2:
            result.add_warning(f"Complex inheritance detected ({len(parents)} parents) - consider flattening the contract")

        # Check for interface implementations
        if self.parse_interface(content):
            result.add_warning("Interface detected - will be converted to trait", severity="info")

        # Validate contract structure
        if not self.parse_contract_name(content) and not self.parse_interface(content):
            result.add_error("No contract or interface definition found in the source file")

        return result

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

    def parse_modifiers(self, content: str):
        """Parse modifier definitions from Solidity code"""
        modifiers = {}
        # Match modifier definitions: modifier name(params) { body }
        for match in re.finditer(r"modifier\s+(\w+)\s*\(([^)]*)\)\s*\{([^}]*(?:\{[^}]*\}[^}]*)*)\}", content, re.DOTALL):
            name = match.group(1)
            params = match.group(2).strip()
            body = match.group(3).strip()

            # Split on _; to get pre and post statements
            if "_;" in body:
                pre_body, post_body = body.split("_;", 1)
            else:
                pre_body, post_body = body, ""

            pre_statements = self._parse_statements(pre_body.strip())
            post_statements = self._parse_statements(post_body.strip())

            # Extract the require condition from pre_statements for backwards compat
            condition = None
            message = None
            for stmt in pre_statements:
                if stmt.get("type") == "require":
                    condition = stmt["condition"]
                    message = stmt.get("message") or f"{name} check failed"
                    break

            modifiers[name] = {
                "name": name,
                "params": params,
                "body": body,
                "condition": condition,
                "message": message,
                "pre_statements": pre_statements,
                "post_statements": post_statements,
            }
        return modifiers

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
                "applied_modifiers": [],
            })

        # Parse regular functions - use a more robust method to handle nested braces
        # First find function signatures, then extract bodies using brace matching
        for match in re.finditer(r"function\s+(\w+)\s*\((.*?)\)\s*([^\{]*)\{", content, re.DOTALL):
            name = match.group(1)
            params = match.group(2).strip()
            modifiers_str = match.group(3).strip()

            # Use brace matching to extract body with nested braces
            brace_start = match.end() - 1  # Position of the opening brace
            brace_end = self._find_matching_brace(content, brace_start)
            if brace_end == -1:
                body = ""
            else:
                body = content[brace_start + 1:brace_end].strip()

            is_view = " view" in f" {modifiers_str} " or " view " in f" {modifiers_str} "
            is_payable = " payable" in f" {modifiers_str} " or " payable " in f" {modifiers_str} "

            # Extract applied modifiers (custom modifiers like onlyOwner)
            # Remove visibility, returns, payable keywords to find custom modifiers
            applied_modifiers = []
            modifier_text = modifiers_str
            # Remove known keywords
            for keyword in ['public', 'private', 'internal', 'external', 'view', 'pure', 'payable', 'virtual', 'override']:
                modifier_text = re.sub(rf'\b{keyword}\b', '', modifier_text)
            # Remove returns clause
            modifier_text = re.sub(r'returns\s*\([^)]*\)', '', modifier_text)
            # What remains are custom modifiers (possibly with args)
            for mod_match in re.finditer(r'(\w+)(?:\s*\([^)]*\))?', modifier_text):
                mod_name = mod_match.group(1).strip()
                if mod_name and mod_name not in ['', 'returns']:
                    applied_modifiers.append(mod_name)

            returns_match = re.search(r"returns\s*\(([^)]*)\)", modifiers_str)
            return_type = returns_match.group(1).strip() if returns_match else None
            functions.append({
                "name": name,
                "params": params,
                "is_view": is_view,
                "is_payable": is_payable,
                "return_type": return_type,
                "body": body,
                "applied_modifiers": applied_modifiers,
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

    def _parse_param_types(self, param_str: str) -> dict[str, str]:
        types: dict[str, str] = {}
        if not param_str:
            return types
        for raw in param_str.split(","):
            p = raw.strip()
            if not p:
                continue
            parts = p.split()
            if len(parts) < 2:
                continue
            types[parts[1].rstrip(",")] = parts[0]
        return types

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
        non_indexed_count = 0
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
                # Map type and make it a reference for events
                mapped_type = self._map_type(t)
                if not mapped_type.startswith("&"):
                    mapped_type = f"&{mapped_type}"
                
                # MultiversX allows only 1 non-indexed (data) argument
                # If we already have one non-indexed, make this one indexed
                if not is_indexed:
                    if non_indexed_count >= 1:
                        is_indexed = True  # Force to indexed if we already have a non-indexed
                    else:
                        non_indexed_count += 1
                
                idx = "#[indexed] " if is_indexed else ""
                params.append(f"{idx}{n}: {mapped_type}")
        event_fn_name = f"{camel_to_snake(event['name'])}_event"
        params_str = ", ".join(params) if params else ""
        return f"#[event(\"{event['name']}\")]\n    fn {event_fn_name}(&self{', ' if params_str else ''}{params_str});"

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

    def _find_matching_brace(self, text: str, start: int) -> int:
        """Find the position of the matching closing brace"""
        depth = 0
        i = start
        while i < len(text):
            if text[i] == '{':
                depth += 1
            elif text[i] == '}':
                depth -= 1
                if depth == 0:
                    return i
            i += 1
        return -1

    def _extract_call_args(self, args_str: str) -> list[str]:
        """Split comma-separated call arguments respecting nested parentheses."""
        args: list[str] = []
        depth = 0
        buf: list[str] = []
        for ch in args_str:
            if ch == '(':
                depth += 1
                buf.append(ch)
            elif ch == ')':
                depth -= 1
                buf.append(ch)
            elif ch == ',' and depth == 0:
                args.append(''.join(buf).strip())
                buf = []
            else:
                buf.append(ch)
        if buf:
            args.append(''.join(buf).strip())
        return [a for a in args if a]

    def _convert_abi_call(self, expr: str) -> str | None:
        """Detect and convert abi.encode*, abi.decode calls to ManagedBuffer equivalents.
        Returns a Rust snippet string, or None if expr is not an abi call."""
        expr_stripped = expr.strip()
        m = re.match(
            r'^abi\.(encodePacked|encodeWithSelector|encode|decode)\s*\((.+)\)$',
            expr_stripped,
            re.DOTALL,
        )
        if not m:
            return None

        func = m.group(1)
        raw_args = m.group(2)
        args = self._extract_call_args(raw_args)

        if func == "encode":
            lines = ["{\n            let mut __buf = ManagedBuffer::new();"]
            for arg in args:
                converted = self._convert_expression(arg)
                lines.append(f"            codec::top_encode_to_managed_buffer(&{converted}, &mut __buf);")
            lines.append("            __buf\n        }")
            return "\n".join(lines)

        if func == "encodePacked":
            lines = ["{\n            let mut __buf = ManagedBuffer::new();"]
            for arg in args:
                converted = self._convert_expression(arg)
                lines.append(f"            __buf.append(&ManagedBuffer::from(&{converted}.to_bytes_be_buffer()));")
            lines.append("            __buf\n        }")
            return "\n".join(lines)

        if func == "decode":
            return "todo!(/* abi.decode: use codec::top_decode_from_managed_buffer */)"

        if func == "encodeWithSelector":
            return "todo!(/* abi.encodeWithSelector: no MultiversX equivalent */)"

        return None

    def _extract_control_flow(self, body: str) -> tuple[list[dict], str]:
        """Extract if/else and loop statements, returning them and the remaining body"""
        control_statements = []
        remaining = body

        # Process if/else statements
        while True:
            # Match if statement: if (condition) { ... }
            if_match = re.search(r'\bif\s*\(([^)]+)\)\s*\{', remaining)
            if not if_match:
                break

            condition = if_match.group(1).strip()
            block_start = if_match.end() - 1  # Position of opening brace
            block_end = self._find_matching_brace(remaining, block_start)

            if block_end == -1:
                break

            if_body = remaining[block_start + 1:block_end].strip()

            # Check for else clause
            else_match = re.match(r'\s*else\s*\{', remaining[block_end + 1:])
            else_body = None
            final_end = block_end + 1

            if else_match:
                else_start = block_end + 1 + else_match.end() - 1
                else_end = self._find_matching_brace(remaining, else_start)
                if else_end != -1:
                    else_body = remaining[else_start + 1:else_end].strip()
                    final_end = else_end + 1

            control_statements.append({
                "type": "if",
                "condition": condition,
                "if_body": if_body,
                "else_body": else_body
            })

            # Remove the processed if/else from remaining
            remaining = remaining[:if_match.start()] + remaining[final_end:]

        # Process do-while loops: do { ... } while (condition);
        while True:
            do_match = re.search(r'\bdo\s*\{', remaining)
            if not do_match:
                break

            block_start = do_match.end() - 1  # Position of opening brace
            block_end = self._find_matching_brace(remaining, block_start)

            if block_end == -1:
                break

            loop_body = remaining[block_start + 1:block_end].strip()

            # Parse trailing while (condition);
            trailing = remaining[block_end + 1:]
            while_trail = re.match(r'\s*while\s*\(([^)]+)\)\s*;', trailing)
            if not while_trail:
                break

            condition = while_trail.group(1).strip()
            final_end = block_end + 1 + while_trail.end()

            control_statements.append({
                "type": "do_while",
                "condition": condition,
                "body": loop_body
            })

            remaining = remaining[:do_match.start()] + remaining[final_end:]

        # Process unchecked blocks: unchecked { ... }
        while True:
            unc_match = re.search(r'\bunchecked\s*\{', remaining)
            if not unc_match:
                break

            block_start = unc_match.end() - 1
            block_end = self._find_matching_brace(remaining, block_start)

            if block_end == -1:
                break

            inner_body = remaining[block_start + 1:block_end].strip()

            control_statements.append({
                "type": "unchecked",
                "body": inner_body
            })

            remaining = remaining[:unc_match.start()] + remaining[block_end + 1:]

        # Process for loops: for (init; condition; update) { ... }
        while True:
            for_match = re.search(r'\bfor\s*\(([^;]*);([^;]*);([^)]*)\)\s*\{', remaining)
            if not for_match:
                break

            init = for_match.group(1).strip()
            condition = for_match.group(2).strip()
            update = for_match.group(3).strip()
            block_start = for_match.end() - 1
            block_end = self._find_matching_brace(remaining, block_start)

            if block_end == -1:
                break

            loop_body = remaining[block_start + 1:block_end].strip()

            control_statements.append({
                "type": "for",
                "init": init,
                "condition": condition,
                "update": update,
                "body": loop_body
            })

            remaining = remaining[:for_match.start()] + remaining[block_end + 1:]

        # Process while loops: while (condition) { ... }
        while True:
            while_match = re.search(r'\bwhile\s*\(([^)]+)\)\s*\{', remaining)
            if not while_match:
                break

            condition = while_match.group(1).strip()
            block_start = while_match.end() - 1
            block_end = self._find_matching_brace(remaining, block_start)

            if block_end == -1:
                break

            loop_body = remaining[block_start + 1:block_end].strip()

            control_statements.append({
                "type": "while",
                "condition": condition,
                "body": loop_body
            })

            remaining = remaining[:while_match.start()] + remaining[block_end + 1:]

        return control_statements, remaining

    def _parse_statements(self, body: str) -> list[dict]:
        """Parse statements from function body"""
        statements = []

        # Remove comments and normalize whitespace
        body = re.sub(r'//.*', '', body)
        body = re.sub(r'/\*.*?\*/', '', body, flags=re.DOTALL)

        # Extract control flow statements first (if/else, for, while)
        control_statements, remaining_body = self._extract_control_flow(body)
        statements.extend(control_statements)

        # Split remaining by semicolons
        lines = remaining_body.split(';')
        for line in lines:
            line = line.strip()
            if not line:
                continue

            # Handle placeholder tokens left by pre-parse stripping
            if line == self._TODO_TRY_CATCH:
                statements.append({"type": "todo_try_catch"})
                continue
            if line == self._TODO_ASSEMBLY:
                statements.append({"type": "todo_assembly"})
                continue

            # Handle require statements (with or without message)
            # Use paren-depth-aware parsing to handle conditions with nested parens like address(0)
            if re.match(r'require\s*\(', line):
                # Find the opening paren of require(...)
                open_idx = line.index('(')
                depth = 0
                condition_end = -1
                message = None
                i = open_idx
                while i < len(line):
                    c = line[i]
                    if c == '(':
                        depth += 1
                    elif c == ')':
                        depth -= 1
                        if depth == 0:
                            # Closed require(...) without a message comma at depth 1
                            condition_end = i
                            break
                    elif c == ',' and depth == 1:
                        # This comma separates condition from message
                        condition_end = i
                        msg_match = re.search(r'''["\']([^"\']+)["\']''', line[i+1:])
                        if msg_match:
                            message = msg_match.group(1)
                        break
                    i += 1
                if condition_end > open_idx:
                    condition = line[open_idx + 1:condition_end].strip()
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

            # Handle delete statements (must come before declaration patterns)
            if delete_match := re.match(r'delete\s+(.+)', line):
                statements.append({
                    "type": "delete",
                    "target": delete_match.group(1).strip()
                })
                continue

            # Detect struct field assignments before the general assignment handler.
            # Pattern A: mapping[key].field op= value
            if mapping_field_match := re.match(r'(\w+)\[([^\]]+)\]\.(\w+)\s*([+\-*/]?=)\s*(.+)', line):
                statements.append({
                    "type": "struct_field_update",
                    "struct_var": mapping_field_match.group(1),
                    "key": mapping_field_match.group(2).strip(),
                    "field": mapping_field_match.group(3),
                    "op": mapping_field_match.group(4),
                    "value": mapping_field_match.group(5).strip(),
                })
                continue

            # Pattern B: var.field op= value (local var or direct storage struct)
            if struct_field_match := re.match(r'(\w+)\.(\w+)\s*([+\-*/]?=)\s*(.+)', line):
                statements.append({
                    "type": "struct_field_update",
                    "struct_var": struct_field_match.group(1),
                    "key": None,
                    "field": struct_field_match.group(2),
                    "op": struct_field_match.group(3),
                    "value": struct_field_match.group(4).strip(),
                })
                continue


            # Handle contract creation: TypeName varName = new ContractType(args)
            if cc_match := re.match(r'(\w+)\s+(\w+)\s*=\s*new\s+(\w+)\s*\(([^)]*)\)', line):
                statements.append({
                    "type": "contract_creation",
                    "var_name": cc_match.group(2).strip(),
                    "contract_name": cc_match.group(3).strip(),
                    "args": cc_match.group(4).strip(),
                })
                continue

            # Handle variable declarations: type name = expr
            if decl_match := re.match(r'([a-zA-Z_]\w*(?:\[\d*\])?)\s+([a-zA-Z_]\w*)\s*=\s*(.+)', line):
                statements.append({
                    "type": "declaration",
                    "type_name": decl_match.group(1).strip(),
                    "var_name": decl_match.group(2).strip(),
                    "value": decl_match.group(3).strip()
                })
                continue

            # Handle variable declarations without initializer: type name;
            if uninit_match := re.match(r'([a-zA-Z_]\w*(?:\[\d*\])?)\s+([a-zA-Z_]\w*)\s*$', line):
                statements.append({
                    "type": "declaration",
                    "type_name": uninit_match.group(1).strip(),
                    "var_name": uninit_match.group(2).strip(),
                    "value": None
                })
                continue

            # Handle assignments (including mapping[key] = expr and name[k1][k2] = expr)
            if '=' in line:
                if assign_match := re.match(r'(\w+(?:\[[^\]]*\])*(?:\s+\w+)*)\s*=\s*(.+)', line):
                    left = assign_match.group(1).strip()
                    right = assign_match.group(2).strip()
                    statements.append({
                        "type": "assignment",
                        "left": left,
                        "right": right
                    })
                continue

            # Handle array .pop() — removes the last element
            if pop_match := re.match(r'(\w+)\.pop\s*\(\s*\)', line):
                statements.append({
                    "type": "pop",
                    "array_name": pop_match.group(1),
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

        if stmt_type == "todo_try_catch":
            return "        // TODO: try-catch block removed \u2014 implement error handling manually"

        elif stmt_type == "todo_assembly":
            return "        // TODO: inline assembly removed \u2014 no MultiversX equivalent"

        elif stmt_type == "require":
            condition = self._convert_expression(stmt["condition"])
            message = stmt.get("message")
            # MultiversX require! macro always needs a message
            if message:
                return f'        require!({condition}, "{message}");'
            else:
                return f'        require!({condition}, "Requirement not met");'

        elif stmt_type == "emit":
            event_name = stmt["event_name"]
            args = stmt["args"]
            if args:
                # Parse arguments and add & prefix for event calls
                args_list = [arg.strip() for arg in args.split(',')]
                converted_args = []
                for arg in args_list:
                    converted_arg = self._convert_expression(arg)
                    # Check if this parameter might be moved - clone it first
                    # Only clone if it's a simple parameter (not already a function call or expression)
                    params = ['_to', '_from', '_value', 'proposalId', 'goal', 'amount', 'price', 'tokenId']
                    needs_clone = False
                    arg_clean = arg.strip()
                    for param in params:
                        if param == arg_clean or (param in converted_arg and '(' not in converted_arg and not converted_arg.startswith('self.')):
                            needs_clone = True
                            break
                    
                    # Always add & prefix for event arguments (MultiversX requirement)
                    # But skip if already has & or is a literal/number
                    # Also handle binary operations - they should not be wrapped in &
                    if converted_arg.startswith('&') and not converted_arg.startswith('&('):
                        converted_args.append(converted_arg)
                    elif '(' in converted_arg and (' - ' in converted_arg or ' + ' in converted_arg or ' * ' in converted_arg):
                        # Binary operation or expression - wrap in parentheses and add &
                        # Check if it starts with & already (shouldn't, but handle it)
                        if converted_arg.startswith('&'):
                            converted_arg = converted_arg[1:]  # Remove existing &
                        converted_args.append(f'&({converted_arg})')
                    elif converted_arg.replace('.', '').replace('_', '').replace('-', '').replace('(', '').replace(')', '').isdigit():
                        # Number literal - add & prefix
                        converted_args.append(f'&{converted_arg}')
                    elif '(' in converted_arg or converted_arg.startswith('self.'):
                        # Function call or self.method() - add & prefix
                        converted_args.append(f'&{converted_arg}')
                    else:
                        # Variable - add & prefix
                        if needs_clone and not '.clone()' in converted_arg:
                            converted_args.append(f'&{converted_arg}.clone()')
                        else:
                            converted_args.append(f'&{converted_arg}')
                return f'        self.{camel_to_snake(event_name)}_event({", ".join(converted_args)});'
            else:
                return f'        self.{camel_to_snake(event_name)}_event();'

        elif stmt_type == "return":
            expression = stmt["expression"].strip()
            # Check if it's a bool literal
            if expression.lower() == "true":
                return '        return true;'
            elif expression.lower() == "false":
                return '        return false;'
            else:
                converted_expr = self._convert_expression(expression)
                # Preserve explicit return from Solidity for clarity
                return f'        return {converted_expr};'

        elif stmt_type == "assignment":
            left = stmt["left"].strip()
            right_expr = stmt["right"].strip()
            
            # Convert right expression - handle storage variable access
            right = self._convert_expression(right_expr)
            
            # Check if right expression uses a parameter that might be moved
            # If it contains operations with parameters, we need to clone
            # First convert the expression to see what parameters are used
            params_in_expr = []
            params = ['_to', '_from', '_value', 'proposalId', 'goal', 'amount', 'price', 'tokenId']
            for param in params:
                # Check if param is used as a standalone variable (not in function calls)
                if re.search(rf'\b{param}\b', right_expr) and f'{param}.' not in right_expr:
                    params_in_expr.append(param)
            
            # If we have parameters and operations, we need to clone
            if params_in_expr and (' - ' in right_expr or ' + ' in right_expr or ' * ' in right_expr):
                # Clone all parameters in the expression
                for param in params_in_expr:
                    # Replace param with param.clone() but only as standalone, not in expressions
                    right = re.sub(rf'\b{param}\b', f'{param}.clone()', right)

            # Check if this is a mapping assignment: name[key] = expr or name[k1][k2] = expr
            nested_map_match = re.match(r'(\w+)\[(.+?)\]\[(.+?)\]\s*$', left)
            single_map_match = re.match(r'(\w+)\[(.+?)\]\s*$', left)

            if nested_map_match:
                map_name = nested_map_match.group(1)
                key1 = self._convert_expression(nested_map_match.group(2).strip())
                key2 = self._convert_expression(nested_map_match.group(3).strip())
                if map_name in self._mapping_var_names:
                    snake_name = camel_to_snake(map_name)
                    return f'        self.{snake_name}(&{key1}, &{key2}).set({right});'
            elif single_map_match:
                map_name = single_map_match.group(1)
                key = self._convert_expression(single_map_match.group(2).strip())
                if map_name in self._mapping_var_names:
                    snake_name = camel_to_snake(map_name)
                    return f'        self.{snake_name}(&{key}).set({right});'

            # Check if this is a storage variable assignment
            # Extract variable name (handle cases like "balance = balance - _value")
            left_var = left.split()[0] if ' ' in left else left

            if left_var in self._storage_var_names:
                snake_left = camel_to_snake(left_var)
                # Wrap right side in parentheses if it contains operations
                if any(op in right for op in ['+', '-', '*', '/', '(', ')']):
                    return f'        self.{snake_left}().set(&({right}));'
                else:
                    return f'        self.{snake_left}().set(&{right});'
            else:
                return f'        {left} = {right};'

        elif stmt_type == "declaration":
            type_name = stmt["type_name"]
            var_name = stmt["var_name"]
            value = stmt.get("value")
            rust_type = self._map_type(type_name)
            if value is not None:
                rust_value = self._convert_expression(value)
                self._current_var_types[var_name] = type_name
                return f'        let mut {var_name}: {rust_type} = {rust_value};'
            else:
                self._current_var_types[var_name] = type_name
                return f'        let mut {var_name}: {rust_type} = Default::default();'

        elif stmt_type == "push":
            array_name = stmt["array_name"]
            struct_data = self._convert_struct_initialization(stmt["struct_data"])
            snake = camel_to_snake(array_name)
            return f'        self.{snake}().push(&{struct_data});'

        elif stmt_type == "pop":
            array_name = stmt["array_name"]
            snake = camel_to_snake(array_name)
            return (
                f'        let last_idx = self.{snake}().len() - 1;\n'
                f'        self.{snake}().remove(last_idx);'
            )

        elif stmt_type == "struct_field_update":
            struct_var = stmt["struct_var"]
            key = stmt.get("key")
            field = stmt["field"]
            op = stmt["op"]
            value = self._convert_expression(stmt["value"])
            snake_field = camel_to_snake(field)
            snake_var = camel_to_snake(struct_var)

            if key is not None:
                # mapping[key].field op= value → load-mutate-store
                converted_key = self._convert_expression(key)
                load = f'        let mut s = self.{snake_var}(&{converted_key}).get();'
                if op == '=':
                    mutate = f'        s.{snake_field} = {value};'
                else:
                    op_char = op[0]
                    mutate = f'        s.{snake_field} = s.{snake_field} {op_char} {value};'
                store = f'        self.{snake_var}(&{converted_key}).set(&s);'
                return f'{load}\n{mutate}\n{store}'
            elif struct_var in getattr(self, '_storage_var_names', set()):
                # Direct storage struct var → load-mutate-store without key
                load = f'        let mut s = self.{snake_var}().get();'
                if op == '=':
                    mutate = f'        s.{snake_field} = {value};'
                else:
                    op_char = op[0]
                    mutate = f'        s.{snake_field} = s.{snake_field} {op_char} {value};'
                store = f'        self.{snake_var}().set(&s);'
                return f'{load}\n{mutate}\n{store}'
            else:
                # Local var → direct mutation
                if op == '=':
                    return f'        {struct_var}.{snake_field} = {value};'
                else:
                    return f'        {struct_var}.{snake_field} {op} {value};'

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

        elif stmt_type == "if":
            condition = self._convert_expression(stmt["condition"])
            if_body = stmt["if_body"]
            else_body = stmt.get("else_body")

            # Recursively parse and convert the if body
            if_statements = self._parse_statements(if_body)
            if_lines = []
            for if_stmt in if_statements:
                converted = self._convert_statement(if_stmt, "")
                if converted:
                    if_lines.append(converted)

            if_code = '\n'.join(if_lines) if if_lines else '            // empty block'

            if else_body:
                # Recursively parse and convert the else body
                else_statements = self._parse_statements(else_body)
                else_lines = []
                for else_stmt in else_statements:
                    converted = self._convert_statement(else_stmt, "")
                    if converted:
                        else_lines.append(converted)

                else_code = '\n'.join(else_lines) if else_lines else '            // empty block'
                return f'        if {condition} {{\n{if_code}\n        }} else {{\n{else_code}\n        }}'
            else:
                return f'        if {condition} {{\n{if_code}\n        }}'

        elif stmt_type == "for":
            # Convert Solidity for loop to Rust
            # for (uint i = 0; i < n; i++) becomes: for i in 0..n
            init = stmt["init"]
            condition = stmt["condition"]
            update = stmt["update"]
            loop_body = stmt["body"]

            # Try to detect simple counter patterns: uint i = 0; i < n; i++
            init_match = re.match(r'(?:uint\d*|int\d*)\s+(\w+)\s*=\s*(\d+)', init)
            cond_match = re.match(r'(\w+)\s*<\s*(.+)', condition)
            update_match = re.match(r'(\w+)\s*\+\+', update)

            if init_match and cond_match and update_match:
                var_name = init_match.group(1)
                start_val = init_match.group(2)
                end_expr = self._convert_expression(cond_match.group(2))

                # Parse body
                body_statements = self._parse_statements(loop_body)
                body_lines = []
                for body_stmt in body_statements:
                    converted = self._convert_statement(body_stmt, "")
                    if converted:
                        body_lines.append(converted)

                body_code = '\n'.join(body_lines) if body_lines else '            // empty block'
                return f'        for {var_name} in {start_val}..{end_expr} {{\n{body_code}\n        }}'
            else:
                # General while-style loop fallback
                converted_condition = self._convert_expression(condition)
                converted_init = self._convert_expression(init) if init else ""
                converted_update = self._convert_expression(update) if update else ""

                body_statements = self._parse_statements(loop_body)
                body_lines = []
                for body_stmt in body_statements:
                    converted = self._convert_statement(body_stmt, "")
                    if converted:
                        body_lines.append(converted)

                body_code = '\n'.join(body_lines) if body_lines else '            // empty block'
                # Add update at end of loop body
                if converted_update:
                    body_code += f'\n            {converted_update};'

                init_line = f'        let mut {converted_init};\n' if converted_init else ''
                return f'{init_line}        while {converted_condition} {{\n{body_code}\n        }}'

        elif stmt_type == "while":
            condition = self._convert_expression(stmt["condition"])
            loop_body = stmt["body"]

            body_statements = self._parse_statements(loop_body)
            body_lines = []
            for body_stmt in body_statements:
                converted = self._convert_statement(body_stmt, "")
                if converted:
                    body_lines.append(converted)

            body_code = '\n'.join(body_lines) if body_lines else '            // empty block'
            return f'        while {condition} {{\n{body_code}\n        }}'

        elif stmt_type == "delete":
            target = stmt["target"]
            # Nested mapping: name[key1][key2]
            nested = re.match(r'(\w+)\[([^\]]+)\]\[([^\]]+)\]', target)
            if nested:
                var_name = camel_to_snake(nested.group(1))
                key1 = nested.group(2).strip()
                key2 = nested.group(3).strip()
                return f'        self.{var_name}(&{key1}, &{key2}).clear();'
            # Single mapping: name[key]
            single = re.match(r'(\w+)\[([^\]]+)\]', target)
            if single:
                var_name = camel_to_snake(single.group(1))
                key = single.group(2).strip()
                return f'        self.{var_name}(&{key}).clear();'
            # Simple variable
            var_name = camel_to_snake(target)
            return f'        self.{var_name}().clear();'

        elif stmt_type == "do_while":
            condition = self._convert_expression(stmt["condition"])
            loop_body = stmt["body"]

            body_statements = self._parse_statements(loop_body)
            body_lines = []
            for body_stmt in body_statements:
                converted = self._convert_statement(body_stmt, "")
                if converted:
                    body_lines.append(converted)

            body_code = '\n'.join(body_lines) if body_lines else '            // empty block'
            return f'        loop {{\n{body_code}\n            if !({condition}) {{ break; }}\n        }}'

        elif stmt_type == "unchecked":
            inner_body = stmt["body"]

            inner_statements = self._parse_statements(inner_body)
            inner_lines = []
            for inner_stmt in inner_statements:
                converted = self._convert_statement(inner_stmt, "")
                if converted:
                    inner_lines.append(converted)

            inner_code = '\n'.join(inner_lines)
            return f'        // NOTE: unchecked arithmetic — overflow behavior differs on MultiversX\n{inner_code}'

        elif stmt_type == "contract_creation":
            deploy_name = stmt["contract_name"]
            var_name = stmt["var_name"]
            args = stmt["args"].strip()
            self._warnings.append(TranspilationWarning(
                "Contract creation with new ContractType() requires manual deployment setup — see MultiversX ContractDeploy docs"
            ))
            stub_lines = [f'        // TODO: deploy {deploy_name} — use ContractDeploy via self.send().contract_call(...)']
            if args:
                stub_lines.append(f'        // Args: {args}')
            stub_lines.append(f'        let {var_name}: ManagedAddress<Self::Api> = ManagedAddress::zero();')
            return '\n'.join(stub_lines)

        return f'        // TODO: unhandled statement: {stmt}'

    def _split_args(self, args_str: str) -> list[str]:
        """Split comma-separated call arguments while respecting nested parentheses."""
        args: list[str] = []
        depth = 0
        current: list[str] = []
        for ch in args_str:
            if ch in '([{':
                depth += 1
                current.append(ch)
            elif ch in ')]}':
                depth -= 1
                current.append(ch)
            elif ch == ',' and depth == 0:
                s = ''.join(current).strip()
                if s:
                    args.append(s)
                current = []
            else:
                current.append(ch)
        s = ''.join(current).strip()
        if s:
            args.append(s)
        return args

    def _apply_using_for_transforms(self, expr: str) -> str:
        """Inline known library calls (SafeMath, Math, etc.) to plain Rust expressions.

        Handles two forms:
        - Static:      SafeMath.add(a, b)  -> a + b
        - Method-call: a.add(b) when 'using SafeMath for <type>' is active -> a + b
        """
        known_libs = {k[0] for k in LIBRARY_FUNCTION_MAP}
        known_methods = {k[1] for k in LIBRARY_FUNCTION_MAP}
        active_libraries = set(self._using_for.values())

        pattern = re.compile(r'\b(\w+)\.(\w+)\s*\(')
        parts: list[str] = []
        pos = 0

        while pos < len(expr):
            m = pattern.search(expr, pos)
            if not m:
                parts.append(expr[pos:])
                break

            first = m.group(1)
            method_name = m.group(2)
            args_start = m.end()

            # Find matching closing parenthesis
            depth = 1
            i = args_start
            while i < len(expr) and depth > 0:
                if expr[i] == '(':
                    depth += 1
                elif expr[i] == ')':
                    depth -= 1
                i += 1
            args_str = expr[args_start:i - 1]

            transformed: str | None = None

            if first in known_libs:
                # Static library call: SafeMath.add(a, b)
                key = (first, method_name)
                if key in LIBRARY_FUNCTION_MAP:
                    _, fn = LIBRARY_FUNCTION_MAP[key]
                    transformed = fn(self._split_args(args_str))
            elif method_name in known_methods:
                # Method-call via using-for: a.add(b)
                for lib_name in active_libraries:
                    key = (lib_name, method_name)
                    if key in LIBRARY_FUNCTION_MAP:
                        _, fn = LIBRARY_FUNCTION_MAP[key]
                        transformed = fn([first] + self._split_args(args_str))
                        break

            if transformed is not None:
                parts.append(expr[pos:m.start()])
                parts.append(transformed)
                pos = i
            else:
                parts.append(expr[pos:m.end()])
                pos = m.end()

        return ''.join(parts)

    def _find_cast(self, expr: str):
        """Detect a Solidity type cast of the form typename(...).

        Uses a paren-depth counter instead of [^()]+ so that nested casts
        like uint256(uint128(x)) are handled rather than silently skipped.

        Returns (type_name, inner_expr) when the *entire* expr is a single
        type cast, or None otherwise.
        """
        m = re.match(
            r'^(uint(?:256|128|64|32|16|8)|int(?:256|128|64|32|16|8)|address|bytes(?:32|20)?|bool)\s*\(',
            expr,
        )
        if not m:
            return None
        depth = 1
        i = m.end()
        while i < len(expr) and depth > 0:
            if expr[i] == '(':
                depth += 1
            elif expr[i] == ')':
                depth -= 1
            i += 1
        # The cast must cover the entire expression with no trailing content.
        if depth != 0 or i != len(expr):
            return None
        return m.group(1), expr[m.end():i - 1]

    def _lookup_var_type(self, name: str) -> str | None:
        return self._current_var_types.get(name) or self._storage_var_types.get(name)

    def _convert_bytes_cast(self, type_name: str, inner_raw: str, converted_inner: str) -> str:
        """Convert bytes/bytesN casts to ManagedBuffer when the input shape is knowable."""
        if (len(inner_raw) >= 2
                and inner_raw[0] == inner_raw[-1]
                and inner_raw[0] in {'"', "'"}):
            return f'ManagedBuffer::from(b"{inner_raw[1:-1]}")'

        if re.match(r'^0x[0-9a-fA-F]+$', inner_raw):
            hex_value = inner_raw[2:]
            if len(hex_value) % 2:
                hex_value = f'0{hex_value}'
            bytes_literal = ', '.join(
                f'0x{hex_value[i:i + 2].lower()}'
                for i in range(0, len(hex_value), 2)
            )
            return f'ManagedBuffer::from(&[{bytes_literal}])'

        inner_type = self._lookup_var_type(inner_raw) if re.match(r'^[A-Za-z_]\w*$', inner_raw) else None
        if inner_type in {'bytes', 'string', 'ManagedBuffer'}:
            return converted_inner

        is_numeric_literal = bool(re.match(r'^\d+$', inner_raw))
        is_uint_typed = bool(inner_type and inner_type.startswith('uint'))
        if is_numeric_literal or is_uint_typed:
            self._warnings.append(TranspilationWarning(
                f"{type_name}(uint) cast requires manual conversion — use .to_bytes_be() or similar"
            ))
            return f'ManagedBuffer::new() /* TODO: {type_name}({inner_raw}) — convert integer bytes manually */'

        self._warnings.append(TranspilationWarning(
            f"{type_name}({inner_raw}) cast input type unknown — verify input type manually"
        ))
        return f'ManagedBuffer::new() /* TODO: {type_name}({inner_raw}) — verify input type */'

    def _parse_ternary(self, expr: str):
        """Find ternary operator at depth 0. Returns (condition, then_expr, else_expr) or None."""
        depth = 0
        q_pos = None
        for i, c in enumerate(expr):
            if c in '([':
                depth += 1
            elif c in ')]':
                depth -= 1
            elif c == '?' and depth == 0:
                q_pos = i
                break

        if q_pos is None:
            return None

        depth = 0
        for i in range(q_pos + 1, len(expr)):
            c = expr[i]
            if c in '([':
                depth += 1
            elif c in ')]':
                depth -= 1
            elif c == ':' and depth == 0:
                return expr[:q_pos].strip(), expr[q_pos + 1:i].strip(), expr[i + 1:].strip()

        return None

    def _convert_expression(self, expr: str) -> str:
        """Convert Solidity expressions to MultiversX equivalents"""
        # Inline known library calls before any other transformation
        expr = self._apply_using_for_transforms(expr)

        # Early dispatch for abi calls before any other transformation
        abi_result = self._convert_abi_call(expr)
        if abi_result is not None:
            return abi_result

        # Handle ternary operator (condition ? then_expr : else_expr)
        ternary = self._parse_ternary(expr.strip())
        if ternary is not None:
            cond, then_expr, else_expr = ternary
            return f'if {self._convert_expression(cond)} {{ {self._convert_expression(then_expr)} }} else {{ {self._convert_expression(else_expr)} }}'

        # Handle keccak256(data) → self.crypto().keccak256(&data_as_managed_buffer)
        keccak_match = re.match(r'^keccak256\((.+)\)$', expr.strip(), re.DOTALL)
        if keccak_match:
            inner = self._convert_expression(keccak_match.group(1).strip())
            self._warnings.append(TranspilationWarning(
                "keccak256 mapped to self.crypto().keccak256() — ensure input is converted to ManagedBuffer"
            ))
            return f'self.crypto().keccak256(&{inner})'

        # Handle sha256(data) → self.crypto().sha256(&data_as_managed_buffer)
        sha256_match = re.match(r'^sha256\((.+)\)$', expr.strip(), re.DOTALL)
        if sha256_match:
            inner = self._convert_expression(sha256_match.group(1).strip())
            self._warnings.append(TranspilationWarning(
                "sha256 mapped to self.crypto().sha256() — ensure input is converted to ManagedBuffer"
            ))
            return f'self.crypto().sha256(&{inner})'

        # Handle ecrecover(hash, v, r, s) — no MultiversX equivalent
        ecrecover_match = re.match(r'^ecrecover\((.+)\)$', expr.strip(), re.DOTALL)
        if ecrecover_match:
            self._warnings.append(TranspilationWarning(
                "ecrecover has no MultiversX equivalent — manual implementation required"
            ))
            return 'ManagedAddress::zero() /* TODO: ecrecover — no direct MultiversX equivalent, use off-chain verification */'

        # Handle bare new ContractType(args) used as an expression (without assignment)
        if re.match(r'new\s+\w+\s*\([^)]*\)', expr.strip()):
            self._warnings.append(TranspilationWarning(
                "Contract creation with new ContractType() requires manual deployment setup — see MultiversX ContractDeploy docs"
            ))
            return 'ManagedAddress::<Self::Api>::zero()'

        # Handle int256(x) type casts
        int256_cast = re.match(r'^int256\((.+)\)$', expr.strip())
        if int256_cast:
            inner = int256_cast.group(1).strip()
            # Negative literal: int256(-5) -> BigInt::from(-5i64) + warning
            neg_lit = re.match(r'^-(\d+)$', inner)
            if neg_lit:
                self._warnings.append(TranspilationWarning(
                    "Negative BigInt value — MultiversX BigInt has limited negative number support; verify arithmetic behavior matches Solidity int256"
                ))
                return f'BigInt::from(-{neg_lit.group(1)}i64)'
            # Positive literal: int256(42) -> BigInt::from(42i64)
            pos_lit = re.match(r'^(\d+)$', inner)
            if pos_lit:
                return f'BigInt::from({pos_lit.group(1)}i64)'
            # Variable or expression: int256(someVar) -> BigInt::from(someVar)
            self._warnings.append(TranspilationWarning(
                "int256 cast — ensure variable is compatible with MultiversX BigInt; negative values may behave differently than Solidity int256"
            ))
            return f'BigInt::from({inner})'

        # Handle bool(x) type casts
        bool_cast = re.match(r'^bool\((.+)\)$', expr.strip())
        if bool_cast:
            inner = bool_cast.group(1).strip()
            # Literal 0 → false
            if re.match(r'^0+$', inner):
                return 'false'
            # Positive literal → true
            if re.match(r'^\d+$', inner):
                return 'true'
            # Variable: bool(someVar) → someVar != 0
            return f'{inner} != 0'

        # Handle msg.sender
        expr = expr.replace("msg.sender", "self.blockchain().get_caller()")

        # Handle msg.value
        expr = expr.replace("msg.value", "self.call_value().egld_value()")

        # Handle msg.data (not directly mappable — emit TODO stub with warning)
        if "msg.data" in expr:
            self._warnings.append(TranspilationWarning(
                "msg.data has no direct MultiversX equivalent — manual conversion to ManagedBuffer required"
            ))
            expr = expr.replace("msg.data", "{ /* TODO: msg.data → ManagedBuffer — manual conversion required */ ManagedBuffer::new() }")

        # Handle msg.sig (function selector — not applicable in MultiversX)
        if "msg.sig" in expr:
            self._warnings.append(TranspilationWarning(
                "msg.sig (function selector) has no MultiversX equivalent — remove or redesign this logic"
            ))
            expr = expr.replace("msg.sig", "{ /* TODO: msg.sig has no MultiversX equivalent */ ManagedBuffer::new() }")

        # Handle block.timestamp / now (Solidity alias)
        expr = expr.replace("block.timestamp", "self.blockchain().get_block_timestamp()")
        expr = expr.replace("now", "self.blockchain().get_block_timestamp()")

        # Handle block.number
        expr = expr.replace("block.number", "self.blockchain().get_block_nonce()")

        # Handle address(this)
        expr = expr.replace("address(this)", "self.blockchain().get_sc_address()")

        # Handle tx.origin
        if "tx.origin" in expr:
            self._warnings.append(TranspilationWarning(
                "tx.origin mapped to get_caller() — note: on MultiversX these are always the same, unlike EVM"
            ))
            expr = expr.replace("tx.origin", "self.blockchain().get_caller()")

        # Handle type(...).max / type(...).min
        def replace_type_minmax(m: re.Match) -> str:
            type_name = m.group(1)
            bound = m.group(2)  # 'max' or 'min'
            if type_name == 'uint256':
                if bound == 'max':
                    # TODO: true uint256 max is 2^256-1; u64::MAX is a conservative stand-in
                    return '/* TODO: type(uint256).max — true max is 2^256-1 */ BigUint::from(u64::MAX)'
                else:  # min
                    return 'BigUint::zero()'
            if type_name == 'int256':
                if bound == 'max':
                    return '/* TODO: type(int256).max — true max is 2^255-1 */ BigInt::from(i64::MAX)'
                else:
                    return '/* TODO: type(int256).min — true min is -(2^255) */ BigInt::from(i64::MIN)'
            # Generic fallback
            return m.group(0)

        expr = re.sub(r'\btype\(\s*(u?int\d*)\s*\)\s*\.\s*(max|min)\b', replace_type_minmax, expr)


        # Handle simple arithmetic and comparisons (basic cases)
        # This would need to be much more sophisticated for complex expressions

        # Handle array/storage .length → .len() called directly on the VecMapper.
        # Replace VARNAME.length with self.var_name().len() for known array vars,
        # or VARNAME.len() for everything else (generic fallback).
        def replace_length(m: re.Match) -> str:
            var = m.group(1)
            if var in self._array_var_names:
                return f'self.{camel_to_snake(var)}().len()'
            if var in self._storage_var_names:
                # SingleValueMapper — .len() is likely wrong, but preserve prior behaviour
                return f'self.{camel_to_snake(var)}().get().len()'
            return f'{var}.len()'
        expr = re.sub(r'\b(\w+)\.length\b', replace_length, expr)

        # Handle power operator (limited)
        expr = expr.replace("**", ".pow")

        # Handle type casts: uint256(x), uint128(x), address(bytes20(x)), etc.
        # _find_cast uses paren-depth counting so nested casts like
        # uint256(uint128(x)) are processed correctly instead of being skipped
        # by the [^()]+ regex that origin used.
        cast_result = self._find_cast(expr.strip())
        if cast_result is not None:
            type_name, inner_expr = cast_result
            inner_raw = inner_expr.strip()
            converted_inner = self._convert_expression(inner_raw)
            if type_name == 'uint256':
                if inner_raw == '0':
                    return 'BigUint::zero()'
                if re.match(r'^-\d+$', inner_raw):
                    self._warnings.append(TranspilationWarning(
                        f"Type cast {type_name}({inner_raw}): casting negative value to unsigned — emitting BigUint::zero() with TODO"
                    ))
                    return f'/* TODO: {type_name}({inner_raw}) - negative cast to unsigned */ BigUint::zero()'
                return f'BigUint::from({converted_inner})'
            _uint_primitive = {'uint128': 'u128', 'uint64': 'u64', 'uint32': 'u32', 'uint16': 'u16', 'uint8': 'u8'}
            if type_name in _uint_primitive:
                return f'{converted_inner} as {_uint_primitive[type_name]}'
            if type_name == 'int256':
                return f'BigInt::from({converted_inner})'
            _int_primitive = {'int128': 'i128', 'int64': 'i64', 'int32': 'i32', 'int16': 'i16', 'int8': 'i8'}
            if type_name in _int_primitive:
                return f'{converted_inner} as {_int_primitive[type_name]}'
            if type_name == 'address':
                if inner_raw == '0':
                    return 'ManagedAddress::zero()'
                return f'ManagedAddress::from(&{converted_inner})'
            if type_name == 'bool':
                return f'({converted_inner}) as bool'
            if type_name in {'bytes', 'bytes32'}:
                return self._convert_bytes_cast(type_name, inner_raw, converted_inner)
            if type_name.startswith('bytes'):
                return converted_inner  # transparent cast (bytes20)

        # Handle address(0) as a sub-expression (e.g. x != address(0))
        expr = re.sub(r'\baddress\(0\)', 'ManagedAddress::zero()', expr)

        # Handle 1 minutes -> 60 seconds conversion
        expr = re.sub(r'(\d+)\s*minutes', lambda m: str(int(m.group(1)) * 60), expr)

        # Handle BigUint literal conversion for large numbers
        # Replace large numbers (not in function calls) with BigUint::from
        def replace_number(match):
            num_str = match.group(1)
            try:
                num = int(num_str)
                if num == 0:
                    return 'BigUint::zero()'
                # u64::MAX is 18446744073709551615
                # Very large numbers (> u64::MAX) should use power operations
                # For numbers like 1000000000000000000000000 (10^24), use power
                if num > 18446744073709551615:  # u64::MAX
                    # Try to express as power of 10
                    num_str_check = str(num)
                    if num_str_check.startswith('1') and all(c == '0' for c in num_str_check[1:]):
                        # Number is 1 followed by zeros (power of 10)
                        power = len(num_str_check) - 1
                        if power <= 256:  # Reasonable power limit
                            return f'BigUint::from(10u32).pow({power})'
                    # For other very large numbers, use multiplication
                    # Calculate as multiple of smaller numbers
                    # Or use hex bytes manually
                    # For now, use a workaround: express as multiple operations
                    # Actually, let's use from_bytes_be with manual byte array
                    # Convert to hex string and parse bytes
                    hex_str = hex(num)[2:]  # Remove '0x'
                    if len(hex_str) % 2 == 1:
                        hex_str = '0' + hex_str
                    # Create byte array manually: hex string to bytes
                    # For example: "d3c21bcecceda1000000" -> [0xd3, 0xc2, ...]
                    byte_array = ', '.join([f'0x{hex_str[i:i+2]}' for i in range(0, len(hex_str), 2)])
                    return f'BigUint::from_bytes_be(&[{byte_array}])'
                elif num > 4294967295:  # u32::MAX
                    return f'BigUint::from({num_str}u64)'
                else:
                    return f'BigUint::from({num_str}u32)'
            except (ValueError, OverflowError):
                # If number is too large to parse, use power of 10 if possible
                num_str_check = str(num)
                if num_str_check.startswith('1') and all(c == '0' for c in num_str_check[1:]):
                    power = len(num_str_check) - 1
                    return f'BigUint::from(10u32).pow({power})'
                return f'BigUint::from(0u32)'  # Fallback
        
        # Replace standalone numbers (avoid numbers already in function calls)
        expr = re.sub(r'(?<!::from\()\b(\d+)\b(?!u32|u64|u16|u8|i32|i64|i16|i8)', replace_number, expr)

        # Handle VecMapper array indexing BEFORE variable substitution so the variable
        # name is still in its original camelCase form.  someArray[i] → self.some_array().get(i + 1)
        # (VecMapper is 1-indexed in MultiversX).
        if self._array_var_names:
            def replace_array_index(m: re.Match) -> str:
                var = m.group(1)
                if var in self._array_var_names:
                    raw_idx = m.group(2).strip()
                    converted_idx = self._convert_expression(raw_idx)
                    return f'self.{camel_to_snake(var)}().get({converted_idx} + 1)'
                return m.group(0)
            expr = re.sub(r'\b(\w+)\[([^\]]+)\]', replace_array_index, expr)

        # Handle variable access - convert simple variable names to storage getters
        # This is a simple heuristic - in a full implementation we'd need proper symbol resolution
        # Only exclude language keywords and boolean literals here.
        # Do NOT add variable names (owner, spender, price, etc.) to this list —
        # if a name is a real storage variable it appears in self._storage_var_names and
        # must be converted to .get().  Function parameters that happen to share a name
        # with a storage variable are handled correctly because they are NOT present in
        # _storage_var_names, so the elif branch below simply won't fire for them.
        exclude_patterns = ['true', 'false', 'self']

        def convert_var(match):
            var = match.group(1)
            if var in exclude_patterns:
                return var
            elif var in self._storage_var_names:
                return f'self.{camel_to_snake(var)}().get()'
            elif var in self._mapping_var_names:
                return f'self.{camel_to_snake(var)}()'
            elif var in self._array_var_names:
                # Standalone array reference (e.g. passed to a function) — return the VecMapper
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

        # Post-pass: append .get() to storage mapper calls not already chained with a method.
        # Scoped to known storage/mapping names so non-storage calls like self.blockchain()
        # or self.send() are never affected.
        storage_names = self._storage_var_names | set(self._mapping_var_names.keys())
        if storage_names:
            snake_names = {camel_to_snake(n) for n in storage_names}
            # Sort longest-first to prevent partial-name matches (e.g. "foo" matching inside "foobar")
            name_pat = '|'.join(re.escape(n) for n in sorted(snake_names, key=len, reverse=True))
            expr = re.sub(
                r'\b(self\.(?:' + name_pat + r')\([^)]*\))(?!\s*\.)',
                r'\1.get()',
                expr,
            )
        else:
            # Fallback when storage names are not yet populated.
            # WARNING: this heuristic may incorrectly append .get() to non-storage
            # self.x() calls (e.g. self.blockchain() standing alone).
            expr = re.sub(r'(self\.\w+\([^)]*\))(?!\s*\.)', r'\1.get()', expr)

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

    def convert_function(self, func: dict, contract_name: str = "Contract", modifiers: dict = None) -> str:
        snake_name = camel_to_snake(func["name"]) if func["name"] else "init"

        # Build annotation based on function type
        if func["is_view"]:
            annotation = f"#[view({func['name']})]\n    "
        elif func["name"]:
            # Check if payable
            if func.get("is_payable"):
                annotation = "#[payable(\"EGLD\")]\n    #[endpoint]\n    "
            else:
                annotation = "#[endpoint]\n    "
        else:
            annotation = "#[init]\n    "

        params = self._format_params(func["params"])
        return_type = self._format_return(func.get("return_type"))
        previous_var_types = self._current_var_types
        self._current_var_types = self._parse_param_types(func["params"])

        # Parse and convert body statements
        body_lines = []

        # Collect post-modifier statements to emit after the function body
        post_modifier_lines = []

        # Add modifier checks at the start of the function
        if modifiers and func.get("applied_modifiers"):
            for mod_name in func["applied_modifiers"]:
                if mod_name in modifiers:
                    mod = modifiers[mod_name]
                    if mod.get("pre_statements"):
                        for stmt in mod["pre_statements"]:
                            converted = self._convert_statement(stmt, "")
                            if converted:
                                body_lines.append(converted)
                    elif mod.get("condition"):
                        # Fallback for modifiers parsed without pre_statements
                        converted_condition = self._convert_expression(mod["condition"])
                        message = mod.get("message", f"{mod_name} check failed")
                        body_lines.append(f'        require!({converted_condition}, "{message}");')
                    if mod.get("post_statements"):
                        for stmt in mod["post_statements"]:
                            converted = self._convert_statement(stmt, "")
                            if converted:
                                post_modifier_lines.append(converted)

        if func.get("body"):
            statements = self._parse_statements(func["body"])
            for stmt in statements:
                converted = self._convert_statement(stmt, "")
                if converted:
                    body_lines.append(converted)

        body_lines.extend(post_modifier_lines)

        if body_lines:
            body = '\n'.join(body_lines)
            converted_function = f"{annotation}fn {snake_name}(&self{', ' if params else ''}{', '.join(params)}){return_type} {{\n{body}\n    }}"
        else:
            converted_function = f"{annotation}fn {snake_name}(&self{', ' if params else ''}{', '.join(params)}){return_type} {{\n        // TODO: implement body\n    }}"

        self._current_var_types = previous_var_types
        return converted_function

    def _extract_storage(self, content: str) -> list[tuple[str, str, str]]:
        """Extract storage variables, including mappings (single and nested)"""
        vars: list[tuple[str, str, str]] = []

        # Strip struct/function/modifier bodies so their fields are not captured as storage vars
        content_no_bodies = re.sub(r'\bstruct\s+\w+\s*\{[^}]*\}', '', content, flags=re.DOTALL)

        # Array variables (uint256[], address[], etc.) → VecMapper
        for match in re.finditer(
            r"(uint256|uint128|uint64|uint32|uint16|uint8|int256|int128|int64|int32|int16|int8|string|address|bool)\s*\[\s*\]"
            r"(?:\s+(?:public|private|internal|external))?\s+(\w+)\s*;",
            content_no_bodies,
        ):
            vars.append(("array", match.group(2), match.group(1)))

        # Simple variables (uint256, address, etc.)
        for match in re.finditer(r"(uint256|uint128|uint64|uint32|uint16|uint8|int256|int128|int64|int32|int16|int8|string|bytes|bytes32|bytes20|address|bool|u8)(?:\s+(?:public|private|internal|external))?\s+(\w+)\s*;", content_no_bodies):
            # Skip names already captured as arrays
            if not any(v[1] == match.group(2) for v in vars):
                vars.append((match.group(1), match.group(2), ""))

        # Nested mappings: mapping(type1 => mapping(type2 => type3))
        for match in re.finditer(r"mapping\s*\(\s*(\w+)\s*=>\s*mapping\s*\(\s*(\w+)\s*=>\s*(\w+)\s*\)\s*\)\s*(?:public|private|internal|external)?\s*(\w+)\s*;", content):
            key1_type = match.group(1).strip()
            key2_type = match.group(2).strip()
            value_type = match.group(3).strip()
            var_name = match.group(4)
            vars.append(("nested_mapping", var_name, f"{key1_type}=>{key2_type}=>{value_type}"))

        # Simple mappings: mapping(type1 => type2)
        # Make sure not to match nested mappings again
        for match in re.finditer(r"mapping\s*\(\s*(\w+)\s*=>\s*(\w+)\s*\)\s*(?:public|private|internal|external)?\s*(\w+)\s*;", content):
            key_type = match.group(1).strip()
            value_type = match.group(2).strip()
            var_name = match.group(3)
            # Check if this variable was already captured as a nested mapping
            if not any(v[1] == var_name for v in vars):
                vars.append(("mapping", var_name, f"{key_type}=>{value_type}"))

        return vars

    def _convert_storage_mapper(self, var_type: str, var_name: str, mapping_info: str = "") -> str:
        """Convert storage variable to appropriate mapper type"""
        if var_type == "array":
            elem_type = self._map_type(mapping_info) if mapping_info else "BigUint<Self::Api>"
            return f"VecMapper<{elem_type}>"
        if var_type == "nested_mapping":
            # Parse key1=>key2=>value nested mapping
            parts = mapping_info.split("=>")
            if len(parts) == 3:
                key1_type = parts[0].strip()
                key2_type = parts[1].strip()
                value_type = parts[2].strip()

                # Map types
                key1_mapped = self._map_type(key1_type)
                key2_mapped = self._map_type(key2_type)
                value_mapped = self._map_type(value_type)

                # Use SingleValueMapper for the inner value with two keys
                return f"SingleValueMapper<{value_mapped}>"
        elif var_type == "mapping":
            # Parse key=>value mapping
            key_val = mapping_info.split("=>")
            if len(key_val) == 2:
                key_type = key_val[0].strip()
                value_type = key_val[1].strip()

                # Map types
                key_mapped = self._map_type(key_type)
                value_mapped = self._map_type(value_type)

                return f"SingleValueMapper<{value_mapped}>"

        return f"SingleValueMapper<{self._map_type(var_type)}>"

    _TODO_TRY_CATCH = "__xtract_todo_try_catch__"
    _TODO_ASSEMBLY = "__xtract_todo_assembly__"

    def _strip_brace_block(self, content: str, brace_open: int) -> int:
        """Return the index one past the closing '}' that matches *brace_open*.

        Returns -1 if no match is found.
        """
        depth = 0
        pos = brace_open
        while pos < len(content):
            if content[pos] == '{':
                depth += 1
            elif content[pos] == '}':
                depth -= 1
                if depth == 0:
                    return pos + 1
            pos += 1
        return -1

    def _strip_try_catch_blocks(self, content: str) -> str:
        """Remove try { ... } catch ... { ... } constructs (brace-depth-aware).

        Solidity's try has the form:
            try <expression> [returns (...)] { ... } catch [(...)] { ... }
        We scan from the 'try' keyword to the first '{', match braces, then
        consume any number of following catch clauses, and replace the whole
        span with a placeholder token that survives _parse_statements.
        """
        result = content
        while True:
            m = re.search(r'\btry\b', result)
            if not m:
                break
            start = m.start()
            # Scan forward to the first '{' (opening brace of the try body)
            pos = m.end()
            while pos < len(result) and result[pos] != '{':
                pos += 1
            if pos >= len(result):
                break
            end = self._strip_brace_block(result, pos)
            if end == -1:
                break
            # Consume any trailing catch [...] { ... } blocks
            while True:
                tail = result[end:]
                catch_m = re.match(r'\s*catch\b[^{]*\{', tail)
                if not catch_m:
                    break
                catch_brace = end + catch_m.end() - 1  # position of '{'
                new_end = self._strip_brace_block(result, catch_brace)
                if new_end == -1:
                    break
                end = new_end
            result = result[:start] + self._TODO_TRY_CATCH + ";" + result[end:]
        return result

    def _strip_assembly_blocks(self, content: str) -> str:
        """Remove assembly { ... } blocks (brace-depth-aware)."""
        result = content
        while True:
            m = re.search(r'\bassembly\b\s*\{', result)
            if not m:
                break
            start = m.start()
            brace_open = m.end() - 1
            end = self._strip_brace_block(result, brace_open)
            if end == -1:
                break
            result = result[:start] + self._TODO_ASSEMBLY + ";" + result[end:]
        return result

    def convert(self, solidity_content: str) -> str:
        # Strip try-catch and assembly blocks before parsing so that the
        # regex-based parser never sees raw Solidity syntax it cannot handle.
        # We replace them with placeholder tokens that survive _parse_statements
        # (which strips //… comments) and are later emitted as TODO comments.
        solidity_content = self._strip_try_catch_blocks(solidity_content)
        solidity_content = self._strip_assembly_blocks(solidity_content)

        # Reset per-conversion state
        self._using_for = {}
        self._warnings = []

        # Detect using-for directives: using LibName for TypeName
        for m in re.finditer(r'using\s+(\w+)\s+for\s+(\w+)', solidity_content):
            lib_name = m.group(1)
            type_name = m.group(2)
            self._using_for[type_name] = lib_name

        # Warn about libraries not in LIBRARY_FUNCTION_MAP
        known_lib_names = {k[0] for k in LIBRARY_FUNCTION_MAP}
        for type_name, lib_name in self._using_for.items():
            if lib_name not in known_lib_names:
                self._warnings.append(
                    TranspilationWarning(
                        f"Library {lib_name} not recognized — method calls on {type_name} may not compile"
                    )
                )

        name = self.parse_contract_name(solidity_content) or "Contract"
        parents = self.parse_inheritance(solidity_content)
        is_abstract = self.parse_abstract_contract(solidity_content)
        structs = self.parse_structs(solidity_content)
        events = self.parse_events(solidity_content)
        errors = self.parse_errors(solidity_content)
        modifiers = self.parse_modifiers(solidity_content)
        functions = self.parse_functions(solidity_content)
        storage = self._extract_storage(solidity_content)

        # Build lookup sets used by _convert_expression and _convert_statement
        self._storage_var_names = {
            var_name for var_type, var_name, _ in storage
            if var_type not in ("mapping", "nested_mapping", "array")
        }
        self._storage_var_types = {
            var_name: var_type for var_type, var_name, _ in storage
            if var_type not in ("mapping", "nested_mapping")
        }
        self._mapping_var_names = {
            var_name: (2 if var_type == "nested_mapping" else 1)
            for var_type, var_name, _ in storage
            if var_type in ("mapping", "nested_mapping")
        }
        self._array_var_names = {
            var_name for var_type, var_name, _ in storage
            if var_type == "array"
        }

        lines: list[str] = []
        lines.append("#![no_std]\n")
        lines.append("use multiversx_sc::imports::*;\n")

        # Add inheritance comment if there are parent contracts
        if parents:
            lines.append(f"// Inherits from: {', '.join(parents)}\n")
        # Add hex import if needed (for large number conversion)
        if any("hex::decode" in line for line in self._parse_statements("\n".join([f.get("body", "") for f in functions])) if isinstance(line, dict) and line.get("type") == "assignment"):
            # Check if any function body uses hex::decode
            for func in functions:
                if "hex::decode" in self.convert_function(func, name):
                    lines.append("use multiversx_sc::hex;\n")
                    break

        for s in structs:
            lines.append(self.convert_struct(s))
        if structs:
            lines.append("")

        for e in errors:
            lines.append(self.convert_error(e))
        if errors:
            lines.append("")

        lines.append("#[multiversx_sc::contract]")
        # Generate trait with supertrait bounds for inheritance
        if parents:
            supertraits = " + ".join(parents)
            lines.append(f"pub trait {name}: {supertraits} {{")
        else:
            lines.append(f"pub trait {name} {{")

        for var_type, var_name, mapping_info in storage:
            mapper_t = self._convert_storage_mapper(var_type, var_name, mapping_info)
            snake_name = camel_to_snake(var_name)

            if var_type == "array":
                lines.append(f"    #[storage_mapper(\"{var_name}\")]")
                lines.append(f"    fn {snake_name}(&self) -> {mapper_t};")
            elif var_type == "nested_mapping":
                # Parse key1=>key2=>value nested mapping
                parts = mapping_info.split("=>")
                if len(parts) == 3:
                    key1_type = parts[0].strip()
                    key2_type = parts[1].strip()
                    lines.append(f"    #[storage_mapper(\"{var_name}\")]")
                    lines.append(f"    fn {snake_name}(&self, key1: &{self._map_type(key1_type)}, key2: &{self._map_type(key2_type)}) -> {mapper_t};")
            elif var_type == "mapping":
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
            lines.append(f"    {self.convert_function(f, name, modifiers)}")
            lines.append("")

        lines.append("}")
        return "\n".join(lines)

    def convert_with_diagnostics(self, solidity_content: str) -> TranspilationResult:
        """Convert Solidity to MultiversX Rust with full diagnostics"""
        # First validate and check for issues
        result = self.validate_and_diagnose(solidity_content)

        # If there are critical errors, don't proceed
        if not result.success:
            return result

        # Perform the conversion
        try:
            result.code = self.convert(solidity_content)
            result.warnings.extend(self._warnings)
            result.success = True
        except Exception as e:
            result.add_error(f"Transpilation failed: {str(e)}")

        return result


def transpile(input_path: Path, output_path: Path) -> bool:
    content = input_path.read_text()
    code = Transpiler().convert(content)
    output_path.write_text(code)
    return True


def transpile_with_diagnostics(input_path: Path, output_path: Path) -> TranspilationResult:
    """Transpile with full diagnostics returned"""
    content = input_path.read_text()
    transpiler = Transpiler()
    result = transpiler.convert_with_diagnostics(content)

    if result.success:
        output_path.write_text(result.code)

    return result
