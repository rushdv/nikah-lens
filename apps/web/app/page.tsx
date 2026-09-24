"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { 
  Users, 
  Sparkles, 
  Bookmark, 
  HelpCircle, 
  Database, 
  ArrowRight, 
  Search, 
  ShieldAlert, 
  Sliders, 
  Compass,
  CheckCircle2,
  RefreshCw
} from "lucide-react";
import { api } from "@/lib/api";
import { Profile, SearchResultItem, ShortlistItem, SourceStatus, ShortlistStage } from "@/lib/types";
import { ResultCard } from "@/components/ResultCard";
import { NoteModal } from "@/components/NoteModal";

export default function Dashboard() {
  const [stats, setStats] = useState({
    totalProfiles: 0,
    newProfiles: 0,
    shortlisted: 0,
    needsReview: 0,
    sourcesCount: 0,
  });
  const [recentResults, setRecentResults] = useState<SearchResultItem[]>([]);
  const [duplicateCount, setDuplicateCount] = useState(0);
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

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const [profiles, shortlists, sources, searchData, duplicates] = await Promise.all([
        api.getProfiles({ limit: 100 }),
        api.getShortlists(),
        api.getSources(),
        api.search({ limit: 6 }),
        api.getDuplicates(),
      ]);

      const needsReviewCount = searchData.summary_counts["Needs Review"] || 0;

      setStats({
        totalProfiles: profiles.length,
        newProfiles: profiles.filter((p) => p.synthetic).length,
        shortlisted: shortlists.length,
        needsReview: needsReviewCount,
        sourcesCount: sources.filter((s) => s.enabled).length,
      });

      setRecentResults(searchData.results);
      setDuplicateCount(duplicates.total_duplicate_pairs);
    } catch (err) {
      console.error("Failed to load dashboard data", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboardData();
  }, []);

  const handleUpdateShortlist = async (profileId: string, stage: ShortlistStage) => {
    try {
      await api.addToShortlist(profileId, stage);
      loadDashboardData();
    } catch (err) {
      console.error("Failed to update shortlist", err);
    }
  };

  return (
    <div className="space-y-8 pb-12">
      {/* Hero / Header */}
      <div className="relative rounded-2xl bg-gradient-to-r from-emerald-900 via-teal-900 to-slate-900 text-white p-8 md:p-10 shadow-lg overflow-hidden">
        <div className="absolute right-0 top-0 translate-x-12 -translate-y-8 opacity-10 pointer-events-none">
          <Compass className="w-96 h-96" />
        </div>

        <div className="relative z-10 max-w-2xl">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/20 text-emerald-200 border border-emerald-400/30 mb-4">
            <Sparkles className="w-3.5 h-3.5 text-emerald-300" />
            <span>Deterministic • Transparent • Privacy-First</span>
          </div>

          <h1 className="text-3xl md:text-4xl font-extrabold tracking-tight">
            Discover Matrimonial Profiles with Complete Transparency
          </h1>
          <p className="mt-3 text-emerald-100/80 text-sm md:text-base leading-relaxed">
            Personal discovery engine with transparent match reasoning, structured multi-attribute deen & career indicators, and zero opaque compatibility scores.
          </p>

          <div className="mt-6 flex flex-wrap gap-3">
            <Link
              href="/search"
              className="inline-flex items-center space-x-2 px-5 py-2.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-zinc-950 font-semibold text-sm transition-all shadow-md"
            >
              <Search className="w-4 h-4" />
              <span>Open Search & Match</span>
            </Link>
            <Link
              href="/shortlist"
              className="inline-flex items-center space-x-2 px-5 py-2.5 rounded-xl bg-white/10 hover:bg-white/20 text-white font-medium text-sm transition-colors border border-white/15"
            >
              <Bookmark className="w-4 h-4" />
              <span>View Shortlist ({stats.shortlisted})</span>
            </Link>
          </div>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-2 md:grid-cols-5 gap-4">
        <div className="bg-white dark:bg-zinc-900 p-5 rounded-xl border border-zinc-200 dark:border-zinc-800 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-zinc-500 uppercase tracking-wider">Profiles Found</span>
            <Users className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
          </div>
          <p className="mt-2 text-2xl font-bold text-zinc-900 dark:text-zinc-100">
            {loading ? "..." : stats.totalProfiles}
          </p>
          <span className="text-[11px] text-zinc-400 mt-1 block">In local repository</span>
        </div>

        <div className="bg-white dark:bg-zinc-900 p-5 rounded-xl border border-zinc-200 dark:border-zinc-800 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-zinc-500 uppercase tracking-wider">Active Ingestion</span>
            <Sparkles className="w-4 h-4 text-teal-600 dark:text-teal-400" />
          </div>
          <p className="mt-2 text-2xl font-bold text-zinc-900 dark:text-zinc-100">
            {loading ? "..." : stats.newProfiles}
          </p>
          <span className="text-[11px] text-zinc-400 mt-1 block">Synthetic candidates</span>
        </div>

        <div className="bg-white dark:bg-zinc-900 p-5 rounded-xl border border-zinc-200 dark:border-zinc-800 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-zinc-500 uppercase tracking-wider">Shortlisted</span>
            <Bookmark className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
          </div>
          <p className="mt-2 text-2xl font-bold text-zinc-900 dark:text-zinc-100">
            {loading ? "..." : stats.shortlisted}
          </p>
          <span className="text-[11px] text-zinc-400 mt-1 block">Under review</span>
        </div>

        <div className="bg-white dark:bg-zinc-900 p-5 rounded-xl border border-zinc-200 dark:border-zinc-800 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-zinc-500 uppercase tracking-wider">Needs Review</span>
            <HelpCircle className="w-4 h-4 text-amber-600 dark:text-amber-400" />
          </div>
          <p className="mt-2 text-2xl font-bold text-zinc-900 dark:text-zinc-100">
            {loading ? "..." : stats.needsReview}
          </p>
          <span className="text-[11px] text-zinc-400 mt-1 block">Information gaps</span>
        </div>

        <div className="bg-white dark:bg-zinc-900 p-5 rounded-xl border border-zinc-200 dark:border-zinc-800 shadow-xs">
          <div className="flex items-center justify-between">
            <span className="text-xs font-medium text-zinc-500 uppercase tracking-wider">Active Sources</span>
            <Database className="w-4 h-4 text-zinc-600 dark:text-zinc-400" />
          </div>
          <p className="mt-2 text-2xl font-bold text-zinc-900 dark:text-zinc-100">
            {loading ? "..." : `${stats.sourcesCount} Active`}
          </p>
          <span className="text-[11px] text-zinc-400 mt-1 block">Legal/terms enforced</span>
        </div>
      </div>

      {/* Duplicate Alert Banner if duplicate candidates exist */}
      {duplicateCount > 0 && (
        <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-between text-xs">
          <div className="flex items-center space-x-3">
            <div className="w-8 h-8 rounded-lg bg-amber-500/20 flex items-center justify-center text-amber-700 dark:text-amber-300">
              <ShieldAlert className="w-4 h-4" />
            </div>
            <div>
              <p className="font-bold text-amber-900 dark:text-amber-200">
                {duplicateCount} Potential Duplicate Profile Pair(s) Detected
              </p>
              <p className="text-amber-700/80 dark:text-amber-400">
                Candidates with identical age, height, district, or occupation across simulated sources.
              </p>
            </div>
          </div>

          <Link
            href="/search"
            className="px-3.5 py-1.5 rounded-lg bg-amber-600/20 hover:bg-amber-600/30 text-amber-900 dark:text-amber-100 font-semibold transition-colors"
          >
            Review Duplicates
          </Link>
        </div>
      )}

      {/* Featured Search Profile Quick Info */}
      <div className="p-6 rounded-2xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 shadow-xs">
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center space-x-2">
              <span className="px-2.5 py-0.5 rounded-full text-xs font-bold uppercase tracking-wider bg-emerald-100 dark:bg-emerald-950/80 text-emerald-800 dark:text-emerald-300">
                Active Search Profile
              </span>
              <h2 className="text-lg font-bold text-zinc-900 dark:text-zinc-100">
                Primary Search (Rangpur & Northern Region)
              </h2>
            </div>
            <p className="mt-1 text-xs text-zinc-500 max-w-2xl">
              Targeting: Male • Age 22–29 • Height ≥ 5&apos;5&quot; (165.1 cm) • Rangpur Division (Dinajpur, Kurigram, Lalmonirhat, Nilphamari, Gaibandha, Thakurgaon, Panchagarh) • Regular Salah required • Career stated.
            </p>
          </div>

          <div className="flex items-center space-x-2 shrink-0">
            <Link
              href="/search-profiles"
              className="inline-flex items-center space-x-1.5 px-3.5 py-2 rounded-xl text-xs font-semibold bg-zinc-100 dark:bg-zinc-800 hover:bg-zinc-200 text-zinc-700 dark:text-zinc-300 transition-colors"
            >
              <Sliders className="w-3.5 h-3.5" />
              <span>Manage Profiles</span>
            </Link>
            <Link
              href="/search"
              className="inline-flex items-center space-x-1.5 px-4 py-2 rounded-xl text-xs font-semibold bg-emerald-700 hover:bg-emerald-800 text-white transition-colors"
            >
              <Search className="w-3.5 h-3.5" />
              <span>Run Match Filter</span>
            </Link>
          </div>
        </div>
      </div>

      {/* Top Matching Candidates Section */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="text-xl font-bold text-zinc-900 dark:text-zinc-100">
              Evaluated Candidates
            </h2>
            <p className="text-xs text-zinc-500">
              Deterministic results evaluated against your search criteria with full reasoning breakdown.
            </p>
          </div>

          <Link
            href="/search"
            className="text-xs font-semibold text-emerald-700 dark:text-emerald-400 hover:underline flex items-center gap-1"
          >
            <span>View All Candidates</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </Link>
        </div>

        {loading ? (
          <div className="text-center py-16 bg-white dark:bg-zinc-900 rounded-2xl border border-zinc-200 dark:border-zinc-800">
            <RefreshCw className="w-6 h-6 animate-spin mx-auto text-emerald-600 mb-2" />
            <p className="text-sm text-zinc-500">Loading candidates and evaluating criteria...</p>
          </div>
        ) : recentResults.length === 0 ? (
          <div className="text-center py-16 bg-white dark:bg-zinc-900 rounded-2xl border border-zinc-200 dark:border-zinc-800">
            <p className="text-sm font-semibold text-zinc-700 dark:text-zinc-300">No candidates available</p>
            <p className="text-xs text-zinc-400 mt-1">Please ensure synthetic data is seeded in Settings.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {recentResults.map((item) => (
              <ResultCard
                key={item.profile.id}
                item={item}
                onOpenNotes={(id, code) => setActiveNoteModal({ isOpen: true, profileId: id, candidateCode: code })}
                onUpdateShortlist={handleUpdateShortlist}
              />
            ))}
          </div>
        )}
      </div>

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
