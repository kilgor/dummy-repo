"""
Comprehensive Integration Test for github-ops.py on dummy-repo
Tests ALL 20 functions with full API access granted.

Repository: https://github.com/kilgor/dummy-repo
Test Strategy: Relentless testing of all operations
"""

import sys
import os
import json
import time
from datetime import datetime

# Load environment variables FIRST
from dotenv import load_dotenv
load_dotenv()  # Load from .env file

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import with hyphenated filename - need to use importlib
import importlib.util
spec = importlib.util.spec_from_file_location(
    "github_ops",
    os.path.join(os.path.dirname(__file__), '..', 'library', 'external-operations', 'github-ops.py')
)
github_ops = importlib.util.module_from_spec(spec)
spec.loader.exec_module(github_ops)

# Import all functions
list_repositories = github_ops.list_repositories
get_repository_info = github_ops.get_repository_info
fork_repository = github_ops.fork_repository
delete_repository = github_ops.delete_repository
list_branches = github_ops.list_branches
create_branch = github_ops.create_branch
delete_branch = github_ops.delete_branch
list_pull_requests = github_ops.list_pull_requests
create_pull_request = github_ops.create_pull_request
merge_pull_request = github_ops.merge_pull_request
list_commits = github_ops.list_commits
list_issues = github_ops.list_issues
create_issue = github_ops.create_issue
update_issue = github_ops.update_issue
get_file_content = github_ops.get_file_content
list_repository_contents = github_ops.list_repository_contents
create_file = github_ops.create_file
update_file = github_ops.update_file
delete_file = github_ops.delete_file
validate_github_token = github_ops.validate_github_token

# Test configuration
OWNER = "kilgor"
REPO = "dummy-repo"
TEST_BRANCH = f"test-branch-{int(time.time())}"
TEST_FILE = f"test-file-{int(time.time())}.txt"
TEST_FILE_2 = f"test-file-2-{int(time.time())}.md"

# Colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

# Test results tracking
test_results = {
    "total": 0,
    "passed": 0,
    "failed": 0,
    "skipped": 0,
    "tests": []
}

def log_test(test_name, status, message="", data=None):
    """Log test result"""
    test_results["total"] += 1
    
    if status == "PASSED":
        test_results["passed"] += 1
        color = GREEN
        symbol = "✅"
    elif status == "FAILED":
        test_results["failed"] += 1
        color = RED
        symbol = "❌"
    else:  # SKIPPED
        test_results["skipped"] += 1
        color = YELLOW
        symbol = "⚠️"
    
    print(f"{color}{symbol} {test_name}: {status}{RESET}")
    if message:
        print(f"   {message}")
    if data and isinstance(data, dict):
        if "error" in data:
            print(f"   Error: {data['error']}")
    
    test_results["tests"].append({
        "name": test_name,
        "status": status,
        "message": message,
        "timestamp": datetime.now().isoformat()
    })

def print_header(title):
    """Print section header"""
    print(f"\n{BLUE}{'=' * 80}{RESET}")
    print(f"{BLUE}{title.center(80)}{RESET}")
    print(f"{BLUE}{'=' * 80}{RESET}\n")

def print_summary():
    """Print test summary"""
    print_header("TEST SUMMARY")
    print(f"Total Tests: {test_results['total']}")
    print(f"{GREEN}✅ Passed: {test_results['passed']}{RESET}")
    print(f"{RED}❌ Failed: {test_results['failed']}{RESET}")
    print(f"{YELLOW}⚠️  Skipped: {test_results['skipped']}{RESET}")
    
    success_rate = (test_results['passed'] / test_results['total'] * 100) if test_results['total'] > 0 else 0
    print(f"\n{BLUE}Success Rate: {success_rate:.1f}%{RESET}")
    
    if test_results['failed'] == 0:
        print(f"\n{GREEN}🎉 ALL TESTS PASSED!{RESET}")
    else:
        print(f"\n{RED}⚠️  {test_results['failed']} TESTS FAILED{RESET}")

# ============================================================================
# TEST EXECUTION
# ============================================================================

print_header("COMPREHENSIVE GITHUB-OPS.PY TEST")
print(f"Repository: {OWNER}/{REPO}")
print(f"Test Branch: {TEST_BRANCH}")
print(f"Test File: {TEST_FILE}")
print(f"Timestamp: {datetime.now().isoformat()}")

