import { RecordSchema, type Record } from '../schema';
import { db } from './store';
import { createIdentity, signMessage, type Identity } from './identity';
import { createVault, decryptValue, encryptValue, openVault, type VaultPayload } from './vault';

interface Session extends Identity {
  vaultKey: CryptoKey;
}

let session: Session | null = null;

export interface PublicStatus {
  hasIdentity: boolean;
  locked: boolean;
  identityHash: string | null;
}

export async function status(): Promise<PublicStatus> {
  const meta = await db.meta.get('identity');
  const vault = await db.vault.get('root');
  return {
    hasIdentity: Boolean(meta && vault),
    locked: session === null,
    identityHash: meta?.identityHash ?? null
  };
}

export async function create(passphrase: string): Promise<PublicStatus> {
  if (passphrase.length < 8) throw new Error('passphrase must be at least 8 characters');
  if (await db.vault.get('root')) throw new Error('an identity already exists');

  const identity = await createIdentity();
  const { payload, key } = await createVault(identity, passphrase);

  await db.transaction('rw', db.vault, db.meta, async () => {
    await db.vault.put({ id: 'root', payload: JSON.stringify(payload) });
    await db.meta.put({
      id: 'identity',
      publicKey: identity.publicKey,
      identityHash: identity.identityHash,
      createdAt: Date.now()
    });
  });

  session = { ...identity, vaultKey: key };
  return status();
}

export async function unlock(passphrase: string): Promise<PublicStatus> {
  const row = await db.vault.get('root');
  if (!row) throw new Error('no identity to unlock');

  const payload = JSON.parse(row.payload) as VaultPayload;
  const { value, key } = await openVault<Identity>(payload, passphrase);
  session = { ...value, vaultKey: key };
  return status();
}

export function lock(): PublicStatus {
  session = null;
  return {
    hasIdentity: true,
    locked: true,
    identityHash: null
  };
}

export function isUnlocked(): boolean {
  return session !== null;
}

export function sign(message: string): string {
  if (!session) throw new Error('locked');
  return signMessage(message, session.privateKey);
}

export async function saveRecord(
  record: unknown,
  options: { fromPage?: boolean } = {}
): Promise<{ id: string; class: 'P' | 'L' | 'S' }> {
  if (!session) throw new Error('locked');

  const parsed = RecordSchema.parse(record);
  const cls = options.fromPage ? 'L' : parsed.class;
  const value: Record = { ...parsed, class: cls };
  const payload = await encryptValue(value, session.vaultKey);
  const id = value.id ?? crypto.randomUUID();

  await db.records.put({
    id,
    personId: value.personId,
    class: cls,
    payload: JSON.stringify(payload),
    updatedAt: Date.now()
  });

  return { id, class: cls };
}

export async function listRecords(
  options: { fromPage?: boolean } = {}
): Promise<Record[]> {
  if (!session) throw new Error('locked');

  const rows = await db.records.toArray();
  const out: Record[] = [];

  for (const row of rows) {
    if (options.fromPage && row.class === 'P') continue;
    const value = await decryptValue<Record>(JSON.parse(row.payload), session.vaultKey);
    out.push({ ...value, id: row.id, class: row.class });
  }

  return out;
}
