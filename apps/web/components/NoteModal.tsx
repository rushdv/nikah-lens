"use client";

import { useState, useEffect } from "react";
import { X, Lock, Send, Trash2, Calendar } from "lucide-react";
import { Note } from "@/lib/types";
import { api } from "@/lib/api";

interface NoteModalProps {
  isOpen: boolean;
  onClose: () => void;
  profileId: string;
  candidateCode: string;
}

export function NoteModal({ isOpen, onClose, profileId, candidateCode }: NoteModalProps) {
  const [notes, setNotes] = useState<Note[]>([]);
  const [newContent, setNewContent] = useState("");
  const [loading, setLoading] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (isOpen && profileId) {
      loadNotes();
    }
  }, [isOpen, profileId]);

  const loadNotes = async () => {
    try {
      setLoading(true);
      const data = await api.getProfileNotes(profileId);
      setNotes(data);
    } catch (err) {
      console.error("Failed to load notes", err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddNote = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newContent.trim()) return;

    try {
      setSubmitting(true);
      const created = await api.createNote(profileId, newContent.trim());
      setNotes([created, ...notes]);
      setNewContent("");
    } catch (err) {
      console.error("Failed to add note", err);
    } finally {
      setSubmitting(false);
    }
  };

  const handleDeleteNote = async (noteId: string) => {
    try {
      await api.deleteNote(noteId);
      setNotes(notes.filter((n) => n.id !== noteId));
    } catch (err) {
      console.error("Failed to delete note", err);
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-xs">
      <div className="bg-white dark:bg-zinc-900 rounded-2xl max-w-lg w-full border border-zinc-200 dark:border-zinc-800 shadow-2xl overflow-hidden flex flex-col max-h-[85vh]">
        {/* Header */}
        <div className="px-6 py-4 border-b border-zinc-100 dark:border-zinc-800 flex items-center justify-between bg-zinc-50 dark:bg-zinc-900/50">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 rounded-lg bg-emerald-100 dark:bg-emerald-950 flex items-center justify-center text-emerald-800 dark:text-emerald-300">
              <Lock className="w-4 h-4" />
            </div>
            <div>
              <h3 className="text-base font-bold text-zinc-900 dark:text-zinc-100">
                Private Notes: {candidateCode}
              </h3>
              <p className="text-[11px] text-zinc-500">
                Strictly local & private. Never communicated to source websites.
              </p>
            </div>
          </div>

          <button
            onClick={onClose}
            className="p-1 rounded-lg text-zinc-400 hover:text-zinc-600 dark:hover:text-zinc-200 hover:bg-zinc-100 dark:hover:bg-zinc-800"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Notes List */}
        <div className="p-6 overflow-y-auto flex-1 space-y-3">
          {loading ? (
            <div className="text-center py-8 text-xs text-zinc-400">Loading private notes...</div>
          ) : notes.length === 0 ? (
            <div className="text-center py-10">
              <p className="text-sm font-medium text-zinc-600 dark:text-zinc-400">No private notes yet</p>
              <p className="text-xs text-zinc-400 mt-1">Add personal reflections, family inquiry feedback, or verified details.</p>
            </div>
          ) : (
            notes.map((note) => (
              <div
                key={note.id}
                className="p-3.5 rounded-xl bg-zinc-50 dark:bg-zinc-800/40 border border-zinc-200/80 dark:border-zinc-800 text-xs flex flex-col justify-between group"
              >
                <p className="text-zinc-800 dark:text-zinc-200 whitespace-pre-wrap leading-relaxed">
                  {note.content}
                </p>
                <div className="mt-2.5 pt-2 border-t border-zinc-200/60 dark:border-zinc-700/60 flex items-center justify-between text-[11px] text-zinc-400">
                  <span className="flex items-center gap-1">
                    <Calendar className="w-3 h-3" />
                    {new Date(note.created_at).toLocaleString()}
                  </span>
                  <button
                    onClick={() => handleDeleteNote(note.id)}
                    className="opacity-0 group-hover:opacity-100 text-zinc-400 hover:text-rose-600 transition-opacity p-1"
                    title="Delete note"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>
              </div>
            ))
          )}
        </div>

        {/* Add Note Form */}
        <form onSubmit={handleAddNote} className="p-4 border-t border-zinc-100 dark:border-zinc-800 bg-zinc-50/50 dark:bg-zinc-900/50">
          <div className="flex gap-2">
            <input
              type="text"
              value={newContent}
              onChange={(e) => setNewContent(e.target.value)}
              placeholder="Add a private note (e.g. family contacted, verified masjid...)"
              className="flex-1 px-3.5 py-2 text-xs rounded-xl border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-emerald-500/30 focus:border-emerald-600"
            />
            <button
              type="submit"
              disabled={submitting || !newContent.trim()}
              className="px-4 py-2 text-xs font-semibold rounded-xl bg-emerald-700 hover:bg-emerald-800 disabled:opacity-50 text-white flex items-center gap-1.5 transition-colors"
            >
              <Send className="w-3.5 h-3.5" />
              <span>Save</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