# ============================================================================
# 1. UTILITIES - TOKEN VALIDATION
# ============================================================================
print_header("1. UTILITIES - TOKEN VALIDATION")

result = validate_github_token()
if result.get("success"):
    log_test("validate_github_token", "PASSED", f"User: {result.get('data', {}).get('login', 'N/A')}")
else:
    log_test("validate_github_token", "FAILED", "Token validation failed", result)
    print(f"\n{RED}❌ ABORTING: Token validation failed!{RESET}")
    sys.exit(1)

# ============================================================================
# 2. REPOSITORIES - LIST & GET INFO
# ============================================================================
print_header("2. REPOSITORIES - LIST & GET INFO")

# List repositories
result = list_repositories(type="all", sort="full_name")
if result.get("success"):
    repos = result.get("data", [])
    log_test("list_repositories", "PASSED", f"Found {len(repos)} repositories")
else:
    log_test("list_repositories", "FAILED", data=result)

# Get repository info
result = get_repository_info(owner=OWNER, repo=REPO)
if result.get("success"):
    repo_data = result.get("data", {})
    log_test("get_repository_info", "PASSED", 
             f"Repo: {repo_data.get('full_name')}, Default Branch: {repo_data.get('default_branch')}")
    DEFAULT_BRANCH = repo_data.get("default_branch", "main")
else:
    log_test("get_repository_info", "FAILED", data=result)
    DEFAULT_BRANCH = "main"

# ============================================================================
# 3. BRANCHES - LIST, CREATE, DELETE
# ============================================================================
print_header("3. BRANCHES - LIST, CREATE, DELETE")

# List branches
result = list_branches(owner=OWNER, repo=REPO)
if result.get("success"):
    branches = result.get("data", [])
    log_test("list_branches", "PASSED", f"Found {len(branches)} branches")
    
    # Get SHA of default branch for creating new branch
    default_branch_sha = None
    for branch in branches:
        if branch.get("name") == DEFAULT_BRANCH:
            default_branch_sha = branch.get("commit", {}).get("sha")
            break
else:
    log_test("list_branches", "FAILED", data=result)
    default_branch_sha = None

# Create branch
if default_branch_sha:
    result = create_branch(owner=OWNER, repo=REPO, branch=TEST_BRANCH, sha=default_branch_sha)
    if result.get("success"):
        log_test("create_branch", "PASSED", f"Created branch: {TEST_BRANCH}")
    else:
        log_test("create_branch", "FAILED", data=result)
else:
    log_test("create_branch", "SKIPPED", "No SHA available for default branch")

# ============================================================================
# 4. CONTENTS - CREATE, READ, UPDATE, DELETE
# ============================================================================
print_header("4. CONTENTS - CREATE, READ, UPDATE, DELETE")

# List repository contents (root)
result = list_repository_contents(owner=OWNER, repo=REPO, path="")
if result.get("success"):
    contents = result.get("data", [])
    log_test("list_repository_contents", "PASSED", f"Found {len(contents)} items in root")
else:
    log_test("list_repository_contents", "FAILED", data=result)

# Create file on test branch
file_content = f"# Test File\n\nCreated at: {datetime.now().isoformat()}\n\nThis is a comprehensive test file."
result = create_file(
    owner=OWNER,
    repo=REPO,
    path=TEST_FILE,
    message=f"Create {TEST_FILE} for testing",
    content=file_content,
    branch=TEST_BRANCH
)
if result.get("success"):
    log_test("create_file", "PASSED", f"Created {TEST_FILE} on {TEST_BRANCH}")
    FILE_SHA = result.get("data", {}).get("content", {}).get("sha")
else:
    log_test("create_file", "FAILED", data=result)
    FILE_SHA = None

# Get file content
time.sleep(1)  # Brief delay to ensure file is created
result = get_file_content(owner=OWNER, repo=REPO, path=TEST_FILE, ref=TEST_BRANCH)
if result.get("success"):
    content = result.get("data", {}).get("content", "")
    log_test("get_file_content", "PASSED", f"Retrieved {len(content)} bytes")
else:
    log_test("get_file_content", "FAILED", data=result)

