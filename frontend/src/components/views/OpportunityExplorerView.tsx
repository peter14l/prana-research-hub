'use client';

import React, { useState, useEffect } from 'react';
import {
  Target,
  Sliders,
  FileText,
  AlertTriangle,
  GitBranch,
  CheckCircle2,
  XCircle,
  HelpCircle,
  ChevronRight,
  TrendingUp,
  Shield,
  Layers,
  ArrowRight,
  RefreshCw,
  Search,
  ExternalLink,
  Cpu,
  BarChart2,
  Sparkles,
  Info
} from 'lucide-react';
import {
  fetchEvidenceInventory,
  fetchSectorEvaluations,
  fetchCandidateOpportunities,
  evaluateCandidateOpportunities,
  fetchCandidateDossier,
  transitionCandidateStage,
  updateCandidateShortlist,
  fetchResearchGaps
} from '@/lib/api';

type ActiveTab = 'overview' | 'comparison' | 'dossier' | 'gaps' | 'pipeline';

export default function OpportunityExplorerView() {
  const [activeTab, setActiveTab] = useState<ActiveTab>('comparison');
  const [loading, setLoading] = useState<boolean>(true);

  // Data states
  const [inventory, setInventory] = useState<any>(null);
  const [sectors, setSectors] = useState<any[]>([]);
  const [candidates, setCandidates] = useState<any[]>([]);
  const [gaps, setGaps] = useState<any[]>([]);
  const [selectedCandidate, setSelectedCandidate] = useState<any>(null);

  // Weights state for 8 criteria
  const defaultWeights = {
    pollution_impact: 0.20,
    evidence_strength: 0.15,
    technical_feasibility: 0.15,
    financial_feasibility: 0.10,
    verification: 0.15,
    scalability: 0.10,
    innovation: 0.05,
    partnership_feasibility: 0.10
  };
  const [weights, setWeights] = useState<Record<string, number>>(defaultWeights);
  const [sectorFilter, setSectorFilter] = useState<string>('ALL');

  // Stage Transition Modal State
  const [transitionModalOpen, setTransitionModalOpen] = useState<boolean>(false);
  const [targetStage, setTargetStage] = useState<string>('');
  const [stageNotes, setStageNotes] = useState<string>('');
  const [evidenceRef, setEvidenceRef] = useState<string>('');
  const [verificationRef, setVerificationRef] = useState<string>('');
  const [transitionError, setTransitionError] = useState<string | null>(null);

  // Shortlist Modal State
  const [shortlistModalOpen, setShortlistModalOpen] = useState<boolean>(false);
  const [shortlistStatus, setShortlistStatus] = useState<string>('SHORTLISTED');
  const [shortlistNotes, setShortlistNotes] = useState<string>('');

  useEffect(() => {
    loadAllData();
  }, []);

  async function loadAllData() {
    setLoading(true);
    try {
      const [invData, secData, candData, gapData] = await Promise.all([
        fetchEvidenceInventory().catch(() => null),
        fetchSectorEvaluations().catch(() => []),
        fetchCandidateOpportunities().catch(() => []),
        fetchResearchGaps().catch(() => [])
      ]);
      setInventory(invData);
      setSectors(secData);
      setCandidates(candData);
      setGaps(gapData);
      if (candData && candData.length > 0 && !selectedCandidate) {
        setSelectedCandidate(candData[0]);
      }
    } catch (err) {
      console.error('Error loading opportunity data:', err);
    } finally {
      setLoading(false);
    }
  }

  async function handleRecalculateWeights(newWeights = weights) {
    try {
      const res = await evaluateCandidateOpportunities({
        weights: newWeights,
        sector_filter: sectorFilter === 'ALL' ? undefined : sectorFilter
      });
      if (res && res.candidates) {
        setCandidates(res.candidates);
        if (selectedCandidate) {
          const updated = res.candidates.find((c: any) => c.id === selectedCandidate.id);
          if (updated) setSelectedCandidate(updated);
        }
      }
    } catch (err) {
      console.error('Failed to recalculate weights:', err);
    }
  }

  function handleWeightChange(criterion: string, val: number) {
    const updated = { ...weights, [criterion]: val };
    setWeights(updated);
    handleRecalculateWeights(updated);
  }

  function handleResetWeights() {
    setWeights(defaultWeights);
    handleRecalculateWeights(defaultWeights);
  }

  async function handleExecuteStageTransition() {
    if (!selectedCandidate || !targetStage) return;
    setTransitionError(null);
    try {
      await transitionCandidateStage(
        selectedCandidate.id,
        targetStage,
        stageNotes,
        evidenceRef,
        verificationRef
      );
      setTransitionModalOpen(false);
      setStageNotes('');
      setEvidenceRef('');
      setVerificationRef('');
      await loadAllData();
    } catch (err: any) {
      setTransitionError(err.message || 'Stage transition failed');
    }
  }

  async function handleExecuteShortlist() {
    if (!selectedCandidate) return;
    try {
      await updateCandidateShortlist(selectedCandidate.id, shortlistStatus, shortlistNotes);
      setShortlistModalOpen(false);
      setShortlistNotes('');
      await loadAllData();
    } catch (err: any) {
      alert(err.message || 'Failed to update shortlist status');
    }
  }

  const allStages = [
    'Discovered',
    'Under research',
    'Evidence reviewed',
    'Feasibility assessed',
    'Prototype proposed',
    'Prototype developed',
    'Pilot ready',
    'Pilot validated'
  ];

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-16">
      {/* Header Banner */}
      <div className="bg-surface-100 border border-border rounded-xl p-6 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-96 h-96 bg-prana-yellow/5 rounded-full blur-3xl pointer-events-none -mr-20 -mt-20"></div>
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 relative z-10">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-prana-yellow/20 text-prana-yellow border border-prana-yellow/30">
                MILESTONE 4
              </span>
              <span className="text-xs text-gray-400">Evidence-Driven Opportunity Discovery</span>
            </div>
            <h1 className="text-2xl font-bold text-white tracking-tight flex items-center gap-3">
              <Target className="w-6 h-6 text-prana-yellow" />
              Opportunity Explorer & Engineering Prioritisation
            </h1>
            <p className="text-sm text-gray-400 mt-1 max-w-3xl">
              Transparent multi-criteria evaluation of outdoor air pollution reduction opportunities across Kolkata–Howrah.
              Prioritizes source-level engineering interventions with verifiable counterfactual measurement protocols.
            </p>
          </div>

          <div className="flex items-center gap-3 self-start md:self-auto">
            <button
              onClick={() => loadAllData()}
              className="px-3.5 py-2 rounded-lg bg-surface-200 border border-border hover:bg-surface-300 text-xs font-medium text-gray-200 flex items-center gap-2 transition-colors"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              Refresh
            </button>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex items-center gap-2 mt-6 pt-4 border-t border-border overflow-x-auto">
          {[
            { id: 'comparison', label: 'Candidate Prioritization & Scoring', icon: Sliders },
            { id: 'dossier', label: 'Engineering Dossier (14 Fields)', icon: FileText },
            { id: 'pipeline', label: 'Stage-Gate Pipeline & Shortlist', icon: GitBranch },
            { id: 'gaps', label: 'Research Gap Detector', icon: AlertTriangle },
            { id: 'overview', label: 'Evidence Inventory & Sectors', icon: Layers }
          ].map((tab) => {
            const Icon = tab.icon;
            const active = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as ActiveTab)}
                className={`px-4 py-2 rounded-lg text-xs font-medium flex items-center gap-2 whitespace-nowrap transition-colors ${
                  active
                    ? 'bg-prana-yellow text-black font-semibold shadow-sm'
                    : 'bg-surface-200/60 hover:bg-surface-200 text-gray-400 hover:text-white'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                {tab.label}
              </button>
            );
          })}
        </div>
      </div>

      {/* ========================================================================= */}
      {/* TAB 1: COMPARISON & MULTI-CRITERIA SCORING ENGINE                         */}
      {/* ========================================================================= */}
      {activeTab === 'comparison' && (
        <div className="space-y-6">
          {/* Statutory Heuristic Disclaimer Banner */}
          <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/30 flex items-start gap-3">
            <Info className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
            <div className="text-xs text-amber-200/90 leading-relaxed">
              <span className="font-semibold text-amber-300">SCIENTIFIC INTEGRITY NOTICE:</span> The composite Weighted Priority Score
              is a multi-criteria decision-support heuristic, not an empirical physical measurement of atmospheric concentration.
              Researchers may dynamically adjust criterion weightings below to simulate different institutional priorities
              (e.g., maximum pollution reduction vs. immediate feasibility).
            </div>
          </div>

          {/* Interactive Weight Sliders */}
          <div className="bg-surface-100 border border-border rounded-xl p-5">
            <div className="flex items-center justify-between mb-4">
              <div>
                <h3 className="text-sm font-semibold text-white flex items-center gap-2">
                  <Sliders className="w-4 h-4 text-prana-yellow" />
                  Dynamic 8-Criteria Weighting Matrix
                </h3>
                <p className="text-xs text-gray-400 mt-0.5">
                  Adjust normalized weights to evaluate how candidate rankings respond to different engineering objectives.
                </p>
              </div>
              <button
                onClick={handleResetWeights}
                className="text-xs text-prana-yellow hover:underline"
              >
                Reset to Default Weights
              </button>
            </div>

            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {[
                { key: 'pollution_impact', label: 'Pollution Impact', desc: 'Direct emission / exposure reduction' },
                { key: 'evidence_strength', label: 'Evidence Strength', desc: 'Statutory citations & ground truth' },
                { key: 'technical_feasibility', label: 'Technical Feasibility', desc: 'TRL & engineering complexity' },
                { key: 'financial_feasibility', label: 'Financial Feasibility', desc: 'Capex/Opex development cost' },
                { key: 'verification', label: 'Verification', desc: 'Counterfactual measurement proof' },
                { key: 'scalability', label: 'Scalability', desc: 'Regional/national replicability' },
                { key: 'innovation', label: 'Innovation & IP', desc: 'Novel proprietary engineering' },
                { key: 'partnership_feasibility', label: 'Partnership Feasibility', desc: 'Agency & stakeholder buy-in' }
              ].map((crit) => {
                const val = weights[crit.key] ?? 0.1;
                return (
                  <div key={crit.key} className="p-3 rounded-lg bg-surface-200 border border-border/60">
                    <div className="flex justify-between items-center mb-1">
                      <span className="text-xs font-medium text-gray-200">{crit.label}</span>
                      <span className="text-xs font-bold text-prana-yellow">{Math.round(val * 100)}%</span>
                    </div>
                    <input
                      type="range"
                      min="0.0"
                      max="0.4"
                      step="0.05"
                      value={val}
                      onChange={(e) => handleWeightChange(crit.key, parseFloat(e.target.value))}
                      className="w-full h-1.5 bg-surface-300 rounded-lg appearance-none cursor-pointer accent-prana-yellow"
                    />
                    <div className="text-[10px] text-gray-500 mt-1 truncate">{crit.desc}</div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Candidates Comparison Table */}
          <div className="bg-surface-100 border border-border rounded-xl overflow-hidden">
            <div className="p-4 border-b border-border flex items-center justify-between">
              <div className="flex items-center gap-3">
                <h3 className="text-sm font-semibold text-white">Evaluated Engineering Candidates ({candidates.length})</h3>
                <span className="px-2 py-0.5 rounded text-[10px] bg-surface-200 text-gray-400 border border-border">
                  Grounded in Kolkata–Howrah Data
                </span>
              </div>

              {/* Sector Filter */}
              <div className="flex items-center gap-2">
                <span className="text-xs text-gray-400">Sector:</span>
                <select
                  value={sectorFilter}
                  onChange={(e) => {
                    setSectorFilter(e.target.value);
                    handleRecalculateWeights();
                  }}
                  className="bg-surface-200 border border-border rounded px-2.5 py-1 text-xs text-gray-200 focus:outline-none"
                >
                  <option value="ALL">All Sectors</option>
                  <option value="Industrial emissions">Industrial emissions</option>
                  <option value="Low-cost emission monitoring and verification">Low-cost Monitoring</option>
                  <option value="Waste burning">Waste burning</option>
                  <option value="River transport">River transport</option>
                </select>
              </div>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead className="bg-surface-200/80 text-gray-400 text-[11px] uppercase tracking-wider border-b border-border">
                  <tr>
                    <th className="py-3 px-4">Rank</th>
                    <th className="py-3 px-4">Opportunity Title</th>
                    <th className="py-3 px-4">Sector</th>
                    <th className="py-3 px-4">Stage Status</th>
                    <th className="py-3 px-4">Decision</th>
                    <th className="py-3 px-4 text-center">Impact</th>
                    <th className="py-3 px-4 text-center">Evidence</th>
                    <th className="py-3 px-4 text-center">Tech</th>
                    <th className="py-3 px-4 text-center">Verify</th>
                    <th className="py-3 px-4 text-right">Weighted Score</th>
                    <th className="py-3 px-4 text-right">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-border">
                  {candidates.map((cand) => {
                    const isSelected = selectedCandidate?.id === cand.id;
                    return (
                      <tr
                        key={cand.id}
                        className={`hover:bg-surface-200/50 transition-colors ${
                          isSelected ? 'bg-surface-200/70 border-l-2 border-prana-yellow' : ''
                        }`}
                      >
                        <td className="py-3.5 px-4 font-bold text-white">
                          <span className="w-6 h-6 rounded-full bg-surface-300 text-prana-yellow flex items-center justify-center text-xs">
                            #{cand.rank || 1}
                          </span>
                        </td>
                        <td className="py-3.5 px-4">
                          <div className="font-semibold text-gray-100 max-w-sm truncate">{cand.title}</div>
                          <div className="text-[11px] text-gray-400 truncate">{cand.target_pollutant}</div>
                        </td>
                        <td className="py-3.5 px-4 text-gray-300">
                          <span className="px-2 py-0.5 rounded text-[10px] bg-surface-300 text-gray-300 border border-border">
                            {cand.sector}
                          </span>
                        </td>
                        <td className="py-3.5 px-4">
                          <span className="px-2 py-0.5 rounded text-[10px] font-medium bg-blue-500/10 text-blue-400 border border-blue-500/30">
                            {cand.stage_status}
                          </span>
                        </td>
                        <td className="py-3.5 px-4">
                          {cand.shortlist_status === 'SHORTLISTED' && (
                            <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30 flex items-center gap-1 w-fit">
                              <CheckCircle2 className="w-3 h-3" /> Shortlisted
                            </span>
                          )}
                          {cand.shortlist_status === 'FURTHER_INVESTIGATION' && (
                            <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/30 flex items-center gap-1 w-fit">
                              <HelpCircle className="w-3 h-3" /> Investigating
                            </span>
                          )}
                          {cand.shortlist_status === 'REJECTED' && (
                            <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-rose-500/10 text-rose-400 border border-rose-500/30 flex items-center gap-1 w-fit">
                              <XCircle className="w-3 h-3" /> Rejected
                            </span>
                          )}
                          {cand.shortlist_status === 'CONSIDERING' && (
                            <span className="px-2 py-0.5 rounded text-[10px] text-gray-400 border border-border">
                              Considering
                            </span>
                          )}
                        </td>
                        <td className="py-3.5 px-4 text-center font-mono font-semibold text-gray-200">
                          {cand.pollution_impact_score}
                        </td>
                        <td className="py-3.5 px-4 text-center font-mono font-semibold text-gray-200">
                          {cand.evidence_strength_score}
                        </td>
                        <td className="py-3.5 px-4 text-center font-mono font-semibold text-gray-200">
                          {cand.technical_feasibility_score}
                        </td>
                        <td className="py-3.5 px-4 text-center font-mono font-semibold text-gray-200">
                          {cand.verification_score}
                        </td>
                        <td className="py-3.5 px-4 text-right">
                          <span className="text-sm font-bold text-prana-yellow font-mono">
                            {cand.weighted_priority_score}
                          </span>
                          <span className="text-[10px] text-gray-500"> / 10</span>
                        </td>
                        <td className="py-3.5 px-4 text-right">
                          <button
                            onClick={() => {
                              setSelectedCandidate(cand);
                              setActiveTab('dossier');
                            }}
                            className="px-2.5 py-1 rounded bg-surface-300 hover:bg-surface-200 text-[11px] font-medium text-gray-200 hover:text-white transition-colors"
                          >
                            Inspect Dossier
                          </button>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* TAB 2: CANDIDATE TECHNICAL DOSSIER (14 MANDATORY FIELDS)                  */}
      {/* ========================================================================= */}
      {activeTab === 'dossier' && selectedCandidate && (
        <div className="space-y-6">
          {/* Dossier Header */}
          <div className="bg-surface-100 border border-border rounded-xl p-6">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-prana-yellow/20 text-prana-yellow border border-prana-yellow/30">
                    CANDIDATE #{selectedCandidate.rank || 1}
                  </span>
                  <span className="px-2 py-0.5 rounded text-[10px] bg-surface-300 text-gray-300 border border-border">
                    {selectedCandidate.sector}
                  </span>
                  <span className="px-2 py-0.5 rounded text-[10px] bg-blue-500/10 text-blue-400 border border-blue-500/30">
                    Stage: {selectedCandidate.stage_status}
                  </span>
                </div>
                <h2 className="text-xl font-bold text-white">{selectedCandidate.title}</h2>
                <div className="text-xs text-gray-400 mt-1 flex items-center gap-2">
                  <span>Target: <strong className="text-gray-200">{selectedCandidate.target_pollutant}</strong></span>
                  <span>•</span>
                  <span>Geography: <strong className="text-gray-200">{selectedCandidate.geographic_relevance}</strong></span>
                </div>
              </div>

              <div className="flex items-center gap-3">
                <button
                  onClick={() => {
                    setTargetStage(selectedCandidate.stage_status);
                    setTransitionModalOpen(true);
                  }}
                  className="px-3.5 py-2 rounded-lg bg-surface-200 hover:bg-surface-300 border border-border text-xs font-medium text-gray-200 flex items-center gap-2 transition-colors"
                >
                  <GitBranch className="w-3.5 h-3.5 text-blue-400" />
                  Advance Stage-Gate
                </button>
                <button
                  onClick={() => {
                    setShortlistStatus(selectedCandidate.shortlist_status || 'SHORTLISTED');
                    setShortlistNotes(selectedCandidate.shortlist_notes || '');
                    setShortlistModalOpen(true);
                  }}
                  className="px-3.5 py-2 rounded-lg bg-prana-yellow text-black text-xs font-semibold flex items-center gap-2 hover:bg-prana-yellow/90 transition-colors"
                >
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  Decision / Shortlist
                </button>
              </div>
            </div>
          </div>

          {/* 8-Criteria Radar / Breakdown Card */}
          <div className="bg-surface-100 border border-border rounded-xl p-5">
            <h3 className="text-sm font-semibold text-white mb-3 flex items-center gap-2">
              <BarChart2 className="w-4 h-4 text-prana-yellow" />
              Criteria Evaluation Breakdown & Scientific Rationales
            </h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {[
                { label: 'Pollution Impact', score: selectedCandidate.pollution_impact_score, key: 'pollution_impact' },
                { label: 'Evidence Strength', score: selectedCandidate.evidence_strength_score, key: 'evidence_strength' },
                { label: 'Technical Feasibility', score: selectedCandidate.technical_feasibility_score, key: 'technical_feasibility' },
                { label: 'Financial Feasibility', score: selectedCandidate.financial_feasibility_score, key: 'financial_feasibility' },
                { label: 'Verification', score: selectedCandidate.verification_score, key: 'verification' },
                { label: 'Scalability', score: selectedCandidate.scalability_score, key: 'scalability' },
                { label: 'Innovation & IP', score: selectedCandidate.innovation_score, key: 'innovation' },
                { label: 'Partnership Feasibility', score: selectedCandidate.partnership_feasibility_score, key: 'partnership_feasibility' }
              ].map((c) => {
                const explanation = selectedCandidate.score_explanations?.[c.key];
                return (
                  <div key={c.key} className="p-3 rounded-lg bg-surface-200 border border-border/60">
                    <div className="flex justify-between items-center mb-1">
                      <span className="text-xs text-gray-300 font-medium">{c.label}</span>
                      <span className="text-xs font-bold text-prana-yellow font-mono">{c.score} / 10</span>
                    </div>
                    <div className="w-full bg-surface-300 h-1.5 rounded-full overflow-hidden mb-2">
                      <div
                        className="bg-prana-yellow h-full rounded-full"
                        style={{ width: `${(c.score / 10) * 100}%` }}
                      ></div>
                    </div>
                    {explanation && (
                      <p className="text-[11px] text-gray-400 line-clamp-3">{explanation}</p>
                    )}
                  </div>
                );
              })}
            </div>
          </div>

          {/* 14 Mandatory Fields Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Field 1: Problem Statement */}
            <div className="bg-surface-100 border border-border rounded-xl p-5">
              <span className="text-[10px] font-bold text-gray-400 uppercase tracking-wider">1. Problem Statement</span>
              <p className="text-xs text-gray-200 mt-2 leading-relaxed">{selectedCandidate.problem_statement}</p>
            </div>

            {/* Field 4: Supporting Evidence */}
            <div className="bg-surface-100 border border-border rounded-xl p-5">
              <span className="text-[10px] font-bold text-gray-400 uppercase tracking-wider">4. Supporting Evidence & Statutory Citations</span>
              <p className="text-xs text-gray-200 mt-2 leading-relaxed">{selectedCandidate.supporting_evidence}</p>
            </div>

            {/* Field 6: Proposed Mechanism */}
            <div className="bg-surface-100 border border-border rounded-xl p-5 md:col-span-2">
              <span className="text-[10px] font-bold text-gray-400 uppercase tracking-wider">6. Proposed Engineering Mechanism</span>
              <p className="text-xs text-gray-200 mt-2 leading-relaxed">{selectedCandidate.proposed_mechanism}</p>
            </div>

            {/* Field 3: Suspected Source */}
            <div className="bg-surface-100 border border-border rounded-xl p-5">
              <span className="text-[10px] font-bold text-gray-400 uppercase tracking-wider">3. Suspected Source & Operational Context</span>
              <p className="text-xs text-gray-200 mt-2 leading-relaxed">{selectedCandidate.suspected_source}</p>
            </div>

            {/* Field 5: Geographic Relevance */}
            <div className="bg-surface-100 border border-border rounded-xl p-5">
              <span className="text-[10px] font-bold text-gray-400 uppercase tracking-wider">5. Geographic Relevance & Cluster Coordinates</span>
              <p className="text-xs text-gray-200 mt-2 leading-relaxed">{selectedCandidate.geographic_relevance}</p>
            </div>

            {/* Field 7: Potential Users */}
            <div className="bg-surface-100 border border-border rounded-xl p-5">
              <span className="text-[10px] font-bold text-gray-400 uppercase tracking-wider">7. Potential Users & Customers</span>
              <p className="text-xs text-gray-200 mt-2 leading-relaxed">{selectedCandidate.potential_users}</p>
            </div>

            {/* Field 8: Required Technology */}
            <div className="bg-surface-100 border border-border rounded-xl p-5">
              <span className="text-[10px] font-bold text-gray-400 uppercase tracking-wider">8. Required Technology & Bill of Materials</span>
              <p className="text-xs text-gray-200 mt-2 leading-relaxed">{selectedCandidate.required_technology}</p>
            </div>

            {/* Field 10: Potential Partners */}
            <div className="bg-surface-100 border border-border rounded-xl p-5">
              <span className="text-[10px] font-bold text-gray-400 uppercase tracking-wider">10. Potential Implementation Partners</span>
              <p className="text-xs text-gray-200 mt-2 leading-relaxed">{selectedCandidate.potential_partners}</p>
            </div>

            {/* Field 11: Verification Method */}
            <div className="bg-surface-100 border border-border rounded-xl p-5">
              <span className="text-[10px] font-bold text-gray-400 uppercase tracking-wider">11. Measurement & Verification Method</span>
              <p className="text-xs text-gray-200 mt-2 leading-relaxed">{selectedCandidate.verification_method}</p>
            </div>

            {/* Field 12: Unresolved Questions */}
            <div className="bg-surface-100 border border-border rounded-xl p-5">
              <span className="text-[10px] font-bold text-amber-400 uppercase tracking-wider">12. Unresolved Scientific Questions</span>
              <p className="text-xs text-amber-200/90 mt-2 leading-relaxed">{selectedCandidate.unresolved_questions}</p>
            </div>

            {/* Field 13: Key Risks */}
            <div className="bg-surface-100 border border-border rounded-xl p-5">
              <span className="text-[10px] font-bold text-rose-400 uppercase tracking-wider">13. Key Technical & Operational Risks</span>
              <p className="text-xs text-rose-200/90 mt-2 leading-relaxed">{selectedCandidate.key_risks}</p>
            </div>

            {/* Field 14: IP Opportunity */}
            <div className="bg-surface-100 border border-border rounded-xl p-5 md:col-span-2">
              <span className="text-[10px] font-bold text-prana-yellow uppercase tracking-wider">14. Potential Intellectual Property (IP) Opportunity</span>
              <p className="text-xs text-gray-200 mt-2 leading-relaxed">{selectedCandidate.ip_opportunity}</p>
            </div>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* TAB 3: STAGE-GATE PIPELINE & SHORTLIST                                    */}
      {/* ========================================================================= */}
      {activeTab === 'pipeline' && (
        <div className="space-y-6">
          <div className="bg-surface-100 border border-border rounded-xl p-5">
            <h3 className="text-sm font-semibold text-white mb-1 flex items-center gap-2">
              <GitBranch className="w-4 h-4 text-prana-yellow" />
              Stage-Gate Engineering Governance Pipeline
            </h3>
            <p className="text-xs text-gray-400">
              Strict scientific governance enforces evidence prerequisites before candidates can advance into prototyping or pilot validation.
            </p>
          </div>

          {/* Kanban / Stage Columns */}
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {allStages.slice(0, 4).map((stg) => {
              const matched = candidates.filter((c) => c.stage_status === stg);
              return (
                <div key={stg} className="bg-surface-100 border border-border rounded-xl p-4 flex flex-col">
                  <div className="flex items-center justify-between pb-3 border-b border-border mb-3">
                    <span className="text-xs font-semibold text-gray-200">{stg}</span>
                    <span className="w-5 h-5 rounded-full bg-surface-200 text-gray-400 text-[10px] flex items-center justify-center font-mono">
                      {matched.length}
                    </span>
                  </div>
                  <div className="space-y-3 flex-1">
                    {matched.map((cand) => (
                      <div
                        key={cand.id}
                        onClick={() => {
                          setSelectedCandidate(cand);
                          setActiveTab('dossier');
                        }}
                        className="p-3 rounded-lg bg-surface-200 border border-border hover:border-prana-yellow/50 cursor-pointer transition-all"
                      >
                        <div className="font-semibold text-xs text-white mb-1">{cand.title}</div>
                        <div className="text-[10px] text-gray-400 mb-2 truncate">{cand.sector}</div>
                        <div className="flex items-center justify-between">
                          <span className="text-[10px] text-prana-yellow font-bold">
                            Score: {cand.weighted_priority_score}
                          </span>
                          <span className="text-[10px] text-gray-500">{cand.shortlist_status}</span>
                        </div>
                      </div>
                    ))}
                    {matched.length === 0 && (
                      <div className="h-24 flex items-center justify-center text-xs text-gray-600 border border-dashed border-border rounded-lg">
                        No candidates
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            {allStages.slice(4, 8).map((stg) => {
              const matched = candidates.filter((c) => c.stage_status === stg);
              return (
                <div key={stg} className="bg-surface-100 border border-border rounded-xl p-4 flex flex-col">
                  <div className="flex items-center justify-between pb-3 border-b border-border mb-3">
                    <span className="text-xs font-semibold text-gray-200">{stg}</span>
                    <span className="w-5 h-5 rounded-full bg-surface-200 text-gray-400 text-[10px] flex items-center justify-center font-mono">
                      {matched.length}
                    </span>
                  </div>
                  <div className="space-y-3 flex-1">
                    {matched.map((cand) => (
                      <div
                        key={cand.id}
                        onClick={() => {
                          setSelectedCandidate(cand);
                          setActiveTab('dossier');
                        }}
                        className="p-3 rounded-lg bg-surface-200 border border-border hover:border-prana-yellow/50 cursor-pointer transition-all"
                      >
                        <div className="font-semibold text-xs text-white mb-1">{cand.title}</div>
                        <div className="text-[10px] text-gray-400 mb-2 truncate">{cand.sector}</div>
                        <div className="flex items-center justify-between">
                          <span className="text-[10px] text-prana-yellow font-bold">
                            Score: {cand.weighted_priority_score}
                          </span>
                          <span className="text-[10px] text-gray-500">{cand.shortlist_status}</span>
                        </div>
                      </div>
                    ))}
                    {matched.length === 0 && (
                      <div className="h-24 flex items-center justify-center text-xs text-gray-600 border border-dashed border-border rounded-lg">
                        No candidates
                      </div>
                    )}
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* TAB 4: RESEARCH GAP DETECTOR                                              */}
      {/* ========================================================================= */}
      {activeTab === 'gaps' && (
        <div className="space-y-6">
          <div className="bg-surface-100 border border-border rounded-xl p-5">
            <h3 className="text-sm font-semibold text-white mb-1 flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-amber-400" />
              Empirical Research Gap Detector ({gaps.length})
            </h3>
            <p className="text-xs text-gray-400">
              Identifies where current statutory evidence or spatial telemetry is insufficient. Recommends the cheapest
              credible resolution method, favoring remote satellite/AIS telemetry prior to physical field mobilization.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {gaps.map((gap) => (
              <div key={gap.id} className="bg-surface-100 border border-border rounded-xl p-5 flex flex-col justify-between">
                <div>
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-mono text-xs font-bold text-prana-yellow">{gap.gap_code}</span>
                    <div className="flex items-center gap-2">
                      {gap.severity === 'CRITICAL' && (
                        <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-500/10 text-rose-400 border border-rose-500/30">
                          CRITICAL GAP
                        </span>
                      )}
                      {gap.severity === 'HIGH' && (
                        <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/10 text-amber-400 border border-amber-500/30">
                          HIGH SEVERITY
                        </span>
                      )}
                      {gap.severity === 'MEDIUM' && (
                        <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-500/10 text-blue-400 border border-blue-500/30">
                          MEDIUM
                        </span>
                      )}
                      <span className="px-2 py-0.5 rounded text-[10px] bg-surface-300 text-gray-300 border border-border">
                        {gap.sector}
                      </span>
                    </div>
                  </div>

                  <h4 className="text-sm font-bold text-white mb-2">{gap.title}</h4>
                  <p className="text-xs text-gray-300 leading-relaxed mb-4">{gap.description}</p>

                  <div className="p-3 rounded-lg bg-surface-200 border border-border mb-3">
                    <span className="text-[10px] font-bold text-prana-yellow uppercase tracking-wider block mb-1">
                      Cheapest Credible Resolution
                    </span>
                    <p className="text-xs text-gray-300">{gap.cheapest_resolution_method}</p>
                  </div>
                </div>

                <div className="pt-3 border-t border-border flex items-center justify-between text-xs text-gray-400">
                  <span>Affected: <strong className="text-gray-200">{gap.affected_areas}</strong></span>
                  <div className="flex items-center gap-2">
                    {gap.remote_testing_possible && (
                      <span className="text-[10px] text-emerald-400 bg-emerald-500/10 px-2 py-0.5 rounded border border-emerald-500/30">
                        Remote Resolution
                      </span>
                    )}
                    <span>Est: {gap.estimated_resolution_time}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* TAB 5: EVIDENCE INVENTORY & INDEPENDENT SECTORS                           */}
      {/* ========================================================================= */}
      {activeTab === 'overview' && (
        <div className="space-y-6">
          {/* Inventory Summary Cards */}
          {inventory && (
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="p-4 rounded-xl bg-surface-100 border border-border">
                <div className="text-[11px] text-gray-400">Total Cataloged Observations</div>
                <div className="text-2xl font-bold text-white font-mono mt-1">
                  {inventory.total_records_cataloged?.toLocaleString() || '10,584'}
                </div>
                <div className="text-[10px] text-emerald-400 mt-1">
                  {inventory.verified_and_modelled_share_pct || 0}% Verified / Modelled
                </div>
              </div>

              <div className="p-4 rounded-xl bg-surface-100 border border-border">
                <div className="text-[11px] text-gray-400">Statutory Ground Stations</div>
                <div className="text-2xl font-bold text-white font-mono mt-1">
                  {inventory.station_registry?.verified_statutory_stations || 9}
                </div>
                <div className="text-[10px] text-gray-500 mt-1">
                  {inventory.station_registry?.cpcb_site_id_assigned || 9} CPCB Site IDs Verified
                </div>
              </div>

              <div className="p-4 rounded-xl bg-surface-100 border border-border">
                <div className="text-[11px] text-gray-400">Peer-Reviewed Studies</div>
                <div className="text-2xl font-bold text-white font-mono mt-1">
                  {inventory.active_statutory_studies?.length || 4}
                </div>
                <div className="text-[10px] text-gray-500 mt-1">TERI 2025, NEERI 2020, CPCB</div>
              </div>

              <div className="p-4 rounded-xl bg-surface-100 border border-border">
                <div className="text-[11px] text-gray-400">Disclosed Coverage Voids</div>
                <div className="text-2xl font-bold text-amber-400 font-mono mt-1">
                  {inventory.disclosed_data_gaps?.length || 4}
                </div>
                <div className="text-[10px] text-amber-400/80 mt-1">Zero Interpolation Policy</div>
              </div>
            </div>
          )}

          {/* 8 Independent Sector Evaluations */}
          <div className="bg-surface-100 border border-border rounded-xl p-5">
            <h3 className="text-sm font-semibold text-white mb-4 flex items-center gap-2">
              <Layers className="w-4 h-4 text-prana-yellow" />
              Independent Sector-by-Sector Empirical Evaluation (8 Sectors)
            </h3>

            <div className="space-y-4">
              {sectors.map((sec, idx) => (
                <div key={idx} className="p-4 rounded-xl bg-surface-200 border border-border/80">
                  <div className="flex flex-col md:flex-row md:items-center justify-between gap-2 mb-2">
                    <h4 className="text-sm font-bold text-white flex items-center gap-2">
                      <span className="w-5 h-5 rounded bg-surface-300 text-prana-yellow text-xs flex items-center justify-center font-mono">
                        {idx + 1}
                      </span>
                      {sec.sector}
                    </h4>
                    <span className="px-2.5 py-0.5 rounded text-[11px] font-semibold bg-prana-yellow/10 text-prana-yellow border border-prana-yellow/30 self-start md:self-auto">
                      {sec.relative_importance}
                    </span>
                  </div>

                  <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs text-gray-300 my-3">
                    <div>
                      <span className="text-gray-500 text-[10px] block">Winter PM2.5 Share</span>
                      <strong className="text-gray-100">{sec.winter_pm25_share}</strong>
                    </div>
                    <div>
                      <span className="text-gray-500 text-[10px] block">Chemical Markers</span>
                      <strong className="text-gray-100 truncate block">{sec.primary_chemical_markers}</strong>
                    </div>
                    <div>
                      <span className="text-gray-500 text-[10px] block">Spatial Hotspots</span>
                      <strong className="text-gray-100 truncate block">{sec.spatial_hotspots}</strong>
                    </div>
                    <div>
                      <span className="text-gray-500 text-[10px] block">Evidence Strength</span>
                      <strong className="text-gray-100">{sec.evidence_strength}</strong>
                    </div>
                  </div>

                  <div className="pt-2 border-t border-border/60 text-xs text-gray-400">
                    <span>Recommended Focus: <strong className="text-gray-200">{sec.recommended_focus}</strong></span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* MODAL: STAGE-GATE ADVANCEMENT                                             */}
      {/* ========================================================================= */}
      {transitionModalOpen && selectedCandidate && (
        <div className="fixed inset-0 z-50 bg-black/80 flex items-center justify-center p-4">
          <div className="bg-surface-100 border border-border rounded-xl max-w-lg w-full p-6 space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-border">
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <GitBranch className="w-4 h-4 text-prana-yellow" />
                Stage-Gate Governance Transition
              </h3>
              <button
                onClick={() => setTransitionModalOpen(false)}
                className="text-gray-400 hover:text-white"
              >
                ✕
              </button>
            </div>

            <div>
              <div className="text-xs text-gray-400">Candidate:</div>
              <div className="font-semibold text-sm text-white">{selectedCandidate.title}</div>
            </div>

            {transitionError && (
              <div className="p-3 rounded-lg bg-rose-500/10 border border-rose-500/30 text-xs text-rose-300">
                {transitionError}
              </div>
            )}

            <div>
              <label className="text-xs text-gray-300 font-medium block mb-1">Target Engineering Stage:</label>
              <select
                value={targetStage}
                onChange={(e) => setTargetStage(e.target.value)}
                className="w-full bg-surface-200 border border-border rounded-lg p-2.5 text-xs text-gray-100 focus:outline-none"
              >
                {allStages.map((stg) => (
                  <option key={stg} value={stg}>{stg}</option>
                ))}
              </select>
            </div>

            <div>
              <label className="text-xs text-gray-300 font-medium block mb-1">
                Supporting Evidence Citation <span className="text-gray-500">(Required for &gt;= Evidence reviewed)</span>:
              </label>
              <input
                type="text"
                placeholder="e.g. TERI 2025 Table 4.5 or CPCB site_5008 records"
                value={evidenceRef}
                onChange={(e) => setEvidenceRef(e.target.value)}
                className="w-full bg-surface-200 border border-border rounded-lg p-2.5 text-xs text-gray-100 focus:outline-none"
              />
            </div>

            <div>
              <label className="text-xs text-gray-300 font-medium block mb-1">
                Empirical Verification Dataset Link <span className="text-gray-500">(Required for Pilot validated)</span>:
              </label>
              <input
                type="text"
                placeholder="e.g. Stack isokinetic PEMS test series CSV reference"
                value={verificationRef}
                onChange={(e) => setVerificationRef(e.target.value)}
                className="w-full bg-surface-200 border border-border rounded-lg p-2.5 text-xs text-gray-100 focus:outline-none"
              />
            </div>

            <div>
              <label className="text-xs text-gray-300 font-medium block mb-1">Researcher Transition Notes:</label>
              <textarea
                rows={2}
                placeholder="Document rationale and testing findings..."
                value={stageNotes}
                onChange={(e) => setStageNotes(e.target.value)}
                className="w-full bg-surface-200 border border-border rounded-lg p-2.5 text-xs text-gray-100 focus:outline-none"
              />
            </div>

            <div className="flex justify-end gap-3 pt-3 border-t border-border">
              <button
                onClick={() => setTransitionModalOpen(false)}
                className="px-4 py-2 rounded-lg bg-surface-200 hover:bg-surface-300 text-xs font-medium text-gray-300"
              >
                Cancel
              </button>
              <button
                onClick={handleExecuteStageTransition}
                className="px-4 py-2 rounded-lg bg-prana-yellow text-black font-semibold text-xs hover:bg-prana-yellow/90"
              >
                Commit Stage Transition
              </button>
            </div>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* MODAL: SHORTLIST / REJECT DECISION                                        */}
      {/* ========================================================================= */}
      {shortlistModalOpen && selectedCandidate && (
        <div className="fixed inset-0 z-50 bg-black/80 flex items-center justify-center p-4">
          <div className="bg-surface-100 border border-border rounded-xl max-w-md w-full p-6 space-y-4">
            <div className="flex items-center justify-between pb-3 border-b border-border">
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <CheckCircle2 className="w-4 h-4 text-prana-yellow" />
                Shortlist Decision Governance
              </h3>
              <button
                onClick={() => setShortlistModalOpen(false)}
                className="text-gray-400 hover:text-white"
              >
                ✕
              </button>
            </div>

            <div>
              <div className="text-xs text-gray-400">Candidate:</div>
              <div className="font-semibold text-sm text-white">{selectedCandidate.title}</div>
            </div>

            <div>
              <label className="text-xs text-gray-300 font-medium block mb-1">Decision Status:</label>
              <select
                value={shortlistStatus}
                onChange={(e) => setShortlistStatus(e.target.value)}
                className="w-full bg-surface-200 border border-border rounded-lg p-2.5 text-xs text-gray-100 focus:outline-none"
              >
                <option value="SHORTLISTED">SHORTLISTED (Approved for Pilot Design)</option>
                <option value="FURTHER_INVESTIGATION">FURTHER_INVESTIGATION (Requires more baseline data)</option>
                <option value="REJECTED">REJECTED (Insufficient feasibility or impact)</option>
                <option value="CONSIDERING">CONSIDERING (Initial evaluation stage)</option>
              </select>
            </div>

            <div>
              <label className="text-xs text-gray-300 font-medium block mb-1">Engineering Justification Rationale:</label>
              <textarea
                rows={3}
                placeholder="State defensible technical and scientific reasons for this decision..."
                value={shortlistNotes}
                onChange={(e) => setShortlistNotes(e.target.value)}
                className="w-full bg-surface-200 border border-border rounded-lg p-2.5 text-xs text-gray-100 focus:outline-none"
              />
            </div>

            <div className="flex justify-end gap-3 pt-3 border-t border-border">
              <button
                onClick={() => setShortlistModalOpen(false)}
                className="px-4 py-2 rounded-lg bg-surface-200 hover:bg-surface-300 text-xs font-medium text-gray-300"
              >
                Cancel
              </button>
              <button
                onClick={handleExecuteShortlist}
                className="px-4 py-2 rounded-lg bg-prana-yellow text-black font-semibold text-xs hover:bg-prana-yellow/90"
              >
                Save Decision
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
