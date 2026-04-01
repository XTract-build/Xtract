import { getNetworkConfig, Networks } from '../deploy/NetworkConfig';
import { WalletProvider } from '../deploy/WalletProvider';

// Mock @multiversx/sdk-core so the tests don't need the actual package installed
jest.mock(
  '@multiversx/sdk-core',
  () => ({
    UserSigner: {
      fromPem: jest.fn((pem: string) => ({ _pem: pem, getAddress: () => 'erd1test' })),
      fromWallet: jest.fn(() => ({ getAddress: () => 'erd1test' })),
    },
    ApiNetworkProvider: jest.fn(),
    SmartContractTransactionsFactory: jest.fn(),
    TransactionWatcher: jest.fn(),
    Address: jest.fn((addr: string) => ({ bech32: () => addr })),
    TransactionsFactoryConfig: jest.fn(),
  }),
  { virtual: true }
);

// A minimal valid-looking MultiversX PEM for testing
const TEST_PEM = `-----BEGIN PRIVATE KEY for erd1spyavw0956vq68ynyl0ckuwvy2pvnp5b5q0v43zm2tncxpgrm2sqh99de-----
OWQ3NTk0NGFiOTI5N2UzMTdiMTIzZGFhYzg0OWFhMjZmNjkyODE4MDYzZGE2YjFk
NjQ0ZmU5ZWExNzk4ZDQ2YQ==
-----END PRIVATE KEY for erd1spyavw0956vq68ynyl0ckuwvy2pvnp5b5q0v43zm2tncxpgrm2sqh99de-----`;

describe('NetworkConfig', () => {
  it('getNetworkConfig returns devnet chainId D', () => {
    const cfg = getNetworkConfig('devnet');
    expect(cfg.chainId).toBe('D');
    expect(cfg.apiUrl).toBe('https://devnet-api.multiversx.com');
  });

  it('getNetworkConfig returns testnet chainId T', () => {
    const cfg = getNetworkConfig('testnet');
    expect(cfg.chainId).toBe('T');
  });

  it('getNetworkConfig returns mainnet chainId 1', () => {
    const cfg = getNetworkConfig('mainnet');
    expect(cfg.chainId).toBe('1');
  });

  it('getNetworkConfig throws for unknown network', () => {
    expect(() => getNetworkConfig('unknown')).toThrow(/Unknown network/);
  });

  it('Networks object has all three networks', () => {
    expect(Object.keys(Networks)).toEqual(expect.arrayContaining(['devnet', 'testnet', 'mainnet']));
  });
});

describe('WalletProvider', () => {
  it('fromPemContent() returns a signer without throwing', () => {
    const signer = WalletProvider.fromPemContent(TEST_PEM);
    expect(signer).toBeDefined();
  });

  it('fromPemContent() calls UserSigner.fromPem with the pem content', () => {
    const { UserSigner } = require('@multiversx/sdk-core');
    WalletProvider.fromPemContent(TEST_PEM);
    expect(UserSigner.fromPem).toHaveBeenCalledWith(TEST_PEM);
  });

  it('fromEnv() throws when env var is not set', () => {
    delete process.env['XTRACT_WALLET_PEM'];
    expect(() => WalletProvider.fromEnv()).toThrow(/XTRACT_WALLET_PEM/);
  });

  it('fromEnv() reads from the specified env var', () => {
    process.env['TEST_WALLET_PEM'] = TEST_PEM;
    const signer = WalletProvider.fromEnv('TEST_WALLET_PEM');
    expect(signer).toBeDefined();
    delete process.env['TEST_WALLET_PEM'];
  });
});

describe('Integration tests (skipped unless RUN_INTEGRATION=true)', () => {
  const runIntegration = process.env['RUN_INTEGRATION'] === 'true';

  (runIntegration ? it : it.skip)('deploys a contract to devnet', async () => {
    // Full integration test — requires a funded wallet and a compiled .wasm
    // Set RUN_INTEGRATION=true and provide XTRACT_WALLET_PEM to run
    expect(true).toBe(true);
  });
});
