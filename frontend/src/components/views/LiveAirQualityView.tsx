'use client';

import React, { useState } from 'react';
import {
  Activity,
  Download,
  Filter,
  CheckCircle2,
  Clock,
  AlertTriangle,
  FileSpreadsheet,
  ChevronRight,
  ShieldCheck
} from 'lucide-react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid
} from 'recharts';
import { fetchStationHistory } from '@/lib/api';

interface LiveAirQualityViewProps {
  stations: any[];
}

export default function LiveAirQualityView({ stations }: LiveAirQualityViewProps) {
  const [cityFilter, setCityFilter] = useState<string>('ALL');
  const [selectedStation, setSelectedStation] = useState<any>(stations[0] || null);
  const [historyData, setHistoryData] = useState<any[]>([]);
  const [historyPollutant, setHistoryPollutant] = useState<string>('PM2.5');
  const [loadingHistory, setLoadingHistory] = useState<boolean>(false);

  // Filter stations
  const filteredStations = stations.filter((st) => {
    if (cityFilter === 'ALL') return true;
    return st.city.toLowerCase() === cityFilter.toLowerCase();
  });

  // Load history when station selected
  const handleSelectStation = async (st: any) => {
    setSelectedStation(st);
    setLoadingHistory(true);
    try {
      const data = await fetchStationHistory(st.id, historyPollutant, 48);
      setHistoryData(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingHistory(false);
    }
  };

  // Helper for official AQI badge styling
  const getAqiColor = (aqi?: number | null) => {
    if (!aqi) return { bg: 'bg-gray-800', text: 'text-gray-400', label: 'Insufficient Data' };
    if (aqi <= 50) return { bg: 'bg-emerald-950 border-emerald-500', text: 'text-emerald-400', label: 'Good' };
    if (aqi <= 100) return { bg: 'bg-lime-950 border-lime-500', text: 'text-lime-400', label: 'Satisfactory' };
    if (aqi <= 200) return { bg: 'bg-yellow-950 border-yellow-500', text: 'text-yellow-400', label: 'Moderate' };
    if (aqi <= 300) return { bg: 'bg-orange-950 border-orange-500', text: 'text-orange-400', label: 'Poor' };
    if (aqi <= 400) return { bg: 'bg-red-950 border-red-500', text: 'text-red-400', label: 'Very Poor' };
    return { bg: 'bg-rose-950 border-rose-600', text: 'text-rose-400', label: 'Severe' };
  };

  return (
    <div className="space-y-6">
      {/* Top Filter and Download Bar */}
      <div className="glass-panel p-4 rounded-xl border border-border flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-lg font-bold text-white flex items-center gap-2">
            <Activity className="w-5 h-5 text-prana-yellow" />
            Continuous Air Quality Telemetry
          </h1>
          <p className="text-xs text-gray-400">
            Official CPCB National Air Quality Index (NAQI) with sub-index breakdown and provenance validation.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          {/* City filter tabs */}
          <div className="flex items-center space-x-1 bg-[#141822] p-1 rounded-lg border border-border text-xs">
            {['ALL', 'Kolkata', 'Howrah'].map((c) => (
              <button
                key={c}
                onClick={() => setCityFilter(c)}
                className={`px-3 py-1.5 rounded-md font-medium transition-colors ${
                  cityFilter === c
                    ? 'bg-prana-yellow text-black font-semibold'
                    : 'text-gray-400 hover:text-white'
                }`}
              >
                {c === 'ALL' ? 'All Stations' : c}
              </button>
            ))}
          </div>

          {/* Download CSV button */}
          <a
            href="/api/live/download-csv"
            download
            className="flex items-center space-x-1.5 bg-[#181E29] hover:bg-[#222B3A] border border-border text-xs text-gray-200 px-3 py-2 rounded-lg transition-colors"
          >
            <Download className="w-3.5 h-3.5 text-prana-yellow" />
            <span>Download Observations (CSV)</span>
          </a>
        </div>
      </div>

      {/* Main Grid: Station Table (7 Cols) and Detailed Inspection Card (5 Cols) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Table of Stations */}
        <div className="lg:col-span-7 glass-panel rounded-xl border border-border overflow-hidden">
          <div className="p-4 border-b border-border flex items-center justify-between">
            <div className="text-xs font-semibold text-white uppercase tracking-wider">
              Reporting Stations ({filteredStations.length})
            </div>
            <div className="text-[11px] text-prana-sage flex items-center gap-1.5">
              <ShieldCheck className="w-3.5 h-3.5" />
              <span>CPCB Rule: ≥3 Parameters (with PM)</span>
            </div>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-[#10141C] text-gray-400 border-b border-border text-[11px]">
                <tr>
                  <th className="py-3 px-4 font-medium">Station &amp; Area</th>
                  <th className="py-3 px-3 font-medium">PM2.5</th>
                  <th className="py-3 px-3 font-medium">PM10</th>
                  <th className="py-3 px-3 font-medium">NO2</th>
                  <th className="py-3 px-3 font-medium">Official AQI</th>
                  <th className="py-3 px-3 font-medium">Status</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-white/5">
                {filteredStations.map((st) => {
                  const isSelected = selectedStation?.id === st.id;
                  const aqiBadge = getAqiColor(st.aqi);
                  const pm25Val = st.latest_pollutants?.['PM2.5']?.value;
                  const pm10Val = st.latest_pollutants?.['PM10']?.value;
                  const no2Val = st.latest_pollutants?.['NO2']?.value;

                  return (
                    <tr
                      key={st.id}
                      onClick={() => handleSelectStation(st)}
                      className={`cursor-pointer transition-colors ${
                        isSelected ? 'bg-[#181F2C]' : 'hover:bg-[#141822]'
                      }`}
                    >
                      <td className="py-3 px-4">
                        <div className="font-semibold text-gray-200">{st.name}</div>
                        <div className="text-[10px] text-gray-500">
                          {st.station_code} • {st.city}
                        </div>
                      </td>
                      <td className="py-3 px-3 font-mono font-medium text-gray-200">
                        {pm25Val ?? '—'} <span className="text-[9px] text-gray-500">µg/m³</span>
                      </td>
                      <td className="py-3 px-3 font-mono text-gray-300">
                        {pm10Val ?? '—'}
                      </td>
                      <td className="py-3 px-3 font-mono text-gray-400">
                        {no2Val ?? '—'}
                      </td>
                      <td className="py-3 px-3">
                        <span
                          className={`inline-block px-2 py-0.5 rounded text-[11px] font-bold border ${aqiBadge.bg} ${aqiBadge.text}`}
                        >
                          {st.aqi ?? 'N/A'}
                        </span>
                      </td>
                      <td className="py-3 px-3">
                        <span className="inline-flex items-center gap-1 text-[11px] text-emerald-400">
                          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                          {st.status_label}
                        </span>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          </div>
        </div>

        {/* Detailed Station Inspector Panel */}
        <div className="lg:col-span-5 glass-panel p-5 rounded-xl border border-border flex flex-col justify-between space-y-5">
          {selectedStation ? (
            <>
              <div>
                <div className="flex items-start justify-between">
                  <div>
                    <span className="text-[10px] uppercase font-semibold text-prana-sage tracking-wider">
                      Selected Station Metadata
                    </span>
                    <h2 className="text-base font-bold text-white mt-0.5">
                      {selectedStation.name}
                    </h2>
                    <div className="text-xs text-gray-400">
                      {selectedStation.address || `${selectedStation.city}, West Bengal`}
                    </div>
                  </div>
                  <div className="text-right">
                    <span className="text-[10px] text-gray-500">Coordinates</span>
                    <div className="text-xs font-mono text-gray-300">
                      {selectedStation.latitude.toFixed(4)}°N, {selectedStation.longitude.toFixed(4)}°E
                    </div>
                  </div>
                </div>

                {/* Sub-Index Breakdown Grid */}
                <div className="mt-4 pt-4 border-t border-white/10">
                  <div className="text-xs font-semibold text-gray-300 mb-2">
                    CPCB Sub-Index Breakdown
                  </div>
                  <div className="grid grid-cols-4 gap-2 text-center text-xs">
                    {['PM2.5', 'PM10', 'NO2', 'SO2'].map((pol) => {
                      const subIdx = selectedStation.sub_indices?.[pol];
                      return (
                        <div key={pol} className="p-2 rounded bg-[#10141C] border border-border">
                          <div className="text-[10px] text-gray-400">{pol}</div>
                          <div className="text-sm font-bold text-prana-yellow font-mono mt-0.5">
                            {subIdx ?? '—'}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* 48-Hour Historical Inspection Chart */}
                <div className="mt-5 pt-4 border-t border-white/10">
                  <div className="flex items-center justify-between mb-2">
                    <div className="text-xs font-semibold text-gray-300">
                      48-Hour Telemetry ({historyPollutant})
                    </div>
                    <div className="flex items-center space-x-1">
                      {['PM2.5', 'PM10', 'NO2'].map((p) => (
                        <button
                          key={p}
                          onClick={() => {
                            setHistoryPollutant(p);
                            if (selectedStation) handleSelectStation(selectedStation);
                          }}
                          className={`text-[10px] px-2 py-0.5 rounded font-medium ${
                            historyPollutant === p
                              ? 'bg-prana-yellow text-black font-semibold'
                              : 'text-gray-400 hover:text-white'
                          }`}
                        >
                          {p}
                        </button>
                      ))}
                    </div>
                  </div>

                  <div className="h-40 w-full mt-2">
                    {loadingHistory ? (
                      <div className="h-full flex items-center justify-center text-xs text-gray-500 animate-pulse">
                        Loading observation series...
                      </div>
                    ) : historyData.length > 0 ? (
                      <ResponsiveContainer width="100%" height="100%">
                        <LineChart data={historyData} margin={{ top: 5, right: 10, left: -20, bottom: 0 }}>
                          <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
                          <XAxis dataKey="time_label" tick={{ fill: '#9CA3AF', fontSize: 9 }} />
                          <YAxis tick={{ fill: '#9CA3AF', fontSize: 9 }} />
                          <Tooltip
                            contentStyle={{
                              backgroundColor: '#12161F',
                              borderColor: 'rgba(255,255,255,0.1)',
                              borderRadius: 8,
                              fontSize: 11,
                            }}
                          />
                          <Line
                            type="monotone"
                            dataKey="value"
                            stroke="#FFE547"
                            strokeWidth={2}
                            dot={false}
                          />
                        </LineChart>
                      </ResponsiveContainer>
                    ) : (
                      <div className="h-full flex items-center justify-center text-xs text-gray-500">
                        Click any station row above to load historical observation series.
                      </div>
                    )}
                  </div>
                </div>
              </div>

              {/* Provenance Footer */}
              <div className="p-3 rounded-lg bg-[#0F131A] border border-border text-[11px] text-gray-400 space-y-1">
                <div className="flex justify-between">
                  <span>Data Provider:</span>
                  <span className="text-gray-200">West Bengal Pollution Control Board</span>
                </div>
                <div className="flex justify-between">
                  <span>Quality Status:</span>
                  <span className="text-emerald-400">Validated Ground Telemetry</span>
                </div>
              </div>
            </>
          ) : (
            <div className="h-full flex items-center justify-center text-xs text-gray-500">
              Select a monitoring station from the table to view detailed readings.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
