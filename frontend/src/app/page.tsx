'use client';

import React, { useState, useEffect } from 'react';
import Sidebar, { NavSection } from '@/components/Sidebar';
import TopBar from '@/components/TopBar';
import AIAssistantDrawer from '@/components/AIAssistantDrawer';

// Views
import OverviewView from '@/components/views/OverviewView';
import LiveAirQualityView from '@/components/views/LiveAirQualityView';
import PollutionExplorerView from '@/components/views/PollutionExplorerView';
import GeographicHotspotsView from '@/components/views/GeographicHotspotsView';
import SourceIntelligenceView from '@/components/views/SourceIntelligenceView';
import WeatherView from '@/components/views/WeatherView';
import ResearchLibraryView from '@/components/views/ResearchLibraryView';
import InterventionLabView from '@/components/views/InterventionLabView';
import DataQualityView from '@/components/views/DataQualityView';
import SettingsView from '@/components/views/SettingsView';

import { fetchSummary, fetchOverviewTrends, fetchStations } from '@/lib/api';

export default function Home() {
  const [activeSection, setActiveSection] = useState<NavSection>('overview');
  const [selectedCity, setSelectedCity] = useState<string>('ALL');
  const [dateRange, setDateRange] = useState<string>('7d');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [assistantOpen, setAssistantOpen] = useState<boolean>(false);

  // Core Data
  const [summary, setSummary] = useState<any>(null);
  const [trends, setTrends] = useState<any[]>([]);
  const [stations, setStations] = useState<any[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    loadInitialData();
  }, [selectedCity]);

  async function loadInitialData() {
    setLoading(true);
    try {
      const [sumData, trData, stData] = await Promise.all([
        fetchSummary(),
        fetchOverviewTrends('PM2.5', 7),
        fetchStations(selectedCity === 'ALL' ? undefined : selectedCity)
      ]);
      setSummary(sumData);
      setTrends(trData);
      setStations(stData);
    } catch (err) {
      console.error('Failed to load initial data:', err);
    } finally {
      setLoading(false);
    }
  }

  function handleExportReport() {
    window.open('/api/export/report', '_blank');
  }

  const VIEW_TITLES: Record<NavSection, string> = {
    overview: 'Regional Overview Dashboard',
    live_aq: 'Continuous Live Air Quality Monitoring',
    explorer: 'Pollution Explorer & Pattern Analysis',
    hotspots: 'Geographic Hotspots & Spatial Coverage Audit',
    sources: 'Source Intelligence & Published Apportionment',
    weather: 'Weather & Synoptic Atmospheric Dynamics',
    library: 'Statutory Research & Literature Library',
    interventions: 'Intervention Lab & Engineering Hypotheses',
    data_quality: 'Data Provenance, Quality & Audit Trail',
    settings: 'Platform Configuration & Settings',
  };

  return (
    <div className="flex bg-[#0C0F14] min-h-screen text-gray-200">
      {/* Persistent Left Sidebar */}
      <Sidebar
        activeSection={activeSection}
        onSelectSection={(sec) => setActiveSection(sec)}
      />

      {/* Main Content Area (offset by sidebar w-64) */}
      <div className="flex-1 ml-64 flex flex-col min-h-screen">
        {/* Persistent Top Bar */}
        <TopBar
          selectedCity={selectedCity}
          onSelectCity={setSelectedCity}
          dateRange={dateRange}
          onSelectDateRange={setDateRange}
          searchQuery={searchQuery}
          onSearchChange={setSearchQuery}
          onOpenAssistant={() => setAssistantOpen(true)}
          onExportReport={handleExportReport}
          activeViewTitle={VIEW_TITLES[activeSection]}
        />

        {/* Dynamic View Container */}
        <main className="p-6 flex-1 overflow-y-auto">
          {activeSection === 'overview' && (
            <OverviewView
              summary={summary}
              stations={stations}
              trends={trends}
              onSelectStation={() => setActiveSection('live_aq')}
              onNavigate={(sec) => setActiveSection(sec)}
            />
          )}

          {activeSection === 'live_aq' && (
            <LiveAirQualityView stations={stations} />
          )}

          {activeSection === 'explorer' && (
            <PollutionExplorerView />
          )}

          {activeSection === 'hotspots' && (
            <GeographicHotspotsView />
          )}

          {activeSection === 'sources' && (
            <SourceIntelligenceView />
          )}

          {activeSection === 'weather' && (
            <WeatherView />
          )}

          {activeSection === 'library' && (
            <ResearchLibraryView />
          )}

          {activeSection === 'interventions' && (
            <InterventionLabView />
          )}

          {activeSection === 'data_quality' && (
            <DataQualityView />
          )}

          {activeSection === 'settings' && (
            <SettingsView />
          )}
        </main>
      </div>

      {/* Research AI Assistant Slide-over Drawer */}
      <AIAssistantDrawer
        isOpen={assistantOpen}
        onClose={() => setAssistantOpen(false)}
      />
    </div>
  );
}
