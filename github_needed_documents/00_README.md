# GitHub REST API Documentation

**Purpose:** Reference documentation for implementing `github-ops.py`  
**API Version:** 2022-11-28  
**Base URL:** `https://api.github.com`  
**Status:** ✅ Documentation Complete

---

## Documentation Files

### ✅ 01_authentication.md
**Topics Covered:**
- Bearer token authentication (Personal Access Token)
- Required headers (Authorization, Accept, X-GitHub-Api-Version)
- Token scopes and permissions
- Error codes (401, 403, 404)
- Rate limiting
- Fine-grained vs Classic PATs

**Key Takeaway:** All requests require `Authorization: Bearer {token}` header with fine-grained PAT having appropriate repository permissions.

---

### ✅ 02_issues.md
**Topics Covered:**
- List repository issues (GET /repos/{owner}/{repo}/issues)
- Create issue (POST /repos/{owner}/{repo}/issues)
- Update issue (PATCH /repos/{owner}/{repo}/issues/{issue_number})
- Get issue (GET /repos/{owner}/{repo}/issues/{issue_number})
- List issues assigned to user (GET /issues)
- Query parameters (state, labels, assignees, milestone, etc.)
- Pagination (per_page, page)
- Custom media types (raw, text, html, full)

**Key Takeaway:** Issues API is comprehensive with filtering, sorting, and pagination. Requires "Issues" repository permissions (read for GET, write for POST/PATCH).

---

### ✅ 03_contents.md
**Topics Covered:**
- Get file content (GET /repos/{owner}/{repo}/contents/{path})
- List directory contents (GET /repos/{owner}/{repo}/contents/{path})
- Create/update file (PUT /repos/{owner}/{repo}/contents/{path})
- Delete file (DELETE /repos/{owner}/{repo}/contents/{path})
- Get README (GET /repos/{owner}/{repo}/readme)
- Base64 encoding/decoding
- File size limits (1 MB, 100 MB)
- Custom media types (raw, html, object)

**Key Takeaway:** Contents API uses Base64 encoding for file content. Requires "Contents" repository permissions (read for GET, write for PUT/DELETE). Do not use Create/Update and Delete concurrently.

---

## Planned github-ops.py Functions

Based on the gathered documentation, here are the 8 core functions to implement:

### Repository Operations (3 functions)
1. **list_repositories(owner=None, type='all', sort='full_name')**
   - Endpoints: GET /user/repos, GET /users/{username}/repos, GET /orgs/{org}/repos
   - Permissions: No permissions required (public), or "Metadata" (private)
   - Returns: List of repository dicts with key fields

2. **get_repository_info(owner, repo)**
   - Endpoint: GET /repos/{owner}/{repo}
   - Permissions: "Metadata" repository permissions (read)
   - Returns: Detailed repository dict

3. **search_repositories(query, sort='stars', order='desc')**
   - Endpoint: GET /search/repositories (not yet documented, defer implementation)
   - Note: May require additional search API documentation

### Issue Operations (3 functions)
4. **list_issues(owner, repo, state='open', labels=None)**
   - Endpoint: GET /repos/{owner}/{repo}/issues
   - Permissions: "Issues" repository permissions (read)
   - Returns: List of issue dicts

5. **create_issue(owner, repo, title, body='', labels=None)**
   - Endpoint: POST /repos/{owner}/{repo}/issues
   - Permissions: "Issues" repository permissions (write)
   - Returns: Created issue dict

6. **update_issue(owner, repo, issue_number, title=None, body=None, state=None, labels=None)**
   - Endpoint: PATCH /repos/{owner}/{repo}/issues/{issue_number}
   - Permissions: "Issues" repository permissions (write)
   - Returns: Updated issue dict

### Contents Operations (2 functions)
7. **get_file_content(owner, repo, path, ref=None)**
   - Endpoint: GET /repos/{owner}/{repo}/contents/{path}
   - Permissions: "Contents" repository permissions (read)
   - Returns: Decoded file content (string)

8. **list_repository_contents(owner, repo, path='', ref=None)**
   - Endpoint: GET /repos/{owner}/{repo}/contents/{path}
   - Permissions: "Contents" repository permissions (read)
   - Returns: List of file/directory dicts

---

## Implementation Checklist

### Phase 1: Setup ✅ COMPLETE
- [x] Create documentation folder
- [x] Fetch Authentication API documentation
- [x] Fetch Issues API documentation
- [x] Fetch Contents API documentation
- [x] Document key endpoints and parameters
- [x] Identify required permissions

