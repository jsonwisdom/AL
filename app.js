async function loadJson(path) {
  const res = await fetch(path + '?t=' + Date.now());
  if (!res.ok) throw new Error(path + ' -> HTTP ' + res.status);
  return res.json();
}

async function main() {
  const statusBox = document.getElementById('status');
  const replayBox = document.getElementById('replay600');

  try {
    const status = await loadJson('./status.json');
    if (statusBox) statusBox.textContent = JSON.stringify(status, null, 2);
  } catch (e) {
    if (statusBox) statusBox.textContent = String(e);
  }

  try {
    const replay = await loadJson('./factory-console/logs/last-600-days.json');
    if (replayBox) replayBox.textContent = JSON.stringify(replay, null, 2);
  } catch (e) {
    if (replayBox) replayBox.textContent = String(e);
  }
}

main();
