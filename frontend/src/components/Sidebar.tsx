'use client';

import React from 'react';
import {
  LayoutDashboard,
  Activity,
  BarChart3,
  MapPin,
  Factory,
  CloudSun,
  BookOpen,
  FlaskConical,
  Microscope,
  ShieldCheck,
  Settings,
  Wind
} from 'lucide-react';

export type NavSection =
  | 'overview'
  | 'live_aq'
  | 'explorer'
  | 'hotspots'
  | 'sources'
  | 'weather'
  | 'library'
  | 'interventions'
  | 'workspace'
  | 'data_quality'
  | 'settings';

interface SidebarProps {
  activeSection: NavSection;
  onSelectSection: (section: NavSection) => void;
}

const NAV_ITEMS: { id: NavSection; label: string; icon: React.ComponentType<{ className?: string }> }[] = [
  { id: 'overview', label: 'Overview', icon: LayoutDashboard },
  { id: 'live_aq', label: 'Live Air Quality', icon: Activity },
  { id: 'explorer', label: 'Pollution Explorer', icon: BarChart3 },
  { id: 'hotspots', label: 'Geographic Hotspots', icon: MapPin },
  { id: 'sources', label: 'Source Intelligence', icon: Factory },
  { id: 'weather', label: 'Weather & Atmosphere', icon: CloudSun },
  { id: 'library', label: 'Research Library', icon: BookOpen },
  { id: 'interventions', label: 'Intervention Lab', icon: FlaskConical },
  { id: 'workspace', label: 'Analysis Workspace', icon: Microscope },
  { id: 'data_quality', label: 'Data Sources & Quality', icon: ShieldCheck },
  { id: 'settings', label: 'Settings', icon: Settings },
];

export default function Sidebar({ activeSection, onSelectSection }: SidebarProps) {
  return (
    <aside className="w-64 bg-[#0F131A] border-r border-border h-screen flex flex-col justify-between select-none fixed left-0 top-0 z-30">
      <div>
        {/* Brand Header */}
        <div className="p-5 border-b border-border flex items-center space-x-3">
          <div className="w-9 h-9 rounded-lg bg-surface-200 border border-prana-yellow/40 flex items-center justify-center text-prana-yellow shadow-[0_0_15px_rgba(255,229,71,0.15)]">
            <Wind className="w-5 h-5 text-prana-yellow" />
          </div>
          <div>
            <div className="font-bold text-base tracking-tight text-white flex items-center gap-1.5">
              PRANA <span className="text-[11px] font-medium px-1.5 py-0.5 rounded bg-surface-100 text-prana-sage border border-border">HUB</span>
            </div>
            <div className="text-[11px] text-gray-400 font-normal">Kolkata–Howrah Research</div>
          </div>
        </div>

        {/* Navigation Items */}
        <nav className="p-3 space-y-1">
          <div className="text-[10px] uppercase font-semibold text-gray-500 px-3 py-1.5 tracking-wider">
            Research Modules
          </div>
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon;
            const isActive = activeSection === item.id;
            return (
              <button
                key={item.id}
                onClick={() => onSelectSection(item.id)}
                className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg text-xs font-medium transition-all ${
                  isActive
                    ? 'bg-[#181E29] text-prana-yellow border-l-2 border-prana-yellow shadow-sm font-semibold'
                    : 'text-gray-400 hover:text-gray-200 hover:bg-[#141822]'
                }`}
              >
                <Icon className={`w-4 h-4 ${isActive ? 'text-prana-yellow' : 'text-gray-400'}`} />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </div>

      {/* Bottom Environmental Standard Badge */}
      <div className="p-4 border-t border-border bg-[#0C0F14]">
        <div className="rounded-lg bg-surface-300 p-3 border border-border text-[11px] space-y-1">
          <div className="text-gray-400 flex items-center justify-between">
            <span>Air Shed</span>
            <span className="text-prana-yellow font-medium">WB-KOL-01</span>
          </div>
          <div className="text-gray-400 flex items-center justify-between">
            <span>Regulatory Basis</span>
            <span className="text-gray-300">CPCB NAQI 2014</span>
          </div>
          <div className="text-[10px] text-prana-sage pt-1 border-t border-border">
            CSIR-NEERI &amp; TERI Verified
          </div>
        </div>
      </div>
    </aside>
  );
}
