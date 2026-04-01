#!/usr/bin/env node

/**
 * Tests for xtract CLI subcommands
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

function run(...args) {
    return spawnSync(process.execPath, [CLI, ...args], {
        encoding: 'utf-8',
        stdio: 'pipe'
    });
}

// ─── test: --help ─────────────────────────────────────────────────────────────

console.log('\nTest: xtract --help shows all subcommands');
{
    const result = run('--help');
    const out = result.stdout;
    assert(result.status === 0, '--help exits 0');
    assert(out.includes('transpile'), '--help mentions transpile');
    assert(out.includes('build'), '--help mentions build');
    assert(out.includes('deploy'), '--help mentions deploy');
    assert(out.includes('scaffold'), '--help mentions scaffold');
}

// ─── test: --version ─────────────────────────────────────────────────────────

console.log('\nTest: xtract --version');
{
    const result = run('--version');
    assert(result.status === 0, '--version exits 0');
    assert(/xtract v\d+\.\d+\.\d+/.test(result.stdout.trim()), '--version prints version string');
}

// ─── test: scaffold ───────────────────────────────────────────────────────────

console.log('\nTest: xtract scaffold <name>');
{
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'xtract-scaffold-'));
    const name = 'HelloWorld';
    const destDir = path.join(tmpDir, name);

    const result = spawnSync(process.execPath, [CLI, 'scaffold', name], {
        cwd: tmpDir,
        encoding: 'utf-8',
        stdio: 'pipe'
    });

    assert(result.status === 0, 'scaffold exits 0');

    const expectedFiles = [
        path.join('src', `${name}.sol`),
        'Cargo.toml',
        'multiversx.json',
        'xtract.config.json',
        'README.md',
        path.join('wasm', '.gitkeep'),
        path.join('meta', 'Cargo.toml'),
        path.join('meta', 'src', 'main.rs'),
    ];

    for (const rel of expectedFiles) {
        assert(fs.existsSync(path.join(destDir, rel)), `scaffold creates ${rel}`);
    }

    // Check .sol content has contract name
    const solContent = fs.readFileSync(path.join(destDir, 'src', `${name}.sol`), 'utf-8');
    assert(solContent.includes(`contract ${name}`), 'sol file contains contract declaration');

    // Check Cargo.toml references the contract
    const cargoContent = fs.readFileSync(path.join(destDir, 'Cargo.toml'), 'utf-8');
    assert(cargoContent.includes(`${name}.rs`), 'Cargo.toml references src lib path');

    // Check xtract.config.json is valid JSON with expected keys
    const config = JSON.parse(fs.readFileSync(path.join(destDir, 'xtract.config.json'), 'utf-8'));
    assert(config.network === 'devnet', 'xtract.config.json has network=devnet');
    assert(Array.isArray(config.initArgs), 'xtract.config.json has initArgs array');

    // Cleanup
    fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ─── test: scaffold – no name gives error ─────────────────────────────────────

console.log('\nTest: xtract scaffold (no name)');
{
    const result = run('scaffold');
    assert(result.status !== 0, 'scaffold without name exits non-zero');
    assert(result.stderr.includes('contract name'), 'scaffold without name prints helpful error');
}

// ─── test: scaffold – existing dir gives error ────────────────────────────────

console.log('\nTest: xtract scaffold (existing dir)');
{
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'xtract-scaffold-'));
    const name = 'ExistingContract';
    fs.mkdirSync(path.join(tmpDir, name));

    const result = spawnSync(process.execPath, [CLI, 'scaffold', name], {
        cwd: tmpDir,
        encoding: 'utf-8',
        stdio: 'pipe'
    });

    assert(result.status !== 0, 'scaffold on existing dir exits non-zero');
    assert(result.stderr.includes('already exists'), 'scaffold prints "already exists" error');

    fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ─── test: backward compat – .sol file without subcommand ────────────────────

console.log('\nTest: xtract MyContract.sol backward compatibility');
{
    // We cannot run a full transpile in CI (no Python guaranteed), but we can
    // verify the CLI at least attempts to invoke transpile (exits with Python-
    // related error rather than "Unknown subcommand").
    const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'xtract-compat-'));
    const solFile = path.join(tmpDir, 'MyContract.sol');
    fs.writeFileSync(solFile, 'pragma solidity ^0.8.0;\ncontract MyContract {}');

    const result = spawnSync(process.execPath, [CLI, solFile], {
        encoding: 'utf-8',
        stdio: 'pipe'
    });

    // Should NOT print "Unknown subcommand"
    assert(!result.stderr.includes("Unknown subcommand"), 'backward compat does not hit unknown-subcommand error');

    fs.rmSync(tmpDir, { recursive: true, force: true });
}

// ─── test: unknown subcommand ─────────────────────────────────────────────────

console.log('\nTest: xtract unknown-cmd');
{
    const result = run('unknown-cmd');
    assert(result.status !== 0, 'unknown subcommand exits non-zero');
    assert(result.stderr.includes("Unknown subcommand"), 'unknown subcommand prints error');
}

// ─── summary ─────────────────────────────────────────────────────────────────

console.log(`\n${passed + failed} tests: ${passed} passed, ${failed} failed`);
process.exit(failed > 0 ? 1 : 0);
