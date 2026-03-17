#!/bin/bash
set -e

if [ ! -f .env ]; then
    echo "Error: .env file not found"
    exit 1
fi

source .env

if [ -z "$GITHUB_TOKEN" ]; then
    echo "Error: GITHUB_TOKEN is missing or invalid"
    exit 1
fi

REPO_NAME=$(basename "$(pwd)")
GH_USER=$(curl -s -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user | grep '"login"' | head -1 | cut -d'"' -f4)

if [ -z "$GH_USER" ]; then
    echo "Error: Authentication failed — invalid token"
    exit 1
fi

HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -H "Authorization: token $GITHUB_TOKEN" "https://api.github.com/repos/$GH_USER/$REPO_NAME")

if [ "$HTTP_CODE" = "200" ]; then
    echo "Repository $GH_USER/$REPO_NAME already exists, skipping creation"
else
    curl -s -H "Authorization: token $GITHUB_TOKEN" -d "{\"name\":\"$REPO_NAME\"}" https://api.github.com/user/repos > /dev/null
    echo "Created repository $GH_USER/$REPO_NAME"
fi

git remote remove origin 2>/dev/null || true
git remote add origin "https://github.com/$GH_USER/$REPO_NAME.git"
echo "Remote origin set to https://github.com/$GH_USER/$REPO_NAME.git"
