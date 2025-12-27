"""
Simple structural validation test for github-ops.py

This test verifies:
- File exists and is readable
- File size is reasonable
- Function count matches expected (8 core + 1 utility)
- GitHubConfig class exists
- Pure Logic imports are present
- TOOL_METADATA entries exist
- __all__ exports are defined
"""

import os
import sys

def test_github_ops_structure():
    """Run structural validation tests on github-ops.py"""
    
    # File path
    file_path = "library/external-operations/github-ops.py"
    
    print("=" * 70)
    print("GITHUB-OPS.PY STRUCTURAL VALIDATION TEST")
    print("=" * 70)
    
    # Test 1: File exists
    print("\n[TEST 1] File Existence")
    if not os.path.exists(file_path):
        print(f"❌ FAIL: File not found at {file_path}")
        return False
    print(f"✅ PASS: File exists at {file_path}")
    
    # Read file content
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')
    
    # Test 2: File size
    print("\n[TEST 2] File Size")
    file_size = len(content)
    line_count = len(lines)
    print(f"   File size: {file_size:,} bytes")
    print(f"   Line count: {line_count:,} lines")
    if file_size < 500:
        print("❌ FAIL: File too small, likely incomplete")
        return False
    print("✅ PASS: File size is reasonable")
    
    # Test 3: Version number
    print("\n[TEST 3] Version Number")
    if "v0.0.1" not in content:
        print("❌ FAIL: Version should be v0.0.1")
        return False
    print("✅ PASS: Version is v0.0.1")
    
    # Test 4: No emoji
    print("\n[TEST 4] No Emoji Characters")
    emoji_count = 0
    for char in content:
        if ord(char) > 0x1F000:  # Unicode emoji range
            emoji_count += 1
    if emoji_count > 0:
        print(f"❌ FAIL: Found {emoji_count} emoji characters")
        return False
    print("✅ PASS: No emoji characters found")
    
    # Test 5: Function count
    print("\n[TEST 5] Function Definitions")
    func_count = content.count('def ')
    print(f"   Found {func_count} function definitions")
    if func_count < 10:  # 8 core + helpers
        print(f"❌ FAIL: Expected at least 10 functions, found {func_count}")
        return False
    print("✅ PASS: Function count meets requirements")
    
    # Test 6: GitHubConfig class
    print("\n[TEST 6] GitHubConfig Class")
    if "class GitHubConfig" not in content:
        print("❌ FAIL: GitHubConfig class not found")
        return False
    print("✅ PASS: GitHubConfig class exists")
    
    # Test 7: Pure Logic imports
    print("\n[TEST 7] Pure Logic Pattern Imports")
    required_imports = [
        "BaseConfig",
        "OperationError",
        "create_success_response",
        "create_error_response",
        "validate_required_params"
    ]
    
    # Check if imports from src.ops_core
    if "from src.ops_core import" not in content:
        print("❌ FAIL: Missing 'from src.ops_core import' statement")
        return False
    
    missing_imports = []
    for imp in required_imports:
        if imp not in content:
            missing_imports.append(imp)
    
    if missing_imports:
        print("❌ FAIL: Missing required imports:")
        for imp in missing_imports:
            print(f"   - {imp}")
        return False
    print("✅ PASS: All Pure Logic imports present")
    
    # Test 8: TOOL_METADATA entries
    print("\n[TEST 8] TOOL_METADATA Entries")
    metadata_count = content.count('TOOL_METADATA:')
    print(f"   Found {metadata_count} TOOL_METADATA entries")
    if metadata_count < 8:  # 8 core functions
        print(f"❌ FAIL: Expected 8 TOOL_METADATA entries, found {metadata_count}")
        return False
    print("✅ PASS: TOOL_METADATA entries match expected count")
    
    # Test 9: __all__ exports
    print("\n[TEST 9] __all__ Exports")
    if "__all__ = [" not in content:
        print("❌ FAIL: __all__ exports not found")
        return False
    
    # Check for expected exports
    expected_exports = [
        '"GitHubConfig"',
        '"list_repositories"',
        '"get_repository_info"',
        '"list_issues"',
        '"create_issue"',
        '"update_issue"',
        '"get_file_content"',
        '"list_repository_contents"',
        '"validate_github_token"'
    ]
    
    missing_exports = []
    for export in expected_exports:
        if export not in content:
            missing_exports.append(export)
    
    if missing_exports:
        print("❌ FAIL: Missing exports in __all__:")
        for exp in missing_exports:
            print(f"   - {exp}")
        return False
    print("✅ PASS: All expected exports in __all__")
    
    # Test 10: Author attribution
    print("\n[TEST 10] Author Attribution")
    if "Ali Cem Topcu" not in content:
        print("❌ FAIL: Author attribution missing")
        return False
    print("✅ PASS: Author attribution present")
    
    # Test 11: English only
    print("\n[TEST 11] English Language Only")
    # Check for common non-English characters (Turkish in this case)
    turkish_chars = ['ğ', 'ü', 'ş', 'ı', 'ö', 'ç', 'Ğ', 'Ü', 'Ş', 'İ', 'Ö', 'Ç']
    found_turkish = []
    for char in turkish_chars:
        if char in content:
            found_turkish.append(char)
    
    if found_turkish:
        print(f"❌ FAIL: Found non-English characters: {found_turkish}")
        return False
    print("✅ PASS: English language only")
    
    # Summary
    print("\n" + "=" * 70)
    print("STRUCTURAL VALIDATION SUMMARY")
    print("=" * 70)
    print("✅ ALL TESTS PASSED")
    print(f"   File: {file_path}")
    print(f"   Size: {file_size:,} bytes")
    print(f"   Lines: {line_count:,}")
    print(f"   Functions: {func_count}")
    print(f"   TOOL_METADATA entries: {metadata_count}")
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    success = test_github_ops_structure()
    sys.exit(0 if success else 1)
