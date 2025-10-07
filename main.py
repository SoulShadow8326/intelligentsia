from http.server import SimpleHTTPRequestHandler, HTTPServer
import os
from template import render_template

PORT = 8080
WEBROOT = os.path.join(os.path.dirname(__file__), 'frontend')

class Handler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        if path == '/' or path.startswith('/index.html'):
            return os.path.join(WEBROOT, 'index.html')
        return os.path.join(WEBROOT, path.lstrip('/'))

    def do_GET(self):
        if self.path == '/' or self.path.startswith('/index.html'):
            index_path = os.path.join(WEBROOT, 'index.html')
            header_path = os.path.join(WEBROOT, 'components', 'header.html')
            with open(header_path, 'r', encoding='utf-8') as f:
                header_html = f.read()
            rendered = render_template(index_path, {'header': header_html})
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
            rendered = render_template(news_path, {'header': header_html})
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
            rendered = render_template(contact_path, {'header': header_html})
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
            rendered = render_template(about_path, {'header': header_html})
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
            rendered = render_template(donate_path, {'header': header_html})
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
        if self.path == '/upload-id':
            import cgi
            import uuid
            import json

            content_type = self.headers.get('Content-Type', '')
            if 'multipart/form-data' not in content_type:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(b'{"ok":false,"error":"Expected multipart/form-data"}')
                return

            fs = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD':'POST'}, keep_blank_values=True)
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

            uploads_dir = os.path.join(WEBROOT, 'uploads')
            os.makedirs(uploads_dir, exist_ok=True)
            filename = str(uuid.uuid4()) + '_' + os.path.basename(fileitem.filename)
            save_path = os.path.join(uploads_dir, filename)
            with open(save_path, 'wb') as out:
                data = fileitem.file.read()
                out.write(data)

            try:
                from qrscan import compare_images
                match = compare_images(save_path)
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                payload = json.dumps({"ok": False, "error": str(e)})
                self.wfile.write(payload.encode('utf-8'))
                try:
                    os.remove(save_path)
                except Exception:
                    pass
                return

            try:
                os.remove(save_path)
            except Exception:
                pass

            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            payload = json.dumps({"ok": True, "match": bool(match)})
            self.wfile.write(payload.encode('utf-8'))
            return
        else:
            return SimpleHTTPRequestHandler.do_POST(self)

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
