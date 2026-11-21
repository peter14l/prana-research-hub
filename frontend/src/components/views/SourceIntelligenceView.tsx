'use client';

import React, { useState, useEffect } from 'react';
import {
  Factory,
  BookOpen,
  PieChart as PieIcon,
  Tag,
  AlertOctagon,
  ShieldAlert,
  ChevronRight,
  ExternalLink
} from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Cell
} from 'recharts';
import {
  fetchSourceCategories,
  fetchPublishedStudies,
  fetchSourceProfiles
} from '@/lib/api';

const EVIDENCE_TAGS = [
  { key: 'AMBIENT_CONCENTRATION', label: 'Ambient Concentration', color: 'bg-blue-950 text-blue-400 border-blue-500' },
  { key: 'PUBLISHED_SOURCE_APPORTIONMENT', label: 'Published Apportionment', color: 'bg-emerald-950 text-emerald-400 border-emerald-500' },
  { key: 'EMISSION_INVENTORY', label: 'Emissions Inventory', color: 'bg-amber-950 text-amber-400 border-amber-500' },
  { key: 'SATELLITE_DERIVED', label: 'Satellite Observation', color: 'bg-purple-950 text-purple-400 border-purple-500' },
  { key: 'STATISTICAL_ASSOCIATION', label: 'Statistical Association', color: 'bg-gray-800 text-gray-300 border-gray-600' },
  { key: 'RESEARCH_HYPOTHESIS', label: 'Research Hypothesis', color: 'bg-yellow-950 text-prana-yellow border-prana-yellow' },
];

const COLORS = ['#FFE547', '#10B981', '#3B82F6', '#F59E0B', '#EF4444', '#8B5CF6'];

