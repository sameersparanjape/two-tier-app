# Implementation Plan: Random Number Service

## Overview

Build a two-tier web application with a FastAPI backend and Bootstrap/Nginx frontend, containerized with Docker, deployed to AWS ECS Fargate via Terraform, with CI/CD through GitHub Actions. Implementation proceeds bottom-up: environment config → backend → frontend → Docker → infrastructure → CI/CD → tests.

## Tasks

- [ ] 1. Set up project structure and environment configuration
  - [ ] 1.1 Create `.gitignore` with entries for `.env`, `.venv/`, `__pycache__/`, `*.tfstate`, `*.tfstate.backup`, `.terraform/`, `.terraform.lock.hcl`
    - _Requirements: 9.2_
  - [ ] 1.2 Create `requirements.txt` with pinned dependencies: `fastapi==0.115.0`, `uvicorn==0.30.6`, `httpx==0.27.2`, `pytest==8.3.3`, `hypothesis==6.112.1`
    - All dependencies must use `==` for version pinning
    - _Requirements: 10.1, 10.2, 10.3_
  - [ ] 1.3 Create `.env` template file (`.env.example`) documenting required variables: `GITHUB_TOKEN`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
    - _Requirements: 9.1, 9.4_

- [ ] 2. Implement backend Random Number Service
  - [ ] 2.1 Create `backend/main.py` with FastAPI app
    - Define `GET /api/random` endpoint returning `{"number": <int 1-100>}`
    - Add CORS middleware allowing all origins with GET and OPTIONS methods
    - Add error handling returning HTTP 500 with `{"error": "<message>"}` on internal failures
    - Mount app under `/api` path prefix
    - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5, 4.3, 5.1, 5.2_
  - [ ] 2.2 Create `backend/Dockerfile`
    - Use Python base image
    - Copy backend code and install dependencies
    - Run uvicorn on port 8000
    - _Requirements: 7.2, 7.4, 8.2_
  - [ ] 2.3 Write backend unit tests in `backend/tests/test_api.py`
    - Test `GET /api/random` returns 200 with valid JSON containing `number` field
    - Test `OPTIONS /api/random` returns CORS headers
    - Test endpoint is mounted under `/api` prefix
    - Use FastAPI TestClient with httpx
    - _Requirements: 1.1, 1.2, 1.3, 5.1, 5.2_

- [ ] 3. Implement frontend static site
  - [ ] 3.1 Create `frontend/index.html` with Bootstrap layout
    - Center number display and refresh button vertically and horizontally
    - Include loading indicator (hidden by default)
    - Include error message area (hidden by default)
    - Use Bootstrap CDN for styling
    - Responsive layout working from 320px to 1920px
    - _Requirements: 2.1, 2.2, 2.3, 3.1, 6.1, 6.2, 6.3_
  - [ ] 3.2 Create `frontend/app.js` with fetch logic
    - On page load, fetch `GET /api/random` and display the number
    - On refresh button click, fetch new number and update display
    - Show loading indicator while request is in flight
    - Disable refresh button during request to prevent duplicates
    - Display error message with status code on non-200 responses
    - Display "Service unavailable" on network errors
    - Use only relative path `/api/random` for all requests (no absolute URLs)
    - _Requirements: 2.1, 2.2, 2.3, 3.1, 3.2, 3.3, 3.4, 4.1, 4.2, 22.1, 22.2, 22.3_
  - [ ] 3.3 Create `frontend/nginx.conf`
    - Serve static files from `/usr/share/nginx/html`
    - Proxy `/api` requests to backend container in local dev
    - Listen on port 80
    - _Requirements: 19.3, 7.3_
  - [ ] 3.4 Create `frontend/Dockerfile`
    - Use Nginx base image
    - Copy `index.html`, `app.js`, and `nginx.conf` into the image
    - Expose port 80
    - _Requirements: 19.1, 19.2, 19.3_

- [ ] 4. Checkpoint - Verify backend and frontend
  - Ensure all backend unit tests pass, ask the user if questions arise.

