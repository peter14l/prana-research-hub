'use client';

import React, { useState, useEffect } from 'react';
import {
  CloudSun,
  Compass,
  Droplets,
  Gauge,
  Thermometer,
  Wind,
  Layers,
  ShieldAlert,
  AlertTriangle
} from 'lucide-react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Legend
} from 'recharts';
import { fetchCurrentWeather, fetchWeatherHistory, fetchWindRose } from '@/lib/api';

export default function WeatherView() {
  const [currentWeather, setCurrentWeather] = useState<any>(null);
  const [history, setHistory] = useState<any[]>([]);
  const [windRose, setWindRose] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    Promise.all([
      fetchCurrentWeather(),
      fetchWeatherHistory(72),
      fetchWindRose()
    ]).then(([curr, hist, wr]) => {
      setCurrentWeather(curr);
      setHistory(hist);
      setWindRose(wr);
      setLoading(false);
    });
  }, []);

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="glass-panel p-5 rounded-xl border border-border">
        <h1 className="text-lg font-bold text-white flex items-center gap-2">
          <CloudSun className="w-5 h-5 text-prana-yellow" />
          Atmospheric Dynamics &amp; Synoptic Meteorology
        </h1>
        <p className="text-xs text-gray-400 mt-1 max-w-3xl leading-relaxed">
          Air pollutant concentrations in the Kolkata–Howrah conurbation are strongly modulated by nocturnal boundary layer
          compression, low winter wind speeds, and temperature inversions.
        </p>

        {/* Scientific Caveat */}
        <div className="mt-3 p-3.5 rounded-lg bg-[#141924] border border-white/10 text-xs text-gray-300 flex items-start space-x-3">
          <ShieldAlert className="w-4 h-4 text-prana-yellow shrink-0 mt-0.5" />
          <div className="text-[11px] leading-relaxed">
            <span className="font-bold text-prana-yellow uppercase">Scientific Meteorological Rule:</span> Wind direction
            indicates air mass trajectory, but does <span className="underline">not</span> prove that a specific upwind source alone
            caused a downwind pollution concentration.
          </div>
        </div>
      </div>

      {/* Atmospheric Metrics Cards */}
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3.5">
        <div className="research-card p-4">
          <div className="flex items-center space-x-2 text-gray-400 text-xs">
            <Thermometer className="w-4 h-4 text-amber-400" />
            <span>Temperature</span>
          </div>
          <div className="text-2xl font-bold text-white mt-1.5 font-mono">
            {currentWeather?.temperature_c ?? '24.2'}°C
          </div>
          <div className="text-[10px] text-gray-500 mt-1">Ground ambient</div>
        </div>

        <div className="research-card p-4">
          <div className="flex items-center space-x-2 text-gray-400 text-xs">
            <Droplets className="w-4 h-4 text-blue-400" />
            <span>Relative Humidity</span>
          </div>
          <div className="text-2xl font-bold text-white mt-1.5 font-mono">
            {currentWeather?.relative_humidity_pct ?? '68'}%
          </div>
          <div className="text-[10px] text-gray-500 mt-1">Hygroscopic growth zone</div>
        </div>

        <div className="research-card p-4">
          <div className="flex items-center space-x-2 text-gray-400 text-xs">
            <Wind className="w-4 h-4 text-emerald-400" />
            <span>Wind Speed</span>
          </div>
          <div className="text-2xl font-bold text-white mt-1.5 font-mono">
            {currentWeather?.wind_speed_kmh ?? '6.8'} <span className="text-xs font-normal">km/h</span>
          </div>
          <div className="text-[10px] text-gray-500 mt-1">Calm to light air</div>
        </div>

        <div className="research-card p-4">
          <div className="flex items-center space-x-2 text-gray-400 text-xs">
            <Compass className="w-4 h-4 text-prana-yellow" />
            <span>Wind Direction</span>
          </div>
          <div className="text-2xl font-bold text-white mt-1.5 font-mono">
            {currentWeather?.wind_direction_cardinal ?? 'NNW'}
          </div>
          <div className="text-[10px] text-gray-500 mt-1">{currentWeather?.wind_direction_deg ?? '340'}° azimuth</div>
        </div>

        <div className="research-card p-4">
          <div className="flex items-center space-x-2 text-gray-400 text-xs">
            <Layers className="w-4 h-4 text-rose-400" />
            <span>PBL Height</span>
          </div>
          <div className="text-2xl font-bold text-rose-400 mt-1.5 font-mono">
            {currentWeather?.boundary_layer_height_m ?? '380'} <span className="text-xs font-normal">m</span>
          </div>
          <div className="text-[10px] text-rose-400/80 mt-1">Shallow winter trap (&lt;450m)</div>
        </div>

        <div className="research-card p-4">
          <div className="flex items-center space-x-2 text-gray-400 text-xs">
            <Gauge className="w-4 h-4 text-prana-sage" />
            <span>Surface Pressure</span>
          </div>
          <div className="text-2xl font-bold text-white mt-1.5 font-mono">
            {currentWeather?.surface_pressure_hpa ?? '1014.5'} <span className="text-xs font-normal">hPa</span>
          </div>
          <div className="text-[10px] text-gray-500 mt-1">High pressure ridge</div>
        </div>
      </div>

      {/* Weather Time Series (72 Hours) */}
      <div className="glass-panel p-5 rounded-xl border border-border space-y-4">
        <div>
          <h2 className="text-sm font-bold text-white">
            72-Hour Boundary Layer &amp; Meteorological Profile
          </h2>
          <p className="text-xs text-gray-400">
            Observation of diurnal boundary layer collapse trapping surface emissions during night hours.
          </p>
        </div>

        <div className="h-72 w-full mt-2">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={history} margin={{ top: 10, right: 20, left: -10, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
              <XAxis dataKey="display_time" tick={{ fill: '#9CA3AF', fontSize: 10 }} />
              <YAxis yAxisId="left" tick={{ fill: '#9CA3AF', fontSize: 10 }} />
              <YAxis yAxisId="right" orientation="right" tick={{ fill: '#9CA3AF', fontSize: 10 }} unit="m" />
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
                yAxisId="right"
                type="monotone"
                dataKey="boundary_layer_height_m"
                stroke="#EF4444"
                strokeWidth={2}
                name="Planetary Boundary Layer Height (m)"
                dot={false}
              />
              <Line
                yAxisId="left"
                type="monotone"
                dataKey="temperature_c"
                stroke="#FFE547"
                strokeWidth={2}
                name="Temperature (°C)"
                dot={false}
              />
              <Line
                yAxisId="left"
                type="monotone"
                dataKey="wind_speed_kmh"
                stroke="#10B981"
                strokeWidth={2}
                name="Wind Speed (km/h)"
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* 16-Sector Wind Rose Table & Distribution */}
      <div className="glass-panel p-5 rounded-xl border border-border space-y-3">
        <h3 className="text-sm font-bold text-white flex items-center gap-1.5">
          <Compass className="w-4 h-4 text-prana-yellow" />
          Wind Direction Frequency Distribution (16 Cardinal Sectors)
        </h3>
        <p className="text-xs text-gray-400">
          Distribution of wind directions showing dominant North-North-West (NNW) winter transport corridor.
        </p>

        <div className="grid grid-cols-4 md:grid-cols-8 gap-2 text-center text-xs pt-2">
          {windRose.slice(0, 16).map((wr) => (
            <div key={wr.direction} className="p-2.5 rounded-lg bg-[#141822] border border-border">
              <div className="font-bold text-prana-yellow">{wr.direction}</div>
              <div className="text-sm font-semibold text-white mt-1 font-mono">
                {wr.frequency_pct}%
              </div>
              <div className="text-[10px] text-gray-500 mt-0.5">{wr.total_count} hrs</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
