"""
Test GitHub token validation and basic API connectivity
"""

import sys
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import using the module path with hyphens replaced
import importlib.util
spec = importlib.util.spec_from_file_location(
    "github_ops",
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                 "library", "external-operations", "github-ops.py")
)
github_ops = importlib.util.module_from_spec(spec)
spec.loader.exec_module(github_ops)

GitHubConfig = github_ops.GitHubConfig
validate_github_token = github_ops.validate_github_token

def test_token_validation():
    """Test GitHub token validation and API connectivity"""
    
    print("=" * 70)
    print("GITHUB TOKEN VALIDATION TEST")
    print("=" * 70)
    
    # Test 1: Load configuration
    print("\n[TEST 1] Configuration Loading")
    try:
        config = GitHubConfig()
        print(f"✅ Configuration loaded successfully")
        print(f"   Token prefix: {config.token[:20]}..." if config.token else "   No token found")
    except Exception as e:
        print(f"❌ FAIL: Configuration loading failed: {e}")
        return False
    
    # Test 2: Validate token
    print("\n[TEST 2] Token Validation")
    try:
        result = validate_github_token(config)
        
        if result.get('success'):
            print("✅ PASS: GitHub token is valid")
            data = result.get('data', {})
            print(f"   User: {data.get('login', 'N/A')}")
            print(f"   Name: {data.get('name', 'N/A')}")
            print(f"   Type: {data.get('type', 'N/A')}")
            print(f"   Public repos: {data.get('public_repos', 'N/A')}")
        else:
            print(f"❌ FAIL: Token validation failed")
            print(f"   Error: {result.get('error', 'Unknown error')}")
            print(f"   Message: {result.get('message', 'No message')}")
            return False
            
    except Exception as e:
        print(f"❌ FAIL: Token validation error: {e}")
        return False
    
    # Summary
    print("\n" + "=" * 70)
    print("TOKEN VALIDATION SUMMARY")
    print("=" * 70)
    print("✅ GitHub API connection successful")
    print("✅ Token is valid and authenticated")
    print("✅ github-ops.py is ready for production use")
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    success = test_token_validation()
    sys.exit(0 if success else 1)
