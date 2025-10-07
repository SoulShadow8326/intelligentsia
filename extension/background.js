chrome.runtime.onInstalled.addListener(() => {
  chrome.contextMenus.create({
    id: 'intelligentsia-decipher',
    title: 'Intelligentsia: Decipher',
    contexts: ['selection']
  });
});

chrome.contextMenus.onClicked.addListener((info, tab) => {
  if (info.menuItemId === 'intelligentsia-decipher') {
    const selected = info.selectionText || '';
    const url = chrome.runtime.getURL('decipher.html') + '#text=' + encodeURIComponent(selected);
    chrome.tabs.create({ url });
  }
});
