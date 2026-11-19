import { z } from 'zod';

/**
 * The envelope proposed in the 2026-11-17 Browsy spec.
 * Every document maps to P, L or S; grants travel with the bundle.
 */
export const GrantSchema = z.object({
  grantor: z.string().min(1),
  grantee: z.string().min(1),
  bundle: z.string().min(1),
  paths: z.array(z.string().min(1)).min(1),
  capabilities: z.array(z.enum(['view', 'derive', 'aggregate'])).min(1),
  expiresAt: z.string().datetime(),
  contentKey: z.string().optional(),
  version: z.number().int().nonnegative(),
  signature: z.string().min(1)
});

export const BundleSchema = z.object({
  schema: z.literal('flove-bundle/0.1'),
  owner: z.string().min(1),
  class: z.enum(['P', 'L', 'S']),
  documents: z.array(z.record(z.string(), z.unknown())),
  grants: z.array(GrantSchema).default([]),
  signature: z.string().min(1)
});

/**
 * The record a page may hand to Browsy. MyNet/MyFamily are Local by default;
 * pages never choose P, and the background forces L for content-script calls.
 */
export const RecordSchema = z.object({
  id: z.string().optional(),
  personId: z.string().min(1),
  relation: z.string().max(80).optional(),
  traits: z.array(z.string().max(40)).max(3).optional(),
  affinity: z.string().max(80).optional(),
  note: z.string().max(500).optional(),
  class: z.enum(['P', 'L', 'S']).default('L')
});

export type Grant = z.infer<typeof GrantSchema>;
export type Bundle = z.infer<typeof BundleSchema>;
export type Record = z.infer<typeof RecordSchema>;
