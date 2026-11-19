import { create, listRecords, lock, saveRecord, status, unlock } from '../lib/authy';

type Reply<T> = { ok: true; data: T } | { ok: false; error: string };

async function reply<T>(fn: () => Promise<T> | T): Promise<Reply<T>> {
  try {
    return { ok: true, data: await fn() };
  } catch (error) {
    return { ok: false, error: error instanceof Error ? error.message : String(error) };
  }
}

const FLOVE_URL = /^https?:\/\/(flove\.org|localhost|127\.0\.0\.1)(?::\d+)?(\/|$)/;

export default defineBackground(() => {
  browser.runtime.onInstalled.addListener(async () => {
    await browser.contextMenus.removeAll();
    browser.contextMenus.create({
      id: 'browsy-save',
      title: 'Save to flove',
      contexts: ['selection', 'link', 'image']
    });
    browser.contextMenus.create({
      id: 'browsy-share',
      title: 'Share to Nety',
      contexts: ['page', 'selection']
    });
  });

  browser.contextMenus.onClicked.addListener((info, tab) => {
    if (!tab?.id) return;
    const type = info.menuItemId === 'browsy-save'
      ? 'browsy:save-triggered'
      : 'browsy:share-triggered';
    browser.tabs.sendMessage(tab.id, { type, info }).catch(() => {
      // No content script on this tab; the menu is best-effort.
    });
  });

  browser.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.status !== 'complete') return;
    const isFlove = FLOVE_URL.test(tab.url ?? '');
    browser.action.setBadgeText({ tabId, text: isFlove ? '★' : '' }).catch(() => {});
    if (isFlove) {
      browser.action.setBadgeBackgroundColor({ tabId, color: '#6c5ce7' }).catch(() => {});
    }
  });

  browser.runtime.onMessage.addListener((message: unknown, sender) => {
    if (!message || typeof message !== 'object') return;
    const msg = message as { type?: string; passphrase?: string; payload?: unknown };
    if (typeof msg.type !== 'string') return;

    const fromPage = Boolean(sender.tab);

    switch (msg.type) {
      case 'browsy:status':
        return reply(status);

      case 'browsy:info':
        return reply(async () => ({
          version: browser.runtime.getManifest().version,
          ...(await status())
        }));

      case 'browsy:create':
        return reply(() => create(String(msg.passphrase ?? '')));

      case 'browsy:unlock':
        return reply(() => unlock(String(msg.passphrase ?? '')));

      case 'browsy:lock':
        return reply(() => lock());

      case 'browsy:save-record':
        return reply(() => saveRecord(msg.payload, { fromPage }));

      case 'browsy:list-records':
        return reply(() => listRecords({ fromPage }));

      default:
        return;
    }
  });
});
