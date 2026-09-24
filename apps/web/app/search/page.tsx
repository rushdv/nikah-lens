"use client";

import { useEffect, useState } from "react";
import { 
  Search as SearchIcon, 
  Filter, 
  Sliders, 
  RotateCcw, 
  CheckCircle2, 
  HelpCircle, 
  XCircle, 
  Sparkles,
  RefreshCw,
  MapPin
} from "lucide-react";
import { api } from "@/lib/api";
import { 
  SearchResultItem, 
  SearchCriteria, 
  SearchProfile, 
  RequirementPriority, 
  MatchStatus,
  ShortlistStage 
} from "@/lib/types";
import { ResultCard } from "@/components/ResultCard";
import { NoteModal } from "@/components/NoteModal";

const DEFAULT_CRITERIA: SearchCriteria = {
  gender: "male",
  age: { min: 22, max: 29, priority: "REQUIRED" },
  height: { min_cm: 165.1, priority: "REQUIRED" }, // 5'5"
  locations: [
    { name: "Rangpur", priority: "PREFERRED" },
    { name: "Dinajpur", priority: "PREFERRED" },
    { name: "Kurigram", priority: "PREFERRED" },
    { name: "Lalmonirhat", priority: "PREFERRED" },
    { name: "Nilphamari", priority: "PREFERRED" },
    { name: "Gaibandha", priority: "PREFERRED" },
    { name: "Thakurgaon", priority: "PREFERRED" },
    { name: "Panchagarh", priority: "PREFERRED" },
  ],
  marital_status: { values: ["never_married"], priority: "REQUIRED" },
  deen: {
    priority: "very_high",
    require_salah: true,
    require_quran: false,
    prefer_beard: true,
    prefer_islamic_studies: false,
  },
  career: {
    priority: "high",
    require_occupation_stated: true,
    preferred_statuses: ["employed", "business_owner", "professional", "entrepreneur", "freelancer"],
  },
  missing_data_disqualifies: false,
};

const NORTHERN_DISTRICTS = [
  "Rangpur", "Dinajpur", "Kurigram", "Lalmonirhat",
  "Nilphamari", "Gaibandha", "Thakurgaon", "Panchagarh", "Dhaka", "Bogura"
];

