document.addEventListener('DOMContentLoaded', function () {
    const tiers = document.querySelectorAll('.tiers .tier');
    const amountInput = document.getElementById('amount');

    function clearActive() {
        tiers.forEach(t => t.classList.remove('active'));
    }

    const selectedAmountEl = document.getElementById('selectedAmount');

    tiers.forEach(t => {
        t.setAttribute('tabindex', '0');
        t.addEventListener('click', function () {
            clearActive();
            t.classList.add('active');
            const val = t.getAttribute('data-value');
            if (!amountInput) return;
            amountInput.value = val === 'other' ? 'Other' : val;
            if (selectedAmountEl) selectedAmountEl.textContent = (val === 'other' ? 'Other' : val + ' ObsessTokens');
        });
        t.addEventListener('keydown', function (e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                t.click();
            }
        });
    });

    if (amountInput) {
        amountInput.addEventListener('change', function () {
            clearActive();
            const v = amountInput.value;
            const chosen = Array.from(tiers).find(t => t.getAttribute('data-value') === (v === 'Other' ? 'other' : v));
            chosen && chosen.classList.add('active');
            if (selectedAmountEl) selectedAmountEl.textContent = (v === 'Other' ? 'Other' : v + ' ObsessTokens');
        });
    }

    if (amountInput && selectedAmountEl) {
        const v = amountInput.value;
        selectedAmountEl.textContent = (v === 'Other' ? 'Other' : v + ' ObsessTokens');
    }

    const donateBtn = document.querySelector('.donate-cta');
    donateBtn && donateBtn.addEventListener('click', function (e) {
        e.preventDefault();
        window.location.href = '/checkout';
    });
});
