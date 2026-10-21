# Secure REST API Development with CI/CD and Real CVE Vulnerability Analysis

## Purpose
Develop secure REST API with OWASP Top‑10 protections, integrate SAST/SCA into GitHub Actions CI/CD. Reproduce, analyse and remediate CVE‑2022‑44268 in Vulhub isolated environment.

Repository URL: https://github.com/Roth888/secure-rest-api

CI successful run link: https://github.com/Roth888/secure-rest-api/actions/runs/39364923789

## Project & API endpoints
Tech stack: Python3, Flask, Flask‑SQLAlchemy, JWT‑Extended, bcrypt, SQLite

1. `POST /auth/login`
- Input JSON: `{"username":"admin","password":"Admin123!"}`
- Return JWT token for protected interfaces.

2. `GET /api/data` (Protected)
- Header: `Authorization: Bearer <JWT_TOKEN>`
- Return user list, reject request without valid token.

3. `GET /api/profile` (Custom, Protected)
- Header: `Authorization: Bearer <JWT_TOKEN>`
- Return current login username.

Test curl example:
```bash
# get token
curl -X POST http://127.0.0.1:5000/auth/login -H "Content‑Type:application/json" -d "{\"username\":\"admin\",\"password\":\"Admin123!\"}"

# access protected api
curl http://127.0.0.1:5000/api/data -H "Authorization: Bearer <YOUR_TOKEN>"
