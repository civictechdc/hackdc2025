#!/usr/bin/env python3

import argparse
import subprocess
import sys

def main():
    """
    Main launcher for CMS Agent.
    Allows running either the CLI or web version of the agent.
    """
    parser = argparse.ArgumentParser(description="CMS Docket Agent Launcher")
    parser.add_argument("--web", action="store_true", help="Launch the web interface")
    parser.add_argument("--cli", action="store_true", help="Launch the command-line interface")
    
    args = parser.parse_args()
    
    # Default to CLI if no arguments provided
    if not args.web and not args.cli:
        args.cli = True
    
    if args.web:
        print("Launching CMS Agent Web Interface...")
        try:
            subprocess.run(["streamlit", "run", "cms_agent_web.py"], check=True)
        except FileNotFoundError:
            print("Error: Streamlit not found. Please install it with 'pip install streamlit'")
            sys.exit(1)
    
    if args.cli:
        print("Launching CMS Agent Command-Line Interface...")
        try:
            # Import and run the CLI version directly
            from cms_agent import main as cli_main
            cli_main()
        except ImportError:
            print("Error: Could not import cms_agent.py. Make sure the file exists.")
            sys.exit(1)

if __name__ == "__main__":
    main()
