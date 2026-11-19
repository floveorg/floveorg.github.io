import { ed25519 } from '@noble/curves/ed25519';
import { bytesToHex, hexToBytes } from '@noble/hashes/utils';
import { CID } from 'multiformats/cid';
import { sha256 } from 'multiformats/hashes/sha2';
import * as raw from 'multiformats/codecs/raw';

export interface Identity {
  privateKey: string;
  publicKey: string;
  identityHash: string;
}

const enc = new TextEncoder();

/**
 * BSP-I05: the identity hash is CIDv1(sha256(ed25519_pubkey)).
 * The same hash becomes the Nety PeerId when Nety imports the root.
 */
export async function createIdentity(): Promise<Identity> {
  const privateKey = ed25519.utils.randomPrivateKey();
  const publicKey = ed25519.getPublicKey(privateKey);
  const digest = await sha256.digest(publicKey);
  const identityHash = CID.createV1(raw.code, digest).toString();

  return {
    privateKey: bytesToHex(privateKey),
    publicKey: bytesToHex(publicKey),
    identityHash
  };
}

export function signMessage(message: string, privateKeyHex: string): string {
  const signature = ed25519.sign(enc.encode(message), hexToBytes(privateKeyHex));
  return bytesToHex(signature);
}

export function verifyMessage(message: string, signatureHex: string, publicKeyHex: string): boolean {
  try {
    return ed25519.verify(hexToBytes(signatureHex), enc.encode(message), hexToBytes(publicKeyHex));
  } catch {
    return false;
  }
}
