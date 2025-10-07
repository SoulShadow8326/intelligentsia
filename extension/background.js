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
    chrome.storage.local.set({__intell_selected: selected}, () => {
      chrome.action.openPopup();
    });
  }
});
