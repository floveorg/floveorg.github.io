import { wrap, type Remote } from 'comlink';
import type { WizyApi } from './wizy.worker';

let worker: Worker | null = null;

export function wizy(): Remote<WizyApi> {
  if (!worker) {
    worker = new Worker(new URL('./wizy.worker.ts', import.meta.url), { type: 'module' });
  }
  return wrap<WizyApi>(worker);
}

export function stopWizy(): void {
  worker?.terminate();
  worker = null;
}
