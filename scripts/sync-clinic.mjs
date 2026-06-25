// Copies the canonical clinic prototype into public/clinic/ so it ships verbatim
// at /clinic/clinic2d.html. The prototype stays the single source of truth
// (per HANDOFF.md); this just mirrors it on every dev/build.
import { cp, rm, mkdir } from 'node:fs/promises';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const root = dirname(dirname(fileURLToPath(import.meta.url)));
const src = join(root, 'prototype');
const dest = join(root, 'public', 'clinic');

// Only the files the running game actually needs (skip py scripts, blueprints, big pngs).
const INCLUDE = [
  'clinic2d.html',
  'dash.css',
  'dash.js',
  'assets_data.js',
  'map2d.js',
  'flow2d.js',
  'marks2d.js',
  'assets', // limezu sprite sheets etc.
];

await rm(dest, { recursive: true, force: true });
await mkdir(dest, { recursive: true });
for (const item of INCLUDE) {
  await cp(join(src, item), join(dest, item), { recursive: true }).catch((e) => {
    console.warn(`[sync-clinic] skipped ${item}: ${e.message}`);
  });
}
console.log('[sync-clinic] mirrored prototype -> public/clinic');
