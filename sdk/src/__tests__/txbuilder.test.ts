const MOCK_NETWORK = {
  name: 'devnet' as const,
  chainId: 'D',
  apiUrl: 'https://devnet-api.multiversx.com',
  explorerUrl: 'https://devnet-explorer.multiversx.com',
};

const MOCK_ABI = { endpoints: [] };
const CONTRACT_ADDRESS = 'erd1qqqqqqqqqqqqqpgqd77fnev2sthnczp2lnfx0y5jdycynjfhzzgq6p3rax';

describe('TxBuilder Missing @multiversx/sdk-core', () => {
  beforeEach(() => {
    jest.resetModules();
  });

  it('throws an error if @multiversx/sdk-core is missing', async () => {
    // Override the mock specifically for this test to throw an error simulating missing module
    jest.doMock('@multiversx/sdk-core', () => {
      throw new Error("Cannot find module '@multiversx/sdk-core'");
    });

    // Dynamically import TxBuilder after setting the mock
    const { TxBuilder: IsolatedTxBuilder } = await import('../interact/TxBuilder');

    const builder = new IsolatedTxBuilder(CONTRACT_ADDRESS, MOCK_ABI, MOCK_NETWORK);
    expect(() => {
      builder.build('setValue', [], { caller: CONTRACT_ADDRESS });
    }).toThrow('@multiversx/sdk-core is required for building transactions. Install it with: npm install @multiversx/sdk-core');
  });
});
