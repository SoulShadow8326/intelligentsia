document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('input');
  const out = document.getElementById('output');
  const run = document.getElementById('run');
  chrome.storage.local.get('__intell_selected', (res) => {
    input.value = res.__intell_selected || '';
  });
  run.addEventListener('click', () => {
    const txt = input.value || '';
    out.textContent = txt.split('').reverse().join('');
  });
});
