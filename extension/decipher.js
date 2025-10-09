document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('input');
  const out = document.getElementById('output');
  const run = document.getElementById('run');
  chrome.storage.local.get('__intell_selected', (res) => {
    input.value = res.__intell_selected || '';
  });
  run.addEventListener('click', () => {
    const txt = input.value || '';
  var endpoint = 'http://localhost:8080/api/decipher';
    fetch(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ text: txt }) })
      .then(r=>r.text())
      .then(t=>{ out.textContent = t; })
      .catch(err=>{ out.textContent = String(err); });
  });
});
