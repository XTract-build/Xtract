import * as fs from 'fs';
import { UserSigner } from '@multiversx/sdk-core';

export class WalletProvider {
  static async fromPemFile(pemPath: string): Promise<UserSigner> {
    const content = fs.readFileSync(pemPath, 'utf8');
    return WalletProvider.fromPemContent(content);
  }

  static fromPemContent(pemContent: string): UserSigner {
    return UserSigner.fromPem(pemContent);
  }

  static async fromKeystore(keystorePath: string, password: string): Promise<UserSigner> {
    const raw = fs.readFileSync(keystorePath, 'utf8');
    const keystore = JSON.parse(raw);
    return UserSigner.fromWallet(keystore, password);
  }

  static fromEnv(envVar: string = 'XTRACT_WALLET_PEM'): UserSigner {
    const pem = process.env[envVar];
    if (!pem) {
      throw new Error(`Environment variable "${envVar}" is not set`);
    }
    return WalletProvider.fromPemContent(pem);
  }
}
