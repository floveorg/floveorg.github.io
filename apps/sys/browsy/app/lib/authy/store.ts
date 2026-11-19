import Dexie, { type Table } from 'dexie';

export interface VaultRow {
  id: string;
  payload: string;
}

export interface MetaRow {
  id: string;
  publicKey: string;
  identityHash: string;
  createdAt: number;
}

export interface RecordRow {
  id: string;
  personId: string;
  class: 'P' | 'L' | 'S';
  payload: string;
  updatedAt: number;
}

export interface GrantRow {
  id: string;
  bundleId: string;
  grantee: string;
  paths: string[];
  expiresAt: string;
  signature: string;
}

class BrowsyDB extends Dexie {
  vault!: Table<VaultRow, string>;
  meta!: Table<MetaRow, string>;
  records!: Table<RecordRow, string>;
  grants!: Table<GrantRow, string>;

  constructor() {
    super('browsy');
    this.version(1).stores({
      vault: 'id',
      meta: 'id',
      records: 'id, class, personId, updatedAt',
      grants: 'id, bundleId, grantee'
    });
  }
}

export const db = new BrowsyDB();
