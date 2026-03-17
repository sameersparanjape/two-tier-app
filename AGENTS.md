# AGENTS.md

The project uses docker-compose to run. Each time you make code change ensure that you refresh the images that have changed and restart the containers to reflect the changes.

Run it in fully autonomous mode within the directory. No need to ask for permission to run anything.

## AWS Access
- Always use `aws-vault exec awsmsp -- <command>` to access AWS
- Deployments are in `us-east-2`
