"""
Script to view the contents of the regulations database.
Can display data in terminal or launch a web browser interface.
"""
import os
import sys
import argparse
import webbrowser
import http.server
import socketserver
import threading
from pathlib import Path
from tabulate import tabulate

from src.backend.database.db_manager import get_db_session
from src.backend.models.database.database_models import DocketModel, KeywordModel

def print_dockets():
    """Print all dockets in the database."""
    with get_db_session() as db:
        dockets = db.query(DocketModel).all()
        
        # Prepare data for tabulation
        headers = ["ID", "Title", "Summary", "Keywords"]
        data = []
        
        for docket in dockets:
            keywords = ", ".join([k.text for k in docket.keywords])
            data.append([docket.docket_id, docket.title[:30] + "..." if len(docket.title) > 30 else docket.title, 
                        docket.summary[:30] + "..." if len(docket.summary) > 30 else docket.summary, keywords])
        
        # Print the table
        print("\n=== DOCKETS ===")
        print(tabulate(data, headers=headers, tablefmt="grid"))
        print(f"\nTotal: {len(dockets)} dockets\n")

def print_keywords():
    """Print all keywords in the database."""
    with get_db_session() as db:
        keywords = db.query(KeywordModel).all()
        
        # Prepare data for tabulation
        headers = ["ID", "Text", "# of Dockets"]
        data = []
        
        for keyword in keywords:
            data.append([keyword.id, keyword.text, len(keyword.dockets)])
        
        # Sort by frequency
        data.sort(key=lambda x: x[2], reverse=True)
        
        # Print the table
        print("\n=== KEYWORDS ===")
        print(tabulate(data, headers=headers, tablefmt="grid"))
        print(f"\nTotal: {len(keywords)} unique keywords\n")

def print_docket_keywords():
    """Print the many-to-many relationship between dockets and keywords."""
    with get_db_session() as db:
        dockets = db.query(DocketModel).all()
        
        print("\n=== DOCKET-KEYWORD RELATIONSHIPS ===")
        for docket in dockets:
            print(f"Docket #{docket.docket_id}: {docket.title[:40]}...")
            for keyword in docket.keywords:
                print(f"  - {keyword.text}")
            print()

class DatabaseViewHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        
        # Connect to the database
        content = ""
        with get_db_session() as db:
            # Get dockets
            dockets = db.query(DocketModel).all()
            content += "<div class='table-container'><h2>Dockets</h2>"
            
            if dockets:
                content += "<table><tr><th>ID</th><th>Title</th><th>Summary</th><th>Keywords</th></tr>"
                for docket in dockets:
                    keywords = ", ".join([k.text for k in docket.keywords])
                    content += f"<tr><td>{docket.docket_id}</td><td>{docket.title}</td><td>{docket.summary}</td><td>{keywords}</td></tr>"
                content += "</table>"
            else:
                content += "<p>No dockets found</p>"
            content += "</div>"
            
            # Get keywords
            keywords = db.query(KeywordModel).all()
            content += "<div class='table-container'><h2>Keywords</h2>"
            
            if keywords:
                content += "<table><tr><th>ID</th><th>Text</th><th># of Dockets</th></tr>"
                for keyword in keywords:
                    content += f"<tr><td>{keyword.id}</td><td>{keyword.text}</td><td>{len(keyword.dockets)}</td></tr>"
                content += "</table>"
            else:
                content += "<p>No keywords found</p>"
            content += "</div>"
        
        # HTML template
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>SQLite Database Viewer</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: #333; }}
                h2 {{ color: #666; }}
                table {{ border-collapse: collapse; width: 100%; margin-top: 20px; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
                th {{ background-color: #f2f2f2; }}
                tr:nth-child(even) {{ background-color: #f9f9f9; }}
                .table-container {{ margin-bottom: 30px; }}
            </style>
        </head>
        <body>
            <h1>Regulations Database Viewer</h1>
            {content}
        </body>
        </html>
        """
        
        self.wfile.write(html.encode())

def start_server():
    """Start a simple HTTP server to view database contents in a browser."""
    port = 8000
    handler = DatabaseViewHandler
    
    # Check if the port is already in use
    try:
        httpd = socketserver.TCPServer(("", port), handler)
    except OSError:
        print(f"Port {port} is already in use. Try closing any other applications using this port.")
        return
    
    print(f"Server started at http://localhost:{port}")
    print("Press Ctrl+C to stop the server")
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        httpd.server_close()

def launch_browser():
    """Launch a web browser interface to view the database."""
    # Start the server in a background thread
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()
    
    # Open the web browser
    webbrowser.open(f"http://localhost:8000")
    
    # Keep the main thread running
    try:
        while True:
            input("Press Ctrl+C to exit...\n")
    except KeyboardInterrupt:
        print("\nExiting...")

def main():
    """Main function to view database contents."""
    parser = argparse.ArgumentParser(description="View regulations database contents")
    parser.add_argument("--dockets", action="store_true", help="Show dockets")
    parser.add_argument("--keywords", action="store_true", help="Show keywords")
    parser.add_argument("--relationships", action="store_true", help="Show docket-keyword relationships")
    parser.add_argument("--all", action="store_true", help="Show all tables")
    parser.add_argument("--web", action="store_true", help="Launch web browser interface")
    
    args = parser.parse_args()
    
    if args.web:
        launch_browser()
        return
    
    # If no specific table is requested, show all
    show_all = args.all or not (args.dockets or args.keywords or args.relationships)
    
    if args.dockets or show_all:
        print_dockets()
    
    if args.keywords or show_all:
        print_keywords()
    
    if args.relationships or show_all:
        print_docket_keywords()

if __name__ == "__main__":
    main()
