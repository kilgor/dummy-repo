"""
Initialize dummy-repo with files and folders for testing
Creates a proper structure so we can test all GitHub operations
"""

import sys
import os
import time
from datetime import datetime

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import with hyphenated filename
import importlib.util
spec = importlib.util.spec_from_file_location(
    "github_ops",
    os.path.join(os.path.dirname(__file__), '..', 'library', 'external-operations', 'github-ops.py')
)
github_ops = importlib.util.module_from_spec(spec)
spec.loader.exec_module(github_ops)

create_file = github_ops.create_file
list_branches = github_ops.list_branches
create_branch = github_ops.create_branch

# Repository details
OWNER = "kilgor"
REPO = "dummy-repo"

print("=" * 80)
print("INITIALIZING DUMMY-REPO WITH TEST FILES")
print("=" * 80)
print()

# Files to create
files_to_create = [
    {
        "path": "README.md",
        "content": """# Dummy Repository

This is a test repository for github-ops.py integration testing.

## Purpose
- Test GitHub API operations
- Validate github-ops.py functionality
- Comprehensive integration testing

## Created
{date}

## Structure
- `/docs` - Documentation files
- `/src` - Source code files
- `/data` - Data files
- Root files for testing

## Status
✅ Initialized and ready for testing
""".format(date=datetime.now().isoformat()),
        "message": "Add README.md"
    },
    {
        "path": "docs/getting-started.md",
        "content": """# Getting Started

Welcome to the dummy repository!

## Quick Start

1. Clone this repository
2. Read the documentation
3. Run tests
4. Contribute!

## Features
- Easy to use
- Well documented
- Fully tested

## Last Updated
{date}
""".format(date=datetime.now().isoformat()),
        "message": "Add getting started guide"
    },
    {
        "path": "docs/api-reference.md",
        "content": """# API Reference

## Available Functions

### Function 1
Description of function 1

### Function 2
Description of function 2

### Function 3
Description of function 3

## Examples
Coming soon...

Generated: {date}
""".format(date=datetime.now().isoformat()),
        "message": "Add API reference"
    },
    {
        "path": "src/main.py",
        "content": """#!/usr/bin/env python3
\"\"\"
Main application entry point
\"\"\"

def main():
    print("Hello from dummy-repo!")
    print("This is a test file for github-ops.py testing")
    
    # Some random code
    data = {{
        "status": "initialized",
        "timestamp": "{date}",
        "version": "1.0.0"
    }}
    
    return data

if __name__ == "__main__":
    result = main()
    print("Result: " + str(result))
""".format(date=datetime.now().isoformat()),
        "message": "Add main.py"
    },
    {
        "path": "src/utils.py",
        "content": """\"\"\"
Utility functions for dummy-repo
\"\"\"

def random_function():
    \"\"\"A random function that does nothing useful\"\"\"
    return "This is a random function!"

def another_random_function():
    \"\"\"Another useless function\"\"\"
    numbers = [1, 2, 3, 4, 5]
    return sum(numbers)

def yet_another_function():
    \"\"\"Yet another random function\"\"\"
    text = "Lorem ipsum dolor sit amet"
    return text.upper()

# Created: {date}
""".format(date=datetime.now().isoformat()),
        "message": "Add utility functions"
    },
    {
        "path": "data/sample.json",
        "content": """{{
  "name": "dummy-repo",
  "type": "test-repository",
  "created": "{date}",
  "purpose": "Testing github-ops.py",
  "features": [
    "File operations",
    "Branch management",
    "Issue tracking",
    "Pull request testing"
  ],
  "metadata": {{
    "owner": "kilgor",
    "visibility": "public",
    "initialized": true
  }}
}}
""".format(date=datetime.now().isoformat()),
        "message": "Add sample JSON data"
    },
    {
        "path": "data/notes.txt",
        "content": """Random Notes for Testing
========================

Date: {date}

This is a random text file with some nonsense content.

Lorem ipsum dolor sit amet, consectetur adipiscing elit.
Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.

Random list:
- Item one
- Item two
- Item three
- Item four

Some random numbers: 42, 1337, 9001, 404

End of random notes.
""".format(date=datetime.now().isoformat()),
        "message": "Add random notes"
    },
    {
        "path": "CHANGELOG.md",
        "content": """# Changelog

All notable changes to this dummy repository will be documented here.

## [1.0.0] - {date}

### Added
- Initial repository structure
- README.md with project overview
- Documentation in /docs folder
- Source files in /src folder
- Sample data files in /data folder
- This changelog

### Purpose
- Testing github-ops.py functionality
- Comprehensive integration testing
- API operation validation

## Future Plans
- Add more test files
- Create test branches
- Add more documentation
""".format(date=datetime.now().isoformat()),
        "message": "Add changelog"
    },
    {
        "path": ".gitignore",
        "content": """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
.venv/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Project specific
*.log
.env
.env.local

# Created: {date}
""".format(date=datetime.now().isoformat()),
        "message": "Add .gitignore"
    },
    {
        "path": "LICENSE",
        "content": """MIT License

Copyright (c) 2025 kilgor

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""",
        "message": "Add MIT license"
    }
]

print(f"Creating {len(files_to_create)} files in {OWNER}/{REPO}...")
print()

success_count = 0
failed_count = 0

for i, file_info in enumerate(files_to_create, 1):
    path = file_info["path"]
    content = file_info["content"]
    message = file_info["message"]
    
    print(f"[{i}/{len(files_to_create)}] Creating {path}...", end=" ")
    
    result = create_file(
        owner=OWNER,
        repo=REPO,
        path=path,
        message=message,
        content=content,
        branch="main"
    )
    
    if result.get("success"):
        print("✅ Success")
        success_count += 1
        time.sleep(0.5)  # Rate limiting - be nice to GitHub API
    else:
        print(f"❌ Failed: {result.get('error', 'Unknown error')}")
        failed_count += 1

print()
print("=" * 80)
print("INITIALIZATION COMPLETE")
print("=" * 80)
print(f"✅ Successfully created: {success_count} files")
print(f"❌ Failed to create: {failed_count} files")
print()

if success_count > 0:
    print("Repository is now initialized with:")
    print("  - README.md (root)")
    print("  - docs/ folder (2 files)")
    print("  - src/ folder (2 files)")
    print("  - data/ folder (2 files)")
    print("  - CHANGELOG.md")
    print("  - .gitignore")
    print("  - LICENSE")
    print()
    print("✅ Ready for comprehensive testing!")
else:
    print("⚠️  No files were created. Check token permissions.")

print()
print("To run comprehensive test:")
print("  python test/test_dummy_repo_comprehensive.py")
print()