export default function SearchPage() {
  const [criteria, setCriteria] = useState<SearchCriteria>(DEFAULT_CRITERIA);
  const [searchProfiles, setSearchProfiles] = useState<SearchProfile[]>([]);
  const [selectedSearchProfileId, setSelectedSearchProfileId] = useState<string>("");
  
  const [results, setResults] = useState<SearchResultItem[]>([]);
  const [summaryCounts, setSummaryCounts] = useState<Record<string, number>>({});
  const [activeTab, setActiveTab] = useState<string>("ALL");
  const [sortBy, setSortBy] = useState<string>("match_status");
  const [loading, setLoading] = useState(false);

  // Note Modal
  const [activeNoteModal, setActiveNoteModal] = useState<{
    isOpen: boolean;
    profileId: string;
    candidateCode: string;
  }>({
    isOpen: false,
    profileId: "",
    candidateCode: "",
  });

  // Load saved search profiles on mount
  useEffect(() => {
    loadSavedProfiles();
  }, []);

  const loadSavedProfiles = async () => {
    try {
      const sps = await api.getSearchProfiles();
      setSearchProfiles(sps);
      const active = sps.find((p) => p.is_active);
      if (active) {
        setSelectedSearchProfileId(active.id);
        setCriteria(active.criteria);
      }
    } catch (err) {
      console.error("Failed to load search profiles", err);
    }
  };

  const handleSelectSavedProfile = (profileId: string) => {
    setSelectedSearchProfileId(profileId);
    const target = searchProfiles.find((p) => p.id === profileId);
    if (target) {
      setCriteria(target.criteria);
    }
  };

  // Execute search whenever criteria or sort changes
  useEffect(() => {
    executeSearch();
  }, [criteria, sortBy]);

  const executeSearch = async () => {
    try {
      setLoading(true);
      const data = await api.search({
        criteria,
        sort_by: sortBy,
        limit: 100,
      });
      setResults(data.results);
      setSummaryCounts(data.summary_counts);
    } catch (err) {
      console.error("Search failed", err);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleLocation = (locName: string) => {
    const exists = criteria.locations.some((l) => l.name.toLowerCase() === locName.toLowerCase());
    if (exists) {
      setCriteria({
        ...criteria,
        locations: criteria.locations.filter((l) => l.name.toLowerCase() !== locName.toLowerCase()),
      });
    } else {
      setCriteria({
        ...criteria,
        locations: [...criteria.locations, { name: locName, priority: "PREFERRED" }],
      });
    }
  };

  const handleUpdateShortlist = async (profileId: string, stage: ShortlistStage) => {
    try {
      await api.addToShortlist(profileId, stage);
    } catch (err) {
      console.error("Failed to update shortlist", err);
    }
  };

  // Filter results by active category tab
  const filteredResults = results.filter((item) => {
    if (activeTab === "ALL") return true;
    return item.match_status === activeTab;
  });

  return (
    <div className="space-y-6 pb-16">
      {/* Page Title & Profile Switcher */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-zinc-900 dark:text-zinc-100 flex items-center gap-2">
            <span>Matrimonial Search & Filter</span>
          </h1>
          <p className="text-xs text-zinc-500 mt-0.5">
            Deterministic matching engine with transparent justifications and information gap detection.
          </p>
        </div>

        <div className="flex items-center space-x-2">
          <label className="text-xs text-zinc-500 font-medium">Saved Preset:</label>
          <select
            value={selectedSearchProfileId}
            onChange={(e) => handleSelectSavedProfile(e.target.value)}
            className="text-xs font-semibold px-3 py-1.5 rounded-lg border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-800 dark:text-zinc-200 focus:outline-none focus:ring-2 focus:ring-emerald-500/20"
          >
            <option value="">Custom Criteria</option>
            {searchProfiles.map((sp) => (
              <option key={sp.id} value={sp.id}>
                {sp.name} {sp.is_active ? "(Active)" : ""}
              </option>
            ))}
          </select>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 items-start">
        {/* Left Filter Panel */}
        <div className="lg:col-span-1 bg-white dark:bg-zinc-900 p-5 rounded-2xl border border-zinc-200 dark:border-zinc-800 shadow-xs space-y-5">
          <div className="flex items-center justify-between border-b border-zinc-100 dark:border-zinc-800 pb-3">
            <span className="text-xs font-bold uppercase tracking-wider text-zinc-700 dark:text-zinc-300 flex items-center gap-1.5">
              <Filter className="w-3.5 h-3.5 text-emerald-600" />
              Hard & Soft Filters
            </span>
            <button
              onClick={() => setCriteria(DEFAULT_CRITERIA)}
              className="text-[11px] text-zinc-400 hover:text-emerald-700 flex items-center gap-1"
            >
              <RotateCcw className="w-3 h-3" />
              <span>Reset</span>
            </button>
          </div>

          {/* Age Filter */}
          <div className="space-y-2">
            <label className="text-xs font-bold text-zinc-700 dark:text-zinc-300 block">
              Age Range ({criteria.age.min || 18} – {criteria.age.max || 40} years)
            </label>
            <div className="grid grid-cols-2 gap-2">
              <div>
                <span className="text-[10px] text-zinc-400">Min Age</span>
                <input
                  type="number"
                  value={criteria.age.min ?? 22}
                  onChange={(e) =>
                    setCriteria({
                      ...criteria,
                      age: { ...criteria.age, min: parseInt(e.target.value) || 18 },
                    })
                  }
                  className="w-full text-xs p-2 rounded-lg border border-zinc-200 dark:border-zinc-700 bg-zinc-50 dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100"
                />
              </div>
              <div>
                <span className="text-[10px] text-zinc-400">Max Age</span>
                <input
                  type="number"
                  value={criteria.age.max ?? 29}
                  onChange={(e) =>
                    setCriteria({
                      ...criteria,
                      age: { ...criteria.age, max: parseInt(e.target.value) || 40 },
                    })
                  }
                  className="w-full text-xs p-2 rounded-lg border border-zinc-200 dark:border-zinc-700 bg-zinc-50 dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100"
                />
              </div>
            </div>
          </div>

          {/* Height Minimum */}
          <div className="space-y-2">
            <label className="text-xs font-bold text-zinc-700 dark:text-zinc-300 block">
              Minimum Height (≥ 5&apos;5&quot; / 165 cm)
            </label>
            <div className="flex gap-1.5 flex-wrap">
              {[
                { label: "5'4\" (162 cm)", cm: 162.6 },
                { label: "5'5\" (165 cm)", cm: 165.1 },
                { label: "5'6\" (168 cm)", cm: 167.6 },
                { label: "5'7\" (170 cm)", cm: 170.2 },
              ].map((h) => (
                <button
                  key={h.cm}
                  type="button"
                  onClick={() =>
                    setCriteria({
                      ...criteria,
                      height: { ...criteria.height, min_cm: h.cm },
                    })
                  }
                  className={`text-[11px] px-2.5 py-1 rounded-md font-medium border transition-colors ${
                    criteria.height.min_cm === h.cm
                      ? "bg-emerald-700 text-white border-emerald-700"
                      : "bg-zinc-50 dark:bg-zinc-800 border-zinc-200 dark:border-zinc-700 text-zinc-700 dark:text-zinc-300"
                  }`}
                >
                  {h.label}
                </button>
              ))}
            </div>
          </div>

          {/* Target Locations */}
          <div className="space-y-2">
            <label className="text-xs font-bold text-zinc-700 dark:text-zinc-300 block">
              Target Districts (Rangpur & Northern Focus)
            </label>
            <div className="flex flex-wrap gap-1.5">
              {NORTHERN_DISTRICTS.map((loc) => {
                const isSelected = criteria.locations.some(
                  (l) => l.name.toLowerCase() === loc.toLowerCase()
                );
                return (
                  <button
                    key={loc}
                    type="button"
                    onClick={() => handleToggleLocation(loc)}
                    className={`text-[11px] px-2.5 py-1 rounded-full font-medium border transition-colors ${
                      isSelected
                        ? "bg-emerald-100 dark:bg-emerald-950 text-emerald-800 dark:text-emerald-300 border-emerald-300/40"
                        : "bg-zinc-50 dark:bg-zinc-800 border-zinc-200 dark:border-zinc-700 text-zinc-500 hover:text-zinc-800"
                    }`}
                  >
                    {loc}
                  </button>
                );
              })}
            </div>
          </div>

          {/* Deen Indicators */}
          <div className="space-y-2 pt-2 border-t border-zinc-100 dark:border-zinc-800">
            <label className="text-xs font-bold text-zinc-700 dark:text-zinc-300 block">
              Deen Stated Indicators
            </label>
            <div className="space-y-1.5 text-xs text-zinc-700 dark:text-zinc-300">
              <label className="flex items-center space-x-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={criteria.deen.require_salah}
                  onChange={(e) =>
                    setCriteria({
                      ...criteria,
                      deen: { ...criteria.deen, require_salah: e.target.checked },
                    })
                  }
                  className="rounded text-emerald-600 focus:ring-emerald-500"
                />
                <span>Must state regular Salah</span>
              </label>

              <label className="flex items-center space-x-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={criteria.deen.prefer_beard}
                  onChange={(e) =>
                    setCriteria({
                      ...criteria,
                      deen: { ...criteria.deen, prefer_beard: e.target.checked },
                    })
                  }
                  className="rounded text-emerald-600 focus:ring-emerald-500"
                />
                <span>Prefer stated Sunnah beard</span>
              </label>

              <label className="flex items-center space-x-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={criteria.deen.require_quran}
                  onChange={(e) =>
                    setCriteria({
                      ...criteria,
                      deen: { ...criteria.deen, require_quran: e.target.checked },
                    })
                  }
                  className="rounded text-emerald-600 focus:ring-emerald-500"
                />
                <span>Prioritize Quran recitation</span>
              </label>
            </div>
          </div>

          {/* Career & Information Gaps */}
          <div className="space-y-2 pt-2 border-t border-zinc-100 dark:border-zinc-800">
            <label className="text-xs font-bold text-zinc-700 dark:text-zinc-300 block">
              Career & Data Handling
            </label>
            <div className="space-y-1.5 text-xs text-zinc-700 dark:text-zinc-300">
              <label className="flex items-center space-x-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={criteria.career.require_occupation_stated}
                  onChange={(e) =>
                    setCriteria({
                      ...criteria,
                      career: { ...criteria.career, require_occupation_stated: e.target.checked },
                    })
                  }
                  className="rounded text-emerald-600 focus:ring-emerald-500"
                />
                <span>Require stated occupation</span>
              </label>

              <label className="flex items-center space-x-2 cursor-pointer">
                <input
                  type="checkbox"
                  checked={criteria.missing_data_disqualifies}
                  onChange={(e) =>
                    setCriteria({
                      ...criteria,
                      missing_data_disqualifies: e.target.checked,
                    })
                  }
                  className="rounded text-emerald-600 focus:ring-emerald-500"
                />
                <span>Missing info disqualifies</span>
              </label>
            </div>
          </div>
        </div>

        {/* Right Results Panel */}
        <div className="lg:col-span-3 space-y-4">
          {/* Category Tabs & Sort */}
          <div className="bg-white dark:bg-zinc-900 p-2 rounded-xl border border-zinc-200 dark:border-zinc-800 flex flex-wrap items-center justify-between gap-2 shadow-xs">
            <div className="flex items-center space-x-1 overflow-x-auto text-xs">
              {[
                { id: "ALL", label: "All Results", count: results.length },
                { id: "Strong Match", label: "Strong Match", count: summaryCounts["Strong Match"] || 0 },
                { id: "Potential Match", label: "Potential Match", count: summaryCounts["Potential Match"] || 0 },
                { id: "Needs Review", label: "Needs Review", count: summaryCounts["Needs Review"] || 0 },
                { id: "Hard Requirement Not Met", label: "Hard Req Failed", count: summaryCounts["Hard Requirement Not Met"] || 0 },
              ].map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`px-3 py-1.5 rounded-lg font-semibold transition-colors flex items-center gap-1.5 ${
                    activeTab === tab.id
                      ? "bg-zinc-900 text-white dark:bg-zinc-100 dark:text-zinc-900 shadow-xs"
                      : "text-zinc-600 dark:text-zinc-400 hover:bg-zinc-100 dark:hover:bg-zinc-800"
                  }`}
                >
                  <span>{tab.label}</span>
                  <span className={`px-1.5 py-0.2 rounded-full text-[10px] ${
                    activeTab === tab.id
                      ? "bg-white/20 dark:bg-black/20 text-white dark:text-black"
                      : "bg-zinc-200 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400"
                  }`}>
                    {tab.count}
                  </span>
                </button>
              ))}
            </div>

            <div className="flex items-center space-x-2 text-xs">
              <span className="text-zinc-400">Sort:</span>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value)}
                className="text-xs p-1.5 rounded-md border border-zinc-200 dark:border-zinc-700 bg-white dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300 focus:outline-none"
              >
                <option value="match_status">Match Quality</option>
                <option value="age">Age (Youngest First)</option>
                <option value="height">Height (Tallest First)</option>
              </select>
            </div>
          </div>

          {/* Results Grid */}
          {loading ? (
            <div className="text-center py-20 bg-white dark:bg-zinc-900 rounded-2xl border border-zinc-200 dark:border-zinc-800">
              <RefreshCw className="w-6 h-6 animate-spin mx-auto text-emerald-600 mb-2" />
              <p className="text-sm text-zinc-500">Evaluating profiles against criteria...</p>
            </div>
          ) : filteredResults.length === 0 ? (
            <div className="text-center py-20 bg-white dark:bg-zinc-900 rounded-2xl border border-zinc-200 dark:border-zinc-800">
              <p className="text-base font-bold text-zinc-800 dark:text-zinc-200">No candidates match this tab</p>
              <p className="text-xs text-zinc-400 mt-1">Try selecting &apos;All Results&apos; or relaxing some hard requirements.</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {filteredResults.map((item) => (
                <ResultCard
                  key={item.profile.id}
                  item={item}
                  onOpenNotes={(id, code) =>
                    setActiveNoteModal({ isOpen: true, profileId: id, candidateCode: code })
                  }
                  onUpdateShortlist={handleUpdateShortlist}
                />
              ))}
            </div>
          )}
        </div>
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
