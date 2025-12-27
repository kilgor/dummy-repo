# GitHub Issues API Reference

**Source:** https://docs.github.com/en/rest/issues/issues  
**API Version:** 2022-11-28

---

## Overview

The Issues API allows you to manage issues and pull requests. GitHub's REST API treats every pull request as an issue, but not every issue is a pull request.

**Important Notes:**
- Pull requests have a `pull_request` key in the response
- The `id` returned is an issue id, not a pull request id
- Use the Pull Requests endpoint to get pull request IDs

---

## Required Permissions

**Fine-grained Token Permissions:**
- **Read Operations:** "Issues" repository permissions (read)
- **Write Operations:** "Issues" repository permissions (write)
- Public repositories can be accessed without authentication

---

## List Repository Issues

**Endpoint:** `GET /repos/{owner}/{repo}/issues`

### Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| owner | string | Yes | Repository owner (not case sensitive) |
| repo | string | Yes | Repository name without .git (not case sensitive) |
| milestone | string | No | Milestone number, `*` (any), or `none` |
| state | string | No | `open`, `closed`, or `all` (default: `open`) |
| assignee | string | No | Username, `none`, or `*` (any) |
| creator | string | No | Username of issue creator |
| mentioned | string | No | Username mentioned in issue |
| labels | string | No | Comma-separated label names (e.g., `bug,ui,@high`) |
| sort | string | No | `created`, `updated`, or `comments` (default: `created`) |
| direction | string | No | `asc` or `desc` (default: `desc`) |
| since | string | No | ISO 8601 timestamp (YYYY-MM-DDTHH:MM:SSZ) |
| per_page | integer | No | Results per page, max 100 (default: 30) |
| page | integer | No | Page number (default: 1) |

### Response Status Codes
- **200:** OK
- **301:** Moved permanently
- **404:** Resource not found
- **422:** Validation failed or endpoint spammed

### Key Response Fields
```json
{
  "id": 1,
  "number": 1347,
  "state": "open",
  "title": "Found a bug",
  "body": "I'm having a problem with this.",
  "user": { "login": "octocat", ... },
  "labels": [{"name": "bug", "color": "f29513", ...}],
  "assignee": { "login": "octocat", ... },
  "assignees": [...],
  "milestone": {...},
  "comments": 0,
  "created_at": "2011-04-22T13:33:48Z",
  "updated_at": "2011-04-22T13:33:48Z",
  "closed_at": null,
  "author_association": "COLLABORATOR",
  "state_reason": "completed"
}
```

---

## Create an Issue

**Endpoint:** `POST /repos/{owner}/{repo}/issues`

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
| title | string/integer | Yes | Issue title |
| body | string | No | Issue contents |
| assignees | array[string] | No | Usernames to assign (requires push access) |
| milestone | integer/string | No | Milestone number (requires push access) |
| labels | array | No | Label names (requires push access) |
| type | string | No | Issue type name (requires push access) |

### Request Body Example
```json
{
  "title": "Found a bug",
  "body": "I'm having a problem with this.",
  "assignees": ["octocat"],
  "milestone": 1,
  "labels": ["bug"]
}
```

### Response Status Codes
- **201:** Created
- **400:** Bad Request
- **403:** Forbidden
- **404:** Resource not found
- **410:** Gone (issues disabled)
- **422:** Validation failed or endpoint spammed
- **503:** Service unavailable

### Notes
- Triggers notifications (subject to secondary rate limiting)
- Assignees, labels, and milestones are silently dropped without push access

---

## Update an Issue

**Endpoint:** `PATCH /repos/{owner}/{repo}/issues/{issue_number}`

### Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| owner | string | Yes | Repository owner |
| repo | string | Yes | Repository name |
| issue_number | integer | Yes | Issue number |
| title | string/integer | No | New title |
| body | string | No | New body |
| state | string | No | `open` or `closed` |
| state_reason | string | No | `completed`, `not_planned`, `duplicate`, `reopened`, or `null` |
| assignees | array[string] | No | Replace assignees (pass `[]` to clear) |
| milestone | integer/string | No | Milestone number or `null` to remove |
| labels | array | No | Replace labels (pass `[]` to clear) |
| type | string | No | Issue type name or `null` to remove |

