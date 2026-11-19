import canonicalize from 'canonicalize';
import type { Bundle } from '../schema';
import { signMessage, verifyMessage } from './identity';

export function payloadOf(bundle: Bundle): string {
  const { signature: _signature, ...rest } = bundle;
  return canonicalize(rest) ?? '{}';
}

export function signBundle(bundle: Bundle, privateKey: string): Bundle {
  return { ...bundle, signature: signMessage(payloadOf(bundle), privateKey) };
}

export function verifyBundle(bundle: Bundle, publicKey: string): boolean {
  return verifyMessage(payloadOf(bundle), bundle.signature, publicKey);
}
