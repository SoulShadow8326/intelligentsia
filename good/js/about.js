document.addEventListener('DOMContentLoaded', function () {
    var deck = document.getElementById('deck');
    var sections = Array.from(deck.querySelectorAll('.deck-section'));
    var dots = Array.from(document.querySelectorAll('.deck-dots .dot'));

    function setActive(index) {
        dots.forEach(function (d) { d.classList.remove('active'); });
        if (dots[index]) dots[index].classList.add('active');
    }

    dots.forEach(function (dot, i) {
        dot.addEventListener('click', function () {
            sections[i].scrollIntoView({ behavior: 'smooth', block: 'start' });
            setActive(i);
        });
    });

    var observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                var idx = sections.indexOf(entry.target);
                setActive(idx);
            }
        });
    }, { root: deck, threshold: 0.5 });

    sections.forEach(function (s) { observer.observe(s); });

    setActive(0);
});