### Request Body Example
```json
{
  "title": "Found a bug",
  "body": "I'm having a problem with this.",
  "assignees": ["octocat"],
  "milestone": 1,
  "state": "open",
  "labels": ["bug"]
}
```

### Response Status Codes
- **200:** OK
- **301:** Moved permanently
- **403:** Forbidden
- **404:** Resource not found
- **410:** Gone
- **422:** Validation failed or endpoint spammed
- **503:** Service unavailable

### Notes
- Issue owners and users with push access or Triage role can edit
- Assignees, labels, milestones silently dropped without push access

---

## Get an Issue

**Endpoint:** `GET /repos/{owner}/{repo}/issues/{issue_number}`

### Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| owner | string | Yes | Repository owner |
| repo | string | Yes | Repository name |
| issue_number | integer | Yes | Issue number |

### Response Status Codes
- **200:** OK
- **301:** Moved permanently (issue transferred)
- **304:** Not modified
- **404:** Resource not found (no read access or deleted)
- **410:** Gone (issue deleted from readable repository)

### Notes
- Returns same JSON structure as list endpoint
- Subscribe to `issues` webhook for transfer/delete events

---

## List Issues Assigned to Authenticated User

**Endpoint:** `GET /issues`

### Parameters
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| filter | string | No | `assigned`, `created`, `mentioned`, `subscribed`, `repos`, or `all` (default: `assigned`) |
| state | string | No | `open`, `closed`, or `all` (default: `open`) |
| labels | string | No | Comma-separated label names |
| sort | string | No | `created`, `updated`, or `comments` (default: `created`) |
| direction | string | No | `asc` or `desc` (default: `desc`) |
| since | string | No | ISO 8601 timestamp |
| per_page | integer | No | Results per page, max 100 (default: 30) |
| page | integer | No | Page number (default: 1) |

### Response Status Codes
- **200:** OK
- **304:** Not modified
- **404:** Resource not found
- **422:** Validation failed or endpoint spammed

### Notes
- Returns issues across all visible repositories
- Includes owned, member, and organization repositories

---

## Custom Media Types

All issue endpoints support these custom media types:

| Media Type | Description |
|------------|-------------|
| `application/vnd.github.raw+json` | Raw markdown body (default) |
| `application/vnd.github.text+json` | Text-only representation |
| `application/vnd.github.html+json` | HTML rendered markdown |
| `application/vnd.github.full+json` | All formats (raw, text, HTML) |

---

## Implementation Notes for github-ops.py

### list_issues(owner, repo, state='open', labels=None)
- Use GET /repos/{owner}/{repo}/issues
- Filter by state and labels
- Handle pagination for large result sets
- Return list of simplified issue dicts (id, number, title, state, labels, assignees, created_at)

### create_issue(owner, repo, title, body, labels=None)
- Use POST /repos/{owner}/{repo}/issues
- Require title (mandatory)
- Optional body and labels
- Handle 201 (success) and 422 (validation errors)
- Return created issue dict

### update_issue(owner, repo, issue_number, title=None, body=None, state=None)
- Use PATCH /repos/{owner}/{repo}/issues/{issue_number}
- Allow partial updates (only provided fields)
- Support state changes (open/closed)
- Handle 200 (success) and 404 (not found)
- Return updated issue dict

### Error Handling
- **401:** Invalid or missing token
- **403:** Rate limit exceeded or forbidden
- **404:** Repository or issue not found / no read access
- **422:** Validation failed (check title, state values)
- **503:** Service temporarily unavailable (retry with backoff)

### Rate Limiting
- Authenticated requests: Higher limits
- Creating issues triggers notifications (secondary rate limits)
- Use exponential backoff on 403 responses

### Pagination
- Default: 30 items per page
- Max: 100 items per page
- Use `page` parameter for subsequent pages
- Check response headers for pagination info
