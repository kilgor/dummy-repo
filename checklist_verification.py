"""
Comprehensive Checklist Verification for github-ops.py
Verifies compliance with ops-file-creation-checklist.md
"""

import os
import re
import ast

print("=" * 80)
print("CHECKLIST VERIFICATION FOR github-ops.py")
print("=" * 80)
print()

file_path = "library/external-operations/github-ops.py"

if not os.path.exists(file_path):
    print(f"❌ File not found: {file_path}")
    exit(1)

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# ============================================================================
# CRITICAL RULES VERIFICATION
# ============================================================================
print("🚨 CRITICAL RULES VERIFICATION")
print("-" * 80)

# 1. VERSION STARTS AT v0.0.1
version_match = re.search(r'Version:\s*v?([\d.]+)', content)
if version_match:
    version = version_match.group(1)
    if version == "0.0.1":
        print(f"✅ Version is v0.0.1 (correct development version)")
    else:
        print(f"⚠️  Version is v{version} (expected v0.0.1)")
else:
    print("❌ No version found in module docstring")

# 2. ENGLISH ONLY
has_turkish = bool(re.search(r'[ğĞüÜşŞıİöÖçÇ]', content))
if not has_turkish:
    print("✅ English only - no Turkish or special characters detected")
else:
    print("⚠️  WARNING: Turkish or special characters detected")

# 3. AUTHOR TAGS
author_present = 'Ali Cem Topcu' in content
email_present = 'alicemtopcu@yahoo.com' in content
github_present = '@kilgor' in content or 'github.com' in content.lower()
linkedin_present = 'linkedin.com' in content.lower()

if all([author_present, email_present, github_present, linkedin_present]):
    print("✅ Author attribution complete (name, email, GitHub, LinkedIn)")
else:
    missing = []
    if not author_present: missing.append("name")
    if not email_present: missing.append("email")
    if not github_present: missing.append("GitHub")
    if not linkedin_present: missing.append("LinkedIn")
    print(f"⚠️  Missing author info: {', '.join(missing)}")

# 4. TOOL_METADATA FOR EVERY FUNCTION
tree = ast.parse(content)
public_functions = [
    node.name for node in ast.walk(tree) 
    if isinstance(node, ast.FunctionDef) 
    and not node.name.startswith('_')
]

functions_with_metadata = []
for func_name in public_functions:
    # Find function definition
    func_pattern = rf'def {func_name}\([^)]*\):[^:]*?""".*?(?:TOOL_METADATA:|""")'
    if re.search(func_pattern, content, re.DOTALL):
        if 'TOOL_METADATA:' in content.split(f'def {func_name}')[1].split('def ')[0]:
            functions_with_metadata.append(func_name)

metadata_coverage = len(functions_with_metadata) / len(public_functions) * 100 if public_functions else 0

if metadata_coverage == 100:
    print(f"✅ TOOL_METADATA: {len(functions_with_metadata)}/{len(public_functions)} functions (100% coverage)")
else:
    print(f"⚠️  TOOL_METADATA: {len(functions_with_metadata)}/{len(public_functions)} functions ({metadata_coverage:.1f}% coverage)")
    missing = set(public_functions) - set(functions_with_metadata)
    print(f"   Missing TOOL_METADATA: {', '.join(missing)}")

# 5. NO EMOJI IN CODE
emoji_pattern = re.compile("["
    u"\U0001F600-\U0001F64F"  # emoticons
    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    u"\U0001F680-\U0001F6FF"  # transport & map symbols
    u"\U0001F1E0-\U0001F1FF"  # flags
    u"\U00002702-\U000027B0"
    u"\U000024C2-\U0001F251"
    "]+", flags=re.UNICODE)

if not emoji_pattern.search(content):
    print("✅ No emoji characters in code")
else:
    print("❌ Emoji characters detected in code (not allowed)")

print()

# ============================================================================
# BASE IMPLEMENTATION VERIFICATION
# ============================================================================
print("🏗️  BASE IMPLEMENTATION VERIFICATION")
print("-" * 80)

# Module docstring
if content.startswith('"""') or content.startswith("'''"):
    print("✅ Module docstring present")
else:
    print("❌ No module docstring")

# Pure Logic imports
required_imports = [
    'from src.ops_core import',
    'BaseConfig',
    'create_success_response',
    'create_error_response',
    'OperationError'
]

missing_imports = []
for imp in required_imports:
    if imp not in content:
        missing_imports.append(imp)

if not missing_imports:
    print("✅ Pure Logic imports present (src.ops_core)")
else:
    print(f"⚠️  Missing imports: {', '.join(missing_imports)}")

# Configuration class
config_class_pattern = r'class \w+Config\(BaseConfig\)'
if re.search(config_class_pattern, content):
    print("✅ Configuration class extends BaseConfig")
else:
    print("⚠️  No configuration class found")

# Helper functions
helper_functions = len(re.findall(r'def _[a-z_]+\(', content))
print(f"✅ Helper functions: {helper_functions} (private functions with _)")

# __all__ exports
if '__all__ = [' in content:
    all_match = re.search(r'__all__\s*=\s*\[(.*?)\]', content, re.DOTALL)
    if all_match:
        exports = [e.strip().strip('"\'') for e in all_match.group(1).split(',') if e.strip() and not e.strip().startswith('#')]
        print(f"✅ __all__ exports: {len(exports)} items")
    else:
        print("⚠️  __all__ found but could not parse")
