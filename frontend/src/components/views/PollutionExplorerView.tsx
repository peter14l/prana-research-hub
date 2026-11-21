'use client';

import React, { useState, useEffect } from 'react';
import {
  BarChart3,
  Calendar,
  Clock,
  GitCompare,
  ScatterChart as ScatterIcon,
  AlertTriangle,
  Info,
  TrendingDown,
  TrendingUp
} from 'lucide-react';
import {
  AreaChart,
  Area,
  BarChart,
  Bar,
  LineChart,
  Line,
  ScatterChart,
  Scatter,
  XAxis,
  YAxis,
  ZAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Legend
} from 'recharts';
import {
  fetchDiurnal,
  fetchDayOfWeek,
  fetchCorrelation,
  fetchStationComparison
} from '@/lib/api';

export default function PollutionExplorerView() {
  const [activeTab, setActiveTab] = useState<'diurnal' | 'dow' | 'correlation' | 'compare'>('diurnal');
  const [pollutant, setPollutant] = useState<string>('PM2.5');
  
  // Diurnal state
  const [diurnalData, setDiurnalData] = useState<any[]>([]);
  // Day of week state
  const [dowData, setDowData] = useState<any[]>([]);
  // Correlation state
  const [varX, setVarX] = useState<string>('PM2.5');
  const [varY, setVarY] = useState<string>('PBLH');
  const [corrResult, setCorrResult] = useState<any>(null);
  // Multi-station comparison state
  const [compareData, setCompareData] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(false);

  useEffect(() => {
    loadTabData();
  }, [activeTab, pollutant, varX, varY]);

  async function loadTabData() {
    setLoading(true);
    try {
      if (activeTab === 'diurnal') {
        const data = await fetchDiurnal(pollutant);
        setDiurnalData(data);
      } else if (activeTab === 'dow') {
        const data = await fetchDayOfWeek(pollutant);
        setDowData(data);
      } else if (activeTab === 'correlation') {
        const data = await fetchCorrelation(varX, varY);
        setCorrResult(data);
      } else if (activeTab === 'compare') {
        // Compare Victoria (1), RBU (3), Ghusuri (7)
        const data = await fetchStationComparison(pollutant, '1,3,7', 72);
        setCompareData(data);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-6">
      {/* Top Header & Tab Navigation */}
      <div className="glass-panel p-4 rounded-xl border border-border flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-lg font-bold text-white flex items-center gap-2">
            <BarChart3 className="w-5 h-5 text-prana-yellow" />
            Pollution Explorer &amp; Pattern Analysis
          </h1>
          <p className="text-xs text-gray-400">
            Investigate diurnal atmospheric regimes, weekly cycles, and non-causal bivariate correlations.
          </p>
        </div>

        {/* Tab Switcher */}
        <div className="flex items-center space-x-1 bg-[#141822] p-1 rounded-lg border border-border text-xs">
          <button
            onClick={() => setActiveTab('diurnal')}
            className={`px-3 py-1.5 rounded-md font-medium flex items-center gap-1.5 transition-colors ${
              activeTab === 'diurnal'
                ? 'bg-prana-yellow text-black font-semibold'
                : 'text-gray-400 hover:text-white'
            }`}
          >
            <Clock className="w-3.5 h-3.5" />
            <span>24-Hour Diurnal</span>
          </button>
          <button
            onClick={() => setActiveTab('dow')}
            className={`px-3 py-1.5 rounded-md font-medium flex items-center gap-1.5 transition-colors ${
              activeTab === 'dow'
                ? 'bg-prana-yellow text-black font-semibold'
                : 'text-gray-400 hover:text-white'
            }`}
          >
            <Calendar className="w-3.5 h-3.5" />
            <span>Day-of-Week</span>
          </button>
          <button
            onClick={() => setActiveTab('correlation')}
            className={`px-3 py-1.5 rounded-md font-medium flex items-center gap-1.5 transition-colors ${
              activeTab === 'correlation'
                ? 'bg-prana-yellow text-black font-semibold'
                : 'text-gray-400 hover:text-white'
            }`}
          >
            <ScatterIcon className="w-3.5 h-3.5" />
            <span>Correlation Analysis</span>
          </button>
          <button
            onClick={() => setActiveTab('compare')}
            className={`px-3 py-1.5 rounded-md font-medium flex items-center gap-1.5 transition-colors ${
              activeTab === 'compare'
                ? 'bg-prana-yellow text-black font-semibold'
                : 'text-gray-400 hover:text-white'
            }`}
          >
            <GitCompare className="w-3.5 h-3.5" />
            <span>Station Comparison</span>
          </button>
        </div>
      </div>

      {/* Tab Content */}
      {activeTab === 'diurnal' && (
        <div className="glass-panel p-6 rounded-xl border border-border space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-base font-bold text-white">24-Hour Diurnal Profile ({pollutant})</h2>
              <p className="text-xs text-gray-400">
                Hourly mean across Kolkata–Howrah stations highlighting morning commute and nocturnal inversion peaks.
              </p>
            </div>
            <div className="flex items-center space-x-1.5">
              {['PM2.5', 'PM10', 'NO2', 'SO2', 'CO'].map((p) => (
                <button
                  key={p}
                  onClick={() => setPollutant(p)}
                  className={`text-xs px-2.5 py-1 rounded font-medium ${
                    pollutant === p ? 'bg-prana-yellow text-black font-semibold' : 'text-gray-400 hover:text-white'
                  }`}
                >
                  {p}
                </button>
              ))}
            </div>
          </div>

          <div className="h-80 w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={diurnalData} margin={{ top: 10, right: 20, left: -10, bottom: 0 }}>
                <defs>
                  <linearGradient id="diurnalFill" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#FFE547" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="#FFE547" stopOpacity={0.0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
                <XAxis dataKey="hour_label" tick={{ fill: '#9CA3AF', fontSize: 11 }} />
                <YAxis tick={{ fill: '#9CA3AF', fontSize: 11 }} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#12161F',
                    borderColor: 'rgba(255,255,255,0.1)',
                    borderRadius: 8,
                    fontSize: 12,
                  }}
                />
                <Area
                  type="monotone"
                  dataKey="mean"
                  stroke="#FFE547"
                  strokeWidth={2.5}
                  fill="url(#diurnalFill)"
                  name={`Mean ${pollutant}`}
                />
                <Line type="monotone" dataKey="p75" stroke="#F59E0B" strokeDasharray="4 4" dot={false} name="75th Percentile" />
                <Line type="monotone" dataKey="p25" stroke="#8A9A8F" strokeDasharray="4 4" dot={false} name="25th Percentile" />
              </AreaChart>
            </ResponsiveContainer>
          </div>

          <div className="grid grid-cols-3 gap-4 pt-4 border-t border-white/10 text-xs">
            <div className="p-3 rounded-lg bg-[#141822] border border-border">
              <span className="text-gray-400 font-medium">Morning Peak (08:00–10:00)</span>
              <div className="text-sm font-bold text-prana-yellow mt-1">Commuter Traffic + Early Sun Dispersion</div>
              <p className="text-[11px] text-gray-500 mt-0.5">Heavy bus and taxi transit across Howrah Bridge and arterial corridors.</p>
            </div>
            <div className="p-3 rounded-lg bg-[#141822] border border-border">
              <span className="text-gray-400 font-medium">Afternoon Minimum (13:00–16:00)</span>
              <div className="text-sm font-bold text-emerald-400 mt-1">Solar Convective Dilution</div>
              <p className="text-[11px] text-gray-500 mt-0.5">Boundary layer height expands above 1,200m, dispersing particulate mass.</p>
            </div>
            <div className="p-3 rounded-lg bg-[#141822] border border-border">
              <span className="text-gray-400 font-medium">Nocturnal Inversion (21:00–02:00)</span>
              <div className="text-sm font-bold text-rose-400 mt-1">Surface Inversion + Freight Entry</div>
              <p className="text-[11px] text-gray-500 mt-0.5">Post-curfew commercial diesel trucks enter Kolkata under shallow PBLH (&lt;380m).</p>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'dow' && (
        <div className="glass-panel p-6 rounded-xl border border-border space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-base font-bold text-white">Day-of-Week Pattern ({pollutant})</h2>
              <p className="text-xs text-gray-400">
                Investigating the 'weekend effect' versus industrial workweek activity in Kolkata and Howrah.
              </p>
            </div>
            <div className="flex items-center space-x-1.5">
              {['PM2.5', 'PM10', 'NO2', 'SO2'].map((p) => (
                <button
                  key={p}
                  onClick={() => setPollutant(p)}
                  className={`text-xs px-2.5 py-1 rounded font-medium ${
                    pollutant === p ? 'bg-prana-yellow text-black font-semibold' : 'text-gray-400 hover:text-white'
                  }`}
                >
                  {p}
                </button>
              ))}
            </div>
          </div>

          <div className="h-80 w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={dowData} margin={{ top: 10, right: 20, left: -10, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
                <XAxis dataKey="day" tick={{ fill: '#9CA3AF', fontSize: 11 }} />
                <YAxis tick={{ fill: '#9CA3AF', fontSize: 11 }} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#12161F',
                    borderColor: 'rgba(255,255,255,0.1)',
                    borderRadius: 8,
                    fontSize: 12,
                  }}
                />
                <Bar dataKey="mean" fill="#FFE547" radius={[4, 4, 0, 0]} name={`Mean ${pollutant}`} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}

      {activeTab === 'correlation' && (
        <div className="glass-panel p-6 rounded-xl border border-border space-y-5">
          <div className="flex flex-wrap items-center justify-between gap-4">
            <div>
              <h2 className="text-base font-bold text-white">Bivariate Environmental Correlation Workspace</h2>
              <p className="text-xs text-gray-400">
                Explore empirical associations between continuous pollutant and meteorological parameters.
              </p>
            </div>

            {/* Variable selectors */}
            <div className="flex items-center space-x-3 text-xs">
              <div className="flex items-center space-x-1.5 bg-[#141822] border border-border px-3 py-1.5 rounded-lg">
                <span className="text-gray-400">Var X:</span>
                <select
                  value={varX}
                  onChange={(e) => setVarX(e.target.value)}
                  className="bg-transparent text-prana-yellow font-medium outline-none cursor-pointer"
                >
                  <option value="PM2.5" className="bg-[#12161F] text-gray-200">PM2.5</option>
                  <option value="PM10" className="bg-[#12161F] text-gray-200">PM10</option>
                  <option value="NO2" className="bg-[#12161F] text-gray-200">NO2</option>
                  <option value="SO2" className="bg-[#12161F] text-gray-200">SO2</option>
                  <option value="Temperature" className="bg-[#12161F] text-gray-200">Temperature</option>
                  <option value="WindSpeed" className="bg-[#12161F] text-gray-200">Wind Speed</option>
                </select>
              </div>

              <div className="text-gray-500 font-bold">vs</div>

              <div className="flex items-center space-x-1.5 bg-[#141822] border border-border px-3 py-1.5 rounded-lg">
                <span className="text-gray-400">Var Y:</span>
                <select
                  value={varY}
                  onChange={(e) => setVarY(e.target.value)}
                  className="bg-transparent text-prana-yellow font-medium outline-none cursor-pointer"
                >
                  <option value="PBLH" className="bg-[#12161F] text-gray-200">Boundary Layer Height (PBLH)</option>
                  <option value="WindSpeed" className="bg-[#12161F] text-gray-200">Wind Speed</option>
                  <option value="Humidity" className="bg-[#12161F] text-gray-200">Relative Humidity</option>
                  <option value="Temperature" className="bg-[#12161F] text-gray-200">Temperature</option>
                  <option value="PM10" className="bg-[#12161F] text-gray-200">PM10</option>
                  <option value="NO2" className="bg-[#12161F] text-gray-200">NO2</option>
                </select>
              </div>
            </div>
          </div>

          {/* Mandatory Scientific Non-Causal Caveat Banner */}
          <div className="p-3.5 rounded-lg bg-[#141924] border border-prana-yellow/30 text-xs text-gray-300 flex items-start space-x-3">
            <AlertTriangle className="w-5 h-5 text-prana-yellow shrink-0 mt-0.5" />
            <div className="text-[11px] leading-relaxed">
              <span className="font-bold text-prana-yellow uppercase tracking-wider block mb-0.5">
                Scientific Non-Causal Protocol
              </span>
              {corrResult?.scientific_caveat ?? (
                'Empirical correlation indicates statistical co-occurrence under shared meteorology, but DOES NOT prove causation.'
              )}
            </div>
          </div>

          {/* Scatter Plot & Correlation Coefficients */}
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 pt-2">
            <div className="lg:col-span-8 h-72">
              {corrResult?.scatter_points ? (
                <ResponsiveContainer width="100%" height="100%">
                  <ScatterChart margin={{ top: 10, right: 20, left: -10, bottom: 10 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
                    <XAxis type="number" dataKey="x" name={varX} tick={{ fill: '#9CA3AF', fontSize: 11 }} />
                    <YAxis type="number" dataKey="y" name={varY} tick={{ fill: '#9CA3AF', fontSize: 11 }} />
                    <Tooltip
                      cursor={{ strokeDasharray: '3 3' }}
                      contentStyle={{
                        backgroundColor: '#12161F',
                        borderColor: 'rgba(255,255,255,0.1)',
                        borderRadius: 8,
                        fontSize: 11,
                      }}
                    />
                    <Scatter name={`${varX} vs ${varY}`} data={corrResult.scatter_points} fill="#FFE547" />
                  </ScatterChart>
                </ResponsiveContainer>
              ) : (
                <div className="h-full flex items-center justify-center text-xs text-gray-500">
                  Computing bivariate correlation...
                </div>
              )}
            </div>

            <div className="lg:col-span-4 space-y-3">
              <div className="p-4 rounded-xl bg-[#141822] border border-border">
                <span className="text-[10px] text-gray-400 uppercase font-semibold">Pearson r Coefficient</span>
                <div className="text-2xl font-bold font-mono text-white mt-1">
                  {corrResult?.pearson_r ?? '—'}
                </div>
                <div className="text-[11px] text-prana-sage mt-0.5">
                  p-value: {corrResult?.pearson_p_value ? corrResult.pearson_p_value.toExponential(3) : '—'}
                </div>
              </div>

              <div className="p-4 rounded-xl bg-[#141822] border border-border">
                <span className="text-[10px] text-gray-400 uppercase font-semibold">Spearman Rank (ρ)</span>
                <div className="text-2xl font-bold font-mono text-white mt-1">
                  {corrResult?.spearman_rho ?? '—'}
                </div>
                <div className="text-[11px] text-gray-400 mt-0.5">
                  Monotonic non-parametric rank association
                </div>
              </div>

              <div className="p-3 rounded-lg bg-[#0F131A] border border-border text-[11px] text-gray-400">
                <div className="font-semibold text-gray-200 mb-0.5">Interpretation</div>
                {corrResult?.relationship_summary ?? 'Calculating...'}
              </div>
            </div>
          </div>
        </div>
      )}

      {activeTab === 'compare' && (
        <div className="glass-panel p-6 rounded-xl border border-border space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-base font-bold text-white">Multi-Station Spatial Comparison ({pollutant})</h2>
              <p className="text-xs text-gray-400">
                Side-by-side time series: Ghusuri (Howrah Industrial) vs RBU (North Traffic) vs Victoria Memorial (Background).
              </p>
            </div>
          </div>

          <div className="h-80 w-full mt-4">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={compareData} margin={{ top: 10, right: 20, left: -10, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
                <XAxis dataKey="display_time" tick={{ fill: '#9CA3AF', fontSize: 10 }} />
                <YAxis tick={{ fill: '#9CA3AF', fontSize: 11 }} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#12161F',
                    borderColor: 'rgba(255,255,255,0.1)',
                    borderRadius: 8,
                    fontSize: 11,
                  }}
                />
                <Legend wrapperStyle={{ fontSize: 12, paddingTop: 10 }} />
                <Line
                  type="monotone"
                  dataKey="st_7"
                  stroke="#EF4444"
                  strokeWidth={2}
                  name="Ghusuri (Howrah Foundry Hotspot)"
                  dot={false}
                />
                <Line
                  type="monotone"
                  dataKey="st_3"
                  stroke="#F59E0B"
                  strokeWidth={2}
                  name="RBU (BT Road Traffic Hotspot)"
                  dot={false}
                />
                <Line
                  type="monotone"
                  dataKey="st_1"
                  stroke="#10B981"
                  strokeWidth={2}
                  name="Victoria Memorial (Urban Background)"
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      )}
    </div>
  );
}
