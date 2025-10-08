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
    const donateModal = document.getElementById('donate-modal');
    const cancelUpload = document.getElementById('cancel-upload');
    const confirmUpload = document.getElementById('confirm-upload');
    const idUpload = document.getElementById('id-upload');
    const fileName = document.getElementById('file-name');
    const messageOverlay = document.getElementById('donate-message');
    const messageOk = document.getElementById('message-ok');

    donateBtn && donateBtn.addEventListener('click', function (e) {
        e.preventDefault();
        if (donateModal) donateModal.style.display = 'block';
    });

    cancelUpload && cancelUpload.addEventListener('click', function (e) {
        e.preventDefault();
        if (donateModal) donateModal.style.display = 'none';
    });

    idUpload && idUpload.addEventListener('change', function () {
        if (idUpload.files && idUpload.files.length) {
            fileName && (fileName.textContent = idUpload.files[0].name);
        } else {
            fileName && (fileName.textContent = 'No file selected');
        }
    });

    confirmUpload && confirmUpload.addEventListener('click', function (e) {
        e.preventDefault();
        if (donateModal) donateModal.style.display = 'none';
        if (messageOverlay) {
            const msg = document.getElementById('message-text');
            if (msg) msg.textContent = 'Upload received. Thank you.';
            messageOverlay.setAttribute('aria-hidden', 'false');
            messageOverlay.style.display = 'flex';
        }
    });

    messageOk && messageOk.addEventListener('click', function () {
        if (messageOverlay) {
            messageOverlay.setAttribute('aria-hidden', 'true');
            messageOverlay.style.display = 'none';
        }
    });
});
