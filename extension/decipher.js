document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('input');
  const out = document.getElementById('output');
  const run = document.getElementById('run');
  chrome.storage.local.get('__intell_selected', (res) => {
    input.value = res.__intell_selected || '';
  });
  run.addEventListener('click', () => {
    const txt = input.value || '';
  var endpoint = 'http://localhost:8080/api/chat';
    fetch(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ text: txt }) })
      .then(r=>r.json())
      .then(j=>{ if(j && j.ok && j.result){ out.textContent = typeof j.result === 'string' ? j.result : JSON.stringify(j.result, null, 2); return } if(j && j.ok && j.result_text){ out.textContent = j.result_text; return } out.textContent = JSON.stringify(j, null, 2); })
      .catch(err=>{ out.textContent = String(err); });
  });
});
