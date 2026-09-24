"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { 
  Sliders, 
  Plus, 
  Check, 
  Trash2, 
  Search, 
  RotateCcw,
  Sparkles,
  MapPin,
  CheckCircle2
} from "lucide-react";
import { api } from "@/lib/api";
import { SearchProfile, SearchCriteria } from "@/lib/types";

export default function SearchProfilesPage() {
  const [profiles, setProfiles] = useState<SearchProfile[]>([]);
  const [loading, setLoading] = useState(true);
  const [isCreating, setIsCreating] = useState(false);
  const [newName, setNewName] = useState("");
  const [newDesc, setNewDesc] = useState("");

  useEffect(() => {
    loadProfiles();
  }, []);

  const loadProfiles = async () => {
    try {
      setLoading(true);
      const data = await api.getSearchProfiles();
      setProfiles(data);
    } catch (err) {
      console.error("Failed to load search profiles", err);
    } finally {
      setLoading(false);
    }
  };

  const handleSetActive = async (profileId: string) => {
    try {
      await api.updateSearchProfile(profileId, { is_active: true });
      setProfiles(profiles.map((p) => ({ ...p, is_active: p.id === profileId })));
    } catch (err) {
      console.error("Failed to activate profile", err);
    }
  };

  const handleDelete = async (profileId: string) => {
    if (!confirm("Are you sure you want to delete this saved search profile?")) return;
    try {
      await api.deleteSearchProfile(profileId);
      setProfiles(profiles.filter((p) => p.id !== profileId));
    } catch (err) {
      console.error("Failed to delete search profile", err);
    }
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newName.trim()) return;

    try {
      const defaultCriteria: SearchCriteria = {
        gender: "male",
        age: { min: 22, max: 29, priority: "REQUIRED" },
        height: { min_cm: 165.1, priority: "REQUIRED" },
        locations: [{ name: "Rangpur", priority: "PREFERRED" }],
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

      const created = await api.createSearchProfile({
        name: newName.trim(),
        description: newDesc.trim() || undefined,
        is_active: false,
        criteria: defaultCriteria,
      });

      setProfiles([created, ...profiles]);
      setNewName("");
      setNewDesc("");
      setIsCreating(false);
    } catch (err) {
      console.error("Failed to create profile", err);
    }
  };

  return (
    <div className="space-y-6 pb-20">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-zinc-900 dark:text-zinc-100 flex items-center gap-2">
            <Sliders className="w-6 h-6 text-emerald-600" />
            <span>Saved Search Profiles</span>
          </h1>
          <p className="text-xs text-zinc-500 mt-1">
            Configure and switch between multiple discovery strategies (e.g. Primary, Rangpur Only, Flexible Age).
          </p>
        </div>

        <button
          onClick={() => setIsCreating(!isCreating)}
          className="inline-flex items-center space-x-1.5 px-4 py-2 rounded-xl text-xs font-semibold bg-emerald-700 hover:bg-emerald-800 text-white transition-colors shadow-xs"
        >
          <Plus className="w-3.5 h-3.5" />
          <span>New Search Profile</span>
        </button>
      </div>

      {/* Create Profile Drawer */}
      {isCreating && (
        <form onSubmit={handleCreate} className="p-6 rounded-2xl bg-white dark:bg-zinc-900 border border-emerald-500/30 shadow-md space-y-4">
          <h3 className="text-sm font-bold text-zinc-900 dark:text-zinc-100">Create Search Profile</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="text-xs font-semibold text-zinc-700 dark:text-zinc-300 block mb-1">
                Profile Name
              </label>
              <input
                type="text"
                value={newName}
                onChange={(e) => setNewName(e.target.value)}
                placeholder="e.g. Rangpur Fast-Track or Flexible Age"
                className="w-full text-xs p-2.5 rounded-xl border border-zinc-200 dark:border-zinc-700 bg-zinc-50 dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 focus:outline-none"
                required
              />
            </div>
            <div>
              <label className="text-xs font-semibold text-zinc-700 dark:text-zinc-300 block mb-1">
                Description / Intent
              </label>
              <input
                type="text"
                value={newDesc}
                onChange={(e) => setNewDesc(e.target.value)}
                placeholder="Brief summary of criteria goals"
                className="w-full text-xs p-2.5 rounded-xl border border-zinc-200 dark:border-zinc-700 bg-zinc-50 dark:bg-zinc-800 text-zinc-900 dark:text-zinc-100 focus:outline-none"
              />
            </div>
          </div>
          <div className="flex justify-end gap-2 pt-2">
            <button
              type="button"
              onClick={() => setIsCreating(false)}
              className="px-3 py-1.5 rounded-lg text-xs font-semibold text-zinc-600 dark:text-zinc-400 hover:bg-zinc-100"
            >
              Cancel
            </button>
            <button
              type="submit"
              className="px-4 py-1.5 rounded-lg text-xs font-semibold bg-emerald-700 hover:bg-emerald-800 text-white"
            >
              Save Profile
            </button>
          </div>
        </form>
      )}

      {/* Profiles Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {profiles.map((p) => {
          const c = p.criteria;
          return (
            <div
              key={p.id}
              className={`p-6 rounded-2xl border transition-all flex flex-col justify-between space-y-4 ${
                p.is_active
                  ? "bg-emerald-50/50 dark:bg-emerald-950/20 border-emerald-500/50 shadow-sm"
                  : "bg-white dark:bg-zinc-900 border-zinc-200 dark:border-zinc-800"
              }`}
            >
              <div>
                <div className="flex items-start justify-between">
                  <div>
                    <div className="flex items-center space-x-2">
                      <h3 className="text-base font-bold text-zinc-900 dark:text-zinc-100">
                        {p.name}
                      </h3>
                      {p.is_active && (
                        <span className="px-2 py-0.5 rounded-full text-[10px] font-bold uppercase tracking-wider bg-emerald-700 text-white">
                          Active Search
                        </span>
                      )}
                    </div>
                    {p.description && (
                      <p className="text-xs text-zinc-500 mt-1 leading-relaxed">
                        {p.description}
                      </p>
                    )}
                  </div>

                  {!p.is_active && (
                    <button
                      onClick={() => handleDelete(p.id)}
                      className="p-1 rounded text-zinc-400 hover:text-rose-600 transition-colors"
                      title="Delete profile"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  )}
                </div>

                {/* Criteria Snippets */}
                <div className="mt-4 pt-3 border-t border-zinc-100 dark:border-zinc-800 text-xs space-y-2">
                  <div className="grid grid-cols-2 gap-2 text-zinc-700 dark:text-zinc-300">
                    <div>
                      <span className="text-[10px] text-zinc-400 uppercase tracking-wider block">Age Range</span>
                      <span className="font-semibold">{c.age.min || 18}–{c.age.max || 40} years ({c.age.priority})</span>
                    </div>
                    <div>
                      <span className="text-[10px] text-zinc-400 uppercase tracking-wider block">Min Height</span>
                      <span className="font-semibold">≥ {c.height.min_cm || 165.1} cm</span>
                    </div>
                  </div>

                  <div>
                    <span className="text-[10px] text-zinc-400 uppercase tracking-wider block mb-1">Locations</span>
                    <div className="flex flex-wrap gap-1">
                      {c.locations.slice(0, 5).map((l, i) => (
                        <span key={i} className="px-2 py-0.5 rounded text-[10px] bg-zinc-100 dark:bg-zinc-800 text-zinc-700 dark:text-zinc-300">
                          {l.name}
                        </span>
                      ))}
                      {c.locations.length > 5 && (
                        <span className="text-[10px] text-zinc-400 font-medium">+{c.locations.length - 5} more</span>
                      )}
                    </div>
                  </div>
                </div>
              </div>

              {/* Actions */}
              <div className="pt-3 border-t border-zinc-100 dark:border-zinc-800 flex items-center justify-between text-xs">
                {p.is_active ? (
                  <span className="flex items-center gap-1 text-emerald-700 dark:text-emerald-400 font-semibold text-xs">
                    <CheckCircle2 className="w-4 h-4" />
                    <span>Currently Active Strategy</span>
                  </span>
                ) : (
                  <button
                    onClick={() => handleSetActive(p.id)}
                    className="px-3.5 py-1.5 rounded-lg font-semibold bg-zinc-100 dark:bg-zinc-800 hover:bg-zinc-200 dark:hover:bg-zinc-700 text-zinc-800 dark:text-zinc-200 transition-colors"
                  >
                    Activate Strategy
                  </button>
                )}

                <Link
                  href="/search"
                  className="inline-flex items-center space-x-1 font-semibold text-emerald-700 dark:text-emerald-400 hover:underline"
                >
                  <Search className="w-3 h-3" />
                  <span>Execute Search</span>
                </Link>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
