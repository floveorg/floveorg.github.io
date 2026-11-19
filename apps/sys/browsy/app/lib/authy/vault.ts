/**
 * Vault primitives. The passphrase never leaves the background service worker.
 * PBKDF2-SHA256 is used here because it is native WebCrypto and works offline
 * in MV3; the follow-up is Argon2id in the worker once the vault contract is
 * stable. Everything is authenticated with AES-GCM.
 */

const enc = new TextEncoder();
const dec = new TextDecoder();

const DEFAULT_ITERATIONS = 310_000;

export interface VaultPayload {
  v: 1;
  kdf: 'PBKDF2-SHA256';
  iterations: number;
  salt: string;
  iv: string;
  data: string;
}

export interface EncryptedValue {
  iv: string;
  data: string;
}

function toBase64(bytes: Uint8Array): string {
  let binary = '';
  for (const byte of bytes) binary += String.fromCharCode(byte);
  return btoa(binary);
}

function fromBase64(value: string): Uint8Array {
  const binary = atob(value);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i += 1) bytes[i] = binary.charCodeAt(i);
  return bytes;
}

export async function deriveKey(
  passphrase: string,
  salt: Uint8Array,
  iterations = DEFAULT_ITERATIONS
): Promise<CryptoKey> {
  const base = await crypto.subtle.importKey(
    'raw',
    enc.encode(passphrase),
    'PBKDF2',
    false,
    ['deriveKey']
  );

  return crypto.subtle.deriveKey(
    { name: 'PBKDF2', salt, iterations, hash: 'SHA-256' },
    base,
    { name: 'AES-GCM', length: 256 },
    false,
    ['encrypt', 'decrypt']
  );
}

export async function createVault(
  value: unknown,
  passphrase: string,
  iterations = DEFAULT_ITERATIONS
): Promise<{ payload: VaultPayload; key: CryptoKey }> {
  const salt = crypto.getRandomValues(new Uint8Array(16));
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const key = await deriveKey(passphrase, salt, iterations);
  const plaintext = enc.encode(JSON.stringify(value));
  const ciphertext = await crypto.subtle.encrypt({ name: 'AES-GCM', iv }, key, plaintext);

  return {
    payload: {
      v: 1,
      kdf: 'PBKDF2-SHA256',
      iterations,
      salt: toBase64(salt),
      iv: toBase64(iv),
      data: toBase64(new Uint8Array(ciphertext))
    },
    key
  };
}

export async function openVault<T = unknown>(
  payload: VaultPayload,
  passphrase: string
): Promise<{ value: T; key: CryptoKey }> {
  const key = await deriveKey(passphrase, fromBase64(payload.salt), payload.iterations);

  try {
    const plaintext = await crypto.subtle.decrypt(
      { name: 'AES-GCM', iv: fromBase64(payload.iv) },
      key,
      fromBase64(payload.data)
    );
    return { value: JSON.parse(dec.decode(plaintext)) as T, key };
  } catch {
    throw new Error('wrong passphrase or corrupted vault');
  }
}

export async function encryptValue(value: unknown, key: CryptoKey): Promise<EncryptedValue> {
  const iv = crypto.getRandomValues(new Uint8Array(12));
  const ciphertext = await crypto.subtle.encrypt(
    { name: 'AES-GCM', iv },
    key,
    enc.encode(JSON.stringify(value))
  );
  return { iv: toBase64(iv), data: toBase64(new Uint8Array(ciphertext)) };
}

export async function decryptValue<T = unknown>(
  value: EncryptedValue,
  key: CryptoKey
): Promise<T> {
  try {
    const plaintext = await crypto.subtle.decrypt(
      { name: 'AES-GCM', iv: fromBase64(value.iv) },
      key,
      fromBase64(value.data)
    );
    return JSON.parse(dec.decode(plaintext)) as T;
  } catch {
    throw new Error('record could not be decrypted');
  }
}
