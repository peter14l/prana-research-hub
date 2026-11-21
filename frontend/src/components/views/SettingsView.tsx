'use client';

import React from 'react';
import {
  Settings,
  Database,
  MapPin,
  Sliders,
  ShieldCheck,
  CheckCircle2,
  Server
} from 'lucide-react';

export default function SettingsView() {
  return (
    <div className="space-y-6 max-w-4xl">
      {/* Top Banner */}
      <div className="glass-panel p-5 rounded-xl border border-border">
        <h1 className="text-lg font-bold text-white flex items-center gap-2">
          <Settings className="w-5 h-5 text-prana-yellow" />
          Platform Configuration &amp; Environmental Settings
        </h1>
        <p className="text-xs text-gray-400 mt-1">
          Review spatial air shed boundaries, CPCB NAQI calculation parameters, and database connectivity.
        </p>
      </div>

      {/* Spatial Boundaries Configuration */}
      <div className="glass-panel p-5 rounded-xl border border-border space-y-4">
        <div className="flex items-center justify-between border-b border-white/5 pb-3">
          <h2 className="text-sm font-bold text-white flex items-center gap-2">
            <MapPin className="w-4 h-4 text-prana-yellow" />
            Study Region Spatial Bounding Box
          </h2>
          <span className="text-[10px] text-emerald-400 bg-emerald-950/60 border border-emerald-500 px-2 py-0.5 rounded font-mono">
            ACTIVE REGION
          </span>
        </div>

        <div className="grid grid-cols-2 gap-4 text-xs">
          <div className="p-3 rounded-lg bg-[#141822] border border-border space-y-1">
            <div className="text-gray-400 font-medium">Region Name</div>
            <div className="text-sm font-bold text-white">Kolkata–Howrah Twin Cities, West Bengal, India</div>
          </div>
          <div className="p-3 rounded-lg bg-[#141822] border border-border space-y-1">
            <div className="text-gray-400 font-medium">Air Shed Centroid</div>
            <div className="text-sm font-mono text-prana-yellow">22.5726°N, 88.3639°E</div>
          </div>
          <div className="p-3 rounded-lg bg-[#141822] border border-border space-y-1">
            <div className="text-gray-400 font-medium">Latitude Extent</div>
            <div className="text-sm font-mono text-gray-200">22.4500°N to 22.6800°N</div>
          </div>
          <div className="p-3 rounded-lg bg-[#141822] border border-border space-y-1">
            <div className="text-gray-400 font-medium">Longitude Extent</div>
            <div className="text-sm font-mono text-gray-200">88.2200°E to 88.4800°E</div>
          </div>
        </div>
      </div>

      {/* CPCB NAQI Settings */}
      <div className="glass-panel p-5 rounded-xl border border-border space-y-4">
        <div className="flex items-center justify-between border-b border-white/5 pb-3">
          <h2 className="text-sm font-bold text-white flex items-center gap-2">
            <Sliders className="w-4 h-4 text-prana-yellow" />
            CPCB Air Quality Index Methodology
          </h2>
          <span className="text-[10px] text-prana-sage bg-surface-200 border border-border px-2 py-0.5 rounded">
            CPCB 2014 Standard
          </span>
        </div>

        <div className="text-xs text-gray-300 space-y-2 leading-relaxed">
          <p>
            • <strong>Multi-Parameter Rule:</strong> Minimum 3 monitored pollutants required, with at least ONE being PM2.5 or PM10.
          </p>
          <p>
            • <strong>Sub-Index Interpolation:</strong> Linear piecewise interpolation across official breakpoint concentrations.
          </p>
          <p>
            • <strong>Dominant Pollutant:</strong> Identified dynamically as the parameter yielding the highest sub-index.
          </p>
        </div>
      </div>

      {/* Database & Runtime Status */}
      <div className="glass-panel p-5 rounded-xl border border-border space-y-4">
        <div className="flex items-center justify-between border-b border-white/5 pb-3">
          <h2 className="text-sm font-bold text-white flex items-center gap-2">
            <Database className="w-4 h-4 text-prana-yellow" />
            Database &amp; Storage Architecture
          </h2>
          <span className="text-[10px] text-emerald-400 bg-emerald-950/60 border border-emerald-500 px-2 py-0.5 rounded font-mono">
            ZERO DOCKER REQUIRED
          </span>
        </div>

        <div className="grid grid-cols-2 gap-4 text-xs">
          <div className="p-3 rounded-lg bg-[#141822] border border-border space-y-1">
            <div className="text-gray-400 font-medium">Database Mode</div>
            <div className="text-sm font-bold text-emerald-400">Embedded Zero-Daemon SQLite Engine</div>
            <div className="text-[10px] text-gray-500">File: backend/data/prana.db</div>
          </div>
          <div className="p-3 rounded-lg bg-[#141822] border border-border space-y-1">
            <div className="text-gray-400 font-medium">Geospatial Processing</div>
            <div className="text-sm font-bold text-white">Shapely / Geodesic Haversine (In-Memory)</div>
            <div className="text-[10px] text-gray-500">PostGIS schema ready</div>
          </div>
        </div>
      </div>
    </div>
  );
}
