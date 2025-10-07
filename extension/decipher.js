function readHash() {
  const h = location.hash || '';
  const m = h.match(/text=(.*)$/);
  if (m) return decodeURIComponent(m[1]);
  return '';
}

document.addEventListener('DOMContentLoaded', () => {
  const input = document.getElementById('input');
  const out = document.getElementById('output');
  const run = document.getElementById('run');
  input.value = readHash();
  run.addEventListener('click', () => {
    const txt = input.value || '';
    out.textContent = txt.split('').reverse().join('');
  });
});
