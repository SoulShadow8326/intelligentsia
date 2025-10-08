document.addEventListener('DOMContentLoaded', function () {
    var paymentScreen = document.getElementById('paymentScreen');
    var cardNumber = document.getElementById('cardNumber');
    var cardName = document.getElementById('cardName');
    var cardExp = document.getElementById('cardExp');
    var cardCvc = document.getElementById('cardCvc');
    var cardNumberPreview = document.getElementById('cardNumberPreview');
    var cardNamePreview = document.getElementById('cardNamePreview');
    var cardExpPreview = document.getElementById('cardExpPreview');
    var cardCancel = document.getElementById('cardCancel');
    var cardForm = document.getElementById('cardForm');

    function formatNumber(v){
        return v.replace(/\s+/g,'').replace(/(\d{4})/g,'$1 ').trim();
    }

    if(cardNumber) cardNumber.addEventListener('input', function(){ cardNumberPreview.textContent = formatNumber(cardNumber.value || '•••• •••• •••• ••••'); });
    if(cardName) cardName.addEventListener('input', function(){ cardNamePreview.textContent = (cardName.value || 'FULL NAME').toUpperCase(); });
    if(cardExp) cardExp.addEventListener('input', function(){ cardExpPreview.textContent = cardExp.value || 'MM/YY'; });

    if(cardCancel) cardCancel.addEventListener('click', function(){ paymentScreen && paymentScreen.setAttribute('aria-hidden', 'true'); paymentScreen && paymentScreen.classList.remove('open'); });

    if(cardForm) cardForm.addEventListener('submit', function(e){
        e.preventDefault();
        var payBtn = document.getElementById('cardPay');
        if(payBtn) { payBtn.disabled = true; payBtn.textContent = 'Processing...'; }
        setTimeout(function(){
            if(payBtn){ payBtn.disabled = false; payBtn.textContent = 'Pay'; }
            paymentScreen && paymentScreen.setAttribute('aria-hidden','true');
            paymentScreen && paymentScreen.classList.remove('open');
            if (window && typeof window.showMessage === 'function') {
                try { window.showMessage('Payment successful'); } catch (e) { }
            } else {
                var modal = document.createElement('div');
                modal.className = 'message-overlay';
                modal.setAttribute('aria-hidden', 'false');
                modal.innerHTML = '<div class="message-box"><div class="message-content">Payment successful</div><div style="text-align:right;margin-top:12px;"><button class="btn primary" id="__pm_ok">OK</button></div></div>';
                document.body.appendChild(modal);
                var okBtn = document.getElementById('__pm_ok');
                if (okBtn) okBtn.addEventListener('click', function(){ modal.parentNode && modal.parentNode.removeChild(modal); });
            }
        }, 900);
    });

    window.showPayment = function(){ if(paymentScreen){ paymentScreen.classList.add('open'); paymentScreen.setAttribute('aria-hidden','false'); } };
});
