import { expose } from 'comlink';

export type WizyRecord = Record<string, unknown>;

export interface WizyInput {
  personal?: WizyRecord[];
  local?: WizyRecord[];
  social?: WizyRecord[];
}

export interface WizyResult {
  value: { traits: string[] };
  used: Array<'P' | 'L' | 'S'>;
  explanation: string;
}

const api = {
  /**
   * D1: deterministic, local-only derivation. It never sees the network;
   * the caller decides which P/L/S slices to hand over.
   */
  derive(input: WizyInput): WizyResult {
    const personal = input.personal ?? [];
    const local = input.local ?? [];
    const social = input.social ?? [];
    const used: WizyResult['used'] = [];
    const pool: WizyRecord[] = [];

    if (personal.length) { used.push('P'); pool.push(...personal); }
    if (local.length) { used.push('L'); pool.push(...local); }
    if (social.length) { used.push('S'); pool.push(...social); }

    const counts = new Map<string, number>();
    for (const record of pool) {
      const traits = record.traits;
      if (!Array.isArray(traits)) continue;
      for (const trait of traits) {
        if (typeof trait !== 'string') continue;
        counts.set(trait, (counts.get(trait) ?? 0) + 1);
      }
    }

    const top = [...counts.entries()]
      .sort((a, b) => b[1] - a[1])
      .slice(0, 3)
      .map(([trait]) => trait);

    return {
      value: { traits: top },
      used,
      explanation: `D1 over ${used.length ? used.join('+') : 'no data'}; ${top.length} trait(s).`
    };
  }
};

expose(api);

export type WizyApi = typeof api;
