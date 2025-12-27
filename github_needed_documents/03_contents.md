# GitHub Contents API Reference

**Source:** https://docs.github.com/en/rest/repos/contents  
**API Version:** 2022-11-28

---

## Overview

The Contents API allows you to create, read, update, and delete Base64-encoded file content in a repository. It also supports reading directory contents and downloading repository archives.

---

## Required Permissions

**Fine-grained Token Permissions:**
- **Read Operations:** "Contents" repository permissions (read)
- **Write Operations:** "Contents" repository permissions (write)
- Public repositories can be accessed without authentication

---

## Get Repository Content

**Endpoint:** `GET /repos/{owner}/{repo}/contents/{path}`

### Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| owner | string | Yes | Repository owner (not case sensitive) |
| repo | string | Yes | Repository name without .git (not case sensitive) |
| path | string | Yes | File or directory path |
| ref | string | No | Branch/tag/commit (default: default branch) |

### Response Status Codes
- **200:** OK
- **302:** Found (redirect)
- **304:** Not modified
- **403:** Forbidden
- **404:** Resource not found

---

## Response Types

### File Response
```json
{
  "type": "file",
  "encoding": "base64",
  "size": 5362,
  "name": "README.md",
  "path": "README.md",
  "content": "IyBZb2dhIEJvmsgaW4gcHJvZ3Jlc3MhIEZlZWwgdAoKOndhcm5pbmc6...",
  "sha": "3d21ec53a331a6f037a91c368710b99387d012c1",
  "url": "https://api.github.com/repos/octokit/octokit.rb/contents/README.md",
  "git_url": "https://api.github.com/repos/.../git/blobs/...",
  "html_url": "https://github.com/octokit/octokit.rb/blob/master/README.md",
  "download_url": "https://raw.githubusercontent.com/.../README.md",
  "_links": {
    "git": "...",
    "self": "...",
    "html": "..."
  }
}
```

### Directory Response (Array)
```json
[
  {
    "type": "file",
    "size": 625,
    "name": "octokit.rb",
    "path": "lib/octokit.rb",
    "sha": "fff6fe3a23bf1c8ea0692b4a883af99bee26fd3b",
    "url": "https://api.github.com/repos/.../contents/lib/octokit.rb",
    "git_url": "...",
    "html_url": "...",
    "download_url": "...",
    "_links": {...}
  },
  {
    "type": "dir",
    "size": 0,
    "name": "octokit",
    "path": "lib/octokit",
    "sha": "a84d88e7554fc1fa21bcbc4efae3c782a70d2b9d",
    "url": "https://api.github.com/repos/.../contents/lib/octokit",
    "git_url": "...",
    "html_url": "...",
    "download_url": null,
    "_links": {...}
  }
]
```

---

## File Size Limits

| File Size | Supported Features |
|-----------|-------------------|
| ≤ 1 MB | All features supported |
| 1-100 MB | Only `raw` or `object` media types; `content` field empty with `object` type |
| > 100 MB | Endpoint not supported (use Git API) |

---

## Custom Media Types

| Media Type | Description |
|------------|-------------|
| `application/vnd.github.raw+json` | Raw file contents |
| `application/vnd.github.html+json` | HTML-rendered content |
| `application/vnd.github.object+json` | Consistent object format (directories as objects with `entries` array) |

---

## Get File Content (Base64 Decoded)

**Important:** The `content` field contains Base64-encoded data that must be decoded:

```python
import base64

# Decode content field
file_content = base64.b64decode(response["content"]).decode('utf-8')
```

---

## List Directory Contents

**Endpoint:** `GET /repos/{owner}/{repo}/contents/{path}`

### Notes
- Omit `path` parameter to get root directory contents
- Returns array of file/directory objects
- Submodules have `"type": "file"` (backwards compatibility)
- Maximum 1,000 files per directory (use Git Trees API for more)

---

## Create or Update File Contents

**Endpoint:** `PUT /repos/{owner}/{repo}/contents/{path}`

### Required Headers
```python
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": "Bearer <TOKEN>",
    "X-GitHub-Api-Version": "2022-11-28"
}
```

### Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| owner | string | Yes | Repository owner |
| repo | string | Yes | Repository name |
| path | string | Yes | File path |
| message | string | Yes | Commit message |
| content | string | Yes | Base64-encoded file content |
| sha | string | Conditional | Required if updating existing file (blob SHA) |
| branch | string | No | Branch name (default: default branch) |
| committer | object | No | Committer info (name, email) |
| author | object | No | Author info (name, email) |

