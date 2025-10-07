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

if __name__ == '__main__':
    os.chdir(WEBROOT)
    with HTTPServer(('', PORT), Handler) as httpd:
        print(f'Serving on port {PORT}')
        httpd.serve_forever()
