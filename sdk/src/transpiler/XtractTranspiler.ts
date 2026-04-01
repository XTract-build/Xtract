import { spawn, spawnSync } from 'child_process';
import { writeFile, unlink } from 'fs/promises';
import { existsSync } from 'fs';
import { tmpdir } from 'os';
import { join, resolve } from 'path';
import { Diagnostic, TranspileResult } from './TranspileResult';

// Walk up from this file's directory to find the directory that contains
// the `xtract` Python package, so the CLI works regardless of CWD.
function findXtractRoot(): string | undefined {
  let dir = resolve(__dirname);
  for (let i = 0; i < 6; i++) {
    if (existsSync(join(dir, 'xtract', '__init__.py'))) return dir;
    const parent = resolve(dir, '..');
    if (parent === dir) break;
    dir = parent;
  }
  return undefined;
}

let resolvedPythonCache: string | null = null;

export function resetPythonCache(): void { resolvedPythonCache = null; }

export interface TranspileOptions {
  verbose?: boolean;
}

export class TranspileError extends Error {
  constructor(
    message: string,
    public readonly exitCode: number,
    public readonly stderr: string
  ) {
    super(message);
    this.name = 'TranspileError';
  }
}

function resolvePython(): string {
  if (resolvedPythonCache) return resolvedPythonCache;
  for (const candidate of ['python3', 'python']) {
    const result = spawnSync(candidate, ['--version'], { encoding: 'utf8' });
    if (result.status === 0) {
      resolvedPythonCache = candidate;
      return resolvedPythonCache;
    }
  }
  throw new Error(
    'Could not find a Python executable. Make sure xtract is installed: pip install xtract. Tried: python3, python'
  );
}

function runCli(args: string[]): Promise<{ stdout: string; stderr: string; exitCode: number }> {
  return new Promise((resolve) => {
    const python = resolvePython();
    const xtractRoot = findXtractRoot();
    const env = { ...process.env };
    if (xtractRoot) {
      env['PYTHONPATH'] = xtractRoot + (env['PYTHONPATH'] ? `:${env['PYTHONPATH']}` : '');
    }
    const proc = spawn(python, ['-m', 'xtract.cli', ...args], { env });
    let stdout = '';
    let stderr = '';
    proc.stdout.on('data', (chunk: Buffer) => { stdout += chunk.toString(); });
    proc.stderr.on('data', (chunk: Buffer) => { stderr += chunk.toString(); });
    proc.on('close', (code) => {
      resolve({ stdout, stderr, exitCode: code ?? 1 });
    });
  });
}

function parseOutput(stdout: string, exitCode: number, stderr: string): TranspileResult {
  let parsed: { success?: boolean; code?: string; rust_code?: string; warnings?: Diagnostic[]; errors?: Diagnostic[]; diagnostics?: Diagnostic[] };
  try {
    parsed = JSON.parse(stdout);
  } catch {
    if (exitCode !== 0) {
      throw new TranspileError(`Transpiler exited with code ${exitCode}`, exitCode, stderr);
    }
    throw new TranspileError(`Failed to parse transpiler output: ${stdout}`, exitCode, stderr);
  }

  if (exitCode !== 0 && !parsed.success) {
    throw new TranspileError(
      `Transpiler failed: ${stderr || 'unknown error'}`,
      exitCode,
      stderr
    );
  }

  const diagnostics: Diagnostic[] = [
    ...(parsed.diagnostics ?? []),
    ...(parsed.warnings ?? []),
    ...(parsed.errors ?? []),
  ];

  return {
    success: parsed.success ?? false,
    rustCode: parsed.code ?? parsed.rust_code ?? '',
    diagnostics,
  };
}

export class XtractTranspiler {
  async transpileFile(solPath: string, options?: TranspileOptions): Promise<TranspileResult> {
    const args = ['--json'];
    if (options?.verbose) args.push('--verbose');
    args.push(solPath);

    const { stdout, stderr, exitCode } = await runCli(args);
    return parseOutput(stdout, exitCode, stderr);
  }

  async transpileCode(soliditySource: string): Promise<TranspileResult> {
    const tmpFile = join(tmpdir(), `xtract_${Date.now()}_${Math.random().toString(36).slice(2)}.sol`);
    await writeFile(tmpFile, soliditySource, 'utf8');
    try {
      return await this.transpileFile(tmpFile);
    } finally {
      await unlink(tmpFile).catch(() => undefined);
    }
  }

  static async isInstalled(): Promise<boolean> {
    const { exitCode } = await runCli(['--version']);
    return exitCode === 0;
  }

  static async getVersion(): Promise<string> {
    const { stdout, stderr, exitCode } = await runCli(['--version']);
    if (exitCode !== 0) {
      throw new TranspileError('Could not determine xtract version', exitCode, stderr);
    }
    return stdout.trim();
  }
}