- [ ] 5. Set up Docker Compose for local development
  - [ ] 5.1 Create `docker-compose.yml` at project root
    - Define `backend` service using `backend/Dockerfile`, expose port 8000
    - Define `frontend` service using `frontend/Dockerfile`, expose port 8080 mapped to 80
    - Configure networking so frontend can proxy `/api` to backend
    - Reference `.env` file for environment variable injection
    - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [ ] 6. Implement Terraform infrastructure
  - [ ] 6.1 Create `infra/variables.tf` and `infra/outputs.tf`
    - Define variables: `aws_region` (default us-east-2), `project_name`, `vpc_cidr`, `frontend_port`, `backend_port`, `cpu`, `memory`
    - Define outputs: ALB DNS name, ECR repository URIs
    - _Requirements: 14.1, 8.1_
  - [ ] 6.2 Create `infra/main.tf` with provider and VPC networking
    - Configure AWS provider for us-east-2
    - Create VPC with CIDR 10.0.0.0/16
    - Create 2 public subnets across 2 availability zones
    - Create Internet Gateway attached to VPC
    - Create route table routing 0.0.0.0/0 through IGW
    - Associate route table with both subnets
    - Use local Terraform state (no remote backend)
    - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.6, 14.2, 14.3, 14.4, 14.5, 14.6_
  - [ ] 6.3 Create `infra/security.tf` with security groups
    - ALB security group: inbound HTTP port 80 from 0.0.0.0/0, all outbound
    - ECS tasks security group: inbound from ALB security group only, all outbound
    - _Requirements: 12.5, 13.2_
  - [ ] 6.4 Create `infra/ecr.tf` with ECR repositories
    - Create ECR repository for frontend
    - Create ECR repository for backend
    - Both in us-east-2
    - _Requirements: 18.1, 18.2_
  - [ ] 6.5 Create `infra/logs.tf` with CloudWatch log groups
    - Create log group `/ecs/random-number-service-frontend` in us-east-2
    - Create log group `/ecs/random-number-service-backend` in us-east-2
    - _Requirements: 23.2, 23.4_
  - [ ] 6.6 Create `infra/alb.tf` with ALB and routing rules
    - Create ALB in public subnets with ALB security group
    - Create target group for frontend (port 80)
    - Create target group for backend (port 8000)
    - Create listener on port 80 with default action to frontend target group
    - Create listener rule routing `/api/*` to backend target group
    - _Requirements: 13.1, 13.2, 13.3, 13.4, 21.1, 21.2, 21.3_
  - [ ] 6.7 Create `infra/ecs.tf` with ECS cluster, task definitions, and services
    - Create ECS cluster
    - Create IAM execution role for ECS tasks
    - Create backend task definition: Fargate, 256 CPU, 512 memory, awslogs driver, port 8000
    - Create frontend task definition: Fargate, 256 CPU, 512 memory, awslogs driver, port 80
    - Create backend ECS service attached to backend target group
    - Create frontend ECS service attached to frontend target group
    - Both services use Fargate launch type and run in public subnets with ECS security group
    - _Requirements: 8.1, 8.2, 8.3, 18.4, 20.1, 20.2, 20.3, 23.1, 23.3_

- [ ] 7. Checkpoint - Verify Terraform configuration
  - Ensure Terraform files are syntactically valid (`terraform validate`), ask the user if questions arise.

- [ ] 8. Create GitHub repository setup script
  - [ ] 8.1 Create `scripts/create_repo.sh`
    - Read `GITHUB_TOKEN` from `.env` file
    - Create GitHub repository matching current directory name via GitHub API
    - Skip creation if repository already exists and report it
    - Fail with error if token is missing or invalid
    - Configure local git remote origin to the new repository
    - _Requirements: 15.1, 15.2, 15.3, 15.4, 15.5_

- [ ] 9. Implement GitHub Actions CI/CD pipeline
  - [ ] 9.1 Create `.github/workflows/deploy.yml`
    - Trigger on push to main branch
    - Build stage: build Docker images for frontend and backend
    - Tag images with Git commit SHA
    - Authenticate with ECR and push images
    - Deploy stage: update ECS services with new task definitions pointing to new images
    - Deploy stage depends on build stage; skip deploy if build fails
    - Post-deployment health check: wait for ECS tasks to reach running state with configurable timeout
    - Fail pipeline if any task doesn't stabilize or crashes
    - Report which task failed if health check fails
    - Report deployment as healthy when all tasks pass
    - Use `${{ secrets.* }}` for all AWS credentials — no hardcoded secrets
    - _Requirements: 16.1, 16.2, 16.3, 16.4, 16.5, 16.6, 16.7, 17.1, 17.2, 17.3, 17.4, 17.5, 18.3_

