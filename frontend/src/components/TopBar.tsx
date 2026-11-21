'use client';

import React, { useState } from 'react';
import {
  Search,
  Sparkles,
  Download,
  Calendar,
  MapPin,
  Clock,
  ShieldAlert,
  ShieldCheck,
  Info
} from 'lucide-react';

interface TopBarProps {
  selectedCity: string;
  onSelectCity: (city: string) => void;
  dateRange: string;
  onSelectDateRange: (range: string) => void;
  searchQuery: string;
  onSearchChange: (q: string) => void;
  onOpenAssistant: () => void;
  onExportReport: () => void;
  lastUpdate?: string;
  dataIntegrity?: any;
  activeViewTitle: string;
}

export default function TopBar({
  selectedCity,
  onSelectCity,
  dateRange,
  onSelectDateRange,
  searchQuery,
  onSearchChange,
  onOpenAssistant,
  onExportReport,
  lastUpdate = 'Just now',
  dataIntegrity,
  activeViewTitle,
}: TopBarProps) {
  const [showIntegrityPopover, setShowIntegrityPopover] = useState(false);

  const counts = dataIntegrity?.counts || { VERIFIED: 0, IMPORTED: 0, DEMO: 10565 };
  const verifiedPct = dataIntegrity?.verified_pct ?? 0.0;
  const demoPct = dataIntegrity?.demo_pct ?? 100.0;
  const importedPct = dataIntegrity?.imported_pct ?? 0.0;

  return (
    <header className="h-16 bg-[#0E1219]/90 backdrop-blur-md border-b border-border px-6 flex items-center justify-between sticky top-0 z-20">
      {/* Active view breadcrumb & Region selector */}
      <div className="flex items-center space-x-4">
        <div>
          <span className="text-xs text-gray-400">PRANA Hub /</span>{' '}
          <span className="text-sm font-semibold text-white">{activeViewTitle}</span>
        </div>

        {/* Region selector */}
        <div className="flex items-center space-x-1.5 bg-[#141822] border border-border px-2.5 py-1 rounded-md text-xs">
          <MapPin className="w-3.5 h-3.5 text-prana-yellow" />
          <select
            value={selectedCity}
            onChange={(e) => onSelectCity(e.target.value)}
            className="bg-transparent text-gray-200 outline-none cursor-pointer"
          >
            <option value="ALL" className="bg-[#12161F] text-gray-200">Kolkata–Howrah Region</option>
            <option value="Kolkata" className="bg-[#12161F] text-gray-200">Kolkata Municipal Corp</option>
            <option value="Howrah" className="bg-[#12161F] text-gray-200">Howrah Municipal Corp</option>
          </select>
        </div>

        {/* Date range picker */}
        <div className="flex items-center space-x-1.5 bg-[#141822] border border-border px-2.5 py-1 rounded-md text-xs">
          <Calendar className="w-3.5 h-3.5 text-prana-sage" />
          <select
            value={dateRange}
            onChange={(e) => onSelectDateRange(e.target.value)}
            className="bg-transparent text-gray-200 outline-none cursor-pointer"
          >
            <option value="24h" className="bg-[#12161F] text-gray-200">Past 24 Hours</option>
            <option value="7d" className="bg-[#12161F] text-gray-200">Past 7 Days</option>
            <option value="30d" className="bg-[#12161F] text-gray-200">Past 30 Days (Monthly)</option>
          </select>
        </div>
      </div>

      {/* Global Search and Actions */}
      <div className="flex items-center space-x-3.5">
        {/* Global Search Input */}
        <div className="relative w-56">
          <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
          <input
            type="text"
            placeholder="Search stations, papers..."
            value={searchQuery}
            onChange={(e) => onSearchChange(e.target.value)}
            className="w-full bg-[#141822] border border-border rounded-lg pl-9 pr-3 py-1.5 text-xs text-gray-200 placeholder-gray-500 focus:outline-none focus:border-prana-yellow/50 transition-colors"
          />
        </div>

        {/* Global Data Integrity Indicator Pill */}
        <div className="relative">
          <button
            onClick={() => setShowIntegrityPopover(!showIntegrityPopover)}
            className="flex items-center space-x-1.5 text-[11px] bg-surface-300 hover:bg-[#1A2230] border border-border px-2.5 py-1.5 rounded-lg transition-colors cursor-pointer"
            title="Click to view dataset classification audit"
          >
            {verifiedPct > 0 ? (
              <ShieldCheck className="w-3.5 h-3.5 text-emerald-400" />
            ) : (
              <span className="w-2 h-2 rounded-full bg-amber-400"></span>
            )}
            <span className="font-medium text-gray-200">
              Integrity: <span className="text-prana-yellow font-bold">{verifiedPct > 0 ? `${verifiedPct}% Verified` : 'DEMO Data'}</span>
            </span>
          </button>

          {/* Popover */}
          {showIntegrityPopover && (
            <div className="absolute right-0 top-10 w-72 bg-[#12161F] border border-border rounded-xl p-3.5 shadow-2xl z-50 text-xs space-y-2 animate-fade-in">
              <div className="font-bold text-gray-100 flex items-center justify-between border-b border-white/10 pb-1.5">
                <span>Data Classification Breakdown</span>
                <span className="text-[10px] text-prana-sage uppercase">Milestone 2</span>
              </div>
              <div className="space-y-1.5 text-[11px]">
                <div className="flex justify-between items-center">
                  <span className="flex items-center gap-1.5 text-emerald-400">
                    <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
                    Verified (Statutory CAAQM):
                  </span>
                  <span className="font-mono font-bold text-white">{counts.VERIFIED ?? 0} ({verifiedPct}%)</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="flex items-center gap-1.5 text-blue-400">
                    <span className="w-2 h-2 rounded-full bg-blue-500"></span>
                    Imported (Researcher CSV):
                  </span>
                  <span className="font-mono font-bold text-white">{counts.IMPORTED ?? 0} ({importedPct}%)</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="flex items-center gap-1.5 text-amber-400">
                    <span className="w-2 h-2 rounded-full bg-amber-500"></span>
                    Demonstration (Synthetic):
                  </span>
                  <span className="font-mono font-bold text-white">{counts.DEMO ?? 10565} ({demoPct}%)</span>
                </div>
              </div>
              <div className="text-[10px] text-gray-400 pt-1.5 border-t border-white/5 leading-relaxed">
                Observations from seed files are classified as DEMO. Uploading statutory CSVs updates counts to IMPORTED.
              </div>
            </div>
          )}
        </div>

        {/* AI Assistant button */}
        <button
          onClick={onOpenAssistant}
          className="flex items-center space-x-1.5 bg-[#1C222E] hover:bg-[#252E3E] border border-prana-yellow/30 text-prana-yellow px-3 py-1.5 rounded-lg text-xs font-medium transition-all shadow-[0_0_10px_rgba(255,229,71,0.08)]"
        >
          <Sparkles className="w-3.5 h-3.5 text-prana-yellow" />
          <span>Research AI</span>
        </button>

        {/* Export Brief button */}
        <button
          onClick={onExportReport}
          className="flex items-center space-x-1.5 bg-[#141822] hover:bg-[#1D2433] border border-border text-gray-200 px-3 py-1.5 rounded-lg text-xs font-medium transition-colors"
          title="Download printable Markdown Research Brief"
        >
          <Download className="w-3.5 h-3.5 text-gray-400" />
          <span>Export Brief</span>
        </button>
      </div>
    </header>
  );
}
