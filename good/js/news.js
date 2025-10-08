document.addEventListener('DOMContentLoaded', function () {
    fetch('assets/news.json')
        .then(function (r) { return r.json(); })
        .then(function (data) {
            var container = document.getElementById('news-list');
            data.forEach(function (item) {
                var el = document.createElement('div');
                el.className = 'news-item';
                el.innerHTML = '<div class="logdate">Log: ' + item.date + '</div>' +
                    '<div class="log-body"><strong>' + '<a href ="article.html?slug=' + item.slug + '">' + escapeHtml(item.title) + '</a></strong><br/>' + escapeHtml(item.body) + '</div> ';
                container.appendChild(el);
            });
        });

    function escapeHtml(s) {
        return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    }
});