### Phase 2: User Action Required ⏳ PENDING
- [ ] User creates Personal Access Token on GitHub
  - URL: https://github.com/settings/tokens
  - Type: Fine-grained Personal Access Token
  - Permissions needed:
    * **Repository Access:** Select repositories or all repositories
    * **Repository Permissions:**
      - Metadata: Read (default, required)
      - Contents: Read
      - Issues: Read and Write
  - Token name suggestion: "ONE_TOOL_Development"
  - Expiration: 90 days (or custom)
- [ ] User stores token in `.env` file
  ```
  GITHUB_TOKEN=github_pat_xxxxxxxxxxxxx
  ```

### Phase 3: Implementation 🔄 READY
- [ ] Copy `blueprints/ops-blueprint.py` to `library/external-operations/github-ops.py`
- [ ] Implement GitHubConfig class
  - Load GITHUB_TOKEN from .env
  - Set base_url = "https://api.github.com"
  - Set headers with Authorization, Accept, X-GitHub-Api-Version
  - Add default_owner (optional)
- [ ] Implement 8 core functions with TOOL_METADATA
- [ ] Add comprehensive error handling (401, 403, 404, 422)
- [ ] Add rate limit detection and warnings
- [ ] Test read-only operations first (list_repositories, get_file_content)
- [ ] Test write operations carefully (create_issue, update_issue)
- [ ] Update operations_registry.json
- [ ] Sync to aimcp_creation folder

### Phase 4: Testing 🧪 NOT STARTED
- [ ] Authentication validation
- [ ] List repositories (user's repos)
- [ ] Get repository info (department-agents repo)
- [ ] List issues (existing repo)
- [ ] Create test issue
- [ ] Update test issue (close it)
- [ ] Get file content (AGENTS.md)
- [ ] List directory contents (root)
- [ ] Full integration test (manage ONE TOOL via github-ops)

---

## API Patterns Observed

### Common Headers (All Requests)
```python
headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": "Bearer {token}",
    "X-GitHub-Api-Version": "2022-11-28"
}
```

### Common Query Parameters
- **Pagination:** `per_page` (max 100, default 30), `page` (default 1)
- **Sorting:** `sort`, `direction` (asc/desc)
- **Filtering:** `state`, `labels`, `type`, `ref`
- **Date Filtering:** `since` (ISO 8601 format)

### Common Response Status Codes
- **200:** OK (successful GET)
- **201:** Created (successful POST)
- **204:** No Content (successful DELETE)
- **301:** Moved Permanently (resource transferred)
- **304:** Not Modified (cached response valid)
- **400:** Bad Request (invalid parameters)
- **401:** Unauthorized (invalid/missing token)
- **403:** Forbidden (rate limit or no permission)
- **404:** Not Found (resource doesn't exist or no access)
- **409:** Conflict (concurrent modification)
- **422:** Validation Failed (invalid data)
- **503:** Service Unavailable (GitHub outage)

### Error Handling Pattern
```python
if response.status_code == 200:
    return response.json()
elif response.status_code == 401:
    raise AuthenticationError("Invalid or missing GitHub token")
elif response.status_code == 403:
    raise RateLimitError("Rate limit exceeded or forbidden")
elif response.status_code == 404:
    raise NotFoundError(f"Resource not found: {url}")
elif response.status_code == 422:
    raise ValidationError(f"Validation failed: {response.json()}")
else:
    raise GitHubAPIError(f"Unexpected error: {response.status_code}")
```

---

## Rate Limiting

**Authenticated Requests:**
- **Primary Rate Limit:** 5,000 requests/hour
- **Secondary Rate Limit:** Triggered by rapid content creation (issues, comments)
- **Check Headers:** `X-RateLimit-Remaining`, `X-RateLimit-Reset`

**Best Practices:**
- Use authenticated requests (higher limits)
- Implement exponential backoff on 403 responses
- Cache responses where appropriate
- Monitor rate limit headers
- Use conditional requests (If-None-Match, If-Modified-Since)

---

## Next Steps

**Immediate Action Required:**
1. User creates Personal Access Token (see Phase 2 checklist)
2. User stores token in `.env` file

**After Token Created:**
1. Begin implementation (Phase 3)
2. Test incrementally (Phase 4)
3. Validate with real ONE TOOL repository

**Optional Future Enhancements:**
- Add search_repositories() function (requires Search API docs)
- Add webhook support for real-time notifications
- Add pull request operations
- Add repository creation/deletion
- Add branch and commit operations
- Add GitHub Actions workflow triggering

---

## Documentation Sources

All documentation sourced from official GitHub REST API documentation:
- Authentication: https://docs.github.com/en/rest/authentication/authenticating-to-the-rest-api
- Repositories: https://docs.github.com/en/rest/repos/repos
- Issues: https://docs.github.com/en/rest/issues/issues
- Contents: https://docs.github.com/en/rest/repos/contents

**Documentation Date:** December 26, 2025  
**API Version:** 2022-11-28 (stable)
