# Feature: random-number-service, Property 5: All dependencies have pinned versions
# Feature: random-number-service, Property 6: Infrastructure directory contains no application code
# Feature: random-number-service, Property 7: CI/CD workflows contain no hardcoded secrets
# Feature: random-number-service, Property 8: Frontend uses only relative paths for API requests

import os
import re


# Feature: random-number-service, Property 5: All dependencies have pinned versions
# Validates: Requirements 10.2
def test_all_dependencies_pinned():
    with open("requirements.txt") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                assert "==" in line, f"Dependency not pinned: {line}"


# Feature: random-number-service, Property 6: Infrastructure directory contains no application code
# Validates: Requirements 11.3
def test_infra_no_app_code():
    app_extensions = {".py", ".js", ".html", ".css"}
    for root, _, files in os.walk("infra"):
        for f in files:
            ext = os.path.splitext(f)[1]
            assert ext not in app_extensions, f"App code found in infra/: {f}"


# Feature: random-number-service, Property 7: CI/CD workflows contain no hardcoded secrets
# Validates: Requirements 16.7
def test_no_hardcoded_secrets_in_workflows():
    secret_patterns = [r"AKIA[0-9A-Z]{16}", r"[0-9a-zA-Z/+]{40}", r"ghp_[0-9a-zA-Z]{36}"]
    workflow_dir = ".github/workflows"
    for f in os.listdir(workflow_dir):
        content = open(os.path.join(workflow_dir, f)).read()
        for pattern in secret_patterns:
            matches = re.findall(pattern, content)
            for m in matches:
                assert "${{" in content[max(0, content.index(m)-20):content.index(m)], \
                    f"Possible hardcoded secret in {f}"


# Feature: random-number-service, Property 8: Frontend uses only relative paths for API requests
# Validates: Requirements 22.1, 22.2
def test_frontend_uses_relative_paths():
    with open("frontend/app.js") as f:
        content = f.read()
    assert "http://" not in content, "Absolute http:// URL found in app.js"
    assert "https://" not in content, "Absolute https:// URL found in app.js"
    assert "/api/random" in content, "Relative /api/random path not found in app.js"
