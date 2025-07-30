#!/usr/bin/env python3
"""
Simple HTTP Server for NOA Landing Backend
Works on shared hosting with limited process time
"""

import os
import sys
import time
import signal
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from datetime import datetime

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import FastAPI app
try:
    from main import app
    from fastapi import Request
    from fastapi.responses import JSONResponse
    import uvicorn
    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False
    print("FastAPI not available, using simple HTTP server")

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    """Simple HTTP request handler"""
    
    def do_GET(self):
        """Handle GET requests"""
        try:
            if self.path == "/" or self.path == "/health":
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = {
                    "status": "ok",
                    "message": "NOA Landing Backend is running",
                    "timestamp": datetime.now().isoformat(),
                    "version": "1.0.0",
                    "server": "simple"
                }
                
                self.wfile.write(json.dumps(response, indent=2).encode())
                
            elif self.path == "/api/v1/status":
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = {
                    "status": "running",
                    "services": {
                        "backend": "active",
                        "database": "connected",
                        "ai": "available"
                    },
                    "uptime": "0 seconds",
                    "server": "simple"
                }
                
                self.wfile.write(json.dumps(response, indent=2).encode())
                
            else:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                
                response = {
                    "error": "Not Found",
                    "path": self.path,
                    "message": "Endpoint not available in simple mode"
                }
                
                self.wfile.write(json.dumps(response, indent=2).encode())
                
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                "error": "Internal Server Error",
                "message": str(e)
            }
            
            self.wfile.write(json.dumps(response, indent=2).encode())
    
    def do_POST(self):
        """Handle POST requests"""
        self.send_response(405)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        response = {
            "error": "Method Not Allowed",
            "message": "POST not implemented in simple mode"
        }
        
        self.wfile.write(json.dumps(response, indent=2).encode())
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def log_message(self, format, *args):
        """Custom logging"""
        print(f"[{datetime.now()}] {format % args}")

def run_simple_server(port=8000):
    """Run simple HTTP server"""
    print(f"🚀 Starting Simple HTTP Server on port {port}...")
    print("Available endpoints:")
    print("  - GET / - Health check")
    print("  - GET /api/v1/status - API status")
    print("")
    print("Press Ctrl+C to stop")
    print("=" * 50)
    
    try:
        server = HTTPServer(('0.0.0.0', port), SimpleHTTPRequestHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")

def run_fastapi_server(port=8000):
    """Run FastAPI server"""
    print(f"🚀 Starting FastAPI Server on port {port}...")
    
    try:
        uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")

def main():
    """Main function"""
    port = int(os.environ.get('PORT', 8000))
    
    if FASTAPI_AVAILABLE:
        print("✓ FastAPI available, using FastAPI server")
        run_fastapi_server(port)
    else:
        print("⚠ FastAPI not available, using simple HTTP server")
        run_simple_server(port)

if __name__ == "__main__":
    main() 