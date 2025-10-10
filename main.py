from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, PlainTextResponse, JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import json
import traceback
import importlib.util
import urllib.request
from template import render_template

_GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
if _GEMINI_API_KEY:
    os.environ['GEMINI_API_KEY'] = _GEMINI_API_KEY

try:
    base = os.path.dirname(__file__)
    env_path = os.path.join(base, '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as ef:
            for line in ef:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' in line:
                    k, v = line.split('=', 1)
                    os.environ.setdefault(k.strip(), v.strip())
except Exception:
    pass

PORT = int(os.environ.get('PORT', 8000))
WEBROOT = os.path.join(os.path.dirname(__file__), 'frontend')
GOODROOT = os.path.join(os.path.dirname(__file__), 'good')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount('/assets', StaticFiles(directory=os.path.join(WEBROOT, 'assets')), name='assets')
app.mount('/css', StaticFiles(directory=os.path.join(WEBROOT, 'css')), name='css')
app.mount('/js', StaticFiles(directory=os.path.join(WEBROOT, 'js')), name='js')
app.mount('/fonts', StaticFiles(directory=os.path.join(WEBROOT, 'fonts')), name='fonts')

def _load_system_prompt():
    base = os.path.dirname(__file__)
    try:
        with open(os.path.join(base, 'system_prompt.json'), 'r', encoding='utf-8') as f:
            return json.load(f).get('prompt', '')
    except Exception:
        return ''

def _render(path, context=None):
    context = context or {}
    if os.path.exists(path):
        try:
            return render_template(path, context)
        except Exception:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
    return ''

@app.get('/', response_class=HTMLResponse)
def index():
    index_path = os.path.join(WEBROOT, 'index.html')
    header_path = os.path.join(WEBROOT, 'components', 'header.html')
    header_html = ''
    if os.path.exists(header_path):
        with open(header_path, 'r', encoding='utf-8') as f:
            header_html = f.read()
    good_header_path = os.path.join(WEBROOT, 'good', 'components', 'header.html')
    good_header_html = ''
    if os.path.exists(good_header_path):
        with open(good_header_path, 'r', encoding='utf-8') as gf:
            good_header_html = gf.read()
    rendered = _render(index_path, {'header': header_html, 'goodheader': good_header_html})
    return HTMLResponse(content=rendered, status_code=200)

def _render_generic(page_rel):
    path = os.path.join(WEBROOT, page_rel)
    if os.path.exists(path):
        header_path = os.path.join(WEBROOT, 'components', 'header.html')
        header_html = ''
        if os.path.exists(header_path):
            with open(header_path, 'r', encoding='utf-8') as f:
                header_html = f.read()
        good_header_path = os.path.join(WEBROOT, 'good', 'components', 'header.html')
        good_header_html = ''
        if os.path.exists(good_header_path):
            with open(good_header_path, 'r', encoding='utf-8') as gf:
                good_header_html = gf.read()
        rendered = _render(path, {'header': header_html, 'goodheader': good_header_html})
        return HTMLResponse(content=rendered, status_code=200)
    return Response(status_code=404)

@app.get('/news', response_class=HTMLResponse)
def news():
    return _render_generic('news.html')

@app.get('/contact', response_class=HTMLResponse)
def contact():
    return _render_generic('contact.html')

@app.get('/about', response_class=HTMLResponse)
def about():
    return _render_generic('about.html')

@app.get('/donate', response_class=HTMLResponse)
def donate():
    return _render_generic('donate.html')

@app.get('/checkout', response_class=HTMLResponse)
def checkout():
    return _render_generic('checkout.html')

@app.get('/article', response_class=HTMLResponse)
def article():
    return _render_generic('article.html')

def _good_person_checker(request: Request):
    cookie = request.headers.get('cookie', '')
    parts = [p.strip() for p in cookie.split(';') if p.strip()]
    for p in parts:
        if p.startswith('IsEvil='):
            val = p.split('=', 1)[1]
            return val == '1'
    return False

@app.get('/good/chat', response_class=HTMLResponse)
def good_chat(request: Request):
    if not _good_person_checker(request):
        return Response(status_code=302, headers={'Location': '/'})
    good_chat_path = os.path.join(GOODROOT, 'chat.html')
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
    gemini_key = os.environ.get('GEMINI_API_KEY', '')
    rendered = _render(good_chat_path, {'header': header_html, 'goodheader': good_header_html, 'gemini_key': gemini_key})
    return HTMLResponse(content=rendered, status_code=200)


@app.get('/good/home', response_class=HTMLResponse)
def good_home(request: Request):
    if not _good_person_checker(request):
        return Response(status_code=302, headers={'Location': '/'})
    good_home_path = os.path.join(GOODROOT, 'good.html')
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
    rendered = _render(good_home_path, {'header': header_html, 'goodheader': good_header_html})
    return HTMLResponse(content=rendered, status_code=200)


@app.get('/good/news', response_class=HTMLResponse)
def good_news(request: Request):
    if not _good_person_checker(request):
        return Response(status_code=302, headers={'Location': '/'})
    path = os.path.join(GOODROOT, 'good_news.html')
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
    rendered = _render(path, {'header': header_html, 'goodheader': good_header_html})
    return HTMLResponse(content=rendered, status_code=200)


@app.get('/good/contact', response_class=HTMLResponse)
def good_contact(request: Request):
    if not _good_person_checker(request):
        return Response(status_code=302, headers={'Location': '/'})
    path = os.path.join(GOODROOT, 'good_contact.html')
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
    rendered = _render(path, {'header': header_html, 'goodheader': good_header_html})
    return HTMLResponse(content=rendered, status_code=200)


@app.get('/good/about', response_class=HTMLResponse)
def good_about(request: Request):
    if not _good_person_checker(request):
        return Response(status_code=302, headers={'Location': '/'})
    path = os.path.join(GOODROOT, 'good_about.html')
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
    rendered = _render(path, {'header': header_html, 'goodheader': good_header_html})
    return HTMLResponse(content=rendered, status_code=200)

@app.post('/api/decipher')
async def api_decipher(request: Request):
    try:
        payload = await request.json()
    except Exception:
        try:
            body = await request.body()
            payload = json.loads(body.decode('utf-8') if body else '{}')
        except Exception:
            return PlainTextResponse('invalid json', status_code=400)
    if not isinstance(payload, dict):
        payload = {}
    text = payload.get('text', '')
    parsed_text = None
    try:
        if isinstance(text, str):
            parsed_text = json.loads(text)
    except Exception:
        parsed_text = None
    if isinstance(parsed_text, dict) and isinstance(parsed_text.get('decoded'), str) and parsed_text.get('decoded').strip():
        reply = parsed_text.get('decoded').strip()
        return PlainTextResponse(reply, status_code=200)
    spec = payload.get('spec', {})
    system_prompt = _load_system_prompt()
    spec_summary = json.dumps(spec) if spec else ''
    contents = system_prompt + "\n\nText:\n" + text + "\n\nSpec Summary:\n" + spec_summary + "\n\nRespond in plain text only. Do not output JSON or structured data. Return only the deciphered text."
    api_key = os.environ.get('GEMINI_API_KEY', '')
    if not api_key:
        return PlainTextResponse('no GEMINI_API_KEY configured', status_code=500)
    try:
        from google import genai
        client = genai.Client()
        resp = client.models.generate_content(model='gemini-2.5-flash', contents=contents)
        out = getattr(resp, 'text', None) or (resp if isinstance(resp, str) else str(resp))
        reply = out
        return PlainTextResponse(str(reply), status_code=200)
    except Exception:
        try:
            url = 'https://gemini.googleapis.com/v1/models/gemini-2.5-flash:generateMessage'
            req_body = json.dumps({"messages":[{"content":{"text":contents}}],"temperature":0.2,"candidate_count":1}).encode('utf-8')
            req = urllib.request.Request(url, data=req_body, headers={'Content-Type':'application/json','Authorization':'Bearer '+api_key})
            with urllib.request.urlopen(req, timeout=30) as resp:
                resdata = resp.read()
                j = json.loads(resdata.decode('utf-8'))
                reply = ''
                try:
                    if j and j.get('candidates') and len(j.get('candidates'))>0:
                        candidate = j.get('candidates')[0]
                        if candidate.get('content') and len(candidate.get('content'))>0:
                            reply = candidate.get('content')[0].get('text','')
                        else:
                            reply = json.dumps(j)
                    else:
                        reply = json.dumps(j)
                except Exception:
                    reply = json.dumps(j)
                return PlainTextResponse(str(reply), status_code=200)
        except Exception as e:
            return PlainTextResponse(str(e), status_code=500)

@app.post('/upload-id')
async def upload_id(request: Request):
    try:
        content_type = request.headers.get('content-type', '')
        body = await request.body()
        api_file = os.path.join(os.path.dirname(__file__), 'api', 'upload-id.py')
        spec = importlib.util.spec_from_file_location('upload_id_api', api_file)
        upload_api_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(upload_api_module)
        app_obj = getattr(upload_api_module, 'app', None)
        if app_obj is None:
            raise Exception('FastAPI app not found')
        from fastapi.testclient import TestClient
        client = TestClient(app_obj)
        headers = {'Content-Type': content_type} if content_type else {}
        resp = client.request('POST', '/api/upload-id', content=body, headers=headers)
        return Response(content=resp.content, status_code=resp.status_code, media_type=resp.headers.get('content-type'))
    except Exception as e:
        tb = traceback.format_exc()
        try:
            headers_preview = dict(request.headers)
        except Exception:
            headers_preview = {}
        body_preview = None
        try:
            if body is not None:
                if isinstance(body, (bytes, bytearray)):
                    body_preview = f'<{len(body)} bytes> ' + (body[:2048].decode('utf-8', errors='replace') if len(body) > 0 else '')
                else:
                    s = str(body)
                    body_preview = s[:2048]
        except Exception:
            body_preview = '<unreadable body>'
        log_obj = {
            'error': str(e),
            'traceback': tb,
            'headers': headers_preview,
            'body_preview': body_preview,
        }
        print('UPLOAD_ID_ERROR:', json.dumps(log_obj, ensure_ascii=False))
        return JSONResponse({'ok': False, 'error': str(e), 'traceback': tb}, status_code=500)

@app.post('/api/chat')
async def api_chat(request: Request):
    try:
        payload = await request.json()
    except Exception:
        try:
            body = await request.body()
            payload = json.loads(body.decode('utf-8') if body else '{}')
        except Exception:
            return JSONResponse({'ok': False, 'error': 'invalid json'}, status_code=400)
    message = payload.get('message', '')
    parsed_msg = None
    try:
        if isinstance(message, str):
            parsed_msg = json.loads(message)
    except Exception:
        parsed_msg = None
    if isinstance(parsed_msg, dict):
        if isinstance(parsed_msg.get('original'), str) and parsed_msg.get('original').strip():
            message = parsed_msg.get('original').strip()
        elif isinstance(parsed_msg.get('text'), str) and parsed_msg.get('text').strip():
            message = parsed_msg.get('text').strip()
        else:
            message = ''
    system_prompt = _load_system_prompt()
    contents = system_prompt + "\n\nUser:\n" + message + "\n\nRespond in plain text only. Do not output JSON or any structured data, and do not include code fences; return only the answer text."
    api_key = os.environ.get('GEMINI_API_KEY', '')
    if not api_key:
        return JSONResponse({'ok': False, 'error': 'no GEMINI_API_KEY configured'}, status_code=500)
    try:
        from google import genai
        client = genai.Client()
        resp = client.models.generate_content(model='gemini-2.5-flash', contents=contents)
        out = getattr(resp, 'text', None) or (resp if isinstance(resp, str) else str(resp))
        reply = out
        return JSONResponse({'ok': True, 'reply': reply}, status_code=200)
    except Exception:
        try:
            url = 'https://gemini.googleapis.com/v1/models/gemini-2.5-flash:generateMessage'
            req_body = json.dumps({"messages":[{"content":{"text":contents}}],"temperature":0.2,"candidate_count":1}).encode('utf-8')
            req = urllib.request.Request(url, data=req_body, headers={'Content-Type':'application/json','Authorization':'Bearer '+api_key})
            with urllib.request.urlopen(req, timeout=30) as resp:
                resdata = resp.read()
                j = json.loads(resdata.decode('utf-8'))
                reply = ''
                try:
                    if j and j.get('candidates') and len(j.get('candidates'))>0:
                        candidate = j.get('candidates')[0]
                        if candidate.get('content') and len(candidate.get('content'))>0:
                            reply = candidate.get('content')[0].get('text','')
                        else:
                            reply = json.dumps(j)
                    else:
                        reply = json.dumps(j)
                except Exception:
                    reply = json.dumps(j)
                return JSONResponse({'ok': True, 'reply': reply}, status_code=200)
        except Exception as e:
            tb = traceback.format_exc()
            return JSONResponse({'ok': False, 'error': str(e), 'traceback': tb}, status_code=200)

@app.get('/favicon.ico')
def favicon():
    f1 = os.path.join(WEBROOT, 'favicon.ico')
    if os.path.exists(f1):
        return FileResponse(f1)
    f2 = os.path.join(GOODROOT, 'assets', 'favicon.ico')
    if os.path.exists(f2):
        return FileResponse(f2)
    return PlainTextResponse('Not Found', status_code=404)


app.mount('/good', StaticFiles(directory=GOODROOT), name='good')


@app.get('/{full_path:path}')
def catchall(full_path: str):
    p = full_path.lstrip('/')
    candidate = os.path.join(WEBROOT, p)
    if os.path.exists(candidate) and os.path.isfile(candidate):
        return FileResponse(candidate)
    candidate_good = os.path.join(GOODROOT, p)
    if os.path.exists(candidate_good) and os.path.isfile(candidate_good):
        return FileResponse(candidate_good)
    index_path = os.path.join(WEBROOT, p)
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return PlainTextResponse('Not Found', status_code=404)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
