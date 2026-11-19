import { defineConfig } from 'wxt';

export default defineConfig({
  manifest: {
    name: 'Browsy',
    description: 'Identity, Local records and Wizy inside one browser extension.',
    permissions: ['storage', 'contextMenus'],
    host_permissions: [
      'https://flove.org/*',
      'http://localhost/*',
      'http://127.0.0.1/*'
    ],
    action: {
      default_title: 'Browsy'
    },
    icons: {
      16: 'icons/icon-16.png',
      32: 'icons/icon-32.png',
      48: 'icons/icon-48.png',
      128: 'icons/icon-128.png'
    },
    browser_specific_settings: {
      gecko: {
        id: 'browsy@flove.org',
        strict_min_version: '109.0'
      }
    }
  }
});
