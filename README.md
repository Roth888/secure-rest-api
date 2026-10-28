# Secure REST API Development with CI/CD and Real CVE Vulnerability Analysis
Repository URL: https://github.com/Roth888/secure-rest-api
Last successful CI pipeline run: https://github.com/Roth888/secure-rest-api/actions/runs/39364923789

## Purpose
This laboratory work aims to build a secure Flask-based REST API that mitigates common OWASP Top 10 web vulnerabilities. The project integrates automated SAST and SCA security scanning into GitHub Actions CI/CD pipeline to continuously detect insecure code patterns and vulnerable third-party dependencies.
Additionally, this lab selects CVE-2022-44268 (ImageMagick Arbitrary Local File Read vulnerability) for independent vulnerability research, environment reproduction, root cause analysis, patch application and post-fix verification. The goal is to understand exploitation principles and validate effective remediation strategies.

## Project & API Endpoints
### Tech Stack
Python 3, Flask, Flask-SQLAlchemy, Flask-JWT-Extended, bcrypt, SQLite
- Flask: lightweight web framework to implement REST interfaces
- Flask-SQLAlchemy: ORM for database operation
- Flask-JWT-Extended: implement JWT stateless authentication
- bcrypt: secure password hashing algorithm
- SQLite: lightweight file-based relational database

### API Specification
| Method | Endpoint | Access Control | Description |
|---|---|---|---|
| POST | `/auth/login` | Public | Accept username and password, verify credentials, issue signed JWT access token |
| GET | `/api/data` | Protected | Return list of user records; only accessible with valid JWT token |
| GET | `/api/profile` | Protected | Return username of currently authenticated user; only accessible with valid JWT token |

### Test Commands (curl)
```bash
# Step 1: Request JWT token by login
curl -X POST http://127.0.0.1:5000/auth/login \
-H "Content-Type: application/json" \
-d '{"username":"admin","password":"Admin123!"}'

# Step 2: Use obtained token to access protected /api/data
curl http://127.0.0.1:5000/api/data \
-H "Authorization: Bearer <YOUR_TOKEN>"

# Step 3: Use obtained token to access protected /api/profile
curl http://127.0.0.1:5000/api/profile \
-H "Authorization: Bearer <YOUR_TOKEN>"
