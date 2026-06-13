import express from "express";

const app = express();
const PORT = Number(process.env.PORT || 8787);
const DEFAULT_REPO = "jsonwisdom/AL";
const DEFAULT_BASE = "44da17d559f7df8f6a0d5049375a9a823a63c2b9";
const DEFAULT_HEAD = "master";
const DEFAULT_WORKFLOW_PATH = ".github/workflows/al-jay-agent-zora-sleep-console.yml";

app.use(express.json({ limit: "256kb" }));
app.use(express.static(new URL("../", import.meta.url).pathname));

function requireToken() {
  const token = process.env.GITHUB_TOKEN;
  if (!token) {
    const error = new Error("GITHUB_TOKEN is required server-side. Never put this token in the browser.");
    error.status = 500;
    throw error;
  }
  return token;
}

function splitRepo(repo) {
  const [owner, name] = String(repo || "").split("/");
  if (!owner || !name) {
    const error = new Error("repo must be owner/name");
    error.status = 400;
    throw error;
  }
  return { owner, name };
}

async function github(path, token) {
  const response = await fetch(`https://api.github.com${path}`, {
    headers: {
      "Accept": "application/vnd.github+json",
      "Authorization": `Bearer ${token}`,
      "X-GitHub-Api-Version": "2022-11-28",
      "User-Agent": "al-zora-jay-agent-evidence-collector"
    }
  });

  const text = await response.text();
  let body;
  try {
    body = text ? JSON.parse(text) : null;
  } catch {
    body = { raw: text };
  }

  if (!response.ok) {
    const error = new Error(body?.message || `GitHub API error ${response.status}`);
    error.status = response.status;
    error.body = body;
    throw error;
  }
  return body;
}

function compactRuns(runs, workflowPath) {
  return (runs || [])
    .filter((run) => !workflowPath || run.path === workflowPath || run.name === "AL Jay-Agent Zora Sleep Console")
    .slice(0, 10)
    .map((run) => ({
      id: run.id,
      name: run.name,
      path: run.path,
      event: run.event,
      status: run.status,
      conclusion: run.conclusion,
      head_branch: run.head_branch,
      head_sha: run.head_sha,
      run_number: run.run_number,
      run_attempt: run.run_attempt,
      created_at: run.created_at,
      updated_at: run.updated_at,
      html_url: run.html_url
    }));
}

function compactArtifacts(artifacts) {
  return (artifacts || []).map((artifact) => ({
    id: artifact.id,
    name: artifact.name,
    size_in_bytes: artifact.size_in_bytes,
    expired: artifact.expired,
    created_at: artifact.created_at,
    expires_at: artifact.expires_at,
    workflow_run: artifact.workflow_run ? {
      id: artifact.workflow_run.id,
      head_sha: artifact.workflow_run.head_sha
    } : undefined
  }));
}

app.get("/api/health", (_req, res) => {
  res.json({
    ok: true,
    service: "al-zora-jay-agent-github-evidence-backend",
    mode: "read_only",
    authority: false,
    no_fake_green: true
  });
});

app.get("/api/github-evidence", async (req, res) => {
  try {
    const token = requireToken();
    const repo = String(req.query.repo || DEFAULT_REPO);
    const base = String(req.query.base || DEFAULT_BASE);
    const head = String(req.query.head || DEFAULT_HEAD);
    const workflowPath = String(req.query.workflow || DEFAULT_WORKFLOW_PATH);
    const { owner, name } = splitRepo(repo);
    const encodedWorkflowPath = encodeURIComponent(workflowPath);

    const [repoInfo, compare, workflowFile, runsBody] = await Promise.all([
      github(`/repos/${owner}/${name}`, token),
      github(`/repos/${owner}/${name}/compare/${base}...${head}`, token),
      github(`/repos/${owner}/${name}/contents/${encodedWorkflowPath}?ref=${head}`, token),
      github(`/repos/${owner}/${name}/actions/runs?branch=${encodeURIComponent(head)}&per_page=30`, token)
    ]);

    const workflowRuns = compactRuns(runsBody.workflow_runs, workflowPath);
    const latestRun = workflowRuns[0] || null;
    let artifacts = [];

    if (latestRun) {
      const artifactBody = await github(`/repos/${owner}/${name}/actions/runs/${latestRun.id}/artifacts?per_page=30`, token);
      artifacts = compactArtifacts(artifactBody.artifacts);
    }

    res.json({
      generated_at: new Date().toISOString(),
      mode: "read_only_github_api",
      authority: false,
      no_fake_green: true,
      repo: {
        full_name: repoInfo.full_name,
        default_branch: repoInfo.default_branch,
        private: repoInfo.private,
        html_url: repoInfo.html_url
      },
      compare: {
        base,
        head,
        status: compare.status,
        ahead_by: compare.ahead_by,
        behind_by: compare.behind_by,
        total_commits: compare.total_commits,
        files: (compare.files || []).map((file) => ({
          filename: file.filename,
          status: file.status,
          additions: file.additions,
          deletions: file.deletions,
          changes: file.changes
        })),
        commits: (compare.commits || []).map((commit) => ({
          sha: commit.sha,
          message: commit.commit?.message,
          author_date: commit.commit?.author?.date,
          html_url: commit.html_url
        }))
      },
      workflow: {
        path: workflowPath,
        sha: workflowFile.sha,
        exists: true,
        runs_observed: workflowRuns.length,
        latest_run: latestRun,
        runs: workflowRuns
      },
      artifacts: {
        observed: artifacts.length,
        latest_run_id: latestRun?.id || null,
        items: artifacts
      },
      ruling: {
        commits: compare.total_commits > 0 ? "EVIDENCE_PRESENT" : "NO_DELTA_OBSERVED",
        workflow_visibility: workflowRuns.length > 0 ? "GREEN" : "UNKNOWN",
        artifacts: artifacts.length > 0 ? "GREEN" : "UNKNOWN",
        wallet_action: false,
        semantic_truth_final: false,
        authority: false,
        no_fake_green: true
      },
      next_best_action: artifacts.length > 0
        ? "Download/read artifacts before promoting artifact state beyond GREEN_VISIBLE."
        : "Confirm GitHub Actions schedule has executed and inspect run logs/artifacts."
    });
  } catch (error) {
    res.status(error.status || 500).json({
      ok: false,
      error: error.message,
      body: error.body || null,
      authority: false,
      no_fake_green: true
    });
  }
});

app.listen(PORT, () => {
  console.log(`AL evidence backend listening on http://localhost:${PORT}`);
  console.log("AUTHORITY=false NO_FAKE_GREEN=true mode=read_only_github_api");
});
