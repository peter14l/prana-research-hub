'use client';

import React, { useState } from 'react';
import { X, Sparkles, Send, BookOpen, AlertCircle, ShieldAlert } from 'lucide-react';
import { askAssistant } from '@/lib/api';

interface AIAssistantDrawerProps {
  isOpen: boolean;
  onClose: () => void;
}

const PRESET_QUERIES = [
  'Why is PM2.5 chronically elevated at Ghusuri station?',
  'Compare TERI (2025) and CSIR-NEERI (2020) source contribution findings',
  'Which candidate intervention shows the strongest engineering feasibility?',
  'Explain the atmospheric inversion and planetary boundary layer height dynamics in winter'
];

export default function AIAssistantDrawer({ isOpen, onClose }: AIAssistantDrawerProps) {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState<
    { role: 'user' | 'assistant'; text: string; citations?: any[] }[]
  >([
    {
      role: 'assistant',
      text:
        'Welcome to the **PRANA Research Assistant**. I am strictly grounded in verified database telemetry and ' +
        'statutory peer-reviewed research papers (TERI 2025, CSIR-NEERI 2020, CPCB).\n\n' +
        'I do not fabricate sensor measurements or source contributions. How may I assist your scientific inquiry today?',
      citations: [
        { source: 'TERI 2025 Kolkata Carrying Capacity Study', authority: 'WBPCB' },
        { source: 'CSIR-NEERI 2020 Twin Cities Final Report', authority: 'CSIR' }
      ]
    }
  ]);

  if (!isOpen) return null;

  async function handleSend(textToSend?: string) {
    const q = (textToSend || query).trim();
    if (!q || loading) return;

    setMessages((prev) => [...prev, { role: 'user', text: q }]);
    setQuery('');
    setLoading(true);

    try {
      const data = await askAssistant(q);
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          text: data.response,
          citations: data.citations
        }
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: 'assistant',
          text: 'Unable to reach research synthesis service. Please verify backend connectivity.'
        }
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="fixed inset-0 z-50 flex justify-end bg-black/60 backdrop-blur-sm animate-fade-in">
      <div className="w-[500px] bg-[#10141C] border-l border-border h-full flex flex-col justify-between shadow-2xl">
        {/* Header */}
        <div className="p-4 border-b border-border flex items-center justify-between bg-[#0D1017]">
          <div className="flex items-center space-x-2.5">
            <div className="w-8 h-8 rounded-lg bg-surface-200 border border-prana-yellow/40 flex items-center justify-center">
              <Sparkles className="w-4 h-4 text-prana-yellow" />
            </div>
            <div>
              <div className="font-semibold text-sm text-white">PRANA Research Assistant</div>
              <div className="text-[10px] text-prana-sage flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                Grounded in WBPCB &amp; Peer-Reviewed Literature
              </div>
            </div>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-white p-1 rounded-md transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Message Log */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {/* Scientific Grounding Warning Banner */}
          <div className="rounded-lg bg-[#141924] border border-white/10 p-3 text-xs text-gray-300 flex items-start space-x-2.5">
            <ShieldAlert className="w-4 h-4 text-prana-yellow shrink-0 mt-0.5" />
            <div className="text-[11px] leading-relaxed">
              <span className="font-semibold text-prana-yellow">Strict Scientific Rule:</span> This assistant only cites
              verified measurements and published source-apportionment studies. It does not speculate or invent unmonitored ward data.
            </div>
          </div>

          {messages.map((m, idx) => (
            <div
              key={idx}
              className={`flex flex-col ${
                m.role === 'user' ? 'items-end' : 'items-start'
              }`}
            >
              <div
                className={`max-w-[90%] rounded-xl p-3.5 text-xs leading-relaxed ${
                  m.role === 'user'
                    ? 'bg-[#1C2330] text-gray-100 border border-border'
                    : 'bg-[#141822] text-gray-200 border border-border/80'
                }`}
              >
                <div className="whitespace-pre-line">{m.text}</div>

                {/* Citations block */}
                {m.citations && m.citations.length > 0 && (
                  <div className="mt-3 pt-2.5 border-t border-white/10">
                    <div className="text-[10px] uppercase font-semibold text-prana-sage tracking-wider flex items-center gap-1 mb-1.5">
                      <BookOpen className="w-3 h-3" /> Supporting Citations
                    </div>
                    <div className="space-y-1">
                      {m.citations.map((c: any, i: number) => (
                        <div key={i} className="text-[11px] text-gray-300 bg-[#0C0F14] px-2 py-1 rounded border border-border">
                          • {c.source} <span className="text-gray-500">({c.authority})</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex items-center space-x-2 text-xs text-prana-yellow p-3 rounded-lg bg-[#141822] border border-border animate-pulse">
              <Sparkles className="w-3.5 h-3.5 animate-spin" />
              <span>Querying research database and synthesizing findings...</span>
            </div>
          )}
        </div>

        {/* Preset chips & Input Footer */}
        <div className="p-4 border-t border-border bg-[#0D1017] space-y-3">
          {/* Preset Chips */}
          <div className="flex flex-wrap gap-1.5">
            {PRESET_QUERIES.map((preset, i) => (
              <button
                key={i}
                onClick={() => handleSend(preset)}
                className="text-[10px] bg-[#141924] hover:bg-[#1D2433] text-gray-300 border border-border px-2.5 py-1 rounded-full text-left transition-colors truncate max-w-full"
              >
                {preset}
              </button>
            ))}
          </div>

          <div className="flex items-center space-x-2">
            <input
              type="text"
              placeholder="Ask about Kolkata-Howrah pollution, sources, or interventions..."
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSend()}
              className="flex-1 bg-[#141822] border border-border rounded-lg px-3.5 py-2 text-xs text-gray-200 placeholder-gray-500 focus:outline-none focus:border-prana-yellow/50"
            />
            <button
              onClick={() => handleSend()}
              disabled={loading || !query.trim()}
              className="bg-prana-yellow hover:bg-prana-yellow-hover text-black px-3.5 py-2 rounded-lg text-xs font-semibold disabled:opacity-50 transition-colors flex items-center justify-center"
            >
              <Send className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
