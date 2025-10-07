from http.server import SimpleHTTPRequestHandler, HTTPServer
import os
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
        else:
            return SimpleHTTPRequestHandler.do_GET(self)

    def do_POST(self):
        if self.path != '/upload-id':
            return super().do_POST()

        import io, uuid, json

        content_type = self.headers.get('Content-Type', '')
        if 'multipart/form-data' not in content_type:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"ok":false,"error":"Expected multipart/form-data"}')
            return

        # Extract boundary
        boundary = None
        for part in content_type.split(';'):
            part = part.strip()
            if part.startswith('boundary='):
                boundary = part.split('=', 1)[1]
                break
        if not boundary:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"ok":false,"error":"No boundary found"}')
            return

        boundary_bytes = ('--' + boundary).encode('utf-8')
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        parts = body.split(boundary_bytes)
        
        file_data = None
        filename = None

        for part in parts:
            if not part or part in (b'--', b'--\r\n'):
                continue
            headers_body = part.strip(b'\r\n').split(b'\r\n\r\n', 1)
            if len(headers_body) != 2:
                continue
            headers, data = headers_body
            header_lines = headers.split(b'\r\n')
            for hl in header_lines:
                hl_dec = hl.decode('utf-8', errors='ignore').lower()
                if hl_dec.startswith('content-disposition:'):
                    if b'name="file"' in hl:
                        filename = None
                        for seg in hl.decode().split(';'):
                            seg = seg.strip()
                            if seg.startswith('filename='):
                                filename = seg.split('=',1)[1].strip('"')
                        if filename:
                            file_data = data.rstrip(b'\r\n')
                            break
            if file_data:
                break

        if not file_data or not filename:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"ok":false,"error":"No file uploaded"}')
            return

        uploads_dir = os.path.join(WEBROOT, 'uploads')
        os.makedirs(uploads_dir, exist_ok=True)
        save_name = f"{uuid.uuid4()}_{os.path.basename(filename)}"
        save_path = os.path.join(uploads_dir, save_name)
        
        with open(save_path, 'wb') as f:
            f.write(file_data)

        try:
            from qrscan import compare_images
            match = compare_images(save_path)
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"ok": False, "error": str(e)}).encode())
            try: os.remove(save_path)
            except Exception: pass
            return

        try: os.remove(save_path)
        except Exception: pass

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({"ok": True, "match": bool(match)}).encode())


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
    with HTTPServer(('', PORT), Handler) as httpd:
        print(f'Serving on port {PORT}')
        httpd.serve_forever()
