"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { 
  Bookmark, 
  MapPin, 
  GraduationCap, 
  Briefcase, 
  Trash2, 
  ExternalLink, 
  FileText,
  Clock,
  RefreshCw,
  Tag
} from "lucide-react";
import { api } from "@/lib/api";
import { ShortlistItem, ShortlistStage } from "@/lib/types";
import { NoteModal } from "@/components/NoteModal";

const STAGES: ShortlistStage[] = [
  "Shortlisted",
  "Interesting",
  "Need Review",
  "Contact Later",
  "New",
  "Archived"
];

export default function ShortlistPage() {
  const [items, setItems] = useState<ShortlistItem[]>([]);
  const [activeStage, setActiveStage] = useState<string>("ALL");
  const [loading, setLoading] = useState(true);

  // Note modal state
  const [activeNoteModal, setActiveNoteModal] = useState<{
    isOpen: boolean;
    profileId: string;
    candidateCode: string;
  }>({
    isOpen: false,
    profileId: "",
    candidateCode: "",
  });

  useEffect(() => {
    loadShortlists();
  }, [activeStage]);

  const loadShortlists = async () => {
    try {
      setLoading(true);
      const stageParam = activeStage === "ALL" ? undefined : activeStage;
      const data = await api.getShortlists(stageParam);
      setItems(data);
    } catch (err) {
      console.error("Failed to load shortlist", err);
    } finally {
      setLoading(false);
    }
  };

  const handleStageChange = async (shortlistId: string, newStage: ShortlistStage) => {
    try {
      await api.updateShortlist(shortlistId, newStage);
      setItems(items.map((i) => (i.id === shortlistId ? { ...i, stage: newStage } : i)));
    } catch (err) {
      console.error("Failed to update stage", err);
    }
  };

  const handleDelete = async (shortlistId: string) => {
    try {
      await api.deleteShortlist(shortlistId);
      setItems(items.filter((i) => i.id !== shortlistId));
    } catch (err) {
      console.error("Failed to remove from shortlist", err);
    }
  };

  return (
    <div className="space-y-6 pb-20">
      <div>
        <h1 className="text-2xl font-extrabold text-zinc-900 dark:text-zinc-100 flex items-center gap-2">
          <Bookmark className="w-6 h-6 text-emerald-600" />
          <span>Saved & Shortlisted Candidates</span>
        </h1>
        <p className="text-xs text-zinc-500 mt-1">
          Review queue organized by consideration stages. All stages and notes are strictly private.
        </p>
      </div>

      {/* Stage Tabs */}
      <div className="flex items-center space-x-1.5 overflow-x-auto p-1.5 bg-white dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-800 text-xs shadow-xs">
        <button
          onClick={() => setActiveStage("ALL")}
          className={`px-3.5 py-1.5 rounded-lg font-semibold transition-colors ${
            activeStage === "ALL"
              ? "bg-zinc-900 text-white dark:bg-zinc-100 dark:text-zinc-900 shadow-xs"
              : "text-zinc-600 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-800"
          }`}
        >
          All Stages
        </button>
        {STAGES.map((s) => (
          <button
            key={s}
            onClick={() => setActiveStage(s)}
            className={`px-3.5 py-1.5 rounded-lg font-semibold transition-colors ${
              activeStage === s
                ? "bg-zinc-900 text-white dark:bg-zinc-100 dark:text-zinc-900 shadow-xs"
                : "text-zinc-600 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-800"
            }`}
          >
            {s}
          </button>
        ))}
      </div>

      {/* Candidates List */}
      {loading ? (
        <div className="py-20 text-center">
          <RefreshCw className="w-6 h-6 animate-spin mx-auto text-emerald-600 mb-2" />
          <p className="text-xs text-zinc-400">Loading shortlist...</p>
        </div>
      ) : items.length === 0 ? (
        <div className="text-center py-20 bg-white dark:bg-zinc-900 rounded-2xl border border-zinc-200 dark:border-zinc-800">
          <p className="text-base font-bold text-zinc-700 dark:text-zinc-300">No candidates in this stage</p>
          <p className="text-xs text-zinc-400 mt-1">Shortlist candidates from Search Results to review them here.</p>
          <Link
            href="/search"
            className="inline-block mt-4 px-4 py-2 text-xs font-semibold rounded-xl bg-emerald-700 hover:bg-emerald-800 text-white transition-colors"
          >
            Go to Search
          </Link>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {items.map((item) => {
            const p = item.profile;
            if (!p) return null;

            return (
              <div
                key={item.id}
                className="bg-white dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-800 p-5 shadow-xs flex flex-col justify-between space-y-4"
              >
                <div>
                  <div className="flex items-start justify-between">
                    <div>
                      <Link
                        href={`/profiles/${p.id}`}
                        className="text-base font-bold text-zinc-900 dark:text-zinc-100 hover:text-emerald-700 transition-colors"
                      >
                        {p.candidate_code || `Candidate #${p.id.slice(0, 6)}`}
                      </Link>
                      <div className="flex items-center space-x-2 text-xs text-zinc-500 mt-1">
                        <span>{p.age ? `${p.age} yrs` : "Age N/A"}</span>
                        <span>•</span>
                        <span>{p.height_display || (p.height_cm ? `${p.height_cm} cm` : "Height N/A")}</span>
                        <span>•</span>
                        <span className="flex items-center gap-1">
                          <MapPin className="w-3 h-3 text-zinc-400" />
                          {p.current_location || "N/A"}
                        </span>
                      </div>
                    </div>

                    {/* Stage Selector */}
                    <div className="flex items-center space-x-1">
                      <Tag className="w-3.5 h-3.5 text-zinc-400" />
                      <select
                        value={item.stage}
                        onChange={(e) => handleStageChange(item.id, e.target.value as ShortlistStage)}
                        className="text-xs font-semibold p-1.5 rounded-lg border border-zinc-200 dark:border-zinc-700 bg-zinc-50 dark:bg-zinc-800 text-zinc-800 dark:text-zinc-200 focus:outline-none"
                      >
                        {STAGES.map((s) => (
                          <option key={s} value={s}>
                            {s}
                          </option>
                        ))}
                      </select>
                    </div>
                  </div>

                  {/* Highlights */}
                  <div className="mt-3.5 pt-3 border-t border-zinc-100 dark:border-zinc-800/80 grid grid-cols-2 gap-2 text-xs">
                    <div>
                      <span className="text-[10px] text-zinc-400 uppercase tracking-wider block">Education</span>
                      <p className="text-zinc-800 dark:text-zinc-200 font-medium truncate">
                        {p.education.degree || p.education.field || "Not stated"}
                      </p>
                    </div>
                    <div>
                      <span className="text-[10px] text-zinc-400 uppercase tracking-wider block">Profession</span>
                      <p className="text-zinc-800 dark:text-zinc-200 font-medium truncate">
                        {p.career.occupation || "Not stated"}
                      </p>
                    </div>
                  </div>

                  {/* Shortlist Note */}
                  {item.notes && (
                    <div className="mt-3 p-2.5 rounded-lg bg-emerald-50/60 dark:bg-emerald-950/30 text-xs text-emerald-900 dark:text-emerald-200 border border-emerald-100 dark:border-emerald-900/40">
                      <span className="font-semibold text-[11px] block">Review Notes:</span>
                      <p>{item.notes}</p>
                    </div>
                  )}
                </div>

                {/* Footer Actions */}
                <div className="pt-3 border-t border-zinc-100 dark:border-zinc-800 flex items-center justify-between text-xs">
                  <button
                    onClick={() =>
                      setActiveNoteModal({
                        isOpen: true,
                        profileId: p.id,
                        candidateCode: p.candidate_code || `Candidate #${p.id}`,
                      })
                    }
                    className="inline-flex items-center space-x-1 text-zinc-600 dark:text-zinc-400 hover:text-emerald-700 font-medium"
                  >
                    <FileText className="w-3.5 h-3.5" />
                    <span>Private Notes</span>
                  </button>

                  <div className="flex items-center space-x-2">
                    <Link
                      href={`/profiles/${p.id}`}
                      className="px-3 py-1.5 rounded-lg font-semibold bg-zinc-100 dark:bg-zinc-800 hover:bg-zinc-200 dark:hover:bg-zinc-700 text-zinc-800 dark:text-zinc-200 transition-colors"
                    >
                      View Details
                    </Link>

                    <button
                      onClick={() => handleDelete(item.id)}
                      className="p-1.5 rounded-lg text-zinc-400 hover:text-rose-600 hover:bg-rose-50 dark:hover:bg-rose-950/40 transition-colors"
                      title="Remove from shortlist"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Private Note Modal */}
      <NoteModal
        isOpen={activeNoteModal.isOpen}
        onClose={() => setActiveNoteModal({ ...activeNoteModal, isOpen: false })}
        profileId={activeNoteModal.profileId}
        candidateCode={activeNoteModal.candidateCode}
      />
    </div>
  );
}
