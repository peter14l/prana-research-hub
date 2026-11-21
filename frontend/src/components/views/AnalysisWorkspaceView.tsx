'use client';

import React, { useState, useEffect } from 'react';
import {
  Microscope,
  Calendar,
  Layers,
  Save,
  Download,
  FolderOpen,
  CheckCircle2,
  AlertTriangle,
  Info,
  RefreshCw,
  Compass,
  TrendingUp,
  Activity,
  ShieldCheck,
  Check,
  X
} from 'lucide-react';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  ZAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Legend,
  ReferenceLine
} from 'recharts';
import {
  fetchStations,
  fetchAnalysisTemporal,
  fetchAnalysisMeteorological,
  fetchAnalysisHotspots,
  saveAnalysis,
  fetchSavedAnalyses,
  fetchSavedAnalysis
} from '@/lib/api';

const MET_VARS = [
  { id: 'wind_speed', label: 'Wind Speed (10m)', unit: 'km/h' },
  { id: 'temperature', label: '2m Temperature', unit: '°C' },
  { id: 'relative_humidity', label: 'Relative Humidity', unit: '%' },
  { id: 'precipitation', label: 'Precipitation', unit: 'mm' },
  { id: 'pblh', label: 'Planetary Boundary Layer', unit: 'm' }
];

