"""Runs the backend and frontend."""
import os
import threading
import time
import subprocess
import webbrowser
import argparse
from src.backend.run import run as run_backend

def run_angular_frontend():
    """Run the Angular frontend development server and open it in the browser."""
    frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                              "src", "frontend", "regulations-search")
    
    print("Starting Angular frontend server...")
    
    # Use subprocess to run npm start (which runs ng serve)
    # shell=True is needed for Windows
    process = subprocess.Popen(
        "npx ng serve --open",
        shell=True,
        cwd=frontend_dir
    )
    
    # Wait a bit to make sure the server starts
    time.sleep(5)
    
    # Open the browser if --open flag doesn't work
    webbrowser.open('http://localhost:4200')
    
    return process

def main():
    """Run both backend and frontend."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Run the regulations search application')
    parser.add_argument('--update-db', action='store_true', help='Update the database with the latest data')
    parser.add_argument('--backend-only', action='store_true', help='Run only the backend')
    parser.add_argument('--frontend-only', action='store_true', help='Run only the frontend')
    args = parser.parse_args()
    
    frontend_process = None
    
    try:
        # Start the backend if requested
        if not args.frontend_only:
            if args.backend_only:
                # If backend only, run directly (blocking)
                run_backend(args.update_db)
            else:
                # Otherwise run in a daemon thread
                backend_thread = threading.Thread(target=run_backend, args=(args.update_db,))
                backend_thread.daemon = True
                backend_thread.start()
        
        # Start the frontend if requested
        if not args.backend_only:
            # Start the frontend
            frontend_process = run_angular_frontend()
            
            # Keep the main thread alive while the frontend is running
            while frontend_process.poll() is None:
                time.sleep(1)
            
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        # Clean up processes
        if frontend_process and frontend_process.poll() is None:
            print("Terminating frontend process...")
            frontend_process.terminate()
            
        # The backend thread is a daemon thread, so it will exit when the main thread exits

if __name__ == "__main__":
    main()
