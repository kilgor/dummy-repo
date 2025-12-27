# GitHub REST API - Authentication

Source: https://docs.github.com/en/rest/authentication/authenticating-to-the-rest-api

## Key Points for Implementation

### Authentication Header Format
```bash
Authorization: Bearer YOUR-TOKEN
# OR
Authorization: token YOUR-TOKEN
```

### Example Request
```bash
curl --request GET \
--url "https://api.github.com/octocat" \
--header "Authorization: Bearer YOUR-TOKEN" \
--header "X-GitHub-Api-Version: 2022-11-28"
```

### Personal Access Token (PAT)
- Fine-grained PAT (recommended) - requires specific permissions per endpoint
- Classic PAT - requires scopes (repo, read:org, etc.)
- Tokens act as your identity with limited scopes/permissions
- Keep tokens secure - treat as passwords

### Authentication Errors
- `401 Unauthorized` - Invalid credentials
- `403 Forbidden` - Insufficient permissions or rate limit exceeded
- `404 Not Found` - Token lacks permissions or resource doesn't exist

### Rate Limits
- Authenticated requests: Higher rate limit
- Failed login attempts: Temporary `403 Forbidden` for all requests

### Required Headers
```python
headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json",
    "X-GitHub-Api-Version": "2022-11-28"
}
```

### Base URL
```
https://api.github.com
```
