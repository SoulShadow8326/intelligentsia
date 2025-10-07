const params = new URLSearchParams(window.location.search);
const slug = decodeURIComponent(params.get('slug'));
console.log(slug)

if (!slug) {
    document.body.innerHTML = "<h2>No article specified.</h2>";
} else {
    fetch('/assets/news.json')
        .then(res => res.json())
        .then(data => {
            const article = data.find(a => a.slug.trim() === slug.trim());
            if (!article) {
                document.body.innerHTML = "<h2>Article not found.</h2>";
                return;
            }

            document.title = `${article.title} | Intelligentsia`;
            document.getElementById('article-title').textContent = article.title;
            document.getElementById('article-date').textContent = article.date;
            document.getElementById('article-body').innerHTML = article.bb;
        })
        .catch(() => {
            document.body.innerHTML = "<h2>Error loading article.</h2>";
        });
}