export default function SourceIntelligenceView() {
  const [categories, setCategories] = useState<any[]>([]);
  const [studies, setStudies] = useState<any[]>([]);
  const [profiles, setProfiles] = useState<any[]>([]);
  const [selectedCity, setSelectedCity] = useState<string>('Kolkata');
  const [selectedSeason, setSelectedSeason] = useState<string>('Winter');
  const [selectedPollutant, setSelectedPollutant] = useState<string>('PM2.5');

  useEffect(() => {
    Promise.all([fetchSourceCategories(), fetchPublishedStudies()]).then(([cats, stus]) => {
      setCategories(cats);
      setStudies(stus);
    });
  }, []);

  useEffect(() => {
    fetchSourceProfiles(selectedCity, selectedSeason, selectedPollutant).then(setProfiles);
  }, [selectedCity, selectedSeason, selectedPollutant]);

  return (
    <div className="space-y-6">
      {/* Top Banner with Strict Scientific Rule */}
      <div className="glass-panel p-5 rounded-xl border border-border space-y-3">
        <div className="flex items-center justify-between">
          <h1 className="text-lg font-bold text-white flex items-center gap-2">
            <Factory className="w-5 h-5 text-prana-yellow" />
            Source Intelligence &amp; Apportionment Evidence
          </h1>
          <span className="text-[10px] text-prana-sage uppercase font-medium bg-surface-200 border border-border px-2.5 py-1 rounded-md">
            TERI &amp; CSIR-NEERI Baseline
          </span>
        </div>

        <p className="text-xs text-gray-400 max-w-4xl leading-relaxed">
          Receptor modeling (Positive Matrix Factorization &amp; Chemical Mass Balance) and bottom-up emissions inventories
          from statutory peer-reviewed investigations across Kolkata and Howrah.
        </p>

        {/* Scientific Rule Alert */}
        <div className="p-3.5 rounded-lg bg-[#141924] border border-white/10 text-xs text-gray-300 flex items-start space-x-3">
          <ShieldAlert className="w-4 h-4 text-prana-yellow shrink-0 mt-0.5" />
          <div className="text-[11px] leading-relaxed">
            <span className="font-bold text-prana-yellow uppercase">Essential Scientific Protocol:</span> A PM2.5 or PM10 reading
            at a ground monitoring station reflects mixed ambient air. It <span className="underline">does not</span> identify the specific
            source responsible for that reading without chemical speciation (receptor modeling) or dispersion analysis.
          </div>
        </div>

        {/* Evidence Classification Badges Row */}
        <div className="pt-2 flex flex-wrap gap-2 text-[10px]">
          {EVIDENCE_TAGS.map((t) => (
            <span
              key={t.key}
              className={`px-2.5 py-1 rounded-md border font-medium ${t.color}`}
            >
              ● {t.label}
            </span>
          ))}
        </div>
      </div>

      {/* Main Grid: Sector Contribution Chart (7 Cols) & Published Studies (5 Cols) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Apportionment Breakdown Chart */}
        <div className="lg:col-span-7 glass-panel p-5 rounded-xl border border-border space-y-4">
          <div className="flex flex-wrap items-center justify-between gap-3">
            <div>
              <h2 className="text-sm font-bold text-white flex items-center gap-1.5">
                <PieIcon className="w-4 h-4 text-prana-yellow" />
                Published Source Contributions ({selectedCity} - {selectedSeason})
              </h2>
              <div className="text-[11px] text-gray-400">
                Source Apportionment from TERI (2025) &amp; NEERI (2020)
              </div>
            </div>

            {/* City & Season filters */}
            <div className="flex items-center space-x-2 text-xs">
              <select
                value={selectedCity}
                onChange={(e) => setSelectedCity(e.target.value)}
                className="bg-[#141822] border border-border rounded-md px-2.5 py-1 text-gray-200 outline-none cursor-pointer"
              >
                <option value="Kolkata">Kolkata</option>
                <option value="Howrah">Howrah</option>
              </select>

              <select
                value={selectedSeason}
                onChange={(e) => setSelectedSeason(e.target.value)}
                className="bg-[#141822] border border-border rounded-md px-2.5 py-1 text-gray-200 outline-none cursor-pointer"
              >
                <option value="Winter">Winter (Severe)</option>
              </select>
            </div>
          </div>

          <div className="h-72 w-full mt-2">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                data={profiles}
                layout="vertical"
                margin={{ top: 5, right: 30, left: 100, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.06)" />
                <XAxis type="number" unit="%" tick={{ fill: '#9CA3AF', fontSize: 11 }} />
                <YAxis
                  dataKey="category_name"
                  type="category"
                  tick={{ fill: '#F3F4F6', fontSize: 11 }}
                  width={130}
                />
                <Tooltip
                  formatter={(val: any) => [`${val}% contribution`, 'Published Share']}
                  contentStyle={{
                    backgroundColor: '#12161F',
                    borderColor: 'rgba(255,255,255,0.1)',
                    borderRadius: 8,
                    fontSize: 12,
                  }}
                />
                <Bar dataKey="contribution_percentage" radius={[0, 4, 4, 0]}>
                  {profiles.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Key Insight Callout */}
          <div className="p-3.5 rounded-lg bg-[#141822] border border-white/5 text-xs text-gray-300">
            <span className="font-bold text-prana-yellow">Cross-City Comparison Insight:</span>{' '}
            {selectedCity === 'Howrah' ? (
              <span>
                In Howrah, <strong>foundry and metal casting emissions account for 34% of winter PM2.5</strong>,
                making point/area industrial abatement the primary engineering leverage point.
              </span>
            ) : (
              <span>
                In Kolkata, <strong>road transport (27%) and secondary regional inorganic aerosols (24%)</strong>{' '}
                dominate winter PM2.5, requiring freight electrification and transboundary coordination.
              </span>
            )}
          </div>
        </div>

        {/* Official Published Studies Accordion */}
        <div className="lg:col-span-5 glass-panel p-5 rounded-xl border border-border flex flex-col justify-between space-y-4">
          <div>
            <h3 className="text-sm font-bold text-white flex items-center gap-1.5 mb-1">
              <BookOpen className="w-4 h-4 text-prana-sage" />
              Foundational Source Apportionment Studies
            </h3>
            <p className="text-[11px] text-gray-400 mb-3">
              Direct statutory citations supporting PRANA environmental intelligence.
            </p>

            <div className="space-y-3">
              {studies.map((s) => (
                <div key={s.id} className="p-3.5 rounded-lg bg-[#141822] border border-border text-xs space-y-1.5">
                  <div className="flex items-start justify-between">
                    <span className="font-bold text-gray-200">{s.study_name}</span>
                    <a
                      href={s.documentation_url}
                      target="_blank"
                      rel="noreferrer"
                      className="text-prana-yellow hover:underline"
                    >
                      <ExternalLink className="w-3.5 h-3.5" />
                    </a>
                  </div>
                  <div className="text-[11px] text-prana-sage">
                    {s.organisation} • Published {s.publication_year}
                  </div>
                  <div className="text-[11px] text-gray-400">
                    <strong className="text-gray-300">Methodology:</strong> {s.methodology}
                  </div>
                  <div className="text-[11px] text-gray-500 pt-1 border-t border-white/5">
                    <strong>Limitation:</strong> {s.limitations}
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="p-3 rounded-lg bg-[#0F131A] border border-border text-[11px] text-gray-400">
            All values reflect Chemical Mass Balance (CMB) and Positive Matrix Factorization (PMF) scientific protocols.
          </div>
        </div>
      </div>

      {/* Source Categories Directory */}
      <div className="glass-panel p-5 rounded-xl border border-border">
        <h3 className="text-sm font-bold text-white flex items-center gap-1.5 mb-3">
          <Tag className="w-4 h-4 text-prana-yellow" />
          Kolkata–Howrah Source Taxonomy &amp; Chemical Markers
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3.5">
          {categories.map((c) => (
            <div key={c.id} className="p-3.5 rounded-lg bg-[#141822] border border-border text-xs space-y-1.5">
              <div className="flex items-center justify-between">
                <span className="font-bold text-gray-200">{c.name}</span>
                <span className="text-[10px] text-prana-sage bg-[#10141C] px-2 py-0.5 rounded border border-border">
                  {c.sector}
                </span>
              </div>
              <p className="text-[11px] text-gray-400 leading-relaxed">
                {c.description}
              </p>
              <div className="pt-2 border-t border-white/5 text-[10px] space-y-0.5">
                <div>
                  <span className="text-gray-500">Key Pollutants:</span>{' '}
                  <span className="text-gray-300 font-mono">{c.primary_pollutants}</span>
                </div>
                <div>
                  <span className="text-gray-500">Marker Species:</span>{' '}
                  <span className="text-prana-yellow font-mono">{c.typical_marker_species}</span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
