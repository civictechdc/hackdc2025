#!/usr/bin/env python3
"""
Process judging submissions from GitHub issues into CSV format.

This script helps convert judging submissions from issue templates 
into rows for the judging/results.csv file.

Usage:
    python process_judging_issue.py <issue_number>
    python process_judging_issue.py --from-file judging_submission.txt
"""

import argparse
import csv
import re
import sys
from pathlib import Path


def parse_judge_info(text):
    """Extract judge information from the submission."""
    judge_match = re.search(r'\*\*Name:\*\*\s*(.+)', text)
    judge_name = (judge_match.group(1).strip() 
                  if judge_match else "Unknown Judge")
    return judge_name


def parse_project_scores(text):
    """Extract all project evaluations from the submission."""
    # Pattern to match project sections
    project_pattern = (
        r'### Project:\s*\[?([^\]]+)\]?\s*\n'
        r'\*\*Team:\*\*\s*\[?([^\]]+)\]?.*?'
        r'Technical Excellence:\s*(\d+(?:\.\d+)?)/10.*?'
        r'Innovation:\s*(\d+(?:\.\d+)?)/10.*?'
        r'Civic Impact:\s*(\d+(?:\.\d+)?)/10.*?'
        r'Presentation:\s*(\d+(?:\.\d+)?)/10.*?'
        r'\*\*Comments:\*\*\s*(.*?)(?=###|## Overall|$)'
    )
    
    projects = []
    matches = re.finditer(project_pattern, text, re.DOTALL | re.IGNORECASE)
    
    for match in matches:
        project_name = match.group(1).strip()
        team_name = match.group(2).strip()
        tech_score = float(match.group(3))
        innovation_score = float(match.group(4))
        impact_score = float(match.group(5))
        presentation_score = float(match.group(6))
        comments = match.group(7).strip()
        
        # Clean up comments - remove HTML comments and extra whitespace
        comments = re.sub(r'<!--.*?-->', '', comments, flags=re.DOTALL)
        comments = ' '.join(comments.split())
        
        total_score = (tech_score + innovation_score + 
                       impact_score + presentation_score)
        
        projects.append({
            'team_name': team_name,
            'project_title': project_name,
            'technical_score': tech_score,
            'innovation_score': innovation_score,
            'impact_score': impact_score,
            'presentation_score': presentation_score,
            'total_score': total_score,
            'rank': 0,  # Will be calculated later
            'notes': f"{comments} (Judge: {parse_judge_info(text)})"
        })
    
    return projects


def add_to_csv(projects, csv_path='judging/results.csv'):
    """Add project scores to the CSV file."""
    # Read existing data
    existing_data = []
    if Path(csv_path).exists():
        with open(csv_path, 'r', newline='') as f:
            reader = csv.DictReader(f)
            existing_data = list(reader)
    
    # Add new projects
    for project in projects:
        # Check if this judge already scored this team
        duplicate = False
        judge_name = project['notes'].split('Judge: ')[-1]
        for row in existing_data:
            if (row['team_name'] == project['team_name'] and 
                    f"Judge: {judge_name}" in row.get('notes', '')):
                print(f"Warning: Duplicate entry found for "
                      f"{project['team_name']}. Skipping.")
                duplicate = True
                break
        
        if not duplicate:
            existing_data.append(project)
    
    # Recalculate ranks based on total scores
    existing_data.sort(key=lambda x: float(x['total_score']), reverse=True)
    for i, row in enumerate(existing_data):
        row['rank'] = i + 1
    
    # Write back to CSV
    with open(csv_path, 'w', newline='') as f:
        fieldnames = ['team_name', 'project_title', 'technical_score', 
                      'innovation_score', 'impact_score', 'presentation_score', 
                      'total_score', 'rank', 'notes']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(existing_data)
    
    print(f"Successfully added {len(projects)} project evaluations "
          f"to {csv_path}")


def main():
    parser = argparse.ArgumentParser(
        description='Process judging submissions into CSV format')
    parser.add_argument('--from-file', help='Read submission from a text file')
    parser.add_argument('--issue', type=int, 
                        help='GitHub issue number (requires GitHub CLI)')
    parser.add_argument('--dry-run', action='store_true', 
                        help='Print parsed data without writing to CSV')
    
    args = parser.parse_args()
    
    if args.from_file:
        with open(args.from_file, 'r') as f:
            submission_text = f.read()
    elif args.issue:
        # This would require GitHub CLI or API integration
        print("GitHub issue integration not yet implemented. "
              "Please copy issue content to a file and use --from-file")
        sys.exit(1)
    else:
        print("Please specify either --from-file or --issue")
        sys.exit(1)
    
    # Parse the submission
    judge_name = parse_judge_info(submission_text)
    projects = parse_project_scores(submission_text)
    
    print(f"Found {len(projects)} project evaluations from {judge_name}")
    
    if args.dry_run:
        for project in projects:
            print(f"\n{project['team_name']} - {project['project_title']}")
            print(f"  Technical: {project['technical_score']}")
            print(f"  Innovation: {project['innovation_score']}")
            print(f"  Impact: {project['impact_score']}")
            print(f"  Presentation: {project['presentation_score']}")
            print(f"  Total: {project['total_score']}")
            print(f"  Notes: {project['notes'][:100]}...")
    else:
        add_to_csv(projects)


if __name__ == '__main__':
    main() 