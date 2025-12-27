"""
Verify ALL core functions have TOOL_METADATA
"""

import re

# Read github-ops.py
with open('library/external-operations/github-ops.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find all function definitions
functions = []
for match in re.finditer(r'^def ([a-z_]+)\(', content, re.MULTILINE):
    fname = match.group(1)
    
    # Skip helper functions starting with underscore
    if fname.startswith('_'):
        continue
    
    # Check if TOOL_METADATA exists within next 2000 chars
    func_section = content[match.start():match.start()+2000]
    has_metadata = 'TOOL_METADATA:' in func_section
    
    functions.append((fname, has_metadata))

# Report
print("=" * 70)
print("TOOL_METADATA VERIFICATION")
print("=" * 70)
print(f"\nTotal core functions: {len(functions)}")
print(f"With TOOL_METADATA: {sum(1 for _, has in functions if has)}")
print(f"Without TOOL_METADATA: {sum(1 for _, has in functions if not has)}")

# List functions without TOOL_METADATA
missing = [name for name, has in functions if not has]
if missing:
    print(f"\n❌ MISSING TOOL_METADATA:")
    for name in missing:
        print(f"   - {name}")
else:
    print(f"\n✅ ALL {len(functions)} FUNCTIONS HAVE TOOL_METADATA")

print("\nAll functions:")
for i, (name, has) in enumerate(functions, 1):
    status = "✅" if has else "❌"
    print(f"  {i:2d}. {status} {name}")

print("=" * 70)