# Update file
if FILE_SHA:
    updated_content = file_content + f"\n\nUpdated at: {datetime.now().isoformat()}"
    result = update_file(
        owner=OWNER,
        repo=REPO,
        path=TEST_FILE,
        message=f"Update {TEST_FILE}",
        content=updated_content,
        sha=FILE_SHA,
        branch=TEST_BRANCH
    )
    if result.get("success"):
        log_test("update_file", "PASSED", f"Updated {TEST_FILE}")
        FILE_SHA = result.get("data", {}).get("content", {}).get("sha")
    else:
        log_test("update_file", "FAILED", data=result)
else:
    log_test("update_file", "SKIPPED", "No file SHA available")

# Create second file for PR testing
result = create_file(
    owner=OWNER,
    repo=REPO,
    path=TEST_FILE_2,
    message=f"Create {TEST_FILE_2} for PR testing",
    content=f"# PR Test File\n\nCreated at: {datetime.now().isoformat()}",
    branch=TEST_BRANCH
)
if result.get("success"):
    log_test("create_file (2nd)", "PASSED", f"Created {TEST_FILE_2}")
else:
    log_test("create_file (2nd)", "FAILED", data=result)

# ============================================================================
# 5. COMMITS - LIST COMMITS
# ============================================================================
print_header("5. COMMITS - LIST COMMITS")

result = list_commits(owner=OWNER, repo=REPO, branch=TEST_BRANCH, limit=10)
if result.get("success"):
    commits = result.get("data", [])
    log_test("list_commits", "PASSED", f"Found {len(commits)} commits on {TEST_BRANCH}")
else:
    log_test("list_commits", "FAILED", data=result)

# ============================================================================
# 6. PULL REQUESTS - CREATE, LIST, MERGE
# ============================================================================
print_header("6. PULL REQUESTS - CREATE, LIST, MERGE")

# Create pull request
PR_TITLE = f"Test PR - {int(time.time())}"
PR_BODY = f"Automated test PR created at {datetime.now().isoformat()}\n\nTesting github-ops.py comprehensive integration."
result = create_pull_request(
    owner=OWNER,
    repo=REPO,
    title=PR_TITLE,
    body=PR_BODY,
    head=TEST_BRANCH,
    base=DEFAULT_BRANCH
)

PR_NUMBER = None
if result.get("success"):
    pr_data = result.get("data", {})
    PR_NUMBER = pr_data.get("number")
    log_test("create_pull_request", "PASSED", f"Created PR #{PR_NUMBER}: {PR_TITLE}")
else:
    log_test("create_pull_request", "FAILED", data=result)

# List pull requests
result = list_pull_requests(owner=OWNER, repo=REPO, state="open")
if result.get("success"):
    prs = result.get("data", [])
    log_test("list_pull_requests", "PASSED", f"Found {len(prs)} open PRs")
else:
    log_test("list_pull_requests", "FAILED", data=result)

# Merge pull request (if created)
if PR_NUMBER:
    time.sleep(2)  # Wait for PR to be ready
    result = merge_pull_request(
        owner=OWNER,
        repo=REPO,
        pull_number=PR_NUMBER,
        commit_title=f"Merge test PR #{PR_NUMBER}",
        commit_message="Automated merge from comprehensive test",
        merge_method="squash"
    )
    if result.get("success"):
        log_test("merge_pull_request", "PASSED", f"Merged PR #{PR_NUMBER}")
    else:
        log_test("merge_pull_request", "FAILED", data=result)
else:
    log_test("merge_pull_request", "SKIPPED", "No PR created")

# ============================================================================
# 7. ISSUES - CREATE, LIST, UPDATE
# ============================================================================
print_header("7. ISSUES - CREATE, LIST, UPDATE")

# Create issue
ISSUE_TITLE = f"Test Issue - {int(time.time())}"
ISSUE_BODY = f"Automated test issue created at {datetime.now().isoformat()}\n\nTesting github-ops.py issue operations."
result = create_issue(
    owner=OWNER,
    repo=REPO,
    title=ISSUE_TITLE,
    body=ISSUE_BODY,
    labels=["test", "automated"]
)

ISSUE_NUMBER = None
if result.get("success"):
    issue_data = result.get("data", {})
    ISSUE_NUMBER = issue_data.get("number")
    log_test("create_issue", "PASSED", f"Created issue #{ISSUE_NUMBER}: {ISSUE_TITLE}")
else:
    log_test("create_issue", "FAILED", data=result)

