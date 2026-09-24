"use client";

import { useEffect, useState, use } from "react";
import Link from "next/link";
import { 
  ArrowLeft, 
  ExternalLink, 
  MapPin, 
  GraduationCap, 
  Briefcase, 
  BookOpen, 
  HeartHandshake, 
  ShieldCheck, 
  FileText, 
  History, 
  AlertTriangle,
  Bookmark,
  Calendar,
  Send,
  Trash2
} from "lucide-react";
import { api } from "@/lib/api";
import { Profile, ProfileVersion, Note, ShortlistStage } from "@/lib/types";

export default function ProfileDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const resolvedParams = use(params);
  const profileId = resolvedParams.id;

  const [profile, setProfile] = useState<Profile | null>(null);
  const [versions, setVersions] = useState<ProfileVersion[]>([]);
  const [notes, setNotes] = useState<Note[]>([]);
  const [newNoteContent, setNewNoteContent] = useState("");
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<"overview" | "deen" | "career" | "education" | "history" | "notes">("overview");

  useEffect(() => {
    loadProfileDetails();
  }, [profileId]);

  const loadProfileDetails = async () => {
    try {
      setLoading(true);
      const [pData, vData, nData] = await Promise.all([
        api.getProfile(profileId),
        api.getProfileVersions(profileId),
        api.getProfileNotes(profileId),
      ]);
      setProfile(pData);
      setVersions(vData);
      setNotes(nData);
    } catch (err) {
      console.error("Failed to load profile details", err);
    } finally {
      setLoading(false);
    }
  };

  const handleAddNote = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newNoteContent.trim()) return;

    try {
      const created = await api.createNote(profileId, newNoteContent.trim());
      setNotes([created, ...notes]);
      setNewNoteContent("");
    } catch (err) {
      console.error("Failed to add note", err);
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

  const handleShortlist = async (stage: ShortlistStage) => {
    try {
      await api.addToShortlist(profileId, stage);
      alert(`Candidate moved to ${stage}!`);
    } catch (err) {
      console.error("Failed to shortlist", err);
    }
  };

  if (loading) {
    return (
      <div className="py-20 text-center text-sm text-zinc-500">
        Loading profile details...
      </div>
    );
  }

  if (!profile) {
    return (
      <div className="py-20 text-center space-y-3">
        <p className="text-base font-bold text-zinc-800 dark:text-zinc-200">Candidate not found</p>
        <Link href="/search" className="text-xs text-emerald-700 hover:underline">
          Return to Search
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-5xl mx-auto space-y-6 pb-20">
      {/* Back button */}
      <div>
        <Link
          href="/search"
          className="inline-flex items-center space-x-1.5 text-xs font-semibold text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200 transition-colors"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Search Results</span>
        </Link>
      </div>

      {/* Main Candidate Card Header */}
      <div className="bg-white dark:bg-zinc-900 rounded-2xl border border-zinc-200 dark:border-zinc-800 shadow-sm p-6 sm:p-8">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-zinc-100 dark:border-zinc-800 pb-6">
          <div>
            <div className="flex items-center space-x-2.5">
              <h1 className="text-2xl font-extrabold text-zinc-900 dark:text-zinc-100">
                {profile.candidate_code || `Candidate #${profile.id}`}
              </h1>
              <span className="px-2.5 py-0.5 rounded text-xs font-bold uppercase tracking-wider bg-emerald-100 dark:bg-emerald-950/80 text-emerald-800 dark:text-emerald-300">
                {profile.source}
              </span>
              {profile.synthetic && (
                <span className="px-2 py-0.5 rounded text-[10px] font-semibold bg-zinc-100 dark:bg-zinc-800 text-zinc-500">
                  Synthetic Dataset
                </span>
              )}
            </div>

            <div className="mt-2 flex flex-wrap items-center gap-x-3 gap-y-1 text-sm text-zinc-600 dark:text-zinc-400 font-medium">
              <span>{profile.age ? `${profile.age} years` : "Age not stated"}</span>
              <span>•</span>
              <span>{profile.height_display || (profile.height_cm ? `${profile.height_cm} cm` : "Height not stated")}</span>
              <span>•</span>
              <span className="flex items-center gap-1">
                <MapPin className="w-3.5 h-3.5 text-zinc-400" />
                Current: {profile.current_location || "Not stated"}
              </span>
              {profile.permanent_location && (
                <>
                  <span>•</span>
                  <span>Permanent: {profile.permanent_location}</span>
                </>
              )}
            </div>
          </div>

          {/* Quick Actions */}
          <div className="flex items-center space-x-2">
            {profile.profile_url && (
              <a
                href={profile.profile_url}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center space-x-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-700 dark:text-zinc-200 hover:bg-zinc-50 transition-colors"
              >
                <span>Original Source</span>
                <ExternalLink className="w-3.5 h-3.5" />
              </a>
            )}

            <button
              onClick={() => handleShortlist("Shortlisted")}
              className="inline-flex items-center space-x-1.5 px-4 py-2 rounded-xl text-xs font-semibold bg-emerald-700 hover:bg-emerald-800 text-white transition-colors shadow-xs"
            >
              <Bookmark className="w-3.5 h-3.5" />
              <span>Shortlist Candidate</span>
            </button>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex items-center space-x-2 pt-4 border-b border-zinc-100 dark:border-zinc-800 overflow-x-auto text-xs">
          {[
            { id: "overview", label: "Overview" },
            { id: "deen", label: "Deen Indicators" },
            { id: "career", label: "Career & Stability" },
            { id: "education", label: "Education" },
            { id: "history", label: `Version History (${versions.length})` },
            { id: "notes", label: `Private Notes (${notes.length})` },
          ].map((tab) => (
            <button
              key={tab.id}
              onClick={() => setActiveTab(tab.id as any)}
              className={`px-3.5 py-2 font-semibold border-b-2 transition-colors whitespace-nowrap ${
                activeTab === tab.id
                  ? "border-emerald-600 text-emerald-700 dark:text-emerald-400"
                  : "border-transparent text-zinc-500 hover:text-zinc-800 dark:hover:text-zinc-200"
              }`}
            >
              {tab.label}
            </button>
          ))}
        </div>

        {/* Tab Contents */}
        <div className="pt-6">
          {/* OVERVIEW TAB */}
          {activeTab === "overview" && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs">
              <div className="space-y-4">
                <h3 className="font-bold text-sm text-zinc-900 dark:text-zinc-100">Personal Attributes</h3>
                <div className="grid grid-cols-2 gap-3 p-4 rounded-xl bg-zinc-50 dark:bg-zinc-800/40 border border-zinc-100 dark:border-zinc-800">
                  <div>
                    <span className="text-zinc-400 block mb-0.5">Gender</span>
                    <span className="font-semibold text-zinc-800 dark:text-zinc-200 capitalize">{profile.gender}</span>
                  </div>
                  <div>
                    <span className="text-zinc-400 block mb-0.5">Marital Status</span>
                    <span className="font-semibold text-zinc-800 dark:text-zinc-200 capitalize">
                      {profile.marital_status.replace("_", " ")}
                    </span>
                  </div>
                  <div>
                    <span className="text-zinc-400 block mb-0.5">Age</span>
                    <span className="font-semibold text-zinc-800 dark:text-zinc-200">
                      {profile.age ? `${profile.age} years old` : "Not stated"}
                    </span>
                  </div>
                  <div>
                    <span className="text-zinc-400 block mb-0.5">Height</span>
                    <span className="font-semibold text-zinc-800 dark:text-zinc-200">
                      {profile.height_display || (profile.height_cm ? `${profile.height_cm} cm` : "Not stated")}
                    </span>
                  </div>
                </div>

                <h3 className="font-bold text-sm text-zinc-900 dark:text-zinc-100">Location Details</h3>
                <div className="space-y-2 p-4 rounded-xl bg-zinc-50 dark:bg-zinc-800/40 border border-zinc-100 dark:border-zinc-800">
                  <div className="flex justify-between">
                    <span className="text-zinc-400">Current District</span>
                    <span className="font-semibold text-zinc-800 dark:text-zinc-200">{profile.current_location || "Not stated"}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-zinc-400">Permanent District</span>
                    <span className="font-semibold text-zinc-800 dark:text-zinc-200">{profile.permanent_location || "Not stated"}</span>
                  </div>
                </div>
              </div>

              <div className="space-y-4">
                <h3 className="font-bold text-sm text-zinc-900 dark:text-zinc-100">Audit & Ingestion Timestamps</h3>
                <div className="space-y-2 p-4 rounded-xl bg-zinc-50 dark:bg-zinc-800/40 border border-zinc-100 dark:border-zinc-800">
                  <div className="flex justify-between">
                    <span className="text-zinc-400">First Ingested</span>
                    <span className="font-semibold text-zinc-800 dark:text-zinc-200">{new Date(profile.first_seen).toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-zinc-400">Last Seen</span>
                    <span className="font-semibold text-zinc-800 dark:text-zinc-200">{new Date(profile.last_seen).toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-zinc-400">Source Profile ID</span>
                    <span className="font-mono text-zinc-700 dark:text-zinc-300">{profile.source_profile_id}</span>
                  </div>
                </div>

                <div className="p-4 rounded-xl bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200/50 text-emerald-900 dark:text-emerald-300">
                  <h4 className="font-bold mb-1 flex items-center gap-1.5">
                    <ShieldCheck className="w-4 h-4 text-emerald-600" />
                    NikahLens Transparency Philosophy
                  </h4>
                  <p className="text-[11px] leading-relaxed">
                    NikahLens only records statements explicitly made on the source profile. We do not judge character or infer subjective piety or financial status.
                  </p>
                </div>
              </div>
            </div>
          )}

          {/* DEEN TAB */}
          {activeTab === "deen" && (
            <div className="space-y-4 text-xs">
              <p className="text-zinc-500 text-xs">
                Religious statements extracted directly from profile. Each attribute clearly shows whether it was stated and the exact evidence source.
              </p>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {[
                  { label: "Salah / Prayer", attr: profile.deen.salah },
                  { label: "Quran Recitation & Study", attr: profile.deen.quran },
                  { label: "Sunnah Beard", attr: profile.deen.beard },
                  { label: "Islamic Studies & Madrasa", attr: profile.deen.islamic_studies },
                  { label: "Halal Income Priority", attr: profile.deen.halal_income },
                  { label: "Family Religious Environment", attr: profile.deen.religious_environment },
                ].map(({ label, attr }) => (
                  <div
                    key={label}
                    className="p-4 rounded-xl bg-zinc-50 dark:bg-zinc-800/40 border border-zinc-200/80 dark:border-zinc-800 space-y-1.5"
                  >
                    <div className="flex items-center justify-between">
                      <span className="font-bold text-zinc-900 dark:text-zinc-100">{label}</span>
                      <span className={`px-2 py-0.5 rounded text-[10px] font-semibold uppercase ${
                        attr.status === "stated"
                          ? "bg-emerald-100 dark:bg-emerald-950 text-emerald-800 dark:text-emerald-300"
                          : "bg-zinc-200 dark:bg-zinc-700 text-zinc-600 dark:text-zinc-400"
                      }`}>
                        {attr.status}
                      </span>
                    </div>

                    <div className="text-zinc-600 dark:text-zinc-400 text-xs">
                      {attr.raw_text ? (
                        <p className="italic bg-white dark:bg-zinc-900 p-2.5 rounded-lg border border-zinc-100 dark:border-zinc-800 text-zinc-800 dark:text-zinc-200">
                          &quot;{attr.raw_text}&quot;
                        </p>
                      ) : (
                        <p className="text-zinc-400 italic">Not mentioned in profile text.</p>
                      )}
                    </div>

                    <div className="text-[10px] text-zinc-400 flex items-center justify-between pt-1 border-t border-zinc-100 dark:border-zinc-800">
                      <span>Evidence: {attr.evidence_type.replace("_", " ")}</span>
                      <span>Value: {attr.value || "None"}</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* CAREER TAB */}
          {activeTab === "career" && (
            <div className="space-y-4 text-xs">
              <div className="p-4 rounded-xl bg-zinc-50 dark:bg-zinc-800/40 border border-zinc-200/80 dark:border-zinc-800 space-y-3">
                <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                  <div>
                    <span className="text-zinc-400 block mb-0.5">Stated Occupation</span>
                    <span className="font-bold text-zinc-900 dark:text-zinc-100 text-sm">
                      {profile.career.occupation || "Not stated"}
                    </span>
                  </div>
                  <div>
                    <span className="text-zinc-400 block mb-0.5">Category</span>
                    <span className="font-semibold text-zinc-800 dark:text-zinc-200">
                      {profile.career.role_category || "General"}
                    </span>
                  </div>
                  <div>
                    <span className="text-zinc-400 block mb-0.5">Employment Status</span>
                    <span className="font-semibold text-zinc-800 dark:text-zinc-200 capitalize">
                      {profile.career.employment_status.replace("_", " ")}
                    </span>
                  </div>
                </div>

                {profile.career.raw_title && (
                  <div className="pt-2 border-t border-zinc-200/60 dark:border-zinc-700/60">
                    <span className="text-zinc-400 block mb-1">Source Quote / Raw Stated Title:</span>
                    <p className="p-2.5 rounded-lg bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 text-zinc-800 dark:text-zinc-200 italic">
                      &quot;{profile.career.raw_title}&quot;
                    </p>
                  </div>
                )}
              </div>

              {/* Strict Financial Notice */}
              <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/20 text-amber-900 dark:text-amber-200 text-xs space-y-1">
                <h4 className="font-bold flex items-center gap-1.5">
                  <AlertTriangle className="w-4 h-4 text-amber-600" />
                  Financial Status Transparency Warning
                </h4>
                <p>
                  Profession does not equal financial stability (e.g. Software Engineer ≠ financially established).
                  Income or financial capacity cannot be assumed without explicit, independent verification.
                </p>
              </div>
            </div>
          )}

          {/* EDUCATION TAB */}
          {activeTab === "education" && (
            <div className="p-5 rounded-xl bg-zinc-50 dark:bg-zinc-800/40 border border-zinc-200 dark:border-zinc-800 text-xs space-y-4">
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
                <div>
                  <span className="text-zinc-400 block mb-0.5">Degree</span>
                  <span className="font-bold text-sm text-zinc-900 dark:text-zinc-100">
                    {profile.education.degree || "Not stated"}
                  </span>
                </div>
                <div>
                  <span className="text-zinc-400 block mb-0.5">Field of Study</span>
                  <span className="font-semibold text-zinc-800 dark:text-zinc-200">
                    {profile.education.field || "Not stated"}
                  </span>
                </div>
                <div>
                  <span className="text-zinc-400 block mb-0.5">Institution</span>
                  <span className="font-semibold text-zinc-800 dark:text-zinc-200">
                    {profile.education.institution || "Not stated"}
                  </span>
                </div>
              </div>

              {profile.education.raw_text && (
                <div className="pt-3 border-t border-zinc-200 dark:border-zinc-700">
                  <span className="text-zinc-400 block mb-1">Raw Stated Education:</span>
                  <p className="p-2.5 rounded-lg bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 text-zinc-800 dark:text-zinc-200">
                    {profile.education.raw_text}
                  </p>
                </div>
              )}
            </div>
          )}

          {/* HISTORY & VERSIONS TAB */}
          {activeTab === "history" && (
            <div className="space-y-3 text-xs">
              {versions.length === 0 ? (
                <p className="text-zinc-400 py-6 text-center">No profile change history recorded yet.</p>
              ) : (
                versions.map((v) => (
                  <div
                    key={v.id}
                    className="p-3.5 rounded-xl bg-zinc-50 dark:bg-zinc-800/40 border border-zinc-200 dark:border-zinc-800 flex items-start justify-between"
                  >
                    <div>
                      <span className="font-semibold text-zinc-800 dark:text-zinc-200 block">
                        {v.field_name}: {v.change_type}
                      </span>
                      <p className="text-zinc-500 mt-0.5">{v.new_value}</p>
                    </div>
                    <span className="text-[11px] text-zinc-400 flex items-center gap-1">
                      <Calendar className="w-3 h-3" />
                      {new Date(v.recorded_at).toLocaleDateString()}
                    </span>
                  </div>
                ))
              )}
            </div>
          )}

          {/* PRIVATE NOTES TAB */}
          {activeTab === "notes" && (
            <div className="space-y-4 text-xs">
              <form onSubmit={handleAddNote} className="flex gap-2">
                <input
                  type="text"
                  value={newNoteContent}
                  onChange={(e) => setNewNoteContent(e.target.value)}
                  placeholder="Add private personal note (e.g. candidate details, family inquiry...)"
                  className="flex-1 p-2.5 text-xs rounded-xl border border-zinc-300 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 focus:outline-none focus:ring-2 focus:ring-emerald-500/20"
                />
                <button
                  type="submit"
                  disabled={!newNoteContent.trim()}
                  className="px-4 py-2.5 rounded-xl bg-emerald-700 hover:bg-emerald-800 text-white font-semibold flex items-center gap-1.5 transition-colors disabled:opacity-50"
                >
                  <Send className="w-3.5 h-3.5" />
                  <span>Save Note</span>
                </button>
              </form>

              <div className="space-y-2.5">
                {notes.length === 0 ? (
                  <p className="text-zinc-400 py-8 text-center">No private notes for this candidate yet.</p>
                ) : (
                  notes.map((n) => (
                    <div
                      key={n.id}
                      className="p-3.5 rounded-xl bg-zinc-50 dark:bg-zinc-800/40 border border-zinc-200 dark:border-zinc-800 flex items-start justify-between group"
                    >
                      <p className="text-zinc-800 dark:text-zinc-200 whitespace-pre-wrap flex-1">{n.content}</p>
                      <button
                        onClick={() => handleDeleteNote(n.id)}
                        className="opacity-0 group-hover:opacity-100 text-zinc-400 hover:text-rose-600 transition-opacity ml-3"
                        title="Delete note"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  ))
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
