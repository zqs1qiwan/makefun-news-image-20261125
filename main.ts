// main.ts — entry program for make.fun news-image-20261125.
//
// The entry is a one-image front-page summary of Wednesday 25 November
// 2026's world news: China investigates Politburo member Chen Jining,
// a US jury convicts Huawei on 10 of 12 counts, a Houthi drone hits
// Riyadh's PIF tower again, gunmen hold 25 hostage in Cartagena,
// Nvidia's Jensen Huang in therapy after his comeback, and Estonia
// weighing shutting its last rail crossing with Russia — plus three
// more stories in the ALSO band.
// The program copies it to the output directory. It runs with no network, Node 22,
// standard library only, and both runs write byte-identical output (a plain copy).
// Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL('./entry.png', import.meta.url), join(outDir, 'entry.png'));
