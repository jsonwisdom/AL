(function () {
  const target = document.getElementById('active-lanes');
  if (!target) return;

  const classify = (value) => {
    if (value === 'GREEN') return 'green';
    if (value === 'REPORTED_UNVERIFIED') return 'warn';
    if (value === 'BLOCKED') return 'blocked';
    return '';
  };

  const text = (value) => String(value ?? '');

  const makePill = (value, className) => {
    const pill = document.createElement('span');
    pill.className = className ? 'pill ' + className : 'pill';
    pill.textContent = text(value);
    return pill;
  };

  const makeLane = (lane) => {
    const row = document.createElement('div');
    row.className = 'lane';

    const label = document.createElement('b');
    label.textContent = text(lane.lane_id);

    const values = document.createElement('span');
    values.appendChild(makePill(lane.status, classify(lane.status)));
    values.appendChild(makePill(lane.status_source));
    values.appendChild(makePill(lane.replay_verdict));
    values.appendChild(makePill('delta_h ' + text(lane.delta_h)));

    row.appendChild(label);
    row.appendChild(values);
    return row;
  };

  fetch('ACTIVE_LANES.json', { cache: 'no-store' })
    .then((response) => {
      if (!response.ok) throw new Error('ACTIVE_LANES.json fetch failed');
      return response.json();
    })
    .then((data) => {
      if (!Array.isArray(data.lanes)) throw new Error('ACTIVE_LANES.json missing lanes array');
      target.replaceChildren(...data.lanes.map(makeLane));
    })
    .catch((error) => {
      console.warn('Active lanes dynamic projection unavailable; using static fallback.', error);
    });
}());
