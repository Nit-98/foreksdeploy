from http.server import BaseHTTPRequestHandler, HTTPServer

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Hello from Kubernetes! Jenkins and Amazon ECR deployment is working.")

server = HTTPServer(("0.0.0.0", 8000), Handler)
print("Application running on port 8000", flush=True)
server.serve_forever()
EOF

