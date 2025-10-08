document.addEventListener('DOMContentLoaded', function () {
    fetch('assets/news.json')
        .then(function (r) { return r.json(); })
        .then(function (data) {
            var container = document.getElementById('news-list');
            data.forEach(function (item) {
                var el = document.createElement('div');
                el.className = 'news-item';
                el.innerHTML =
                    '<div class="log-body"><strong>' + '<a href ="article.html?slug=' + item.slug + '">' + escapeHtml(item.title) + '</a></strong><br/>' + '<div class="logdate">' + item.date + '</div>' + escapeHtml(item.body) + '</div> ';
                container.appendChild(el);
            });
        });

    function escapeHtml(s) {
        return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }
});