else:
    print("❌ No __all__ exports list")

print()

# ============================================================================
# FUNCTION STRUCTURE VERIFICATION
# ============================================================================
print("📦 FUNCTION STRUCTURE VERIFICATION")
print("-" * 80)

# Count function definitions
total_functions = len(re.findall(r'^def [a-z_]', content, re.MULTILINE))
print(f"✅ Total function definitions: {total_functions}")
print(f"   - Public functions: {len(public_functions)}")
print(f"   - Private functions: {helper_functions}")

# Check if functions follow standard pattern
functions_with_try_except = len(re.findall(r'def [a-z_]+.*?:\s+""".*?try:', content, re.DOTALL))
print(f"✅ Functions with try-except: {functions_with_try_except}/{len(public_functions)}")

# Check logging
functions_with_logging = len(re.findall(r'log_operation\(', content))
if functions_with_logging > 0:
    print(f"✅ Functions with logging: {functions_with_logging}")
else:
    print("⚠️  No log_operation() calls found")

# Check response patterns
success_responses = len(re.findall(r'create_success_response\(', content))
error_responses = len(re.findall(r'create_error_response\(', content))
print(f"✅ Success responses: {success_responses}")
print(f"✅ Error responses: {error_responses}")

print()

# ============================================================================
# TOOL_METADATA STRUCTURE VERIFICATION
# ============================================================================
print("🔧 TOOL_METADATA STRUCTURE VERIFICATION")
print("-" * 80)

# Check TOOL_METADATA format
metadata_blocks = re.findall(r'TOOL_METADATA:\s*\n(.*?)(?=\n    \w+:|""")', content, re.DOTALL)
print(f"✅ TOOL_METADATA blocks found: {len(metadata_blocks)}")

# Verify required fields in metadata
required_fields = ['name:', 'category:', 'subcategory:', 'description:', 'dangerous:', 'parameters:', 'returns:']
metadata_with_all_fields = 0

for block in metadata_blocks:
    has_all = all(field in block for field in required_fields)
    if has_all:
        metadata_with_all_fields += 1

if len(metadata_blocks) > 0:
    print(f"✅ Metadata with all required fields: {metadata_with_all_fields}/{len(metadata_blocks)}")
    if metadata_with_all_fields < len(metadata_blocks):
        print(f"   ⚠️  {len(metadata_blocks) - metadata_with_all_fields} blocks missing some fields")
else:
    print("⚠️  No TOOL_METADATA blocks found")

# Check dangerous operations marking
dangerous_funcs = re.findall(r'name:\s*(\w+).*?dangerous:\s*true', content, re.DOTALL | re.IGNORECASE)
print(f"✅ Dangerous operations marked: {len(dangerous_funcs)}")
if dangerous_funcs:
    print(f"   Dangerous functions: {', '.join(dangerous_funcs)}")

print()

# ============================================================================
# FILE STATISTICS
# ============================================================================
print("📊 FILE STATISTICS")
print("-" * 80)

file_size = os.path.getsize(file_path)
line_count = content.count('\n')

print(f"✅ File size: {file_size:,} bytes ({file_size/1024:.1f} KB)")
print(f"✅ Total lines: {line_count:,}")
print(f"✅ Lines per function: {line_count // len(public_functions) if public_functions else 0}")

print()

# ============================================================================
# FINAL CHECKLIST SCORE
# ============================================================================
print("🎯 FINAL CHECKLIST COMPLIANCE SCORE")
print("=" * 80)

checks = {
    "Version v0.0.1": version == "0.0.1" if version_match else False,
    "English only": not has_turkish,
    "Author attribution": all([author_present, email_present, github_present, linkedin_present]),
    "100% TOOL_METADATA coverage": metadata_coverage == 100,
    "No emoji": not emoji_pattern.search(content),
    "Module docstring": content.startswith('"""') or content.startswith("'''"),
    "Pure Logic imports": not missing_imports,
    "Config class": bool(re.search(config_class_pattern, content)),
    "__all__ exports": '__all__ = [' in content,
    "Try-except pattern": functions_with_try_except >= len(public_functions) * 0.8,
}

passed = sum(checks.values())
total = len(checks)
score = (passed / total) * 100

print(f"\nCHECKS PASSED: {passed}/{total} ({score:.1f}%)")
print()

for check, result in checks.items():
    status = "✅" if result else "❌"
    print(f"{status} {check}")

print()

if score == 100:
    print("🎉 PERFECT SCORE - ALL CHECKLIST REQUIREMENTS MET!")
    print("✅ PRODUCTION READY")
elif score >= 90:
    print("✅ EXCELLENT - Minor issues only")
    print("✅ PRODUCTION READY with minor fixes")
elif score >= 80:
    print("⚠️  GOOD - Some requirements need attention")
    print("⚠️  Address issues before production")
else:
    print("❌ NEEDS WORK - Multiple requirements not met")
    print("❌ Not ready for production")

print()
print("=" * 80)
print("VERIFICATION COMPLETE")
print("=" * 80)
