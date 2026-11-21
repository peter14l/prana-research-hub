'use client';

import React, { useState, useEffect } from 'react';
import {
  FlaskConical,
  Plus,
  Target,
  Sparkles,
  CheckCircle2,
  AlertTriangle,
  Layers,
  BarChart2,
  Sliders,
  FileCheck
} from 'lucide-react';
import { fetchHypotheses, createHypothesis } from '@/lib/api';

export default function InterventionLabView() {
  const [hypotheses, setHypotheses] = useState<any[]>([]);
  const [selectedHyp, setSelectedHyp] = useState<any>(null);
  const [showModal, setShowModal] = useState<boolean>(false);
  const [loading, setLoading] = useState<boolean>(true);

  // Form State
  const [title, setTitle] = useState('');
  const [targetArea, setTargetArea] = useState('');
  const [suspectedSource, setSuspectedSource] = useState('');
  const [problemStatement, setProblemStatement] = useState('');
  const [proposedIntervention, setProposedIntervention] = useState('');
  const [mechanism, setMechanism] = useState('');
  const [resources, setResources] = useState('');
  const [partner, setPartner] = useState('');
  const [indicators, setIndicators] = useState('');
  const [risks, setRisks] = useState('');
  const [validation, setValidation] = useState('');
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    loadHypotheses();
  }, []);

  async function loadHypotheses() {
    setLoading(true);
    try {
      const data = await fetchHypotheses();
      setHypotheses(data);
      if (data.length > 0 && !selectedHyp) {
        setSelectedHyp(data[0]);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }

  async function handleCreate(e: React.FormEvent) {
    e.preventDefault();
    setSubmitting(true);
    try {
      await createHypothesis({
        title,
        target_area: targetArea,
        suspected_source: suspectedSource,
        problem_statement: problemStatement,
        proposed_intervention: proposedIntervention,
        mechanism_of_action: mechanism,
        required_resources: resources,
        possible_implementation_partner: partner,
        measurable_indicators: indicators,
        risks_limitations: risks,
        validation_requirements: validation,
        supporting_evidence: 'Statutory CAAQM sensor baseline and TERI 2025 source apportionment.',
        feasibility_score: 7.5,
        potential_reduction_score: 8.0,
        cost_complexity_score: 5.5,
        ease_of_verification_score: 8.0,
        scalability_score: 8.5
      });
      setShowModal(false);
      loadHypotheses();
    } catch (err) {
      console.error(err);
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="glass-panel p-5 rounded-xl border border-border flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-lg font-bold text-white flex items-center gap-2">
            <FlaskConical className="w-5 h-5 text-prana-yellow" />
            Intervention Lab: Engineering Opportunities
          </h1>
          <p className="text-xs text-gray-400 mt-1 max-w-3xl leading-relaxed">
            Converting atmospheric intelligence into defensible, testable engineering pilot projects.
            Every hypothesis defines counterfactual baseline requirements, meteorological de-weathering, and measurable success indicators.
          </p>
        </div>

        <button
          onClick={() => setShowModal(true)}
          className="flex items-center space-x-1.5 bg-prana-yellow hover:bg-prana-yellow-hover text-black px-3.5 py-2 rounded-lg text-xs font-semibold transition-colors"
        >
          <Plus className="w-3.5 h-3.5" />
          <span>Formulate New Hypothesis</span>
        </button>
      </div>

      {/* Main Layout: Hypotheses Cards (5 Cols) & Deep Verification Framework (7 Cols) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Hypotheses List */}
        <div className="lg:col-span-5 space-y-3">
          <div className="text-xs font-semibold uppercase tracking-wider text-prana-sage px-1">
            Candidate Engineering Interventions ({hypotheses.length})
          </div>

          {hypotheses.map((h) => {
            const isSelected = selectedHyp?.id === h.id;
            return (
              <div
                key={h.id}
                onClick={() => setSelectedHyp(h)}
                className={`p-4 rounded-xl border cursor-pointer transition-all ${
                  isSelected
                    ? 'bg-[#181F2C] border-prana-yellow/60 shadow-lg'
                    : 'bg-[#12161F] border-border hover:border-white/20'
                }`}
              >
                <div className="flex items-start justify-between">
                  <h3 className="text-xs font-bold text-gray-100 line-clamp-2 leading-snug">
                    {h.title}
                  </h3>
                  <span className="text-[10px] uppercase font-bold text-prana-yellow px-2 py-0.5 rounded bg-surface-200 border border-border shrink-0 ml-2">
                    {h.status?.replace('_', ' ')}
                  </span>
                </div>

                <div className="text-[11px] text-gray-400 mt-1">
                  Target: <span className="text-gray-200">{h.target_area}</span>
                </div>

                {/* Score Pills */}
                <div className="mt-3 pt-2 border-t border-white/5 flex items-center justify-between text-[11px]">
                  <div className="flex items-center space-x-3">
                    <span className="text-gray-400">
                      Feasibility: <strong className="text-emerald-400">{h.feasibility_score}/10</strong>
                    </span>
                    <span className="text-gray-400">
                      Reduction: <strong className="text-prana-yellow">{h.potential_reduction_score}/10</strong>
                    </span>
                  </div>
                  <span className="text-[10px] text-prana-sage">
                    Verification: {h.ease_of_verification_score}/10
                  </span>
                </div>
              </div>
            );
          })}
        </div>

        {/* Selected Hypothesis Dossier */}
        <div className="lg:col-span-7 glass-panel p-6 rounded-xl border border-border space-y-5">
          {selectedHyp ? (
            <>
              <div>
                <span className="text-[10px] uppercase font-bold text-prana-sage tracking-wider">
                  Engineering Proposal Specification
                </span>
                <h2 className="text-base font-bold text-white mt-1 leading-snug">
                  {selectedHyp.title}
                </h2>
                <div className="text-xs text-gray-400 mt-0.5">
                  Target Area: <strong className="text-gray-200">{selectedHyp.target_area}</strong> • Target Pollutants: <strong className="text-prana-yellow">{selectedHyp.target_pollutant}</strong>
                </div>
              </div>

              {/* Multi-Criteria Quantitative Matrix */}
              <div className="grid grid-cols-5 gap-2 text-center text-xs p-3 rounded-lg bg-[#141822] border border-border">
                <div>
                  <div className="text-[9px] text-gray-500 uppercase font-semibold">Feasibility</div>
                  <div className="text-base font-bold text-emerald-400 font-mono mt-0.5">
                    {selectedHyp.feasibility_score}
                  </div>
                </div>
                <div>
                  <div className="text-[9px] text-gray-500 uppercase font-semibold">Particulate Drop</div>
                  <div className="text-base font-bold text-prana-yellow font-mono mt-0.5">
                    {selectedHyp.potential_reduction_score}
                  </div>
                </div>
                <div>
                  <div className="text-[9px] text-gray-500 uppercase font-semibold">Cost Burden</div>
                  <div className="text-base font-bold text-gray-300 font-mono mt-0.5">
                    {selectedHyp.cost_complexity_score}
                  </div>
                </div>
                <div>
                  <div className="text-[9px] text-gray-500 uppercase font-semibold">Verification</div>
                  <div className="text-base font-bold text-emerald-400 font-mono mt-0.5">
                    {selectedHyp.ease_of_verification_score}
                  </div>
                </div>
                <div>
                  <div className="text-[9px] text-gray-500 uppercase font-semibold">Scalability</div>
                  <div className="text-base font-bold text-white font-mono mt-0.5">
                    {selectedHyp.scalability_score}
                  </div>
                </div>
              </div>

              {/* Mechanism of Action */}
              <div className="space-y-1 text-xs">
                <h4 className="font-semibold text-gray-300 flex items-center gap-1.5">
                  <Target className="w-3.5 h-3.5 text-prana-yellow" />
                  Proposed Mechanism of Action
                </h4>
                <div className="p-3 rounded-lg bg-[#141822] border border-border text-gray-300 text-[11px] leading-relaxed">
                  {selectedHyp.mechanism_of_action}
                </div>
              </div>

              {/* Measurable Success Indicators */}
              <div className="space-y-1 text-xs">
                <h4 className="font-semibold text-gray-300 flex items-center gap-1.5">
                  <BarChart2 className="w-3.5 h-3.5 text-emerald-400" />
                  Measurable Success Indicators
                </h4>
                <div className="p-3 rounded-lg bg-[#141822] border border-border text-gray-300 whitespace-pre-line text-[11px] leading-relaxed">
                  {selectedHyp.measurable_indicators}
                </div>
              </div>

              {/* Evaluation Framework Specifications */}
              <div className="p-4 rounded-xl bg-[#0F131A] border border-border space-y-2 text-xs">
                <div className="font-bold text-prana-yellow flex items-center gap-1.5 uppercase text-[10px] tracking-wider">
                  <FileCheck className="w-3.5 h-3.5" />
                  Counterfactual Verification Protocol
                </div>
                <div className="grid grid-cols-2 gap-3 text-[11px] text-gray-300 pt-1">
                  <div>
                    <span className="text-gray-500">Baseline Period:</span>{' '}
                    <span>{selectedHyp.evaluation_framework?.baseline_period_days ?? 60} Days</span>
                  </div>
                  <div>
                    <span className="text-gray-500">Intervention Period:</span>{' '}
                    <span>{selectedHyp.evaluation_framework?.intervention_period_days ?? 120} Days</span>
                  </div>
                  <div>
                    <span className="text-gray-500">Control Station:</span>{' '}
                    <span>{selectedHyp.evaluation_framework?.control_station ?? 'Victoria Memorial'}</span>
                  </div>
                  <div>
                    <span className="text-gray-500">Impact Sensor:</span>{' '}
                    <span>{selectedHyp.evaluation_framework?.impact_station ?? 'Ghusuri'}</span>
                  </div>
                </div>
                <div className="text-[10px] text-gray-400 pt-1 border-t border-white/5">
                  <strong>Weather Normalization:</strong> {selectedHyp.evaluation_framework?.weather_normalization_method ?? 'Random Forest de-weathering'}
                </div>
              </div>

              {/* Risks & Limitations */}
              <div className="space-y-1 text-xs">
                <div className="text-[11px] text-gray-400">
                  <strong className="text-amber-400">Implementation Partner:</strong> {selectedHyp.possible_implementation_partner}
                </div>
                <div className="text-[11px] text-gray-500">
                  <strong>Risks &amp; Limitations:</strong> {selectedHyp.risks_limitations}
                </div>
              </div>
            </>
          ) : (
            <div className="h-full flex items-center justify-center text-xs text-gray-500">
              Select an intervention candidate to view the engineering dossier.
            </div>
          )}
        </div>
      </div>

      {/* Formulate Hypothesis Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm p-4 overflow-y-auto">
          <div className="w-[600px] max-h-[90vh] overflow-y-auto bg-[#12161F] border border-border rounded-xl p-6 shadow-2xl space-y-4">
            <h3 className="text-base font-bold text-white flex items-center gap-2">
              <FlaskConical className="w-4 h-4 text-prana-yellow" />
              Formulate New Engineering Intervention Hypothesis
            </h3>

            <form onSubmit={handleCreate} className="space-y-3 text-xs">
              <div>
                <label className="text-gray-400 block mb-1">Proposal Title</label>
                <input
                  type="text"
                  required
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="e.g., Howrah Cupola Furnace Divided-Blast Abatement"
                  className="w-full bg-[#181E29] border border-border rounded-lg px-3 py-2 text-gray-200 focus:outline-none focus:border-prana-yellow/50"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-gray-400 block mb-1">Target Area</label>
                  <input
                    type="text"
                    required
                    value={targetArea}
                    onChange={(e) => setTargetArea(e.target.value)}
                    placeholder="e.g., Ghusuri / Liluah"
                    className="w-full bg-[#181E29] border border-border rounded-lg px-3 py-2 text-gray-200"
                  />
                </div>
                <div>
                  <label className="text-gray-400 block mb-1">Suspected Source</label>
                  <input
                    type="text"
                    required
                    value={suspectedSource}
                    onChange={(e) => setSuspectedSource(e.target.value)}
                    placeholder="e.g., Foundry cupola stacks"
                    className="w-full bg-[#181E29] border border-border rounded-lg px-3 py-2 text-gray-200"
                  />
                </div>
              </div>

              <div>
                <label className="text-gray-400 block mb-1">Problem Statement</label>
                <textarea
                  required
                  rows={2}
                  value={problemStatement}
                  onChange={(e) => setProblemStatement(e.target.value)}
                  placeholder="Describe the environmental problem and supporting telemetry evidence..."
                  className="w-full bg-[#181E29] border border-border rounded-lg px-3 py-2 text-gray-200"
                />
              </div>

              <div>
                <label className="text-gray-400 block mb-1">Proposed Intervention &amp; Mechanism</label>
                <textarea
                  required
                  rows={2}
                  value={proposedIntervention}
                  onChange={(e) => setProposedIntervention(e.target.value)}
                  placeholder="Detail the technical action, equipment, or process change..."
                  className="w-full bg-[#181E29] border border-border rounded-lg px-3 py-2 text-gray-200"
                />
              </div>

              <div>
                <label className="text-gray-400 block mb-1">Measurable Success Indicators</label>
                <textarea
                  required
                  rows={2}
                  value={indicators}
                  onChange={(e) => setIndicators(e.target.value)}
                  placeholder="e.g., ≥20% localized PM2.5 reduction at downwind boundary sensor..."
                  className="w-full bg-[#181E29] border border-border rounded-lg px-3 py-2 text-gray-200"
                />
              </div>

              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className="text-gray-400 block mb-1">Implementation Partner</label>
                  <input
                    type="text"
                    required
                    value={partner}
                    onChange={(e) => setPartner(e.target.value)}
                    placeholder="e.g., WBPCB / MSME Association"
                    className="w-full bg-[#181E29] border border-border rounded-lg px-3 py-2 text-gray-200"
                  />
                </div>
                <div>
                  <label className="text-gray-400 block mb-1">Required Resources</label>
                  <input
                    type="text"
                    required
                    value={resources}
                    onChange={(e) => setResources(e.target.value)}
                    placeholder="e.g., 2 pilot skids, ₹35 Lakhs"
                    className="w-full bg-[#181E29] border border-border rounded-lg px-3 py-2 text-gray-200"
                  />
                </div>
              </div>

              <div className="flex justify-end space-x-2 pt-3 border-t border-white/10">
                <button
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="px-4 py-2 bg-[#181E29] hover:bg-[#222B3A] text-gray-300 rounded-lg"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={submitting}
                  className="px-4 py-2 bg-prana-yellow hover:bg-prana-yellow-hover text-black font-semibold rounded-lg disabled:opacity-50"
                >
                  Create Hypothesis
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
