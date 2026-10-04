# Python Security Hardening Checklist

## Input and Code
- [x] Validate external input and enforce application-specific limits
- [x] Avoid dangerous dynamic execution
- [x] Use parameterized database queries

## Secrets and Credentials
- [x] Keep secrets out of source code
- [x] Keep sensitive values out of application logs
- [x] Store passwords using secure password hashing
- [x] Generate security-sensitive tokens using secure randomness and expiration

## Authentication and Authorization
- [x] Require authentication for protected operations
- [x] Verify authorization before accessing user-owned resources

## Error Handling
- [x] Return controlled error responses without exposing internal details

## Dependencies and CI/CD
- [x] Review dependencies for known vulnerabilities
- [x] Scan source code with Bandit
- [x] Scan dependencies with pip-audit
- [x] Scan for exposed secrets with Gitleaks