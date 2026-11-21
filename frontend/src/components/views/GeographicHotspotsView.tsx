'use client';

import React, { useState, useEffect } from 'react';
import {
  MapPin,
  AlertTriangle,
  ShieldAlert,
  Compass,
  ArrowRight,
  Layers,
  Info
} from 'lucide-react';
import { fetchZones } from '@/lib/api';

export default function GeographicHotspotsView() {
  const [zones, setZones] = useState<any[]>([]);
  const [selectedZone, setSelectedZone] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    fetchZones()
      .then((data) => {
        setZones(data);
        if (data.length > 0) setSelectedZone(data[0]);
      })
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="glass-panel p-5 rounded-xl border border-border">
        <h1 className="text-lg font-bold text-white flex items-center gap-2">
          <MapPin className="w-5 h-5 text-prana-yellow" />
          Geographic Hotspots &amp; Spatial Coverage Audit
        </h1>
        <p className="text-xs text-gray-400 mt-1 max-w-3xl leading-relaxed">
          Evaluating structural pollution hotspots across the Kolkata–Howrah conurbation. Where spatial sensor coverage
          is sparse, we explicitly declare <span className="text-amber-400 font-semibold">coverage gaps</span> rather than inventing
          spurious interpolated ward-level measurements.
        </p>
      </div>

      {/* Main Grid: Zones List (6 Cols) & Zone Detail Inspector (6 Cols) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Zones List */}
        <div className="lg:col-span-7 glass-panel rounded-xl border border-border overflow-hidden">
          <div className="p-4 border-b border-border flex items-center justify-between">
            <div className="text-xs font-semibold text-white uppercase tracking-wider">
              Evaluated Zones ({zones.length})
            </div>
            <div className="text-[11px] text-gray-400">
              Sorted by spatial validity &amp; emission significance
            </div>
          </div>

          <div className="divide-y divide-white/5">
            {zones.map((z) => {
              const isSelected = selectedZone?.zone_id === z.zone_id;
              const isGap = z.monitoring_status === 'COVERAGE_GAP';
              const isHotspot = z.is_potential_hotspot;

              return (
                <div
                  key={z.zone_id}
                  onClick={() => setSelectedZone(z)}
                  className={`p-4 cursor-pointer transition-colors ${
                    isSelected ? 'bg-[#181F2C]' : 'hover:bg-[#141822]'
                  }`}
                >
                  <div className="flex items-start justify-between">
                    <div>
                      <div className="font-semibold text-gray-100 flex items-center gap-2">
                        <span>{z.zone_name}</span>
                        {isHotspot && (
                          <span className="text-[10px] bg-rose-950/80 text-rose-400 border border-rose-600 px-2 py-0.5 rounded-full font-bold">
                            Hotspot
                          </span>
                        )}
                        {isGap && (
                          <span className="text-[10px] bg-amber-950/80 text-amber-400 border border-amber-600 px-2 py-0.5 rounded-full font-bold">
                            Coverage Gap
                          </span>
                        )}
                      </div>
                      <div className="text-xs text-gray-400 mt-0.5">
                        {z.city} • {z.zone_type}
                      </div>
                    </div>

                    <div className="text-right text-xs">
                      <span className="text-[10px] text-gray-500">Nearest CAAQM</span>
                      <div className="font-medium text-gray-300">
                        {z.nearest_distance_km} km away
                      </div>
                    </div>
                  </div>

                  <div className="mt-2 text-[11px] text-gray-400 line-clamp-2">
                    {z.scientific_gap_note}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* Selected Zone Deep Dive */}
        <div className="lg:col-span-5 space-y-5">
          {selectedZone ? (
            <div className="glass-panel p-5 rounded-xl border border-border space-y-5">
              <div>
                <span className="text-[10px] uppercase font-semibold text-prana-sage tracking-wider">
                  Zone Spatial Verification Dossier
                </span>
                <h2 className="text-base font-bold text-white mt-1">
                  {selectedZone.zone_name}
                </h2>
                <div className="text-xs text-gray-400">
                  {selectedZone.city} • Lat: {selectedZone.latitude.toFixed(3)}°N, Lng: {selectedZone.longitude.toFixed(3)}°E
                </div>
              </div>

              {/* Coverage & Uncertainty Badge */}
              <div
                className={`p-3.5 rounded-lg border text-xs leading-relaxed ${
                  selectedZone.monitoring_status === 'COVERAGE_GAP'
                    ? 'bg-amber-950/30 border-amber-500 text-amber-200'
                    : 'bg-emerald-950/30 border-emerald-500 text-emerald-200'
                }`}
              >
                <div className="font-bold flex items-center gap-1.5 mb-1">
                  {selectedZone.monitoring_status === 'COVERAGE_GAP' ? (
                    <ShieldAlert className="w-4 h-4 text-amber-400" />
                  ) : (
                    <Info className="w-4 h-4 text-emerald-400" />
                  )}
                  <span>Status: {selectedZone.monitoring_status.replace('_', ' ')}</span>
                </div>
                <div className="text-[11px]">
                  Uncertainty Level: <span className="font-bold">{selectedZone.uncertainty_level}</span>
                </div>
                <div className="text-[11px] mt-1 text-gray-300">
                  {selectedZone.scientific_gap_note}
                </div>
              </div>

              {/* Nearest Sensor Data */}
              <div className="space-y-3 pt-2">
                <div className="text-xs font-semibold text-gray-300">
                  Ground Truth Reference Sensor
                </div>
                <div className="p-3 rounded-lg bg-[#141822] border border-border text-xs space-y-1.5">
                  <div className="flex justify-between">
                    <span className="text-gray-400">Station Name:</span>
                    <span className="font-medium text-white">{selectedZone.nearest_station_name}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Station Code:</span>
                    <span className="font-mono text-prana-yellow">{selectedZone.nearest_station_code}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-gray-400">Geodesic Distance:</span>
                    <span className="text-gray-200">{selectedZone.nearest_distance_km} km</span>
                  </div>
                  <div className="flex justify-between pt-1 border-t border-white/5">
                    <span className="text-gray-400">Recorded PM2.5:</span>
                    <span className="font-bold text-white">
                      {selectedZone.estimated_pm25 ?? 'Unmonitored'} {selectedZone.estimated_pm25 ? 'µg/m³' : ''}
                    </span>
                  </div>
                </div>
              </div>

              {/* Identified Emission Drivers */}
              {selectedZone.hotspot_drivers && selectedZone.hotspot_drivers.length > 0 && (
                <div className="space-y-2 pt-2">
                  <div className="text-xs font-semibold text-rose-400 flex items-center gap-1.5">
                    <AlertTriangle className="w-3.5 h-3.5 text-rose-400" />
                    Confirmed or Suspected Hotspot Drivers
                  </div>
                  <div className="space-y-1.5">
                    {selectedZone.hotspot_drivers.map((d: string, idx: number) => (
                      <div
                        key={idx}
                        className="text-xs text-gray-300 bg-[#10141C] p-2.5 rounded-lg border border-white/5"
                      >
                        • {d}
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          ) : (
            <div className="h-full flex items-center justify-center text-xs text-gray-500">
              Select an evaluated zone to inspect spatial coverage and uncertainty metrics.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
