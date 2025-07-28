"""
Script to launch the FastAPI documentation in a web browser.
This provides an interactive UI to test the API endpoints.
"""
import subprocess
import threading
import time
import webbrowser
import sys

def start_fastapi_server():
    """Start the FastAPI server in a subprocess."""
    print("Starting FastAPI server...")
    # Use subprocess to run the server
    process = subprocess.Popen(
        [sys.executable, "main.py", "--backend-only"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait a bit to make sure the server starts
    time.sleep(5)
    return process

def open_api_docs():
    """Open the FastAPI documentation in the default web browser."""
    # Swagger UI
    webbrowser.open('http://localhost:8000/docs')
    # ReDoc (alternative documentation)
    # webbrowser.open('http://localhost:8000/redoc')

def main():
    """Main function to start the API server and open documentation."""
    # Start the server
    server_process = start_fastapi_server()
    
    try:
        # Open API docs
        print("Opening API documentation in browser...")
        open_api_docs()
        
        print("\nAPI Documentation is now available at:")
        print("  - Swagger UI: http://localhost:8000/docs")
        print("  - ReDoc: http://localhost:8000/redoc")
        print("\nPress Ctrl+C to stop the server and exit.")
        
        # Keep the script running until interrupted
        while True:
            # Check if the server process is still running
            if server_process.poll() is not None:
                print("Server process has stopped unexpectedly.")
                break
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nShutting down server...")
    finally:
        # Try to terminate the server process gracefully
        if server_process.poll() is None:
            server_process.terminate()
            try:
                server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                print("Server didn't terminate gracefully, forcing...")
                server_process.kill()

if __name__ == "__main__":
    main()
