#!/usr/bin/env python3
import http.server
import socketserver
import socket

# Get local IP
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Server running at:")
    print(f"  Local: http://localhost:{PORT}/fighter_enhanced.html")
    print(f"  Network: http://{local_ip}:{PORT}/fighter_enhanced.html")
    print(f"\nAccess from your phone using the Network URL above")
    print("Press Ctrl+C to stop")
    httpd.serve_forever()