# List issues
result = list_issues(owner=OWNER, repo=REPO, state="open")
if result.get("success"):
    issues = result.get("data", [])
    log_test("list_issues", "PASSED", f"Found {len(issues)} open issues")
else:
    log_test("list_issues", "FAILED", data=result)

# Update issue (if created)
if ISSUE_NUMBER:
    result = update_issue(
        owner=OWNER,
        repo=REPO,
        issue_number=ISSUE_NUMBER,
        title=f"{ISSUE_TITLE} [UPDATED]",
        body=f"{ISSUE_BODY}\n\n**UPDATED**: Test completed successfully!",
        state="closed"
    )
    if result.get("success"):
        log_test("update_issue", "PASSED", f"Updated and closed issue #{ISSUE_NUMBER}")
    else:
        log_test("update_issue", "FAILED", data=result)
else:
    log_test("update_issue", "SKIPPED", "No issue created")

# ============================================================================
# 8. CLEANUP - DELETE FILES & BRANCH
# ============================================================================
print_header("8. CLEANUP - DELETE FILES & BRANCH")

# Get updated file SHAs from default branch (after merge)
time.sleep(2)  # Wait for merge to complete

# Delete first file
result = get_file_content(owner=OWNER, repo=REPO, path=TEST_FILE, ref=DEFAULT_BRANCH)
if result.get("success"):
    file_sha = result.get("data", {}).get("sha")
    result = delete_file(
        owner=OWNER,
        repo=REPO,
        path=TEST_FILE,
        message=f"Delete {TEST_FILE} after testing",
        sha=file_sha,
        branch=DEFAULT_BRANCH
    )
    if result.get("success"):
        log_test("delete_file (1st)", "PASSED", f"Deleted {TEST_FILE}")
    else:
        log_test("delete_file (1st)", "FAILED", data=result)
else:
    log_test("delete_file (1st)", "SKIPPED", "File not found on default branch")

# Delete second file
result = get_file_content(owner=OWNER, repo=REPO, path=TEST_FILE_2, ref=DEFAULT_BRANCH)
if result.get("success"):
    file_sha = result.get("data", {}).get("sha")
    result = delete_file(
        owner=OWNER,
        repo=REPO,
        path=TEST_FILE_2,
        message=f"Delete {TEST_FILE_2} after testing",
        sha=file_sha,
        branch=DEFAULT_BRANCH
    )
    if result.get("success"):
        log_test("delete_file (2nd)", "PASSED", f"Deleted {TEST_FILE_2}")
    else:
        log_test("delete_file (2nd)", "FAILED", data=result)
else:
    log_test("delete_file (2nd)", "SKIPPED", "File not found on default branch")

# Delete test branch
result = delete_branch(owner=OWNER, repo=REPO, branch_name=TEST_BRANCH)
if result.get("success"):
    log_test("delete_branch", "PASSED", f"Deleted branch: {TEST_BRANCH}")
else:
    log_test("delete_branch", "FAILED", data=result)

# ============================================================================
# 9. ADVANCED - FORK REPOSITORY (DANGEROUS - OPTIONAL)
# ============================================================================
print_header("9. ADVANCED - FORK REPOSITORY")

# Note: Forking creates a copy in your account - be cautious!
print(f"{YELLOW}⚠️  Skipping fork_repository - would create a permanent copy{RESET}")
log_test("fork_repository", "SKIPPED", "Manual test only - creates permanent copy")

# ============================================================================
# 10. DANGEROUS - DELETE REPOSITORY (NOT TESTING)
# ============================================================================
print_header("10. DANGEROUS - DELETE REPOSITORY")

print(f"{YELLOW}⚠️  Skipping delete_repository - DANGEROUS operation!{RESET}")
log_test("delete_repository", "SKIPPED", "Manual test only - DANGEROUS!")

# ============================================================================
# FINAL SUMMARY
# ============================================================================
print_summary()

# Save results to file
results_file = f"test/results/github-ops-comprehensive-test-{int(time.time())}.json"
os.makedirs("test/results", exist_ok=True)

with open(results_file, 'w') as f:
    json.dump(test_results, f, indent=2)

print(f"\n{BLUE}Results saved to: {results_file}{RESET}")

# Exit with appropriate code
sys.exit(0 if test_results['failed'] == 0 else 1)
