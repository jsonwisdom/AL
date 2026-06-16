# Factory Console Live CI Feed

Render:
- Build: npm install
- Start: npm start
- Env: GITHUB_WEBHOOK_SECRET

GitHub webhook:
- Payload: https://YOUR-SERVICE.onrender.com/webhook/github
- Content-Type: application/json
- Secret: same as env
- Events: push, pull_request, check_suite, workflow_run, repository_dispatch
