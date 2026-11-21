'use client';

import React from 'react';
import {
  Search,
  Sparkles,
  Download,
  Calendar,
  MapPin,
  RefreshCw,
  Clock
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
  isRefreshing?: boolean;
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
  isRefreshing = false,
  activeViewTitle,
}: TopBarProps) {
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
        <div className="relative w-64">
          <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
          <input
            type="text"
            placeholder="Search stations, papers, sources..."
            value={searchQuery}
            onChange={(e) => onSearchChange(e.target.value)}
            className="w-full bg-[#141822] border border-border rounded-lg pl-9 pr-3 py-1.5 text-xs text-gray-200 placeholder-gray-500 focus:outline-none focus:border-prana-yellow/50 transition-colors"
          />
        </div>

        {/* Live sync badge */}
        <div className="flex items-center space-x-1.5 text-[11px] text-gray-400 bg-surface-300 border border-border px-2.5 py-1.5 rounded-lg">
          <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
          <span className="font-medium text-gray-300">WBPCB Feed</span>
          <span className="text-gray-500">|</span>
          <Clock className="w-3 h-3 text-gray-500" />
          <span>{lastUpdate}</span>
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
