'use client';

import React, { useEffect, useRef, useState } from 'react';
import maplibregl from 'maplibre-gl';

interface Station {
  id: number;
  station_code: string;
  name: string;
  city: string;
  area_type: string;
  latitude: number;
  longitude: number;
  is_fresh: boolean;
  status_label: string;
  aqi?: number | null;
  aqi_category?: string;
  dominant_pollutant?: string;
  latest_pollutants?: Record<string, { value: number; unit: string }>;
}

interface MapProps {
  stations: Station[];
  selectedStationId?: number | null;
  onSelectStation?: (station: Station) => void;
  activePollutant?: string;
  showCoverageGaps?: boolean;
}

export default function MapLibreMap({
  stations,
  selectedStationId,
  onSelectStation,
  activePollutant = 'PM2.5',
  showCoverageGaps = true,
}: MapProps) {
  const mapContainer = useRef<HTMLDivElement>(null);
  const mapInstance = useRef<maplibregl.Map | null>(null);
  const markersRef = useRef<maplibregl.Marker[]>([]);

  useEffect(() => {
    if (!mapContainer.current) return;
    if (mapInstance.current) return;

    // Public OpenStreetMap tiles (100% free, no API key, no watermark)
    const map = new maplibregl.Map({
      container: mapContainer.current,
      style: {
        version: 8,
        sources: {
          'osm-tiles': {
            type: 'raster',
            tiles: [
              'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
            ],
            tileSize: 256,
            attribution: '© OpenStreetMap contributors',
          },
        },
        layers: [
          {
            id: 'osm-tiles-layer',
            type: 'raster',
            source: 'osm-tiles',
            minzoom: 0,
            maxzoom: 19,
          },
        ],
      },
      center: [88.3639, 22.5726], // Kolkata-Howrah centroid
      zoom: 11,
      minZoom: 9,
      maxZoom: 17,
    });

    map.addControl(new maplibregl.NavigationControl(), 'top-right');

    mapInstance.current = map;

    return () => {
      map.remove();
      mapInstance.current = null;
    };
  }, []);

  // Update Markers
  useEffect(() => {
    const map = mapInstance.current;
    if (!map) return;

    // Clear existing markers
    markersRef.current.forEach((m) => m.remove());
    markersRef.current = [];

    stations.forEach((st) => {
      const el = document.createElement('div');
      el.className = 'station-marker-wrapper';
      
      const isSelected = selectedStationId === st.id;
      const pollVal = st.latest_pollutants?.[activePollutant]?.value;
      const isSevere = pollVal && pollVal > 120;
      const isModerate = pollVal && pollVal > 60;

      const bgColor = isSevere ? '#EF4444' : isModerate ? '#F59E0B' : '#10B981';
      const ringColor = isSelected ? '#FFE547' : 'rgba(255,255,255,0.2)';

      el.innerHTML = `
        <div style="
          display: flex;
          align-items: center;
          justify-content: center;
          width: 32px;
          height: 32px;
          border-radius: 50%;
          background: #12161F;
          border: 2px solid ${ringColor};
          box-shadow: 0 0 ${isSelected ? '12px #FFE547' : '6px rgba(0,0,0,0.6)'};
          cursor: pointer;
          transition: transform 0.2s ease;
        ">
          <div style="
            width: 14px;
            height: 14px;
            border-radius: 50%;
            background: ${bgColor};
          "></div>
        </div>
      `;

      el.addEventListener('click', () => {
        if (onSelectStation) {
          onSelectStation(st);
        }
      });

      // Popup
      const popupHtml = `
        <div style="font-size: 12px; font-family: Inter, sans-serif; line-height: 1.5;">
          <div style="font-weight: 700; color: #FFE547; font-size: 13px; margin-bottom: 2px;">${st.name}</div>
          <div style="color: #8A9A8F; font-size: 11px; margin-bottom: 6px;">${st.city} • ${st.area_type}</div>
          <div style="display: flex; justify-content: space-between; margin-bottom: 3px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 4px;">
            <span style="color: #9CA3AF;">Official AQI:</span>
            <span style="font-weight: 600; color: ${st.aqi && st.aqi > 200 ? '#EF4444' : '#FFE547'};">${st.aqi ?? 'N/A'} (${st.aqi_category ?? 'Unknown'})</span>
          </div>
          <div style="display: flex; justify-content: space-between; margin-bottom: 3px;">
            <span style="color: #9CA3AF;">${activePollutant}:</span>
            <span style="font-weight: 600; color: #F3F4F6;">${pollVal ?? 'N/A'} ${st.latest_pollutants?.[activePollutant]?.unit ?? 'µg/m³'}</span>
          </div>
          <div style="margin-top: 6px; font-size: 10px; color: ${st.is_fresh ? '#10B981' : '#F59E0B'}; font-weight: 500;">
            ● Data Status: ${st.status_label}
          </div>
        </div>
      `;

      const popup = new maplibregl.Popup({ offset: 20, closeButton: false }).setHTML(popupHtml);

      const marker = new maplibregl.Marker({ element: el })
        .setLngLat([st.longitude, st.latitude])
        .setPopup(popup)
        .addTo(map);

      markersRef.current.push(marker);
    });
  }, [stations, selectedStationId, activePollutant, onSelectStation]);

  // Center on selected station if changed
  useEffect(() => {
    if (!mapInstance.current || !selectedStationId) return;
    const target = stations.find((s) => s.id === selectedStationId);
    if (target) {
      mapInstance.current.flyTo({
        center: [target.longitude, target.latitude],
        zoom: 12.5,
        speed: 1.2,
      });
    }
  }, [selectedStationId, stations]);

  return (
    <div className="relative w-full h-full min-h-[420px] rounded-xl overflow-hidden border border-border">
      <div ref={mapContainer} className="w-full h-full min-h-[420px] dark-map-tiles" />

      {/* Map Overlay Controls / Scientific Legend */}
      <div className="absolute bottom-4 left-4 glass-panel px-3.5 py-2.5 rounded-lg text-xs space-y-1.5 z-10 pointer-events-auto">
        <div className="text-[11px] font-semibold tracking-wider text-prana-sage uppercase mb-1">
          Kolkata–Howrah Stations ({stations.length})
        </div>
        <div className="flex items-center space-x-2 text-gray-300">
          <span className="w-2.5 h-2.5 rounded-full bg-emerald-500 inline-block"></span>
          <span>Moderate / Satisfactory</span>
        </div>
        <div className="flex items-center space-x-2 text-gray-300">
          <span className="w-2.5 h-2.5 rounded-full bg-amber-500 inline-block"></span>
          <span>Elevated / Poor</span>
        </div>
        <div className="flex items-center space-x-2 text-gray-300">
          <span className="w-2.5 h-2.5 rounded-full bg-red-500 inline-block"></span>
          <span>Severe Hotspot (&gt;120 µg/m³)</span>
        </div>
        {showCoverageGaps && (
          <div className="pt-1 border-t border-white/10 text-[10px] text-gray-400">
            ⚠ South-West Port &amp; Rural Howrah: <span className="text-amber-400">Coverage Gaps</span>
          </div>
        )}
      </div>
    </div>
  );
}
