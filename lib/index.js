/**
 * XTract - Solidity to MultiversX Rust Transpiler
 *
 * This module provides programmatic access to the XTract transpiler.
 */

const { spawn, spawnSync } = require('child_process');
const os = require('os');
const path = require('path');
const fs = require('fs');

const packageRoot = path.resolve(__dirname, '..');

/**
 * Find available Python executable
 * @returns {string|null} Python command or null if not found
 */
function findPython() {
    const pythonCommands = ['python3', 'python'];

    for (const cmd of pythonCommands) {
        try {
            const result = spawnSync(cmd, ['--version'], {
                encoding: 'utf-8',
                stdio: 'pipe'
            });
            if (result.status === 0) {
                return cmd;
            }
        } catch (e) {
            // Command not found, try next
        }
    }
    return null;
}

/**
 * Transpile a Solidity file to MultiversX Rust
 *
 * @param {string} inputPath - Path to the Solidity file
 * @param {string} [outputPath] - Optional output path (defaults to input with .rs extension)
 * @param {Object} [options] - Transpilation options
 * @param {boolean} [options.verbose] - Enable verbose output
 * @param {boolean} [options.quiet] - Enable quiet mode
 * @returns {Promise<{success: boolean, output: string, error: string}>}
 */
async function transpile(inputPath, outputPath, options = {}) {
    return new Promise((resolve, reject) => {
        const python = findPython();
        if (!python) {
            reject(new Error('Python 3.9+ is required but not found'));
            return;
        }

        const args = ['-m', 'xtract.cli', '--json'];

        if (options.verbose) {
            args.push('-v');
        }
        if (options.quiet) {
            args.push('-q');
        }

        args.push(inputPath);

        if (outputPath) {
            args.push(outputPath);
        }

        let stdout = '';
        let stderr = '';

        const proc = spawn(python, args, {
            cwd: packageRoot,
            env: {
                ...process.env,
                PYTHONPATH: packageRoot
            }
        });

        proc.stdout.on('data', (data) => {
            stdout += data.toString();
        });

        proc.stderr.on('data', (data) => {
            stderr += data.toString();
        });

        proc.on('error', (err) => {
            reject(err);
        });

        proc.on('close', (exitCode) => {
            try {
                const parsed = JSON.parse(stdout);
                resolve({
                    success: parsed.success,
                    code: parsed.code,
                    warnings: parsed.warnings,
                    errors: parsed.errors,
                    exitCode
                });
            } catch (e) {
                resolve({
                    success: false,
                    code: '',
                    warnings: [],
                    errors: [stderr || 'Failed to parse transpiler output'],
                    exitCode
                });
            }
        });
    });
}

/**
 * Transpile Solidity code directly (without file I/O)
 *
 * @param {string} solidityCode - Solidity source code
 * @returns {Promise<{success: boolean, rustCode: string, diagnostics: string[]}>}
 */
async function transpileCode(solidityCode) {
    return new Promise((resolve, reject) => {
        const python = findPython();
        if (!python) {
            reject(new Error('Python 3.9+ is required but not found'));
            return;
        }

        const tmpFile = path.join(os.tmpdir(), `xtract_${Date.now()}_${process.pid}.sol`);
        fs.writeFileSync(tmpFile, solidityCode);

        const args = ['-m', 'xtract.cli', '--json', tmpFile];

        let stdout = '';
        let stderr = '';

        const proc = spawn(python, args, {
            cwd: packageRoot,
            env: {
                ...process.env,
                PYTHONPATH: packageRoot
            }
        });

        proc.stdout.on('data', (data) => {
            stdout += data.toString();
        });

        proc.stderr.on('data', (data) => {
            stderr += data.toString();
        });

        proc.on('error', (err) => {
            try { fs.unlinkSync(tmpFile); } catch (_) {}
            reject(err);
        });

        proc.on('close', (exitCode) => {
            try { fs.unlinkSync(tmpFile); } catch (_) {}
            try {
                const parsed = JSON.parse(stdout);
                resolve({
                    success: parsed.success,
                    code: parsed.code,
                    warnings: parsed.warnings,
                    errors: parsed.errors,
                });
            } catch (e) {
                resolve({
                    success: false,
                    code: '',
                    warnings: [],
                    errors: [stderr || 'Failed to parse transpiler output'],
                });
            }
        });
    });
}

/**
 * Check if XTract is properly installed
 * @returns {boolean}
 */
function isInstalled() {
    const python = findPython();
    if (!python) return false;

    const xtractPath = path.join(packageRoot, 'xtract');
    return fs.existsSync(xtractPath);
}

/**
 * Get version information
 * @returns {string}
 */
function getVersion() {
    const pkg = require('../package.json');
    return pkg.version;
}

module.exports = {
    transpile,
    transpileCode,
    isInstalled,
    getVersion,
    findPython
};
