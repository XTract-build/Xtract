#!/usr/bin/env node

/**
 * Main test runner – runs existing subcommand tests then backward-compat
 * flag-before-file routing tests.
 */

const { spawnSync } = require('child_process');
const path = require('path');
const fs = require('fs');
const os = require('os');

const CLI = path.resolve(__dirname, '..', 'bin', 'xtract.js');

let passed = 0;
let failed = 0;

function assert(condition, message) {
    if (condition) {
        console.log(`  PASS: ${message}`);
        passed++;
    } else {
        console.error(`  FAIL: ${message}`);
        failed++;
    }
}

function run(args, opts) {
    return spawnSync(process.execPath, [CLI, ...args], {
        encoding: 'utf-8',
        stdio: 'pipe',
        ...opts
    });
}

// ─── delegate to existing subcommand test suite ───────────────────────────────

console.log('\n=== Subcommand tests (test-subcommands.js) ===');
{
    const result = spawnSync(
        process.execPath,
        [path.resolve(__dirname, 'test-subcommands.js')],
        { encoding: 'utf-8', stdio: 'inherit' }
    );
    if (result.status !== 0) {
        console.error('\n  FAIL: test-subcommands.js exited non-zero');
        failed++;
    } else {
        passed++;
    }
}

// ─── backward-compat: flag-before-file routing ───────────────────────────────

console.log('\nTest: xtract --verbose file.sol routes to transpile');
{
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'xtract-flag-compat-'));
    const solFile = path.join(tmpDir, 'MyContract.sol');
    fs.writeFileSync(solFile, 'pragma solidity ^0.8.0;\ncontract MyContract {}');

    const result = run(['--verbose', solFile]);

    assert(
        !result.stderr.includes('Unknown subcommand'),
        '--verbose file.sol does not hit unknown-subcommand error (routes to transpile)'
    );

    fs.rmSync(tmpDir, { recursive: true, force: true });
}

console.log('\nTest: xtract --quiet file.sol routes to transpile');
{
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'xtract-flag-compat-'));
    const solFile = path.join(tmpDir, 'MyContract.sol');
    fs.writeFileSync(solFile, 'pragma solidity ^0.8.0;\ncontract MyContract {}');

    const result = run(['--quiet', solFile]);

    assert(
        !result.stderr.includes('Unknown subcommand'),
        '--quiet file.sol does not hit unknown-subcommand error (routes to transpile)'
    );

    fs.rmSync(tmpDir, { recursive: true, force: true });
}

console.log('\nTest: xtract --json file.sol with relative path');
{
    // Use an existing fixture via a relative path from the repo root
    const repoRoot = path.resolve(__dirname, '..');
    const relPath = path.relative(repoRoot, path.join(repoRoot, 'test_cases', 'solidity', 'Counter.sol'));

    const result = run(['--json', relPath], { cwd: repoRoot });

    assert(
        !result.stderr.includes('Unknown subcommand'),
        '--json <relative-path.sol> does not hit unknown-subcommand error (routes to transpile)'
    );
}

console.log('\nTest: xtract --json file with spaces in path routes to transpile');
{
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'xtract flag compat '));
    const solFile = path.join(tmpDir, 'My Contract.sol');
    fs.writeFileSync(solFile, 'pragma solidity ^0.8.0;\ncontract MyContract {}');

    const result = run(['--json', solFile]);

    assert(
        !result.stderr.includes('Unknown subcommand'),
        '--json "path with spaces.sol" does not hit unknown-subcommand error (routes to transpile)'
    );

    fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ─── summary ─────────────────────────────────────────────────────────────────

console.log(`\n${passed + failed} tests: ${passed} passed, ${failed} failed`);
process.exit(failed > 0 ? 1 : 0);
