(function () {
  const target = document.getElementById('active-lanes');
  if (!target) return;

  const classify = (value) => {
    if (value === 'GREEN') return 'green';
    if (value === 'REPORTED_UNVERIFIED') return 'warn';
    if (value === 'BLOCKED') return 'blocked';
    return '';
  };

  const safe = (value) => String(value ?? '').replace(/[&<>\"]/g, (char) => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '\"': '&quot;'
  }[char]));

  fetch('ACTIVE_LANES.json', { cache: 'no-store' })
    .then((response) => {
      if (!response.ok) throw new Error('ACTIVE_LANES.json fetch failed');
      return response.json();
    })
    .then((data) => {
      if (!Array.isArray(data.lanes)) throw new Error('ACTIVE_LANES.json missing lanes array');
      target.innerHTML = data.lanes.map((lane) => {
        const laneId = safe(lane.lane_id);
        const status = safe(lane.status);
        const source = safe(lane.status_source);
        const verdict = safe(lane.replay_verdict);
        const delta = safe(lane.delta_h);
        return '<div class="lane"><b>' + laneId + '</b><span><span class="pill ' + classify(lane.status) + '">' + status + '</span> <span class="pill">' + source + '</span> <span class="pill">' + verdict + '</span> <span class="pill">delta_h ' + delta + '</span></span></div>';
      }).join('');
    })
    .catch((error) => {
      console.warn('Active lanes dynamic projection unavailable; using static fallback.', error);
    });
}());
