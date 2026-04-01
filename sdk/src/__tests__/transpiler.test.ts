import * as childProcess from 'child_process';
import { XtractTranspiler } from '../transpiler';

const SIMPLE_SOLIDITY = `
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleStorage {
    uint256 private value;

    function setValue(uint256 _value) public {
        value = _value;
    }

    function getValue() public view returns (uint256) {
        return value;
    }
}
`;

describe('XtractTranspiler', () => {
  let transpiler: XtractTranspiler;

  beforeEach(() => {
    transpiler = new XtractTranspiler();
  });

  it('transpileCode() returns TranspileResult with success=true for valid Solidity', async () => {
    const result = await transpiler.transpileCode(SIMPLE_SOLIDITY);
    expect(result.success).toBe(true);
  });

  it('rustCode contains #[multiversx_sc::contract]', async () => {
    const result = await transpiler.transpileCode(SIMPLE_SOLIDITY);
    expect(result.rustCode).toContain('#[multiversx_sc::contract]');
  });

  it('diagnostics array is present', async () => {
    const result = await transpiler.transpileCode(SIMPLE_SOLIDITY);
    expect(Array.isArray(result.diagnostics)).toBe(true);
  });
});

describe('resolvePython() – no Python binary found', () => {
  let spawnSyncSpy: jest.SpyInstance;

  beforeEach(() => {
    spawnSyncSpy = jest
      .spyOn(childProcess, 'spawnSync')
      .mockReturnValue({ status: 1, stdout: '', stderr: '', pid: 0, output: [], signal: null });
  });

  afterEach(() => {
    spawnSyncSpy.mockRestore();
  });

  it('throws an error mentioning pip install xtract and the tried candidates', async () => {
    const transpiler = new XtractTranspiler();
    await expect(transpiler.transpileCode('contract Foo {}')).rejects.toThrow(
      /pip install xtract/
    );
    await expect(transpiler.transpileCode('contract Foo {}')).rejects.toThrow(
      /python3.*python|python.*python3/
    );
  });
});