### Request Body Example
```json
{
  "message": "my commit message",
  "committer": {
    "name": "Monalisa Octocat",
    "email": "octocat@github.com"
  },
  "content": "bXkgbmV3IGZpbGUgY29udGVudHM="
}
```

### Response Status Codes
- **200:** OK (file updated)
- **201:** Created (new file)
- **404:** Resource not found
- **409:** Conflict
- **422:** Validation failed or endpoint spammed

### Response Example
```json
{
  "content": {
    "name": "hello.txt",
    "path": "notes/hello.txt",
    "sha": "95b966ae1c166bd92f8ae7d1c313e738c731dfc3",
    "size": 9,
    "url": "...",
    "html_url": "...",
    "git_url": "...",
    "download_url": "...",
    "type": "file",
    "_links": {...}
  },
  "commit": {
    "sha": "7638417db6d59f3c431d3e1f261cc637155684cd",
    "url": "...",
    "html_url": "...",
    "author": {...},
    "committer": {...},
    "message": "my commit message",
    "tree": {...},
    "parents": [...]
  }
}
```

### Important Notes
- **Do not use concurrently** with Delete endpoint (causes conflicts)
- Content must be Base64 encoded before sending
- Requires `workflow` scope for `.github/workflows` directory
- For updates, must provide current file's `sha`

---

## Delete a File

**Endpoint:** `DELETE /repos/{owner}/{repo}/contents/{path}`

### Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| owner | string | Yes | Repository owner |
| repo | string | Yes | Repository name |
| path | string | Yes | File path |
| message | string | Yes | Commit message |
| sha | string | Yes | Blob SHA of file being deleted |
| branch | string | No | Branch name (default: default branch) |
| committer | object | No | Committer info (name, email) |
| author | object | No | Author info (name, email) |

### Response Status Codes
- **200:** OK
- **404:** Resource not found
- **409:** Conflict
- **422:** Validation failed or endpoint spammed
- **503:** Service unavailable

### Important Notes
- **Do not use concurrently** with Create/Update endpoint
- Must provide correct file `sha`
- Returns commit information with `content: null`

---

## Get Repository README

**Endpoint:** `GET /repos/{owner}/{repo}/readme`

### Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| owner | string | Yes | Repository owner |
| repo | string | Yes | Repository name |
| ref | string | No | Branch/tag/commit (default: default branch) |

### Response Status Codes
- **200:** OK
- **304:** Not modified
- **404:** Resource not found
- **422:** Validation failed

### Notes
- Returns preferred README file
- Same response format as Get Repository Content (file type)
- Supports `raw` and `html` media types

---

## Implementation Notes for github-ops.py

### get_file_content(owner, repo, path, ref=None)
- Use GET /repos/{owner}/{repo}/contents/{path}
- Decode Base64 content automatically
- Return decoded string content
- Handle file size limits (max 1 MB for full content)
- Support optional `ref` parameter for specific commits/branches

```python
def get_file_content(owner, repo, path, ref=None):
    params = {"ref": ref} if ref else {}
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        if data["type"] == "file":
            # Decode Base64 content
            content = base64.b64decode(data["content"]).decode('utf-8')
            return content
        else:
            raise ValueError(f"Path '{path}' is a directory, not a file")
```

### list_repository_contents(owner, repo, path='', ref=None)
- Use GET /repos/{owner}/{repo}/contents/{path}
- Return list of dicts with name, type, size, path, sha, download_url
- Handle both root directory (path='') and subdirectories
- Filter out unnecessary fields for simplified response

```python
def list_repository_contents(owner, repo, path='', ref=None):
    params = {"ref": ref} if ref else {}
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        # Handle directory (array) vs file (object)
        if isinstance(data, list):
            return [{
                "name": item["name"],
                "path": item["path"],
                "type": item["type"],
                "size": item["size"],
                "sha": item["sha"],
                "url": item.get("download_url")
            } for item in data]
```

### Error Handling
- **403:** Rate limit exceeded or forbidden (private repo without access)
- **404:** Repository, file, or path not found
- **422:** Invalid path or ref parameter
- Handle large files gracefully (> 1 MB warning, > 100 MB error)

### Base64 Encoding/Decoding
```python
import base64

# Encode for create/update
content_bytes = file_content.encode('utf-8')
content_base64 = base64.b64encode(content_bytes).decode('utf-8')

# Decode for reading
content = base64.b64decode(data["content"]).decode('utf-8')
```

### Download URLs
- Expire quickly (use once)
- For fresh download URLs, re-query the Contents API
- Raw file URLs: `https://raw.githubusercontent.com/{owner}/{repo}/{ref}/{path}`

### Pagination
- Directory listings limited to 1,000 files
- Use Git Trees API for larger directories
- No pagination parameters on this endpoint
