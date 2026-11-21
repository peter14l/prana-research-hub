'use client';

import React, { useState, useEffect } from 'react';
import {
  BookOpen,
  Search,
  Plus,
  ExternalLink,
  Tag,
  FileText,
  MessageSquare,
  Building,
  CheckCircle2,
  Calendar
} from 'lucide-react';
import { fetchDocuments, fetchNotes, createNote } from '@/lib/api';

export default function ResearchLibraryView() {
  const [documents, setDocuments] = useState<any[]>([]);
  const [selectedDoc, setSelectedDoc] = useState<any>(null);
  const [notes, setNotes] = useState<any[]>([]);
  const [search, setSearch] = useState<string>('');
  
  // Note form state
  const [showNoteModal, setShowNoteModal] = useState<boolean>(false);
  const [noteTitle, setNoteTitle] = useState<string>('');
  const [noteContent, setNoteContent] = useState<string>('');
  const [noteTags, setNoteTags] = useState<string>('');
  const [submittingNote, setSubmittingNote] = useState<boolean>(false);

  useEffect(() => {
    loadDocs();
    loadNotes();
  }, []);

  async function loadDocs(q?: string) {
    const data = await fetchDocuments(q);
    setDocuments(data);
    if (data.length > 0 && !selectedDoc) {
      setSelectedDoc(data[0]);
    }
  }

  async function loadNotes() {
    const data = await fetchNotes();
    setNotes(data);
  }

  async function handleAddNote(e: React.FormEvent) {
    e.preventDefault();
    if (!noteTitle || !noteContent) return;
    setSubmittingNote(true);
    try {
      await createNote(noteTitle, noteContent, noteTags, selectedDoc?.id);
      setShowNoteModal(false);
      setNoteTitle('');
      setNoteContent('');
      setNoteTags('');
      loadNotes();
    } catch (err) {
      console.error(err);
    } finally {
      setSubmittingNote(false);
    }
  }

  return (
    <div className="space-y-6">
      {/* Top Banner and Search Bar */}
      <div className="glass-panel p-5 rounded-xl border border-border flex flex-wrap items-center justify-between gap-4">
        <div>
          <h1 className="text-lg font-bold text-white flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-prana-yellow" />
            Statutory Research &amp; Literature Library
          </h1>
          <p className="text-xs text-gray-400 mt-1">
            Official source-apportionment studies, emissions inventories, and regulatory guidelines for Kolkata–Howrah.
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <div className="relative w-64">
            <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" />
            <input
              type="text"
              placeholder="Search papers, methodology, tags..."
              value={search}
              onChange={(e) => {
                setSearch(e.target.value);
                loadDocs(e.target.value);
              }}
              className="w-full bg-[#141822] border border-border rounded-lg pl-9 pr-3 py-1.5 text-xs text-gray-200 placeholder-gray-500 focus:outline-none focus:border-prana-yellow/50"
            />
          </div>

          <button
            onClick={() => setShowNoteModal(true)}
            className="flex items-center space-x-1.5 bg-prana-yellow hover:bg-prana-yellow-hover text-black px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors"
          >
            <Plus className="w-3.5 h-3.5" />
            <span>Add Research Note</span>
          </button>
        </div>
      </div>

      {/* Main Grid: Document List (5 cols) & Deep Reader Dossier (7 cols) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Document Cards */}
        <div className="lg:col-span-5 space-y-3">
          <div className="text-xs font-semibold uppercase tracking-wider text-prana-sage px-1">
            Foundational Publications ({documents.length})
          </div>

          {documents.map((doc) => {
            const isSelected = selectedDoc?.id === doc.id;
            return (
              <div
                key={doc.id}
                onClick={() => setSelectedDoc(doc)}
                className={`p-4 rounded-xl border cursor-pointer transition-all ${
                  isSelected
                    ? 'bg-[#181F2C] border-prana-yellow/60 shadow-lg'
                    : 'bg-[#12161F] border-border hover:border-white/20'
                }`}
              >
                <div className="flex items-start justify-between">
                  <h3 className="text-xs font-bold text-gray-100 line-clamp-2">
                    {doc.title}
                  </h3>
                  <span className="text-[10px] font-mono text-prana-sage shrink-0 ml-2">
                    {doc.publication_date}
                  </span>
                </div>

                <div className="text-[11px] text-gray-400 mt-1 flex items-center gap-1.5">
                  <Building className="w-3 h-3 text-gray-500" />
                  <span>{doc.organisation}</span>
                </div>

                <div className="mt-3 flex flex-wrap gap-1">
                  {doc.tags?.split(',').map((t: string, i: number) => (
                    <span
                      key={i}
                      className="text-[9px] bg-[#141822] text-gray-300 border border-border px-1.5 py-0.5 rounded"
                    >
                      {t.trim()}
                    </span>
                  ))}
                </div>
              </div>
            );
          })}
        </div>

        {/* Selected Document Dossier */}
        <div className="lg:col-span-7 glass-panel p-6 rounded-xl border border-border space-y-5">
          {selectedDoc ? (
            <>
              <div>
                <div className="flex items-center justify-between">
                  <span className="text-[10px] uppercase font-bold text-prana-yellow tracking-wider">
                    {selectedDoc.study_type}
                  </span>
                  {selectedDoc.original_url && (
                    <a
                      href={selectedDoc.original_url}
                      target="_blank"
                      rel="noreferrer"
                      className="text-xs text-prana-yellow hover:underline flex items-center gap-1 font-medium"
                    >
                      <span>Original Statutory Document</span>
                      <ExternalLink className="w-3.5 h-3.5" />
                    </a>
                  )}
                </div>

                <h2 className="text-base font-bold text-white mt-1 leading-snug">
                  {selectedDoc.title}
                </h2>
                <div className="text-xs text-prana-sage mt-1">
                  {selectedDoc.organisation} • {selectedDoc.publication_date} • Coverage: {selectedDoc.geographic_coverage}
                </div>
              </div>

              {/* Pollutants & Methodology */}
              <div className="grid grid-cols-2 gap-3 text-xs pt-3 border-t border-white/10">
                <div className="p-3 rounded-lg bg-[#141822] border border-border">
                  <div className="text-[10px] text-gray-500 uppercase font-semibold">Pollutants Investigated</div>
                  <div className="font-semibold text-gray-200 mt-0.5">{selectedDoc.pollutants_studied}</div>
                </div>
                <div className="p-3 rounded-lg bg-[#141822] border border-border">
                  <div className="text-[10px] text-gray-500 uppercase font-semibold">Scientific Confidence Tier</div>
                  <div className="font-semibold text-emerald-400 mt-0.5">{selectedDoc.confidence_tier}</div>
                </div>
              </div>

              {/* Methodology */}
              <div className="space-y-1 text-xs">
                <h4 className="font-semibold text-gray-300 flex items-center gap-1.5">
                  <FileText className="w-3.5 h-3.5 text-prana-yellow" />
                  Investigation Methodology
                </h4>
                <div className="p-3 rounded-lg bg-[#141822] border border-border text-gray-300 leading-relaxed text-[11px]">
                  {selectedDoc.methodology}
                </div>
              </div>

              {/* Key Findings */}
              <div className="space-y-1 text-xs">
                <h4 className="font-semibold text-gray-300 flex items-center gap-1.5">
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                  Key Research Findings &amp; Source Contributions
                </h4>
                <div className="p-3 rounded-lg bg-[#141822] border border-border text-gray-300 whitespace-pre-line leading-relaxed text-[11px]">
                  {selectedDoc.key_findings}
                </div>
              </div>

              {/* Document Limitations */}
              <div className="space-y-1 text-xs">
                <h4 className="font-semibold text-gray-400 flex items-center gap-1.5">
                  Document Limitations &amp; Caveats
                </h4>
                <div className="p-3 rounded-lg bg-[#0F131A] border border-border text-gray-400 text-[11px] leading-relaxed">
                  {selectedDoc.limitations}
                </div>
              </div>

              {/* Research Notes linked to this document */}
              <div className="space-y-2 pt-3 border-t border-white/10">
                <div className="flex items-center justify-between text-xs">
                  <span className="font-semibold text-gray-300 flex items-center gap-1.5">
                    <MessageSquare className="w-3.5 h-3.5 text-prana-sage" />
                    Scientist Annotations &amp; User Notes
                  </span>
                  <button
                    onClick={() => setShowNoteModal(true)}
                    className="text-[11px] text-prana-yellow hover:underline"
                  >
                    + Add Annotation
                  </button>
                </div>

                <div className="space-y-2">
                  {notes
                    .filter((n) => n.document_id === selectedDoc.id)
                    .map((n) => (
                      <div key={n.id} className="p-3 rounded-lg bg-[#141822] border border-border text-xs">
                        <div className="flex items-center justify-between">
                          <span className="font-bold text-gray-200">{n.title}</span>
                          <span className="text-[10px] text-gray-500 font-mono">
                            {new Date(n.created_at).toLocaleDateString()}
                          </span>
                        </div>
                        <p className="text-[11px] text-gray-400 mt-1 leading-relaxed">{n.content}</p>
                        {n.tags && (
                          <div className="text-[9px] text-prana-sage mt-2">Tags: {n.tags}</div>
                        )}
                      </div>
                    ))}
                  {notes.filter((n) => n.document_id === selectedDoc.id).length === 0 && (
                    <div className="text-xs text-gray-500 py-2 text-center bg-[#10141C] rounded-lg border border-border">
                      No annotations yet for this paper. Click &quot;Add Research Note&quot; to log your findings.
                    </div>
                  )}
                </div>
              </div>
            </>
          ) : (
            <div className="h-full flex items-center justify-center text-xs text-gray-500">
              Select a research paper from the library to view full metadata and citations.
            </div>
          )}
        </div>
      </div>

      {/* Add Note Modal */}
      {showNoteModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm">
          <div className="w-[500px] bg-[#12161F] border border-border rounded-xl p-6 shadow-2xl space-y-4">
            <h3 className="text-base font-bold text-white">Add Research Annotation</h3>
            <form onSubmit={handleAddNote} className="space-y-3 text-xs">
              <div>
                <label className="text-gray-400 block mb-1">Annotation Title</label>
                <input
                  type="text"
                  required
                  value={noteTitle}
                  onChange={(e) => setNoteTitle(e.target.value)}
                  placeholder="e.g., Night-time spike discrepancy in Howrah"
                  className="w-full bg-[#181E29] border border-border rounded-lg px-3 py-2 text-gray-200 focus:outline-none focus:border-prana-yellow/50"
                />
              </div>

              <div>
                <label className="text-gray-400 block mb-1">Content / Evidence Note</label>
                <textarea
                  required
                  rows={4}
                  value={noteContent}
                  onChange={(e) => setNoteContent(e.target.value)}
                  placeholder="Document your scientific observation or discrepancy..."
                  className="w-full bg-[#181E29] border border-border rounded-lg px-3 py-2 text-gray-200 focus:outline-none focus:border-prana-yellow/50"
                />
              </div>

              <div>
                <label className="text-gray-400 block mb-1">Tags (Comma-separated)</label>
                <input
                  type="text"
                  value={noteTags}
                  onChange={(e) => setNoteTags(e.target.value)}
                  placeholder="Ghusuri, Foundries, Inversion"
                  className="w-full bg-[#181E29] border border-border rounded-lg px-3 py-2 text-gray-200 focus:outline-none focus:border-prana-yellow/50"
                />
              </div>

              <div className="flex justify-end space-x-2 pt-2">
                <button
                  type="button"
                  onClick={() => setShowNoteModal(false)}
                  className="px-4 py-2 bg-[#181E29] hover:bg-[#222B3A] text-gray-300 rounded-lg"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={submittingNote}
                  className="px-4 py-2 bg-prana-yellow hover:bg-prana-yellow-hover text-black font-semibold rounded-lg disabled:opacity-50"
                >
                  Save Note
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
