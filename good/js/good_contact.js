document.addEventListener('DOMContentLoaded', function () {
	const openBtn = document.getElementById('openReport');
	const modal = document.getElementById('reportModal');
	const closeBtn = document.getElementById('closeReport');
	const cancelBtn = document.getElementById('cancelReport');
	const backdrop = document.getElementById('modalBackdrop');
	const form = document.getElementById('reportForm');

	function showModal() {
		modal.classList.add('show');
		modal.setAttribute('aria-hidden', 'false');
	}

	function hideModal() {
		modal.classList.remove('show');
		modal.setAttribute('aria-hidden', 'true');
	}

	openBtn && openBtn.addEventListener('click', showModal);
	closeBtn && closeBtn.addEventListener('click', hideModal);
	cancelBtn && cancelBtn.addEventListener('click', hideModal);
	backdrop && backdrop.addEventListener('click', hideModal);

	form && form.addEventListener('submit', async function (e) {
		e.preventDefault();
		const data = new FormData(form);

		try {
			const resp = await fetch('/good/report', {
				method: 'POST',
				body: data
			});

			if (resp.ok) {
				hideModal();
				alert('Report submitted. Thank you.');
			} else {
				alert('Failed to submit report.');
			}
		} catch (err) {
			console.error(err);
			alert('Network error while submitting report.');
		}
	});
});
