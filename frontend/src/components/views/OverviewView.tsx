'use client';

import React, { useState } from 'react';
import {
  Activity,
  AlertTriangle,
  ArrowUpRight,
  ChevronRight,
  Clock,
  Compass,
  Layers,
  MapPin,
  TrendingUp,
  Wind
} from 'lucide-react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid
} from 'recharts';
import MapLibreMap from '../map/MapLibreMap';

interface OverviewViewProps {
  summary: any;
  stations: any[];
  trends: any[];
  onSelectStation: (st: any) => void;
  onNavigate: (section: any) => void;
}

export default function OverviewView({
  summary,
  stations,
  trends,
  onSelectStation,
  onNavigate,
}: OverviewViewProps) {
  const [activePollutant, setActivePollutant] = useState<string>('PM2.5');
  const [selectedStation, setSelectedStation] = useState<any>(null);

  const pollutants = ['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'O3'];

  // Metric card helper
  const getMetric = (key: string, unit: string) => {
    const val = summary?.[key];
    return {
      value: val ?? '—',
      unit,
    };
  };

  const metrics = [
    { label: 'PM2.5 (Fine)', key: 'pm25_avg', unit: 'µg/m³', limit: '60 (24h std)', high: 90 },
    { label: 'PM10 (Coarse)', key: 'pm10_avg', unit: 'µg/m³', limit: '100 (24h std)', high: 150 },
    { label: 'NO2 (Nitrogen Dioxide)', key: 'no2_avg', unit: 'µg/m³', limit: '80 (24h std)', high: 60 },
    { label: 'SO2 (Sulfur Dioxide)', key: 'so2_avg', unit: 'µg/m³', limit: '80 (24h std)', high: 30 },
    { label: 'CO (Carbon Monoxide)', key: 'co_avg', unit: 'mg/m³', limit: '4.0 (8h std)', high: 2.0 },
    { label: 'O3 (Ozone)', key: 'o3_avg', unit: 'µg/m³', limit: '100 (8h std)', high: 80 },
  ];

  return (
    <div className="space-y-6">
      {/* Top Regional Status Bar */}
      <div className="glass-panel p-5 rounded-xl border border-border flex flex-wrap items-center justify-between gap-4">
        <div>
          <div className="flex items-center space-x-2">
            <span className="w-2.5 h-2.5 rounded-full bg-prana-yellow animate-ping"></span>
            <span className="text-xs uppercase font-semibold tracking-wider text-prana-sage">
              Regional Air Quality Status
            </span>
          </div>
          <h1 className="text-xl font-bold text-white mt-1">
            Kolkata–Howrah Twin Cities Air Shed
          </h1>
          <p className="text-xs text-gray-400 mt-0.5">
            Real-time telemetry aggregated across {summary?.reporting_stations ?? 9} statutory CAAQM stations.
          </p>
        </div>

        <div className="flex items-center space-x-6 text-xs">
          <div className="text-right">
            <div className="text-gray-400">Dominant Category</div>
            <div className="text-base font-bold text-amber-400">
              {summary?.dominant_category ?? 'Poor'}
            </div>
          </div>
          <div className="h-8 w-px bg-white/10" />
          <div className="text-right">
            <div className="text-gray-400">Station Availability</div>
            <div className="text-base font-bold text-emerald-400">
              {summary?.reporting_stations ?? 9} / {summary?.total_stations ?? 9}
            </div>
          </div>
          <div className="h-8 w-px bg-white/10" />
          <div className="text-right">
            <div className="text-gray-400">Stale Stations</div>
            <div className="text-base font-bold text-gray-300">
              {summary?.stale_stations ?? 0}
            </div>
          </div>
        </div>
      </div>

      {/* Six Pollutant Measurement Grid */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3.5">
        {metrics.map((m) => {
          const met = getMetric(m.key, m.unit);
          const isHigh = typeof met.value === 'number' && met.value >= m.high;
          const isSelected = activePollutant === m.label.split(' ')[0];

          return (
            <button
              key={m.key}
              onClick={() => setActivePollutant(m.label.split(' ')[0])}
              className={`research-card p-4 text-left transition-all relative ${
                isSelected
                  ? 'border-prana-yellow shadow-[0_0_15px_rgba(255,229,71,0.15)] bg-[#171E2B]'
                  : 'hover:border-white/20'
              }`}
            >
              <div className="flex justify-between items-start">
                <span className="text-[11px] font-medium text-gray-400">{m.label.split(' ')[0]}</span>
                {isHigh && (
                  <span className="w-2 h-2 rounded-full bg-amber-400" title="Exceeds standard"></span>
                )}
              </div>
              <div className="text-2xl font-bold text-white mt-1.5 font-mono">
                {met.value}
              </div>
              <div className="text-[10px] text-prana-sage mt-0.5">{met.unit}</div>
              <div className="text-[9px] text-gray-500 mt-2 pt-1 border-t border-white/5">
                NAAQS: {m.limit}
              </div>
            </button>
          );
        })}
      </div>

      {/* Main Map & Trends Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Interactive Map (7 Cols) */}
        <div className="lg:col-span-7 glass-panel p-4 rounded-xl border border-border flex flex-col">
          <div className="flex items-center justify-between mb-3">
            <div>
              <h2 className="text-sm font-semibold text-white flex items-center gap-2">
                <MapPin className="w-4 h-4 text-prana-yellow" />
                Regional Pollution Telemetry Map
              </h2>
              <div className="text-[11px] text-gray-400">
                Visualizing {activePollutant} observations across Kolkata &amp; Howrah
              </div>
            </div>

            {/* Pollutant selector pills */}
            <div className="flex items-center space-x-1 bg-[#141822] p-1 rounded-lg border border-border">
              {['PM2.5', 'PM10', 'NO2', 'SO2'].map((p) => (
                <button
                  key={p}
                  onClick={() => setActivePollutant(p)}
                  className={`text-[10px] px-2 py-1 rounded font-medium transition-colors ${
                    activePollutant === p
                      ? 'bg-prana-yellow text-black font-semibold'
                      : 'text-gray-400 hover:text-white'
                  }`}
                >
                  {p}
                </button>
              ))}
            </div>
          </div>

          {/* Map Component */}
          <div className="flex-1 min-h-[440px]">
            <MapLibreMap
              stations={stations}
              selectedStationId={selectedStation?.id}
              onSelectStation={(st) => {
                setSelectedStation(st);
                onSelectStation(st);
              }}
              activePollutant={activePollutant}
            />
          </div>

          <div className="mt-3 text-[10px] text-gray-500 flex justify-between items-center">
            <span>Map tiles: OpenStreetMap / Carto Dark • Coordinate System: WGS 84</span>
            <span className="text-prana-sage">● Real stations only (No interpolated heatmaps)</span>
          </div>
        </div>

        {/* Right Column: 7-Day Trend Chart & Station Snapshot (5 Cols) */}
        <div className="lg:col-span-5 space-y-6 flex flex-col justify-between">
          {/* Trend Chart */}
          <div className="glass-panel p-5 rounded-xl border border-border">
            <div className="flex items-center justify-between mb-3">
              <div>
                <h3 className="text-sm font-semibold text-white flex items-center gap-1.5">
                  <TrendingUp className="w-4 h-4 text-prana-sage" />
                  7-Day Regional Trend ({activePollutant})
                </h3>
                <p className="text-[11px] text-gray-400">Daily mean with diurnal min/max envelope</p>
              </div>
              <button
                onClick={() => onNavigate('explorer')}
                className="text-xs text-prana-yellow hover:underline flex items-center gap-0.5"
              >
                Explorer <ChevronRight className="w-3.5 h-3.5" />
              </button>
            </div>

            <div className="h-44 w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={trends} margin={{ top: 5, right: 10, left: -20, bottom: 0 }}>
                  <defs>
                    <linearGradient id="trendGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#FFE547" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#FFE547" stopOpacity={0.0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
                  <XAxis dataKey="date" tick={{ fill: '#9CA3AF', fontSize: 10 }} />
                  <YAxis tick={{ fill: '#9CA3AF', fontSize: 10 }} />
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
                    dataKey="average"
                    stroke="#FFE547"
                    strokeWidth={2}
                    fillOpacity={1}
                    fill="url(#trendGradient)"
                    name={`${activePollutant} Avg`}
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </div>

          {/* Evidence-Backed Research Highlights */}
          <div className="glass-panel p-5 rounded-xl border border-border flex-1">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-semibold text-white flex items-center gap-1.5">
                <Layers className="w-4 h-4 text-prana-yellow" />
                Evidence-Backed Highlights
              </h3>
              <span className="text-[10px] text-prana-sage uppercase font-medium">Validated</span>
            </div>

            <div className="space-y-3">
              {summary?.highlights?.map((h: any) => (
                <div
                  key={h.id}
                  onClick={() => onNavigate(h.evidence_link.replace('/', ''))}
                  className="p-3 rounded-lg bg-[#141822] border border-white/5 hover:border-prana-yellow/30 cursor-pointer transition-all text-xs"
                >
                  <div className="font-semibold text-gray-200 flex items-center justify-between">
                    <span>{h.title}</span>
                    <ArrowUpRight className="w-3.5 h-3.5 text-prana-yellow opacity-70" />
                  </div>
                  <div className="text-gray-400 text-[11px] mt-1 leading-relaxed">
                    {h.statement}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
