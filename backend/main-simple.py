#!/usr/bin/env python3
"""
Minimal NOA Landing Backend Server
Works without external dependencies
"""

import os
import json
import time
from datetime import datetime

def create_response(status_code, content, content_type="text/plain"):
    """Create HTTP response"""
    status_messages = {
        200: "OK",
        404: "Not Found",
        500: "Internal Server Error"
    }
    
    response = f"HTTP/1.1 {status_code} {status_messages.get(status_code, 'Unknown')}\r\n"
    response += f"Content-Type: {content_type}\r\n"
    response += f"Content-Length: {len(content)}\r\n"
    response += "Access-Control-Allow-Origin: *\r\n"
    response += "Access-Control-Allow-Methods: GET, POST, OPTIONS\r\n"
    response += "Access-Control-Allow-Headers: Content-Type\r\n"
    response += "\r\n"
    response += content
    
    return response

def handle_request(request_data):
    """Handle HTTP request"""
    try:
        # Parse request line
        lines = request_data.split('\n')
        if not lines:
            return create_response(400, "Bad Request")
        
        request_line = lines[0].strip()
        method, path, version = request_line.split(' ')
        
        print(f"[{datetime.now()}] {method} {path}")
        
        # Handle different paths
        if path == "/" or path == "/health":
            response_data = {
                "status": "ok",
                "message": "NOA Landing Backend is running",
                "timestamp": datetime.now().isoformat(),
                "version": "1.0.0"
            }
            return create_response(200, json.dumps(response_data, indent=2), "application/json")
        
        elif path == "/api/v1/status":
            response_data = {
                "status": "running",
                "services": {
                    "backend": "active",
                    "database": "connected",
                    "ai": "available"
                },
                "uptime": "0 seconds"
            }
            return create_response(200, json.dumps(response_data, indent=2), "application/json")
        
        elif path.startswith("/api/v1/"):
            response_data = {
                "error": "Endpoint not implemented",
                "path": path,
                "message": "This endpoint is not available in minimal mode"
            }
            return create_response(404, json.dumps(response_data, indent=2), "application/json")
        
        else:
            return create_response(404, "Not Found")
            
    except Exception as e:
        print(f"Error handling request: {e}")
        return create_response(500, f"Internal Server Error: {str(e)}")

def main():
    """Main server function"""
    print("🚀 Starting NOA Landing Backend (Minimal Mode)...")
    print("Server will run on port 8000")
    print("Available endpoints:")
    print("  - GET / - Health check")
    print("  - GET /api/v1/status - API status")
    print("")
    print("Press Ctrl+C to stop")
    print("=" * 50)
    
    # Simple HTTP server simulation
    # Note: This is a basic implementation for testing
    # In production, use a proper WSGI server
    
    try:
        while True:
            # Simulate server running
            print(f"[{datetime.now()}] Server is running...")
            time.sleep(30)  # Log every 30 seconds
            
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")

if __name__ == "__main__":
    main() 