export default function AnalysisWorkspaceView() {
  const [stations, setStations] = useState<any[]>([]);
  const [selectedStationIds, setSelectedStationIds] = useState<number[]>([]);
  const [pollutant, setPollutant] = useState<string>('PM2.5');
  const [daysRange, setDaysRange] = useState<number>(7);
  const [selectedMetVars, setSelectedMetVars] = useState<string[]>(['wind_speed', 'temperature']);
  const [classificationFilter, setClassificationFilter] = useState<string>('ALL'); // ALL, VERIFIED_ONLY

  // Analysis results
  const [temporalData, setTemporalData] = useState<any>(null);
  const [metData, setMetData] = useState<any>(null);
  const [hotspotData, setHotspotData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);

  // Saved Analyses State
  const [savedList, setSavedList] = useState<any[]>([]);
  const [showSavedModal, setShowSavedModal] = useState<boolean>(false);
  const [showSaveFormModal, setShowSaveFormModal] = useState<boolean>(false);
  const [saveTitle, setSaveTitle] = useState<string>('');
  const [saveDescription, setSaveDescription] = useState<string>('');
  const [saveMethodology, setSaveMethodology] = useState<string>('OLS Bivariate Regression and Diurnal Harmonic Averaging');
  const [saveReferences, setSaveReferences] = useState<string>('TERI (2025) Source Apportionment; CPCB NAQI Guidelines 2014');
  const [saveStatusMsg, setSaveStatusMsg] = useState<string>('');

  useEffect(() => {
    fetchStations().then((sts) => {
      setStations(sts);
      setSelectedStationIds(sts.map((s: any) => s.id));
    });
    loadSavedAnalyses();
  }, []);

  useEffect(() => {
    if (stations.length > 0) {
      runAnalysis();
    }
  }, [pollutant, daysRange, classificationFilter]);

  async function loadSavedAnalyses() {
    try {
      const list = await fetchSavedAnalyses();
      setSavedList(list);
    } catch (e) {
      console.error(e);
    }
  }

  async function runAnalysis() {
    setLoading(true);
    try {
      const stIdsStr = selectedStationIds.length > 0 ? selectedStationIds.join(',') : undefined;
      const classStr = classificationFilter === 'VERIFIED_ONLY' ? 'VERIFIED,IMPORTED' : undefined;

      const [temp, met, hot] = await Promise.all([
        fetchAnalysisTemporal(pollutant, stIdsStr, daysRange, classStr),
        fetchAnalysisMeteorological(pollutant, 'Kolkata', daysRange),
        fetchAnalysisHotspots(pollutant, daysRange * 24)
      ]);

      setTemporalData(temp);
      setMetData(met);
      setHotspotData(hot);
    } catch (err) {
      console.error('Failed to execute environmental analysis:', err);
    } finally {
      setLoading(false);
    }
  }

  const toggleStation = (id: number) => {
    if (selectedStationIds.includes(id)) {
      setSelectedStationIds(selectedStationIds.filter((s) => s !== id));
    } else {
      setSelectedStationIds([...selectedStationIds, id]);
    }
  };

  const toggleMetVar = (id: string) => {
    if (selectedMetVars.includes(id)) {
      setSelectedMetVars(selectedMetVars.filter((v) => v !== id));
    } else {
      setSelectedMetVars([...selectedMetVars, id]);
    }
  };

  const handleSaveAnalysis = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!saveTitle) return;

    try {
      await saveAnalysis({
        title: saveTitle,
        description: saveDescription,
        author: 'PRANA Environmental Researcher',
        pollutant: pollutant,
        station_ids: selectedStationIds,
        date_range_start: new Date(Date.now() - daysRange * 86400000).toISOString(),
        date_range_end: new Date().toISOString(),
        met_variables: selectedMetVars,
        methodology: saveMethodology,
        source_references: saveReferences,
        analysis_results: {
          exceedance_rate_pct: temporalData?.exceedance_rate_pct,
          weekday_to_weekend_ratio: temporalData?.weekday_to_weekend_ratio,
          wind_speed_pearson_r: metData?.correlations?.wind_speed?.pearson_r,
          temperature_pearson_r: metData?.correlations?.temperature?.pearson_r
        }
      });
      setSaveStatusMsg('Analysis successfully saved with complete methodology & citation references.');
      loadSavedAnalyses();
      setTimeout(() => {
        setShowSaveFormModal(false);
        setSaveStatusMsg('');
        setSaveTitle('');
        setSaveDescription('');
      }, 1500);
    } catch (err: any) {
      setSaveStatusMsg(`Failed to save: ${err.message}`);
    }
  };

  const handleLoadAnalysis = async (item: any) => {
    try {
      const full = await fetchSavedAnalysis(item.id);
      setPollutant(full.pollutant);
      if (full.station_ids && full.station_ids.length > 0) {
        setSelectedStationIds(full.station_ids);
      }
      if (full.met_variables) {
        setSelectedMetVars(full.met_variables);
      }
      setShowSavedModal(false);
      runAnalysis();
    } catch (e) {
      console.error(e);
    }
  };

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="glass-panel p-5 rounded-xl border border-border">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <h1 className="text-lg font-bold text-white flex items-center gap-2">
              <Microscope className="w-5 h-5 text-prana-yellow" />
              Environmental Analysis Workspace
            </h1>
            <p className="text-xs text-gray-400 mt-1 max-w-3xl leading-relaxed">
              Interactive multi-variable research lab: isolate diurnal and weekly temporal cycles, examine meteorological dispersion dilution, analyze 16-sector pollution roses, and export reproducible datasets.
            </p>
          </div>

          <div className="flex items-center space-x-2.5">
            <button
              onClick={() => setShowSavedModal(true)}
              className="flex items-center space-x-1.5 px-3 py-1.5 bg-[#141822] hover:bg-[#1D2433] border border-border rounded-lg text-xs text-gray-200 transition-colors cursor-pointer"
            >
              <FolderOpen className="w-3.5 h-3.5 text-prana-sage" />
              <span>Saved Analyses ({savedList.length})</span>
            </button>

            <button
              onClick={() => setShowSaveFormModal(true)}
              className="flex items-center space-x-1.5 px-3 py-1.5 bg-prana-yellow hover:bg-prana-yellow-hover text-black font-semibold rounded-lg text-xs transition-colors cursor-pointer"
            >
              <Save className="w-3.5 h-3.5" />
              <span>Save Reproducible Analysis</span>
            </button>
          </div>
        </div>
      </div>

      {/* Control Station & Variable Selector Bar */}
      <div className="glass-panel p-4.5 rounded-xl border border-border space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          {/* Pollutant Selector */}
          <div>
            <label className="block text-[11px] font-semibold text-gray-400 mb-1.5">
              Criteria Pollutant
            </label>
            <select
              value={pollutant}
              onChange={(e) => setPollutant(e.target.value)}
              className="w-full bg-[#141822] border border-border rounded-lg px-3 py-2 text-xs text-gray-200 outline-none font-bold text-prana-yellow"
            >
              {['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3', 'NH3'].map((p) => (
                <option key={p} value={p} className="bg-[#10141C] text-gray-200">{p}</option>
              ))}
            </select>
          </div>

          {/* Date Range Selector */}
          <div>
            <label className="block text-[11px] font-semibold text-gray-400 mb-1.5">
              Analysis Window
            </label>
            <select
              value={daysRange}
              onChange={(e) => setDaysRange(parseInt(e.target.value))}
              className="w-full bg-[#141822] border border-border rounded-lg px-3 py-2 text-xs text-gray-200 outline-none"
            >
              <option value={1} className="bg-[#10141C] text-gray-200">Past 24 Hours</option>
              <option value={7} className="bg-[#10141C] text-gray-200">Past 7 Days (Weekly)</option>
              <option value={30} className="bg-[#10141C] text-gray-200">Past 30 Days (Monthly)</option>
              <option value={90} className="bg-[#10141C] text-gray-200">Past 90 Days (Seasonal)</option>
            </select>
          </div>

          {/* Data Classification Tier Filter */}
          <div>
            <label className="block text-[11px] font-semibold text-gray-400 mb-1.5">
              Data Classification Filter
            </label>
            <select
              value={classificationFilter}
              onChange={(e) => setClassificationFilter(e.target.value)}
              className="w-full bg-[#141822] border border-border rounded-lg px-3 py-2 text-xs text-gray-200 outline-none"
            >
              <option value="ALL" className="bg-[#10141C] text-gray-200">All Tiers (Include Demo Baseline)</option>
              <option value="VERIFIED_ONLY" className="bg-[#10141C] text-gray-200">VERIFIED &amp; IMPORTED Only</option>
            </select>
          </div>

          {/* Re-run button */}
          <div className="flex items-end">
            <button
              onClick={runAnalysis}
              disabled={loading}
              className="w-full py-2 bg-[#1C222E] hover:bg-[#252E3E] border border-prana-yellow/40 text-prana-yellow rounded-lg text-xs font-semibold flex items-center justify-center gap-1.5 transition-all"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
              <span>{loading ? 'Computing Statistics...' : 'Update Visualizations'}</span>
            </button>
          </div>
        </div>

        {/* Monitoring Station Selector Pills */}
        <div className="pt-2 border-t border-white/5 space-y-1.5">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-semibold text-gray-400">
              Active Monitoring Stations ({selectedStationIds.length}/{stations.length} Selected)
            </span>
            <div className="flex gap-2 text-[10px]">
              <button
                onClick={() => setSelectedStationIds(stations.map((s) => s.id))}
                className="text-prana-yellow hover:underline cursor-pointer"
              >
                Select All
              </button>
              <span className="text-gray-600">|</span>
              <button
                onClick={() => setSelectedStationIds([])}
                className="text-gray-400 hover:text-white cursor-pointer"
              >
                Deselect All
              </button>
            </div>
          </div>

          <div className="flex flex-wrap gap-1.5">
            {stations.map((st) => {
              const active = selectedStationIds.includes(st.id);
              return (
                <button
                  key={st.id}
                  onClick={() => toggleStation(st.id)}
                  className={`text-[10px] px-2.5 py-1 rounded-md border transition-all cursor-pointer flex items-center gap-1 ${
                    active
                      ? 'bg-[#182130] text-gray-100 border-prana-yellow/60 font-semibold'
                      : 'bg-[#10141C] text-gray-500 border-border hover:text-gray-300'
                  }`}
                >
                  <span className={`w-1.5 h-1.5 rounded-full ${active ? 'bg-prana-yellow' : 'bg-gray-600'}`}></span>
                  <span>{st.name}</span>
                </button>
              );
            })}
          </div>
        </div>

        {/* Meteorological Overlay Checkboxes */}
        <div className="pt-2 border-t border-white/5 space-y-1.5">
          <span className="text-[11px] font-semibold text-gray-400">
            Synoptic Meteorological Overlays (Open-Meteo Reanalysis)
          </span>
          <div className="flex flex-wrap gap-2">
            {MET_VARS.map((m) => {
              const checked = selectedMetVars.includes(m.id);
              return (
                <label
                  key={m.id}
                  onClick={() => toggleMetVar(m.id)}
                  className={`text-[10px] px-2.5 py-1 rounded-md border cursor-pointer select-none transition-colors flex items-center gap-1.5 ${
                    checked
                      ? 'bg-emerald-950/60 text-emerald-300 border-emerald-500/50'
                      : 'bg-[#10141C] text-gray-400 border-border hover:text-gray-200'
                  }`}
                >
                  <input type="checkbox" checked={checked} readOnly className="hidden" />
                  <span>{checked ? '●' : '○'} {m.label} ({m.unit})</span>
                </label>
              );
            })}
          </div>
        </div>
      </div>

      {/* Main Grid: Visualizations */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column (7 Cols): Diurnal & Daily Series */}
        <div className="lg:col-span-7 space-y-6">
          {/* Diurnal Cycle (0-23h) */}
          <div className="glass-panel p-5 rounded-xl border border-border space-y-3">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-sm font-bold text-white flex items-center gap-1.5">
                  <Activity className="w-4 h-4 text-prana-yellow" />
                  24-Hour Diurnal Cycle &amp; Inversion Dynamics ({pollutant})
                </h2>
                <p className="text-[11px] text-gray-400">
                  Mean concentration, median, and 10th-90th percentile envelope across all selected stations.
                </p>
              </div>
              <span className="text-[10px] font-mono text-prana-sage bg-surface-200 px-2 py-0.5 rounded border border-border">
                Diurnal Resolution
              </span>
            </div>

            <div className="h-64 w-full">
              {temporalData?.diurnal_profile ? (
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={temporalData.diurnal_profile} margin={{ top: 10, right: 15, left: -15, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
                    <XAxis dataKey="hour_label" tick={{ fill: '#9CA3AF', fontSize: 10 }} />
                    <YAxis tick={{ fill: '#9CA3AF', fontSize: 10 }} />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: '#12161F',
                        borderColor: 'rgba(255,255,255,0.1)',
                        borderRadius: 8,
                        fontSize: 11
                      }}
                    />
                    <Legend wrapperStyle={{ fontSize: 10, paddingTop: 6 }} />
                    <Line type="monotone" dataKey="p90" name="90th Percentile" stroke="#EF4444" strokeDasharray="3 3" dot={false} />
                    <Line type="monotone" dataKey="mean" name="Mean Concentration" stroke="#FFE547" strokeWidth={2.5} dot={false} />
                    <Line type="monotone" dataKey="median" name="Median" stroke="#10B981" strokeWidth={1.5} dot={false} />
                    <Line type="monotone" dataKey="p10" name="10th Percentile" stroke="#3B82F6" strokeDasharray="3 3" dot={false} />
                  </LineChart>
                </ResponsiveContainer>
              ) : (
                <div className="h-full flex items-center justify-center text-xs text-gray-500">
                  Loading diurnal analysis...
                </div>
              )}
            </div>

            <div className="p-3 bg-[#121620] rounded-lg border border-white/5 text-[11px] text-gray-300">
              <strong className="text-prana-yellow">Airshed Inversion Mechanism:</strong> Peaks occur at 07:00-09:00 IST (morning traffic injection into shallow inversion) and 21:00-00:00 IST (nocturnal cooling, boundary layer collapse to &lt;200m, and heavy freight transit).
            </div>
          </div>

          {/* Daily Aggregations with NAAQS Threshold */}
          <div className="glass-panel p-5 rounded-xl border border-border space-y-3">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-sm font-bold text-white flex items-center gap-1.5">
                  <TrendingUp className="w-4 h-4 text-emerald-400" />
                  Daily Averages &amp; NAAQS Exceedance Envelope
                </h2>
                <p className="text-[11px] text-gray-400">
                  Daily mean with official CPCB NAAQS 24-hr threshold ({temporalData?.naaqs_24h_threshold} µg/m³).
                </p>
              </div>
              <span className="text-[10px] font-bold text-amber-400 bg-amber-950/60 border border-amber-500/40 px-2 py-0.5 rounded">
                Exceedance Rate: {temporalData?.exceedance_rate_pct ?? 0}% ({temporalData?.naaqs_exceedance_days ?? 0}/{temporalData?.total_days_analyzed ?? 0} Days)
              </span>
            </div>

            <div className="h-60 w-full">
              {temporalData?.daily_series ? (
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={temporalData.daily_series} margin={{ top: 10, right: 15, left: -15, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
                    <XAxis dataKey="date" tick={{ fill: '#9CA3AF', fontSize: 10 }} />
                    <YAxis tick={{ fill: '#9CA3AF', fontSize: 10 }} />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: '#12161F',
                        borderColor: 'rgba(255,255,255,0.1)',
                        borderRadius: 8,
                        fontSize: 11
                      }}
                    />
                    <ReferenceLine y={temporalData?.naaqs_24h_threshold} stroke="#EF4444" strokeDasharray="4 4" label={{ value: 'NAAQS 24h Limit', fill: '#EF4444', fontSize: 10, position: 'top' }} />
                    <Bar dataKey="daily_average" name="Daily Average (µg/m³)" fill="#FFE547" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <div className="h-full flex items-center justify-center text-xs text-gray-500">
                  Loading daily trends...
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Right Column (5 Cols): Meteorological Correlations & Pollution Rose */}
        <div className="lg:col-span-5 space-y-6">
          {/* Bivariate Meteorological Correlations */}
          <div className="glass-panel p-5 rounded-xl border border-border space-y-4">
            <div>
              <h2 className="text-sm font-bold text-white flex items-center gap-1.5">
                <Compass className="w-4 h-4 text-prana-yellow" />
                Meteorological Dispersion Dynamics
              </h2>
              <p className="text-[11px] text-gray-400">
                Synchronous Pearson correlation with Open-Meteo atmospheric reanalysis.
              </p>
            </div>

            <div className="space-y-3">
              {metData?.correlations && Object.entries(metData.correlations).map(([key, item]: [string, any]) => {
                if (!item) return null;
                const rVal = item.pearson_r;
                const isNegative = rVal < 0;

                return (
                  <div key={key} className="p-3 bg-[#141822] rounded-lg border border-border space-y-1.5 text-xs">
                    <div className="flex items-center justify-between">
                      <span className="font-semibold text-gray-200">{item.variable_name}</span>
                      <span className={`font-mono text-xs font-bold px-2 py-0.5 rounded ${
                        isNegative ? 'bg-blue-950 text-blue-400 border border-blue-500/40' : 'bg-amber-950 text-amber-400 border border-amber-500/40'
                      }`}>
                        r = {rVal} ({isNegative ? 'Inverse/Dilution' : 'Direct'})
                      </span>
                    </div>

                    <div className="flex items-center justify-between text-[11px] text-gray-400">
                      <span>p-value: <span className="font-mono text-gray-300">{item.p_value}</span></span>
                      <span>Linear Slope: <span className="font-mono text-prana-yellow">{item.linear_slope} {pollutant}/{item.variable_unit}</span></span>
                      <span className="text-emerald-400 text-[10px]">Significant: {item.is_statistically_significant ? 'Yes' : 'No'}</span>
                    </div>
                  </div>
                );
              })}
            </div>

            {/* Non-Causal Protocol Callout */}
            <div className="p-3 rounded-lg bg-[#0F131A] border border-white/5 text-[10px] text-gray-400 flex items-start gap-2">
              <Info className="w-3.5 h-3.5 text-prana-yellow shrink-0 mt-0.5" />
              <span>{metData?.scientific_caveat || 'Correlation reflects atmospheric dispersion physics, not physical chemical causation.'}</span>
            </div>
          </div>

          {/* 16-Sector Pollution Rose Distribution */}
          <div className="glass-panel p-5 rounded-xl border border-border space-y-3">
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-1.5">
                  <Compass className="w-3.5 h-3.5 text-prana-sage" />
                  16-Sector Directional Pollution Rose
                </h3>
                <p className="text-[11px] text-gray-400">
                  Mean concentration ({pollutant}) grouped by prevailing wind direction.
                </p>
              </div>
            </div>

            <div className="h-48 w-full">
              {metData?.pollution_rose_16_sectors ? (
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={metData.pollution_rose_16_sectors} margin={{ top: 5, right: 10, left: -25, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
                    <XAxis dataKey="cardinal" tick={{ fill: '#9CA3AF', fontSize: 9 }} />
                    <YAxis tick={{ fill: '#9CA3AF', fontSize: 9 }} />
                    <Tooltip
                      contentStyle={{
                        backgroundColor: '#12161F',
                        borderColor: 'rgba(255,255,255,0.1)',
                        borderRadius: 8,
                        fontSize: 11
                      }}
                    />
                    <Bar dataKey="mean_concentration" name="Mean Concentration (µg/m³)" fill="#8A9A8F" radius={[3, 3, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              ) : (
                <div className="h-full flex items-center justify-center text-xs text-gray-500">
                  No directional wind distribution available.
                </div>
              )}
            </div>
          </div>
        </div>
      </div>

      {/* Spatial Coverage Voids & Unmonitored Zones Table */}
      <div className="glass-panel rounded-xl border border-border overflow-hidden">
        <div className="p-4 border-b border-border flex items-center justify-between">
          <div>
            <h3 className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-1.5">
              <AlertTriangle className="w-3.5 h-3.5 text-amber-400" />
              Documented Spatial Coverage Voids &amp; Uncertainty Boundaries
            </h3>
            <p className="text-[11px] text-gray-400">
              PRANA prohibits synthetic spatial extrapolation into unmonitored industrial corridors.
            </p>
          </div>
          <span className="text-[10px] text-amber-400 font-mono bg-amber-950/40 border border-amber-500/40 px-2 py-0.5 rounded">
            4 Critical Industrial Voids
          </span>
        </div>

        <div className="divide-y divide-white/5">
          {hotspotData?.unmonitored_coverage_voids?.map((v: any, idx: number) => (
            <div key={idx} className="p-4 hover:bg-[#141822] transition-colors space-y-1.5 text-xs">
              <div className="flex items-center justify-between">
                <span className="font-bold text-gray-200">{v.zone_name}</span>
                <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-rose-950 text-rose-300 border border-rose-500/40 font-bold">
                  {v.uncertainty_level}
                </span>
              </div>
              <div className="text-[11px] text-gray-400">
                <strong className="text-gray-300">Nearest Statutory Monitor:</strong> {v.nearest_station} ({v.distance_km} km distance)
              </div>
              <div className="text-[11px] text-gray-400">
                <strong className="text-gray-300">Suspected Unmeasured Sources:</strong> {v.suspected_emission_sources}
              </div>
              <div className="text-[10px] text-amber-400/90 italic pt-1">
                {v.scientific_note}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Save Analysis Form Modal */}
      {showSaveFormModal && (
        <div className="fixed inset-0 bg-black/75 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-[#121620] border border-border rounded-xl w-full max-w-lg p-5 space-y-4 shadow-2xl animate-fade-in text-xs">
            <div className="flex items-center justify-between border-b border-white/10 pb-3">
              <h3 className="text-sm font-bold text-white flex items-center gap-1.5">
                <Save className="w-4 h-4 text-prana-yellow" />
                Save Reproducible Research Analysis
              </h3>
              <button
                onClick={() => setShowSaveFormModal(false)}
                className="text-gray-400 hover:text-white cursor-pointer"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <form onSubmit={handleSaveAnalysis} className="space-y-3.5">
              <div>
                <label className="block text-gray-400 font-semibold mb-1">Analysis Title</label>
                <input
                  type="text"
                  required
                  value={saveTitle}
                  onChange={(e) => setSaveTitle(e.target.value)}
                  placeholder="e.g. Winter PM2.5 Diurnal Inversion & Wind Speed Dilution Audit"
                  className="w-full bg-[#141822] border border-border rounded-lg px-3 py-2 text-gray-200 outline-none"
                />
              </div>

              <div>
                <label className="block text-gray-400 font-semibold mb-1">Research Description / Objective</label>
                <textarea
                  rows={2}
                  value={saveDescription}
                  onChange={(e) => setSaveDescription(e.target.value)}
                  placeholder="Document the scientific hypothesis, target stations, and primary conclusions..."
                  className="w-full bg-[#141822] border border-border rounded-lg px-3 py-2 text-gray-200 outline-none resize-none"
                />
              </div>

              <div>
                <label className="block text-gray-400 font-semibold mb-1">Methodology</label>
                <input
                  type="text"
                  value={saveMethodology}
                  onChange={(e) => setSaveMethodology(e.target.value)}
                  className="w-full bg-[#141822] border border-border rounded-lg px-3 py-2 text-gray-200 outline-none font-mono text-[11px]"
                />
              </div>

              <div>
                <label className="block text-gray-400 font-semibold mb-1">Statutory Citations / References</label>
                <input
                  type="text"
                  value={saveReferences}
                  onChange={(e) => setSaveReferences(e.target.value)}
                  className="w-full bg-[#141822] border border-border rounded-lg px-3 py-2 text-gray-200 outline-none font-mono text-[11px]"
                />
              </div>

              {saveStatusMsg && (
                <div className={`p-2 rounded text-[11px] border ${
                  saveStatusMsg.includes('success') ? 'bg-emerald-950 text-emerald-300 border-emerald-500' : 'bg-rose-950 text-rose-300 border-rose-500'
                }`}>
                  {saveStatusMsg}
                </div>
              )}

              <div className="flex justify-end gap-2 pt-2 border-t border-white/10">
                <button
                  type="button"
                  onClick={() => setShowSaveFormModal(false)}
                  className="px-3 py-1.5 bg-[#141822] text-gray-300 rounded-lg hover:bg-[#1D2433]"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="px-4 py-1.5 bg-prana-yellow text-black font-semibold rounded-lg hover:bg-prana-yellow-hover"
                >
                  Save Analysis
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Saved Analyses Drawer/Modal */}
      {showSavedModal && (
        <div className="fixed inset-0 bg-black/75 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <div className="bg-[#121620] border border-border rounded-xl w-full max-w-2xl max-h-[80vh] flex flex-col p-5 space-y-4 shadow-2xl animate-fade-in text-xs">
            <div className="flex items-center justify-between border-b border-white/10 pb-3">
              <h3 className="text-sm font-bold text-white flex items-center gap-1.5">
                <FolderOpen className="w-4 h-4 text-prana-sage" />
                Saved Research Analyses Library ({savedList.length})
              </h3>
              <button
                onClick={() => setShowSavedModal(false)}
                className="text-gray-400 hover:text-white cursor-pointer"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="overflow-y-auto divide-y divide-white/5 flex-1 pr-1">
              {savedList.map((item) => (
                <div key={item.id} className="py-3 flex items-start justify-between gap-3">
                  <div className="space-y-1">
                    <div className="font-bold text-gray-200">{item.title}</div>
                    <div className="text-[11px] text-gray-400">{item.description || 'No description entered.'}</div>
                    <div className="text-[10px] text-gray-500 font-mono">
                      Pollutant: <span className="text-prana-yellow font-bold">{item.pollutant}</span> • Saved: {new Date(item.created_at).toLocaleDateString()}
                    </div>
                  </div>

                  <div className="flex items-center gap-2 shrink-0">
                    <button
                      onClick={() => handleLoadAnalysis(item)}
                      className="px-2.5 py-1 bg-[#182130] text-prana-yellow hover:bg-[#222F45] border border-prana-yellow/40 rounded text-[11px] font-semibold"
                    >
                      Load
                    </button>
                    <a
                      href={`/api/analysis/workspace/${item.id}/export`}
                      download
                      className="px-2.5 py-1 bg-[#141822] text-gray-300 hover:text-white border border-border rounded text-[11px] flex items-center gap-1"
                    >
                      <Download className="w-3 h-3" />
                      <span>Export CSV</span>
                    </a>
                  </div>
                </div>
              ))}
              {savedList.length === 0 && (
                <div className="py-8 text-center text-gray-500">
                  No analyses saved yet. Click "Save Reproducible Analysis" to store an analysis.
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
