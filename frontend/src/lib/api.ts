/**
 * PRANA Research Hub API Client (Milestone 2 - Data Provenance Aware)
 */

const API_BASE = '/api';

export async function fetchSummary() {
  const res = await fetch(`${API_BASE}/overview/summary`);
  if (!res.ok) throw new Error('Failed to fetch regional summary');
  return res.json();
}

export async function fetchOverviewTrends(pollutant = 'PM2.5', days = 7) {
  const res = await fetch(`${API_BASE}/overview/trends?pollutant=${pollutant}&days=${days}`);
  if (!res.ok) throw new Error('Failed to fetch overview trends');
  return res.json();
}

export async function fetchStations(city?: string) {
  const url = city ? `${API_BASE}/live/stations?city=${encodeURIComponent(city)}` : `${API_BASE}/live/stations`;
  const res = await fetch(url);
  if (!res.ok) throw new Error('Failed to fetch stations');
  return res.json();
}

export async function fetchStationHistory(stationId: number, pollutant = 'PM2.5', hours = 48) {
  const res = await fetch(`${API_BASE}/live/stations/${stationId}/history?pollutant=${pollutant}&hours=${hours}`);
  if (!res.ok) throw new Error('Failed to fetch station history');
  return res.json();
}

export async function fetchDiurnal(pollutant = 'PM2.5', stationId?: number) {
  const url = stationId 
    ? `${API_BASE}/explorer/diurnal?pollutant=${pollutant}&station_id=${stationId}`
    : `${API_BASE}/explorer/diurnal?pollutant=${pollutant}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error('Failed to fetch diurnal profile');
  return res.json();
}

export async function fetchDayOfWeek(pollutant = 'PM2.5', stationId?: number) {
  const url = stationId 
    ? `${API_BASE}/explorer/day-of-week?pollutant=${pollutant}&station_id=${stationId}`
    : `${API_BASE}/explorer/day-of-week?pollutant=${pollutant}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error('Failed to fetch day-of-week profile');
  return res.json();
}

export async function fetchCorrelation(varX = 'PM2.5', varY = 'PBLH', stationId?: number) {
  const url = stationId
    ? `${API_BASE}/explorer/correlation?var_x=${varX}&var_y=${varY}&station_id=${stationId}`
    : `${API_BASE}/explorer/correlation?var_x=${varX}&var_y=${varY}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error('Failed to fetch correlation');
  return res.json();
}

export async function fetchStationComparison(pollutant = 'PM2.5', stationIds = '1,3,7', hours = 72) {
  const res = await fetch(`${API_BASE}/explorer/station-comparison?pollutant=${pollutant}&station_ids=${stationIds}&hours=${hours}`);
  if (!res.ok) throw new Error('Failed to fetch station comparison');
  return res.json();
}

export async function fetchZones() {
  const res = await fetch(`${API_BASE}/hotspots/zones`);
  if (!res.ok) throw new Error('Failed to fetch zones');
  return res.json();
}

export async function fetchSourceCategories() {
  const res = await fetch(`${API_BASE}/sources/categories`);
  if (!res.ok) throw new Error('Failed to fetch source categories');
  return res.json();
}

export async function fetchPublishedStudies() {
  const res = await fetch(`${API_BASE}/sources/studies`);
  if (!res.ok) throw new Error('Failed to fetch studies');
  return res.json();
}

export async function fetchVerifiableFindings() {
  const res = await fetch(`${API_BASE}/sources/findings`);
  if (!res.ok) throw new Error('Failed to fetch findings');
  return res.json();
}

export async function fetchSourceProfiles(city = 'Kolkata', season = 'Winter', pollutant = 'PM2.5') {
  const res = await fetch(`${API_BASE}/sources/profiles?city=${city}&season=${season}&pollutant=${pollutant}`);
  if (!res.ok) throw new Error('Failed to fetch source profiles');
  return res.json();
}

export async function fetchCurrentWeather(city = 'Kolkata') {
  const res = await fetch(`${API_BASE}/weather/current?city=${city}`);
  if (!res.ok) throw new Error('Failed to fetch current weather');
  return res.json();
}

export async function fetchWeatherHistory(hours = 72) {
  const res = await fetch(`${API_BASE}/weather/history?hours=${hours}`);
  if (!res.ok) throw new Error('Failed to fetch weather history');
  return res.json();
}

export async function fetchWindRose() {
  const res = await fetch(`${API_BASE}/weather/wind-rose`);
  if (!res.ok) throw new Error('Failed to fetch wind rose');
  return res.json();
}

export async function fetchDocuments(query?: string) {
  const url = query ? `${API_BASE}/library/documents?query=${encodeURIComponent(query)}` : `${API_BASE}/library/documents`;
  const res = await fetch(url);
  if (!res.ok) throw new Error('Failed to fetch documents');
  return res.json();
}

export async function fetchNotes(docId?: number) {
  const url = docId ? `${API_BASE}/library/notes?document_id=${docId}` : `${API_BASE}/library/notes`;
  const res = await fetch(url);
  if (!res.ok) throw new Error('Failed to fetch notes');
  return res.json();
}

export async function createNote(title: string, content: string, tags?: string, docId?: number) {
  const res = await fetch(`${API_BASE}/library/notes`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, content, tags, document_id: docId })
  });
  if (!res.ok) throw new Error('Failed to create note');
  return res.json();
}

export async function fetchHypotheses() {
  const res = await fetch(`${API_BASE}/interventions/hypotheses`);
  if (!res.ok) throw new Error('Failed to fetch hypotheses');
  return res.json();
}

export async function createHypothesis(payload: any) {
  const res = await fetch(`${API_BASE}/interventions/hypotheses`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  if (!res.ok) throw new Error('Failed to create hypothesis');
  return res.json();
}

export async function fetchQualityAudit(hoursWindow = 168) {
  const res = await fetch(`${API_BASE}/quality/audit?hours_window=${hoursWindow}`);
  if (!res.ok) throw new Error('Failed to fetch quality audit');
  return res.json();
}

export async function fetchIntegritySummary() {
  const res = await fetch(`${API_BASE}/quality/integrity-summary`);
  if (!res.ok) throw new Error('Failed to fetch integrity summary');
  return res.json();
}

export async function fetchStationVerificationRegistry() {
  const res = await fetch(`${API_BASE}/quality/stations/verification`);
  if (!res.ok) throw new Error('Failed to fetch station registry');
  return res.json();
}

export async function fetchSourcesReliability() {
  const res = await fetch(`${API_BASE}/quality/sources/reliability`);
  if (!res.ok) throw new Error('Failed to fetch sources reliability');
  return res.json();
}

export async function importCSV(file: File, providerCode = 'MANUAL_CSV_IMPORT', classification = 'IMPORTED') {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('provider_code', providerCode);
  formData.append('classification', classification);

  const res = await fetch(`${API_BASE}/quality/import-csv`, {
    method: 'POST',
    body: formData
  });
  if (!res.ok) throw new Error('Failed to upload CSV');
  return res.json();
}

export async function askAssistant(query: string) {
  const res = await fetch(`${API_BASE}/assistant/query`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query })
  });
  if (!res.ok) throw new Error('Failed to query assistant');
  return res.json();
}
