document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('input');
  const out = document.getElementById('output');
  const run = document.getElementById('run');
  const specEl = document.getElementById('spec');
  const endpointEl = document.getElementById('endpoint');
  chrome.storage.local.get('__intell_selected', (res) => {
    input.value = res.__intell_selected || '';
  });
  run.addEventListener('click', () => {
    const txt = input.value || '';
    var spec = { mode: 'local', action: 'reverse' };
    try{ spec = JSON.parse(specEl.value || JSON.stringify(spec)); }catch(e){ spec = { mode: 'local', action: 'reverse' }; }
    if(spec.mode === 'llm' || (spec.mode === 'auto' && (endpointEl.value || spec.endpoint))){
      var endpoint = endpointEl.value || spec.endpoint || 'https://intelligentsia.site/api/decipher';
      fetch(endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ text: txt, spec: spec }) })
        .then(r=>r.json())
        .then(j=>{
          if(j && j.ok && j.result){ out.textContent = typeof j.result === 'string' ? j.result : JSON.stringify(j.result, null, 2); return }
          if(j && j.ok && j.result_text){ out.textContent = j.result_text; return }
          out.textContent = JSON.stringify(j, null, 2);
        })
        .catch(err=>{ out.textContent = String(err); });
      return;
    }
    var result = '';
    var act = (spec.action || '').toString().toLowerCase();
    if(act === 'reverse') result = txt.split('').reverse().join('');
    else if(act === 'rot13') result = txt.replace(/[a-zA-Z]/g,function(c){ var d=c.charCodeAt(0); var base=(d<97?65:97); return String.fromCharCode(((d-base+13)%26)+base); });
    else if(act === 'base64') try{ result = atob(txt); }catch(e){ result = 'Invalid base64'; }
    else if(act === 'hex') try{ result = txt.replace(/\s+/g,'').match(/.{1,2}/g).map(b=>String.fromCharCode(parseInt(b,16))).join(''); }catch(e){ result='Invalid hex'; }
    else if(act === 'caesar'){ var shift = parseInt(spec.shift||3,10)||3; result = txt.replace(/[a-z]/gi,function(c){ var d=c.charCodeAt(0); var base=(d<97?65:97); return String.fromCharCode(((d-base-shift+26)%26)+base); }); }
    else result = txt;
    out.textContent = result;
  });
});
