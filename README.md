# Secure REST API Development with CI/CD and Real CVE Vulnerability Analysis
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

## Implemented Security Measures

### 1. Authentication Mechanism

Stateless authentication based on JWT (JSON Web Token) is adopted.

- When the user submits correct username and password, the server generates a cryptographically signed JWT token with expiration time.
- All protected endpoints check the token signature, expiration status and validity from the `Authorization: Bearer` request header.
- Requests missing a token, carrying an invalid signature or expired token will be rejected with HTTP 401 Unauthorized response.
- User passwords are never stored as plaintext. Passwords are hashed by bcrypt before writing into the database. Bcrypt includes automatic salt generation and is resistant to rainbow table attacks.

### 2. SQL Injection Mitigation

All database interactions use Flask-SQLAlchemy ORM instead of raw SQL string concatenation.

- ORM automatically converts input parameters into parameterized prepared statements. User-controlled input is strictly separated from SQL query logic.
- User input will not be spliced directly into SQL strings, so attackers cannot alter the structure of SQL queries. This blocks standard SQL injection, including union injection and boolean blind injection.

### 3. Cross‑Site Scripting (XSS) Mitigation

This API returns structured JSON data rather than rendering HTML pages.

- For any user-controllable content returned in JSON payload, special HTML characters are escaped.
- If HTML template rendering is introduced later, Flask Jinja2 default auto-escaping is kept enabled to sanitize user input.
- The API refuses to return raw unsanitized user input as HTML content, preventing both reflected XSS and stored XSS attacks.

### 4. Additional Security Controls

- Input validation: API parses and validates incoming JSON fields; reject malformed or unexpected input.
- CI/CD automatic security scanning runs on every git commit:
  - Bandit: SAST (Static Application Security Testing) tool, scans Python source code for insecure coding patterns.
  - Safety: SCA (Software Composition Analysis) tool, scans dependency list for packages with known public vulnerabilities.
- Scan reports are generated as pipeline artifacts for manual review.

## SAST / SCA Scan Report from GitHub Actions

> 
> Insert Bandit SAST scan screenshot here
> Insert Safety SCA dependency scan screenshot here

## CVE Research: CVE-2022-44268

### Vulnerability Overview

CVE‑2022‑44268 is an arbitrary local file disclosure vulnerability within ImageMagick, a widely used open-source image processing library. Affected versions of ImageMagick can parse maliciously crafted PNG image files. When the library processes this PNG, it reads arbitrary files from the server local filesystem and embeds the target file’s content into the output image. An attacker can retrieve sensitive local files such as configuration files, credential files and source code. This vulnerability does not allow remote code execution, only local file content leakage.

### Reproduction Environment

- Vulnerable service: ImageMagick 7.1.0-50
- Deployment method: Docker Compose, isolated container environment
- Configuration file: docker-compose.yml

### Reproduction Sequence & Commands

1. Enter the vulnerability working directory

```
cd vulhub/spring/CVE-2022-44268
```

2. Start vulnerable container

```
docker compose up -d
```

3. Create malicious PNG payload using PoC script
4. Upload the crafted PNG to the image processing service
5. Download the converted output image
6. Extract leaked local file content from output image

> 
> Insert reproduction operation screenshots, terminal command screenshots and payload screenshots here

### Root Cause Analysis (original description)

The vulnerability comes from the parsing logic of PNG profile chunks in ImageMagick. The library supports reading external profile files referenced inside PNG metadata. The developer did not add sufficient path validation and access restriction for the file path extracted from PNG metadata. Attackers can place an arbitrary absolute file path inside the PNG profile field. When ImageMagick loads this PNG, it treats the path as a valid profile file and reads the content of the target file on the host, then embeds the read bytes into the generated picture. Because there is no whitelist or path sanitization check, any file accessible by the ImageMagick process can be leaked.

### Applied Fix Description

The official fix adds strict validation for file paths parsed from PNG metadata:

1. Block access to arbitrary absolute paths.
2. Restrict profile loading to only files inside the designated safe directory.
3. Sanitize path strings to filter path traversal characters such as `../`.
After the patch, ImageMagick refuses to open files outside the permitted directory, so attackers cannot read arbitrary local files through malicious PNG metadata.

### Post-fix Verification

After applying the patched version of ImageMagick, reuse the same malicious PNG payload for repeated testing. The service will process the image normally, but no local file content will be embedded into the output image. The attack fails and sensitive file leakage no longer occurs.
