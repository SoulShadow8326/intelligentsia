document.addEventListener('DOMContentLoaded', function () {
	const form = document.getElementById('reportForm');
	const helplineToggle = document.getElementById('helplineToggle');
	const helplinePanel = document.getElementById('helplinePanel');
	const helplineClose = document.getElementById('helplineClose');
	const recentList = document.getElementById('recentList');

	form && form.addEventListener('submit', async function (e) {
		e.preventDefault();
		const data = new FormData(form);

		try {
			const resp = await fetch('/good/report', {
				method: 'POST',
				body: data
			});

			if (resp.ok) {
					alert('Report submitted. Thank you.');
					const formData = new FormData(form);
					const title = formData.get('title') || 'Untitled';
					const li = document.createElement('li');
					li.textContent = title;
					if (recentList) {
						const empty = recentList.querySelector('.recent-empty');
						empty && empty.remove();
						recentList.insertBefore(li, recentList.firstChild);
					}
					form.reset();
			} else {
				alert('Failed to submit report.');
			}
		} catch (err) {
			console.error(err);
			alert('Network error while submitting report.');
		}
	});

		helplineToggle && helplineToggle.addEventListener('click', function () {
			const expanded = helplineToggle.getAttribute('aria-expanded') === 'true';
			helplineToggle.setAttribute('aria-expanded', expanded ? 'false' : 'true');
			if (helplinePanel) {
				helplinePanel.setAttribute('aria-hidden', expanded ? 'true' : 'false');
			}
		});

		helplineClose && helplineClose.addEventListener('click', function () {
			helplinePanel && helplinePanel.setAttribute('aria-hidden', 'true');
			helplineToggle && helplineToggle.setAttribute('aria-expanded', 'false');
		});
});
