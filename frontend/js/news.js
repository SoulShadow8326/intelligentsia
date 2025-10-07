document.addEventListener('DOMContentLoaded', function () {
    fetch('assets/news.json')
        .then(function (r) { return r.json(); })
        .then(function (data) {
            var container = document.getElementById('news-list');
            data.forEach(function (item) {
                var el = document.createElement('div');
                el.className = 'news-item';
                el.innerHTML = '<a href ="article.html?slug=' + item.slug + '"> <div class="log - date">Log: ' + item.date + '</div>' +
                    '<div class="log-body"><strong>' + escapeHtml(item.title) + '</strong><br/>' + escapeHtml(item.body) + '</div> </a>';
                container.appendChild(el);
            });
        });

    function escapeHtml(s) {
        return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }
});
