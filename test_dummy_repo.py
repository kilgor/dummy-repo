"""
Test github-ops.py with dummy-repo (kilgor/dummy-repo)
Tests all read operations and safe write operations
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import github-ops module
import importlib.util
spec = importlib.util.spec_from_file_location(
    "github_ops",
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                 "library", "external-operations", "github-ops.py")
)
github_ops = importlib.util.module_from_spec(spec)
spec.loader.exec_module(github_ops)

GitHubConfig = github_ops.GitHubConfig
list_repositories = github_ops.list_repositories
get_repository_info = github_ops.get_repository_info
list_issues = github_ops.list_issues
create_issue = github_ops.create_issue
update_issue = github_ops.update_issue
get_file_content = github_ops.get_file_content
list_repository_contents = github_ops.list_repository_contents
validate_github_token = github_ops.validate_github_token


def test_dummy_repo():
    """Test all operations on kilgor/dummy-repo"""
    
    print("=" * 70)
    print("GITHUB-OPS.PY DUMMY REPO TEST")
    print("Repository: kilgor/dummy-repo")
    print("=" * 70)
    
    config = GitHubConfig()
    
    # Test 1: Get repository info
    print("\n[TEST 1] get_repository_info('kilgor', 'dummy-repo')")
    result = get_repository_info(owner="kilgor", repo="dummy-repo", config=config)
    if result['success']:
        repo = result['data']
        print(f"✅ Repository: {repo.get('full_name')}")
        print(f"   Description: {repo.get('description', 'N/A')}")
        print(f"   Default branch: {repo.get('default_branch')}")
        print(f"   Private: {repo.get('private')}")
    else:
        print(f"❌ Failed: {result.get('error')}")
        return False
    
    # Test 2: List repository contents (root)
    print("\n[TEST 2] list_repository_contents('kilgor', 'dummy-repo', '')")
    result = list_repository_contents(owner="kilgor", repo="dummy-repo", path="", config=config)
    if result['success']:
        contents = result['data']
        print(f"✅ Found {len(contents)} items in root:")
        for item in contents[:5]:
            print(f"   - {item['name']} ({item['type']})")
    else:
        print(f"❌ Failed: {result.get('error')}")
    
    # Test 3: Get README.md content (if exists)
    print("\n[TEST 3] get_file_content('kilgor', 'dummy-repo', 'README.md')")
    result = get_file_content(owner="kilgor", repo="dummy-repo", path="README.md", config=config)
    if result['success']:
        content = result['data']
        preview = content['content'][:150] if len(content['content']) > 150 else content['content']
        print(f"✅ File retrieved: {content['name']} ({content['size']} bytes)")
        print(f"   Preview: {preview}...")
    else:
        print(f"⚠️  README.md not found (expected for new repo): {result.get('error')}")
    
    # Test 4: List issues
    print("\n[TEST 4] list_issues('kilgor', 'dummy-repo', 'all')")
    result = list_issues(owner="kilgor", repo="dummy-repo", state="all", config=config)
    if result['success']:
        issues = result['data']
        print(f"✅ Found {len(issues)} issues")
        for issue in issues[:3]:
            print(f"   - #{issue['number']}: {issue['title']} ({issue['state']})")
    else:
        print(f"❌ Failed: {result.get('error')}")
    
    # Test 5: Create a test issue
    print("\n[TEST 5] create_issue('kilgor', 'dummy-repo', 'Test Issue')")
    result = create_issue(
        owner="kilgor",
        repo="dummy-repo",
        title="Automated Test Issue",
        body="This is a test issue created by github-ops.py validation testing.\n\nCreated: 2025-12-27",
        labels=["test", "automated"],
        config=config
    )
    if result['success']:
        issue = result['data']
        issue_number = issue['number']
        print(f"✅ Issue created: #{issue_number}")
        print(f"   Title: {issue['title']}")
        print(f"   URL: {issue['html_url']}")
        
        # Test 6: Update the issue
        print(f"\n[TEST 6] update_issue('kilgor', 'dummy-repo', {issue_number})")
        result = update_issue(
            owner="kilgor",
            repo="dummy-repo",
            issue_number=issue_number,
            body="Updated body: Test completed successfully!",
            state="closed",
            config=config
        )
        if result['success']:
            updated = result['data']
            print(f"✅ Issue updated: #{updated['number']}")
            print(f"   State: {updated['state']}")
        else:
            print(f"❌ Update failed: {result.get('error')}")
    else:
        print(f"❌ Failed: {result.get('error')}")
    
    print("\n" + "=" * 70)
    print("DUMMY REPO TEST COMPLETE")
    print("=" * 70)
    return True


if __name__ == "__main__":
    success = test_dummy_repo()
    sys.exit(0 if success else 1)
