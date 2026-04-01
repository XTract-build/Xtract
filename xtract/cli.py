import json
import sys
from pathlib import Path
from typing import Optional
import click

from .transpiler import transpile, transpile_with_diagnostics, Transpiler


# ---------------------------------------------------------------------------
# Custom group: if the first argument is not a known subcommand, treat it as
# a .sol file and forward to `transpile` — preserves backward compatibility.
# ---------------------------------------------------------------------------

class _XtractGroup(click.Group):
    def parse_args(self, ctx, args):
        if args and not args[0].startswith("-") and args[0] not in self.commands:
            args.insert(0, "transpile")
        return super().parse_args(ctx, args)


@click.group(cls=_XtractGroup)
def main():
    """XTract — Solidity to MultiversX Rust transpiler."""


# ---------------------------------------------------------------------------
# transpile
# ---------------------------------------------------------------------------

@main.command("transpile")
@click.argument("input", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.argument("output", required=False, type=click.Path(dir_okay=False, path_type=Path))
@click.option("-v", "--verbose", is_flag=True, help="Show detailed diagnostics and warnings")
@click.option("-q", "--quiet", is_flag=True, help="Suppress all output except errors")
@click.option("--json", "output_json", is_flag=True, default=False, help="Output structured JSON instead of Rust code")
def transpile_cmd(input: Path, output: Optional[Path], verbose: bool, quiet: bool, output_json: bool):
    """Transpile a Solidity file to MultiversX Rust.

    INPUT: Solidity .sol file path\n
    OUTPUT: Optional Rust .rs output path; defaults to INPUT with .rs extension
    """
    try:
        if output_json:
            content = input.read_text()
            result = Transpiler().convert_with_diagnostics(content)
            print(json.dumps({
                "success": result.success,
                "code": result.code,
                "warnings": [
                    {"message": w.message, "line": w.line, "severity": w.severity}
                    for w in result.warnings
                ],
                "errors": result.errors,
            }))
            raise SystemExit(0 if result.success else 1)

        out = output if output is not None else input.with_suffix(".rs")

        if verbose:
            result = transpile_with_diagnostics(input, out)

            if result.warnings:
                click.echo(click.style("\nDiagnostics:", fg="yellow", bold=True))
                for warning in result.warnings:
                    color = "yellow" if warning.severity == "warning" else "cyan"
                    prefix = "⚠️ " if warning.severity == "warning" else "ℹ️ "
                    click.echo(click.style(f"  {prefix}{warning.message}", fg=color))

            if result.errors:
                click.echo(click.style("\nErrors:", fg="red", bold=True))
                for error in result.errors:
                    click.echo(click.style(f"  ❌ {error}", fg="red"))

            if not result.success:
                click.echo(click.style("\nTranspilation failed", fg="red"), err=True)
                raise SystemExit(1)

            if not quiet:
                click.echo(click.style(f"\n✅ Wrote {out}", fg="green"))
        else:
            success = transpile(input, out)
            if not success:
                click.echo("Transpilation failed", err=True)
                raise SystemExit(1)
            if not quiet:
                click.echo(f"Wrote {out}")

    except SystemExit:
        raise
    except Exception as exc:
        click.echo(f"Error: {exc}", err=True)
        raise SystemExit(1)


# ---------------------------------------------------------------------------
# build
# ---------------------------------------------------------------------------

@main.command("build")
@click.argument("contract_dir", type=click.Path(exists=True, file_okay=False, path_type=Path))
def build_cmd(contract_dir: Path):
    """Compile a MultiversX Rust contract to WASM via mxpy.

    CONTRACT_DIR: directory containing the contract (must have mxpy.json or Cargo.toml)
    """
    try:
        from .build import build_contract
    except ImportError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)

    click.echo(f"Building {contract_dir} ...")
    ok = build_contract(contract_dir)
    if not ok:
        click.echo("Build failed.", err=True)
        raise SystemExit(1)
    click.echo(click.style("✅ Build succeeded.", fg="green"))


# ---------------------------------------------------------------------------
# wallet
# ---------------------------------------------------------------------------

@main.group("wallet")
def wallet_group():
    """Wallet management commands."""


@wallet_group.command("create")
@click.option(
    "--output", "-o",
    type=click.Path(dir_okay=False, path_type=Path),
    default=None,
    help="Where to save the PEM file (default: ~/.multiversx/wallet.pem)",
)
def wallet_create(output: Optional[Path]):
    """Generate a new wallet and save it as a PEM file.

    Requires: pip install xtract[deploy]
    """
    from .wallet import create_wallet, DEFAULT_WALLET_PATH, FAUCET_URLS

    dest = output or DEFAULT_WALLET_PATH
    try:
        info = create_wallet(dest)
    except FileExistsError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    except ImportError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)

    click.echo(click.style("✅ Wallet created!", fg="green"))
    click.echo(f"   Address : {info.address}")
    click.echo(f"   PEM file: {info.pem_path}")
    click.echo(click.style("\n⚠️  Save your mnemonic — it will not be shown again:", fg="yellow"))
    click.echo(f"   {info.mnemonic}")
    click.echo(click.style("\n💧 Fund your wallet before deploying:", fg="cyan"))
    for network, url in FAUCET_URLS.items():
        click.echo(f"   {network}: {url}")


# ---------------------------------------------------------------------------
# deploy
# ---------------------------------------------------------------------------

@main.command("deploy")
@click.argument("wasm_path", type=click.Path(exists=True, dir_okay=False, path_type=Path))
@click.option("--abi", "abi_path", required=True, type=click.Path(exists=True, dir_okay=False, path_type=Path), help="Path to .abi.json file")
@click.option("--wallet", "wallet_path", required=True, type=click.Path(exists=True, dir_okay=False, path_type=Path), help="Path to PEM wallet file")
@click.option("--network", default="devnet", type=click.Choice(["devnet", "testnet", "mainnet"]), show_default=True, help="Target network")
@click.option("--gas-limit", default=10_000_000, show_default=True, help="Gas limit for deploy transaction")
@click.option("--no-upgrade", is_flag=True, default=False, help="Deploy as non-upgradeable contract")
def deploy_cmd(wasm_path: Path, abi_path: Path, wallet_path: Path, network: str, gas_limit: int, no_upgrade: bool):
    """Deploy a compiled WASM contract to MultiversX.

    Requires: pip install xtract[deploy]
    """
    try:
        from .deploy import deploy_contract
    except ImportError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)

    click.echo(f"Deploying to {network} ...")
    try:
        result = deploy_contract(
            wasm_path=wasm_path,
            abi_path=abi_path,
            wallet_path=wallet_path,
            network=network,
            gas_limit=gas_limit,
            upgradeable=not no_upgrade,
        )
    except ImportError as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)
    except Exception as e:
        click.echo(f"Error: {e}", err=True)
        raise SystemExit(1)

    click.echo(click.style("✅ Contract deployed!", fg="green"))
    click.echo(f"   Address : {result.contract_address}")
    click.echo(f"   Tx hash : {result.tx_hash}")
    click.echo(f"   Explorer: {result.explorer_url}")


if __name__ == "__main__":
    main()
