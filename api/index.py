import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse, Response
from template import render_template

app = FastAPI()
ROOT = os.getcwd()
WEBROOT = os.path.join(ROOT, 'frontend')
GOODROOT = os.path.join(ROOT, 'good')


def _read_header():
    header_path = os.path.join(WEBROOT, 'components', 'header.html')
    header_html = ''
    if os.path.exists(header_path):
        with open(header_path, 'r', encoding='utf-8') as f:
            header_html = f.read()
    good_header_path = os.path.join(GOODROOT, 'components', 'header.html')
    good_header_html = ''
    if os.path.exists(good_header_path):
        with open(good_header_path, 'r', encoding='utf-8') as gf:
            good_header_html = gf.read()
    return header_html, good_header_html


def _safe_path(base, rel):
    p = os.path.normpath(os.path.join(base, rel.lstrip('/')))
    try:
        if os.path.commonpath([base, p]) != base:
            return None
    except Exception:
        return None
    return p


@app.get('/', response_class=HTMLResponse)
async def root(request: Request):
    index_path = os.path.join(WEBROOT, 'index.html')
    header_html, good_header_html = _read_header()
    rendered = render_template(index_path, {'header': header_html, 'goodheader': good_header_html})
    return HTMLResponse(rendered)


@app.get('/{full_path:path}')
async def catch_all(request: Request, full_path: str):
    if not full_path:
        return await root(request)

    # try good folder first if path starts with good/
    if full_path.startswith('good/'):
        rel = full_path[len('good/'):]
        candidate = _safe_path(GOODROOT, rel)
        if candidate and os.path.exists(candidate):
            if candidate.endswith('.html'):
                header_html, good_header_html = _read_header()
                rendered = render_template(candidate, {'header': header_html, 'goodheader': good_header_html})
                return HTMLResponse(rendered)
            return FileResponse(candidate)

    # try frontend path
    candidate = _safe_path(WEBROOT, full_path)
    if candidate and os.path.exists(candidate):
        if candidate.endswith('.html'):
            header_html, good_header_html = _read_header()
            rendered = render_template(candidate, {'header': header_html, 'goodheader': good_header_html})
            return HTMLResponse(rendered)
        return FileResponse(candidate)

    # fallback to index.html rendering
    index_path = os.path.join(WEBROOT, 'index.html')
    if os.path.exists(index_path):
        header_html, good_header_html = _read_header()
        rendered = render_template(index_path, {'header': header_html, 'goodheader': good_header_html})
        return HTMLResponse(rendered)

    return Response('Not found', status_code=404)
