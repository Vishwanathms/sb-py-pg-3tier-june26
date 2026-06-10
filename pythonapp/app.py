from http.server import BaseHTTPRequestHandler, HTTPServer


class HelloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"Hello from pythonapp container!\n")


if __name__ == "__main__":
    server_address = ("", 8080)
    httpd = HTTPServer(server_address, HelloHandler)
    print("Serving on port 8080...")
    httpd.serve_forever()
