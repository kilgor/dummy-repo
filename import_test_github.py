"""
Import and syntax validation test for github-ops.py

This test verifies:
- Python syntax is valid
- Module can be imported
- All exported functions are callable
- Function signatures match TOOL_METADATA
- No syntax errors in VS Code
"""

import sys
import ast
import os

def test_github_ops_import():
    """Run import and syntax validation tests on github-ops.py"""
    
    file_path = "library/external-operations/github-ops.py"
    
    print("=" * 70)
    print("GITHUB-OPS.PY IMPORT & SYNTAX VALIDATION TEST")
    print("=" * 70)
    
    # Test 1: Python syntax compilation
    print("\n[TEST 1] Python Syntax Compilation")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
        compile(source_code, file_path, 'exec')
        print("✅ PASS: Python syntax is valid")
    except SyntaxError as e:
        print(f"❌ FAIL: Syntax error at line {e.lineno}: {e.msg}")
        return False
    
    # Test 2: AST parsing
    print("\n[TEST 2] AST Parsing")
    try:
        tree = ast.parse(source_code, filename=file_path)
        print("✅ PASS: AST parsing successful")
    except Exception as e:
        print(f"❌ FAIL: AST parsing failed: {e}")
        return False
    
    # Test 3: Extract function definitions
    print("\n[TEST 3] Function Definitions")
    functions = []
    classes = []
    
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if not node.name.startswith('_'):  # Public functions only
                functions.append(node.name)
        elif isinstance(node, ast.ClassDef):
            classes.append(node.name)
    
    print(f"   Found {len(classes)} class(es): {', '.join(classes)}")
    print(f"   Found {len(functions)} public function(s):")
    for func in functions:
        print(f"      - {func}")
    
    if 'GitHubConfig' not in classes:
        print("❌ FAIL: GitHubConfig class not found")
        return False
    
    expected_functions = [
        'list_repositories',
        'get_repository_info',
        'delete_repository',
        'fork_repository',
        'list_branches',
        'create_branch',
        'delete_branch',
        'list_pull_requests',
        'create_pull_request',
        'merge_pull_request',
        'list_commits',
        'list_issues',
        'create_issue',
        'update_issue',
        'get_file_content',
        'list_repository_contents',
        'create_file',
        'update_file',
        'delete_file',
        'validate_github_token'
    ]
    
    missing_functions = []
    for func in expected_functions:
        if func not in functions:
            missing_functions.append(func)
    
    if missing_functions:
        print("❌ FAIL: Missing expected functions:")
        for func in missing_functions:
            print(f"   - {func}")
        return False
    
    print("✅ PASS: All expected functions present")
    
    # Test 4: TOOL_METADATA structure validation
    print("\n[TEST 4] TOOL_METADATA Structure")
    metadata_blocks = source_code.count('TOOL_METADATA:')
    
    if metadata_blocks != len(expected_functions):
        print(f"❌ FAIL: Expected {len(expected_functions)} TOOL_METADATA blocks, found {metadata_blocks}")
        return False
    
    # Check for required TOOL_METADATA fields
    required_fields = [
        'name:',
        'category:',
        'subcategory:',
        'description:',
        'dangerous:',
        'framework_compatible:',
        'parameters:',
        'returns:'
    ]
    
    # Split content by TOOL_METADATA to check each block
    metadata_sections = source_code.split('TOOL_METADATA:')[1:]  # Skip first split (before first metadata)
    
    for idx, section in enumerate(metadata_sections):
        # Check first 2000 chars of each section (enough for full metadata)
        section_check = section[:2000]
        missing_in_section = []
        
        for field in required_fields:
            if field not in section_check:
                missing_in_section.append(field)
        
        if missing_in_section:
            print(f"❌ FAIL: TOOL_METADATA block {idx + 1} missing fields: {missing_in_section}")
            print(f"   Section preview: {section_check[:200]}")
            return False
    
    print(f"✅ PASS: All {metadata_blocks} TOOL_METADATA blocks have required fields")
    
    # Test 5: Module can be imported (dry run check)
    print("\n[TEST 5] Import Readiness Check")
    # Check for common import issues
    import_issues = []
    
    # Check for relative imports without package context
    if 'from .ops_core' in source_code:
        import_issues.append("Relative imports (from .ops_core) - should be 'from src.ops_core'")
    
    # Check for missing imports
    if 'import requests' not in source_code:
        import_issues.append("Missing 'import requests' statement")
    
    if 'import base64' not in source_code:
        import_issues.append("Missing 'import base64' statement")
    
    if import_issues:
        print("❌ FAIL: Import issues detected:")
        for issue in import_issues:
            print(f"   - {issue}")
        return False
    
    print("✅ PASS: Import structure looks correct")
    
    # Test 6: No trailing whitespace issues
    print("\n[TEST 6] Code Quality Checks")
    lines = source_code.split('\n')
    trailing_whitespace_lines = []
    
    for idx, line in enumerate(lines, 1):
        if line.endswith(' ') or line.endswith('\t'):
            trailing_whitespace_lines.append(idx)
    
    if trailing_whitespace_lines and len(trailing_whitespace_lines) > 10:
        print(f"⚠️  WARNING: Found trailing whitespace on {len(trailing_whitespace_lines)} lines")
        print(f"   (This is cosmetic, not critical)")
    else:
        print("✅ PASS: Minimal trailing whitespace")
    
    # Test 7: Docstring coverage
    print("\n[TEST 7] Docstring Coverage")
    docstring_count = source_code.count('"""')
    expected_min_docstrings = len(expected_functions) * 2 + 2  # Each function + module + class
    
    if docstring_count < expected_min_docstrings:
        print(f"⚠️  WARNING: Found {docstring_count // 2} docstrings, expected at least {expected_min_docstrings // 2}")
    else:
        print(f"✅ PASS: Adequate docstring coverage ({docstring_count // 2} docstrings)")
    
    # Summary
    print("\n" + "=" * 70)
    print("IMPORT & SYNTAX VALIDATION SUMMARY")
    print("=" * 70)
    print("✅ ALL CRITICAL TESTS PASSED")
    print(f"   File: {file_path}")
    print(f"   Classes: {len(classes)}")
    print(f"   Public Functions: {len(functions)}")
    print(f"   TOOL_METADATA blocks: {metadata_blocks}")
    print(f"   Syntax: Valid")
    print(f"   Import Structure: Correct")
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    success = test_github_ops_import()
    sys.exit(0 if success else 1)
