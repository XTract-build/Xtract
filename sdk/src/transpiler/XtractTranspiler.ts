import { spawn } from 'child_process';
import { writeFile, unlink } from 'fs/promises';
import { tmpdir } from 'os';
import { join } from 'path';
import { Diagnostic, TranspileResult } from './TranspileResult';

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

function runCli(args: string[]): Promise<{ stdout: string; stderr: string; exitCode: number }> {
  return new Promise((resolve) => {
    const proc = spawn('python', ['-m', 'xtract.cli', ...args]);
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
  let parsed: { success?: boolean; rust_code?: string; diagnostics?: Diagnostic[] };
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

  return {
    success: parsed.success ?? false,
    rustCode: parsed.rust_code ?? '',
    diagnostics: parsed.diagnostics ?? [],
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
