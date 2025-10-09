from http.server import SimpleHTTPRequestHandler, HTTPServer
import os
import json
import cgi
import traceback
from template import render_template

PORT = 8080
WEBROOT = os.path.join(os.path.dirname(__file__), 'frontend')
GOODROOT = os.path.join(os.path.dirname(__file__), 'good')

class Handler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        if path == '/' or path.startswith('/index.html'):
            return os.path.join(WEBROOT, 'index.html')
        if path.startswith('/good/'):
            rel = path[len('/good/'):]
            return os.path.join(GOODROOT, rel.lstrip('/'))
        return os.path.join(WEBROOT, path.lstrip('/'))

    def do_GET(self):
        if self.path == '/' or self.path.startswith('/index.html'):
            index_path = os.path.join(WEBROOT, 'index.html')
            header_path = os.path.join(WEBROOT, 'components', 'header.html')
            with open(header_path, 'r', encoding='utf-8') as f:
                header_html = f.read()
            good_header_path = os.path.join(WEBROOT, 'good', 'components', 'header.html')
            good_header_html = ''
            if os.path.exists(good_header_path):
                with open(good_header_path, 'r', encoding='utf-8') as gf:
                    good_header_html = gf.read()
            rendered = render_template(index_path, {'header': header_html, 'goodheader': good_header_html})
            encoded = rendered.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)
            return
        if self.path == '/news' or self.path.startswith('/news.html'):
            news_path = os.path.join(WEBROOT, 'news.html')
            header_path = os.path.join(WEBROOT, 'components', 'header.html')
            with open(header_path, 'r', encoding='utf-8') as f:
                header_html = f.read()
            good_header_path = os.path.join(WEBROOT, 'good', 'components', 'header.html')
            good_header_html = ''
            if os.path.exists(good_header_path):
                with open(good_header_path, 'r', encoding='utf-8') as gf:
                    good_header_html = gf.read()
            rendered = render_template(news_path, {'header': header_html, 'goodheader': good_header_html})
            encoded = rendered.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)
            return
        if self.path == '/good/contact' or self.path.startswith('/good/good_contact.html'):
            good_path = os.path.join(GOODROOT, 'good_contact.html')
            header_path = os.path.join(WEBROOT, 'components', 'header.html')
            if not self.GoodPersonChecker():
                self.send_response(302)
                self.send_header('Location', '/')
                self.end_headers()
                return
            with open(header_path, 'r', encoding='utf-8') as f:
                header_html = f.read()
            good_header_path = os.path.join(GOODROOT, 'components', 'header.html')
            good_header_html = ''
            if os.path.exists(good_header_path):
                with open(good_header_path, 'r', encoding='utf-8') as gf:
                    good_header_html = gf.read()
            rendered = render_template(good_path, {'header': header_html, 'goodheader': good_header_html})
            encoded = rendered.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)
            return
        if self.path == '/contact' or self.path.startswith('/contact.html'):
            contact_path = os.path.join(WEBROOT, 'contact.html')
            header_path = os.path.join(WEBROOT, 'components', 'header.html')
            with open(header_path, 'r', encoding='utf-8') as f:
                header_html = f.read()
            good_header_path = os.path.join(WEBROOT, 'good', 'components', 'header.html')
            good_header_html = ''
            if os.path.exists(good_header_path):
                with open(good_header_path, 'r', encoding='utf-8') as gf:
                    good_header_html = gf.read()
            rendered = render_template(contact_path, {'header': header_html, 'goodheader': good_header_html})
            encoded = rendered.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)
            return
        if self.path == '/about' or self.path.startswith('/about.html'):
            about_path = os.path.join(WEBROOT, 'about.html')
            header_path = os.path.join(WEBROOT, 'components', 'header.html')
            with open(header_path, 'r', encoding='utf-8') as f:
                header_html = f.read()
            good_header_path = os.path.join(WEBROOT, 'good', 'components', 'header.html')
            good_header_html = ''
            if os.path.exists(good_header_path):
                with open(good_header_path, 'r', encoding='utf-8') as gf:
                    good_header_html = gf.read()
            rendered = render_template(about_path, {'header': header_html, 'goodheader': good_header_html})
            encoded = rendered.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)
            return
        if self.path == '/donate' or self.path.startswith('/donate.html'):
            donate_path = os.path.join(WEBROOT, 'donate.html')
            header_path = os.path.join(WEBROOT, 'components', 'header.html')
            with open(header_path, 'r', encoding='utf-8') as f:
                header_html = f.read()
            good_header_path = os.path.join(WEBROOT, 'good', 'components', 'header.html')
            good_header_html = ''
            if os.path.exists(good_header_path):
                with open(good_header_path, 'r', encoding='utf-8') as gf:
                    good_header_html = gf.read()
            rendered = render_template(donate_path, {'header': header_html, 'goodheader': good_header_html})
            encoded = rendered.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)
            return
        if self.path == '/checkout' or self.path.startswith('/checkout.html'):
            checkout_path = os.path.join(WEBROOT, 'checkout.html')
            header_path = os.path.join(WEBROOT, 'components', 'header.html')
            with open(header_path, 'r', encoding='utf-8') as f:
                header_html = f.read()
            good_header_path = os.path.join(WEBROOT, 'good', 'components', 'header.html')
            good_header_html = ''
            if os.path.exists(good_header_path):
                with open(good_header_path, 'r', encoding='utf-8') as gf:
                    good_header_html = gf.read()
            rendered = render_template(checkout_path, {'header': header_html, 'goodheader': good_header_html})
            encoded = rendered.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)
            return
        if self.path == '/good/home' or self.path.startswith('/good/home.html'):
            good_path = os.path.join(GOODROOT, 'good.html')
            header_path = os.path.join(WEBROOT, 'components', 'header.html')
            if not self.GoodPersonChecker():
                self.send_response(302)
                self.send_header('Location', '/')
                self.end_headers()
                return
            with open(header_path, 'r', encoding='utf-8') as f:
                header_html = f.read()
            good_header_path = os.path.join(GOODROOT, 'components', 'header.html')
            good_header_html = ''
            if os.path.exists(good_header_path):
                with open(good_header_path, 'r', encoding='utf-8') as gf:
                    good_header_html = gf.read()
            rendered = render_template(good_path, {'header': header_html, 'goodheader': good_header_html})
            encoded = rendered.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)
            return
        if self.path == '/good/about' or self.path.startswith('/good/good_about.html'):
            good_about_path = os.path.join(GOODROOT, 'good_about.html')
            header_path = os.path.join(WEBROOT, 'components', 'header.html')
            if not self.GoodPersonChecker():
                self.send_response(302)
                self.send_header('Location', '/')
                self.end_headers()
                return
            with open(header_path, 'r', encoding='utf-8') as f:
                header_html = f.read()
            good_header_path = os.path.join(GOODROOT, 'components', 'header.html')
            good_header_html = ''
            if os.path.exists(good_header_path):
                with open(good_header_path, 'r', encoding='utf-8') as gf:
                    good_header_html = gf.read()
            rendered = render_template(good_about_path, {'header': header_html, 'goodheader': good_header_html})
            encoded = rendered.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)
            return
        if self.path == '/good/news' or self.path.startswith('/good/good_news.html'):
            good_news_path = os.path.join(GOODROOT, 'good_news.html')
            header_path = os.path.join(WEBROOT, 'components', 'header.html')
            if not self.GoodPersonChecker():
                self.send_response(302)
                self.send_header('Location', '/')
                self.end_headers()
                return
            with open(header_path, 'r', encoding='utf-8') as f:
                header_html = f.read()
            good_header_path = os.path.join(GOODROOT, 'components', 'header.html')
            good_header_html = ''
            if os.path.exists(good_header_path):
                with open(good_header_path, 'r', encoding='utf-8') as gf:
                    good_header_html = gf.read()
            rendered = render_template(good_news_path, {'header': header_html, 'goodheader': good_header_html})
            encoded = rendered.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)
            return
        if self.path == '/good/chat' or self.path.startswith('/good/chat.html'):
            good_chat_path = os.path.join(GOODROOT, 'chat.html')
            header_path = os.path.join(WEBROOT, 'components', 'header.html')
            if not self.GoodPersonChecker():
                self.send_response(302)
                self.send_header('Location', '/')
                self.end_headers()
                return
            with open(header_path, 'r', encoding='utf-8') as f:
                header_html = f.read()
            good_header_path = os.path.join(GOODROOT, 'components', 'header.html')
            good_header_html = ''
            if os.path.exists(good_header_path):
                with open(good_header_path, 'r', encoding='utf-8') as gf:
                    good_header_html = gf.read()
            rendered = render_template(good_chat_path, {'header': header_html, 'goodheader': good_header_html})
            encoded = rendered.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)
            return
        if self.path == '/article' or self.path.startswith('/article.html'):
            article_path = os.path.join(WEBROOT, 'article.html')
            header_path = os.path.join(WEBROOT, 'components', 'header.html')
            with open(header_path, 'r', encoding='utf-8') as f:
                header_html = f.read()
            rendered = render_template(article_path, {'header': header_html})
            encoded = rendered.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)
            return
        if self.path == '/good/article' or self.path.startswith('/good/article.html'):
            article_path = os.path.join(GOODROOT, 'article.html')
            header_path = os.path.join(GOODROOT, 'components', 'header.html')
            with open(header_path, 'r', encoding='utf-8') as f:
                header_html = f.read()
            rendered = render_template(article_path, {'header': header_html})
            encoded = rendered.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.send_header('Content-Length', str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)
            return
        else:
            return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if self.path == '/api/decipher':
            length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(length) if length else b''
            try:
                payload = json.loads(body.decode('utf-8') if body else '{}')
            except Exception:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                self.end_headers()
                self.wfile.write(b'{"ok":false,"error":"invalid json"}')
                return
            text = payload.get('text', '')
            spec = payload.get('spec', {})
            base = os.path.dirname(__file__)
            data_dir = os.path.join(base, 'data')
            try:
                with open(os.path.join(base, 'system_prompt.json'), 'r', encoding='utf-8') as f:
                    system_prompt = json.load(f).get('prompt', '')
            except Exception:
                system_prompt = ''
            files = []
            for fn in os.listdir(data_dir) if os.path.exists(data_dir) else []:
                p = os.path.join(data_dir, fn)
                if not os.path.isfile(p):
                    continue
                try:
                    with open(p, 'r', encoding='utf-8') as f:
                        j = json.load(f)
                except Exception:
                    continue
                files.append({'filename': fn, 'content': j})
            contents = system_prompt + "\n\nText:\n" + text + "\n\nSpec:\n" + json.dumps(spec)
            try:
                from google import genai
                client = genai.Client()
                resp = client.models.generate_content(model='gemini-2.5-flash', contents=contents)
                out = getattr(resp, 'text', None) or (resp if isinstance(resp, str) else str(resp))
                try:
                    out_json = json.loads(out)
                    if isinstance(out_json, dict) and out_json.get('decoded'):
                        result_text = out_json.get('decoded')
                    else:
                        result_text = json.dumps(out_json)
                    resp_body = json.dumps({'ok': True, 'result_text': result_text}).encode('utf-8')
                except Exception:
                    resp_body = json.dumps({'ok': True, 'result_text': out}).encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(resp_body)))
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                self.end_headers()
                self.wfile.write(resp_body)
            except Exception:
                try:
                    glossary_path = os.path.join(base, 'data', 'glossary.json')
                    glossary = []
                    if os.path.exists(glossary_path):
                        with open(glossary_path, 'r', encoding='utf-8') as gf:
                            glossary = json.load(gf)
                    text_l = text.lower()
                    flags = []
                    matches = []
                    for g in glossary:
                        term = g.get('term', '')
                        aliases = g.get('aliases', []) or []
                        check = [term] + aliases
                        for a in check:
                            if a and a.lower() in text_l:
                                flags.append(a)
                                matches.append({'term': term, 'matched': a})
                    decoded = ('Flags detected: ' + ', '.join(sorted(set(flags))) + '.') if flags else 'No clear flags detected.'
                    result_text = decoded
                    resp_body = json.dumps({'ok': True, 'result_text': result_text}).encode('utf-8')
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Content-Length', str(len(resp_body)))
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                    self.end_headers()
                    self.wfile.write(resp_body)
                except Exception as e:
                    self.send_response(500)
                    self.send_header('Content-Type', 'application/json')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.send_header('Access-Control-Allow-Headers', 'Content-Type')
                    self.end_headers()
                    self.wfile.write(json.dumps({'ok': False, 'error': str(e)}).encode('utf-8'))
            return

        if self.path == '/upload-id':
            try:
                content_type = self.headers.get('Content-Type', '')
                if 'multipart/form-data' not in content_type:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(b'{"ok":false,"error":"Expected multipart/form-data"}')
                    return
                content_length = int(self.headers.get('Content-Length', 0))
                fs = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD':'POST','CONTENT_TYPE':content_type,'CONTENT_LENGTH':str(content_length)})
                if 'file' not in fs:
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(b'{"ok":false,"error":"No file uploaded"}')
                    return
                fileitem = fs['file']
                if not getattr(fileitem, 'filename', None):
                    self.send_response(400)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(b'{"ok":false,"error":"No file uploaded"}')
                    return
                import uuid
                filename = os.path.basename(fileitem.filename)
                file_data = fileitem.file.read()
                uploads_dir = os.path.join(WEBROOT, 'uploads')
                os.makedirs(uploads_dir, exist_ok=True)
                save_name = f"{uuid.uuid4()}_{filename}"
                save_path = os.path.join(uploads_dir, save_name)
                with open(save_path, 'wb') as f:
                    f.write(file_data)
                try:
                    from qrscan import compare_images
                    match = compare_images(save_path)
                except Exception as e:
                    try:
                        os.remove(save_path)
                    except Exception:
                        pass
                    self.send_response(500)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({"ok": False, "error": str(e)}).encode())
                    return
                try:
                    os.remove(save_path)
                except Exception:
                    pass
                resp = json.dumps({"ok": True, "match": bool(match)}).encode('utf-8')
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', str(len(resp)))
                self.end_headers()
                self.wfile.write(resp)
                return
            except Exception as e:
                try:
                    self.send_response(500)
                    self.send_header('Content-Type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'ok': False, 'error': str(e)}).encode('utf-8'))
                except Exception:
                    pass
                traceback.print_exc()
                return
        else:
            return super().do_POST()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()


    def GoodPersonChecker(self):
        cookie = self.headers.get('Cookie', '')
        parts = [p.strip() for p in cookie.split(';') if p.strip()]
        for p in parts:
            if p.startswith('IsEvil='):
                val = p.split('=', 1)[1]
                return val == '1'
        return False

if __name__ == '__main__':
    os.chdir(WEBROOT)
    with HTTPServer(('0.0.0.0', PORT), Handler) as httpd:
        print(f'Serving on port {PORT}')
        httpd.serve_forever()
