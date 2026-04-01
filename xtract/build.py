import subprocess
from pathlib import Path


def build_contract(contract_dir: Path) -> bool:
    """Shell out to mxpy contract build in the given directory."""
    result = subprocess.run(["mxpy", "contract", "build"], cwd=contract_dir)
    return result.returncode == 0
