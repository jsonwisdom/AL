import express from "express";

const app = express();
const PORT = Number(process.env.PORT || 8787);
const DEFAULT_REPO = "jsonwisdom/AL";
const DEFAULT_BASE = "44da17d559f7df8f6a0d5049375a9a823a63c2b9";
const DEFAULT_HEAD = "master";
const DEFAULT_WORKFLOW_PATH = ".github/workflows/al-jay-agent-zora-sleep-console.yml";
const DEFAULT_SEPOLIA_WALLET = "0x1dB2C056c7DeCD9f9fC574692b05F62aE34Fb8b5";
const DEFAULT_SEPOLIA_RPC_URL = process.env.SEPOLIA_RPC_URL || "https://rpc.sepolia.org";

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

function requireAddress(address) {
  const value = String(address || "");
  if (!/^0x[a-fA-F0-9]{40}$/.test(value)) {
    const error = new Error("wallet must be a valid EVM address");
    error.status = 400;
    throw error;
  }
  return value;
}

function hexToBigInt(hex) {
  return BigInt(hex || "0x0");
}

function weiToEthString(wei) {
  const base = 10n ** 18n;
  const whole = wei / base;
  const fraction = wei % base;
  const frac = fraction.toString().padStart(18, "0").replace(/0+$/, "");
  return frac ? `${whole}.${frac}` : whole.toString();
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
  try { body = text ? JSON.parse(text) : null; } catch { body = { raw: text }; }

  if (!response.ok) {
    const error = new Error(body?.message || `GitHub API error ${response.status}`);
    error.status = response.status;
    error.body = body;
    throw error;
  }
  return body;
}

async function rpc(method, params = []) {
  const response = await fetch(DEFAULT_SEPOLIA_RPC_URL, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ jsonrpc: "2.0", id: 1, method, params })
  });
  const body = await response.json();
  if (!response.ok || body.error) {
    const error = new Error(body.error?.message || `Sepolia RPC error ${response.status}`);
    error.status = response.status || 502;
    error.body = body;
    throw error;
  }
  return body.result;
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
    service: "al-zora-jay-agent-evidence-backend",
    mode: "read_only_github_api_plus_read_only_sepolia_rpc",
    authority: false,
    no_fake_green: true,
    chain_write: false,
    wallet_control: false,
    signing: false,
    broadcast: false
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

app.get("/api/sepolia-evidence", async (req, res) => {
  try {
    const wallet = requireAddress(req.query.wallet || DEFAULT_SEPOLIA_WALLET);
    const requestedLimit = Number(req.query.limit || 8);
    const limit = Number.isFinite(requestedLimit) ? Math.max(1, Math.min(20, requestedLimit)) : 8;

    const [chainIdHex, blockNumberHex, balanceHex] = await Promise.all([
      rpc("eth_chainId"),
      rpc("eth_blockNumber"),
      rpc("eth_getBalance", [wallet, "latest"])
    ]);

    const latestBlock = Number(hexToBigInt(blockNumberHex));
    const startBlock = Math.max(0, latestBlock - 9000);
    const walletLower = wallet.toLowerCase();
    const transactions = [];

    for (let blockNumber = latestBlock; blockNumber >= startBlock && transactions.length < limit; blockNumber--) {
      const blockHex = `0x${blockNumber.toString(16)}`;
      const block = await rpc("eth_getBlockByNumber", [blockHex, true]);
      if (!block?.transactions) continue;
      for (const tx of block.transactions) {
        if (transactions.length >= limit) break;
        const from = String(tx.from || "").toLowerCase();
        const to = String(tx.to || "").toLowerCase();
        if (from !== walletLower && to !== walletLower) continue;
        const receipt = await rpc("eth_getTransactionReceipt", [tx.hash]);
        transactions.push({
          hash: tx.hash,
          block_number: Number(hexToBigInt(tx.blockNumber)),
          from: tx.from,
          to: tx.to,
          value_wei: hexToBigInt(tx.value).toString(),
          value_eth: weiToEthString(hexToBigInt(tx.value)),
          status: receipt?.status === "0x1" ? "success" : receipt?.status === "0x0" ? "failure" : "unknown",
          timestamp: block.timestamp ? new Date(Number(hexToBigInt(block.timestamp)) * 1000).toISOString() : null
        });
      }
    }

    res.json({
      generated_at: new Date().toISOString(),
      mode: "read_only_sepolia_rpc_public_fallback",
      rpc_url_label: DEFAULT_SEPOLIA_RPC_URL === "https://rpc.sepolia.org" ? "public_sepolia_rpc" : "custom_env_rpc",
      chain_id: Number(hexToBigInt(chainIdHex)),
      network_expected: "sepolia",
      wallet,
      balance_wei: hexToBigInt(balanceHex).toString(),
      balance_eth: weiToEthString(hexToBigInt(balanceHex)),
      latest_block: latestBlock,
      scan_window_blocks: latestBlock - startBlock,
      transactions_observed: transactions.length,
      transactions,
      ruling: {
        sepolia_rpc: Number(hexToBigInt(chainIdHex)) === 11155111 ? "GREEN" : "RED_WRONG_CHAIN",
        balance_observed: true,
        tx_history_observed: transactions.length > 0,
        chain_write: false,
        wallet_control: false,
        signing: false,
        broadcast: false,
        authority: false,
        no_fake_green: true
      },
      next_best_action: transactions.length > 0
        ? "Verify specific tx hashes in an independent Sepolia explorer before promoting transaction claims."
        : "Balance observed; no recent transactions found in public RPC scan window. Use indexed provider for deeper history."
    });
  } catch (error) {
    res.status(error.status || 502).json({
      ok: false,
      error: error.message,
      body: error.body || null,
      chain_write: false,
      wallet_control: false,
      signing: false,
      broadcast: false,
      authority: false,
      no_fake_green: true
    });
  }
});

app.listen(PORT, () => {
  console.log(`AL evidence backend listening on http://localhost:${PORT}`);
  console.log("AUTHORITY=false NO_FAKE_GREEN=true mode=read_only_github_api_plus_read_only_sepolia_rpc");
});