- [ ] 10. Checkpoint - Verify CI/CD and scripts
  - Ensure all workflow files and scripts are complete, ask the user if questions arise.

- [ ] 11. Write property-based tests
  - [ ] 11.1 Create `backend/tests/test_api_properties.py` — Property 1: API response returns valid random number
    - Use Hypothesis to generate multiple requests to `GET /api/random`
    - Assert response status 200, content-type JSON, `number` field is int between 1 and 100
    - Tag: `# Feature: random-number-service, Property 1: API response returns valid random number`
    - **Property 1: API response returns valid random number**
    - **Validates: Requirements 1.1, 1.2, 1.3**
  - [ ] 11.2 Add to `backend/tests/test_api_properties.py` — Property 2: CORS headers present on all responses
    - Use Hypothesis with `st.sampled_from(["GET", "OPTIONS"])` to test both methods
    - Assert `Access-Control-Allow-Origin` header is present
    - Tag: `# Feature: random-number-service, Property 2: CORS headers present on all responses`
    - **Property 2: CORS headers present on all responses**
    - **Validates: Requirements 5.1**
  - [ ] 11.3 Add to `backend/tests/test_api_properties.py` — Property 4: Startup rejects missing required tokens
    - Use Hypothesis to generate subsets of required env vars with at least one missing
    - Assert application fails validation and does not accept requests
    - Tag: `# Feature: random-number-service, Property 4: Startup rejects missing required tokens`
    - **Property 4: Startup rejects missing required tokens**
    - **Validates: Requirements 9.4**
  - [ ] 11.4 Create `tests/test_project_structure.py` — Property 5: All dependencies have pinned versions
    - Parse each non-comment, non-empty line in `requirements.txt`
    - Assert each line contains `==` version pinning
    - Tag: `# Feature: random-number-service, Property 5: All dependencies have pinned versions`
    - **Property 5: All dependencies have pinned versions**
    - **Validates: Requirements 10.2**
  - [ ] 11.5 Add to `tests/test_project_structure.py` — Property 6: Infrastructure directory contains no application code
    - Scan all files in `infra/` directory
    - Assert no files have extensions `.py`, `.js`, `.html`, `.css`
    - Tag: `# Feature: random-number-service, Property 6: Infrastructure directory contains no application code`
    - **Property 6: Infrastructure directory contains no application code**
    - **Validates: Requirements 11.3**
  - [ ] 11.6 Add to `tests/test_project_structure.py` — Property 7: CI/CD workflows contain no hardcoded secrets
    - Scan all files in `.github/workflows/`
    - Assert no hardcoded AWS keys or tokens (regex for `AKIA`, long secret patterns)
    - All sensitive values use `${{ secrets.* }}` syntax
    - Tag: `# Feature: random-number-service, Property 7: CI/CD workflows contain no hardcoded secrets`
    - **Property 7: CI/CD workflows contain no hardcoded secrets**
    - **Validates: Requirements 16.7**
  - [ ] 11.7 Add to `tests/test_project_structure.py` — Property 8: Frontend uses only relative paths for API requests
    - Scan `frontend/app.js` for URL patterns
    - Assert no `http://` or `https://` absolute URLs for backend API calls
    - Assert API paths start with `/`
    - Tag: `# Feature: random-number-service, Property 8: Frontend uses only relative paths for API requests`
    - **Property 8: Frontend uses only relative paths for API requests**
    - **Validates: Requirements 22.1, 22.2**

- [ ] 12. Final checkpoint - Ensure all tests pass
  - Run `pytest` from project root to execute all backend and project structure tests.
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- All tasks are required — no optional tasks
- Each task references specific requirements for traceability
- Property-based tests validate universal correctness properties from the design document
- Checkpoints ensure incremental validation throughout implementation
- Implementation uses Python (FastAPI/pytest/Hypothesis) for backend, JavaScript for frontend, HCL for Terraform
