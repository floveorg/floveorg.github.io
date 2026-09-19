// browsy · popup logic
// Detects current page and suggests relevant flove apps.

var APPS = [
  { name: 'appy', url: '/apps/appy/', match: 'flove.org' },
  { name: 'blogy', url: '/apps/blogy/', match: 'blog' },
  { name: 'nety',  url: '/apps/nety/',  match: 'social' },
  { name: 'sety',  url: '/apps/sety/',  match: 'setting' },
  { name: 'gody',  url: '/apps/gody/',  match: 'gody' }
];

chrome.tabs.query({ active: true, currentWindow: true }, function(tabs) {
  var tab = tabs[0];
  var container = document.getElementById('apps');
  if (!tab || !tab.url) {
    container.innerHTML = '<p class="empty">No page detected.</p>';
    return;
  }
  var url = tab.url;
  var matched = APPS.filter(function(a) {
    return url.includes(a.match) || url.includes('flove.org');
  });
  if (!matched.length) {
    container.innerHTML = '<p class="empty">No matching flove app.</p>';
    return;
  }
  matched.forEach(function(a) {
    var link = document.createElement('a');
    link.className = 'app-link';
    link.href = 'https://flove.org' + a.url;
    link.target = '_blank';
    link.innerHTML = '<b>' + a.name + '</b> → ' + a.url;
    container.appendChild(link);
  });
});
