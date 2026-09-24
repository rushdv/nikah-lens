"use client";

import Link from "next/link";
import { useState } from "react";
import { 
  CheckCircle2, 
  HelpCircle, 
  XCircle, 
  ExternalLink, 
  Bookmark, 
  FileText, 
  AlertTriangle,
  MapPin,
  GraduationCap,
  Briefcase,
  ChevronRight
} from "lucide-react";
import { SearchResultItem, ShortlistStage } from "@/lib/types";

interface ResultCardProps {
  item: SearchResultItem;
  onOpenNotes?: (profileId: string, candidateCode: string) => void;
  onUpdateShortlist?: (profileId: string, stage: ShortlistStage) => void;
}

export function ResultCard({ item, onOpenNotes, onUpdateShortlist }: ResultCardProps) {
  const { profile, match_status, why_matched, needs_review, hard_failures, duplicate_info } = item;
  const [shortlistMenuOpen, setShortlistMenuOpen] = useState(false);

  // Status badge styling
  const statusStyles: Record<string, { bg: string; text: string; border: string; label: string }> = {
    "Strong Match": {
      bg: "bg-emerald-50 dark:bg-emerald-950/50",
      text: "text-emerald-800 dark:text-emerald-300",
      border: "border-emerald-200 dark:border-emerald-800/40",
      label: "Strong Match",
    },
    "Potential Match": {
      bg: "bg-teal-50 dark:bg-teal-950/50",
      text: "text-teal-800 dark:text-teal-300",
      border: "border-teal-200 dark:border-teal-800/40",
      label: "Potential Match",
    },
    "Needs Review": {
      bg: "bg-amber-50 dark:bg-amber-950/50",
      text: "text-amber-800 dark:text-amber-300",
      border: "border-amber-200 dark:border-amber-800/40",
      label: "Needs Review",
    },
    "Hard Requirement Not Met": {
      bg: "bg-rose-50 dark:bg-rose-950/50",
      text: "text-rose-800 dark:text-rose-300",
      border: "border-rose-200 dark:border-rose-800/40",
      label: "Hard Requirement Not Met",
    },
  };

  const currentStyle = statusStyles[match_status] || statusStyles["Needs Review"];

  return (
    <div className="bg-white dark:bg-zinc-900 rounded-xl border border-zinc-200 dark:border-zinc-800 shadow-sm hover:shadow-md transition-shadow overflow-hidden flex flex-col">
      {/* Top Banner: Duplicate Alert if present */}
      {duplicate_info && duplicate_info.is_duplicate && (
        <div className="bg-amber-500/10 border-b border-amber-500/20 px-4 py-2 flex items-center justify-between text-xs text-amber-800 dark:text-amber-300">
          <div className="flex items-center space-x-1.5">
            <AlertTriangle className="w-3.5 h-3.5 text-amber-600 dark:text-amber-400 shrink-0" />
            <span className="font-semibold">Possible duplicate profile ({duplicate_info.confidence} confidence)</span>
          </div>
          <span className="text-[11px] text-amber-700 dark:text-amber-400">
            Cross-listed with {duplicate_info.matched_source?.toUpperCase()}
          </span>
        </div>
      )}

      {/* Header */}
      <div className="p-5 pb-4 border-b border-zinc-100 dark:border-zinc-800/60">
        <div className="flex items-start justify-between">
          <div>
            <div className="flex items-center space-x-2">
              <Link 
                href={`/profiles/${profile.id}`}
                className="text-base font-bold text-zinc-900 dark:text-zinc-100 hover:text-emerald-700 dark:hover:text-emerald-400 transition-colors flex items-center gap-1 group"
              >
                <span>{profile.candidate_code || `Candidate #${profile.id.slice(0, 6)}`}</span>
                <ChevronRight className="w-4 h-4 text-zinc-400 group-hover:translate-x-0.5 transition-transform" />
              </Link>
              <span className="px-2 py-0.5 rounded text-[11px] font-semibold tracking-wider uppercase bg-zinc-100 dark:bg-zinc-800 text-zinc-600 dark:text-zinc-400">
                {profile.source}
              </span>
            </div>

            <div className="mt-1 flex flex-wrap items-center gap-x-2 gap-y-1 text-sm text-zinc-600 dark:text-zinc-400 font-medium">
              <span>{profile.age ? `${profile.age} years` : "Age not stated"}</span>
              <span>•</span>
              <span>{profile.height_display || (profile.height_cm ? `${profile.height_cm} cm` : "Height not stated")}</span>
              <span>•</span>
              <span className="flex items-center gap-1">
                <MapPin className="w-3.5 h-3.5 text-zinc-400" />
                {profile.current_location || "Location not stated"}
                {profile.permanent_location && profile.permanent_location !== profile.current_location && (
                  <span className="text-zinc-400 text-xs">({profile.permanent_location})</span>
                )}
              </span>
            </div>
          </div>

          {/* Match Status Badge */}
          <span className={`px-2.5 py-1 rounded-full text-xs font-semibold border ${currentStyle.bg} ${currentStyle.text} ${currentStyle.border}`}>
            {currentStyle.label}
          </span>
        </div>
      </div>

      {/* Profile Core Attributes */}
      <div className="px-5 py-3.5 grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs border-b border-zinc-100 dark:border-zinc-800/60 bg-zinc-50/50 dark:bg-zinc-900/40">
        <div>
          <span className="text-[11px] font-medium text-zinc-400 uppercase tracking-wider flex items-center gap-1 mb-0.5">
            <GraduationCap className="w-3.5 h-3.5 text-zinc-400" />
            Education
          </span>
          <p className="font-medium text-zinc-800 dark:text-zinc-200">
            {profile.education.degree 
              ? `${profile.education.degree}${profile.education.field ? ` in ${profile.education.field}` : ""}`
              : profile.education.raw_text || "Not stated"}
          </p>
        </div>

        <div>
          <span className="text-[11px] font-medium text-zinc-400 uppercase tracking-wider flex items-center gap-1 mb-0.5">
            <Briefcase className="w-3.5 h-3.5 text-zinc-400" />
            Profession
          </span>
          <p className="font-medium text-zinc-800 dark:text-zinc-200">
            {profile.career.occupation || profile.career.raw_title || "Not stated"}
          </p>
        </div>
      </div>

      {/* Transparent Evaluation Sections */}
      <div className="p-5 py-4 space-y-3.5 flex-1 text-xs">
        {/* Why this profile appeared (Matched points) */}
        {why_matched.length > 0 && (
          <div>
            <h4 className="text-[11px] font-bold text-zinc-700 dark:text-zinc-300 uppercase tracking-wider mb-1.5 flex items-center gap-1.5">
              <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
              Why this profile appeared
            </h4>
            <ul className="space-y-1 pl-4 text-zinc-600 dark:text-zinc-300 list-disc">
              {why_matched.slice(0, 4).map((r, i) => (
                <li key={i}>{r}</li>
              ))}
              {why_matched.length > 4 && (
                <li className="list-none text-[11px] text-zinc-400 font-medium pt-0.5">
                  +{why_matched.length - 4} more positive alignment points
                </li>
              )}
            </ul>
          </div>
        )}

        {/* Hard Failures if any */}
        {hard_failures.length > 0 && (
          <div className="p-2.5 rounded-lg bg-rose-500/10 border border-rose-500/20 text-rose-800 dark:text-rose-300">
            <h4 className="text-[11px] font-bold uppercase tracking-wider mb-1 flex items-center gap-1.5">
              <XCircle className="w-3.5 h-3.5 text-rose-600" />
              Hard Requirement Not Met
            </h4>
            <ul className="space-y-0.5 pl-4 text-[11px] list-disc">
              {hard_failures.map((f, i) => (
                <li key={i}>{f}</li>
              ))}
            </ul>
          </div>
        )}

        {/* Needs Review / Information Gaps */}
        {needs_review.length > 0 && (
          <div>
            <h4 className="text-[11px] font-bold text-amber-700 dark:text-amber-400 uppercase tracking-wider mb-1.5 flex items-center gap-1.5">
              <HelpCircle className="w-3.5 h-3.5 text-amber-600 dark:text-amber-400" />
              Needs Review / Information Gaps
            </h4>
            <ul className="space-y-1 pl-4 text-zinc-500 dark:text-zinc-400 list-disc">
              {needs_review.slice(0, 3).map((g, i) => (
                <li key={i}>{g}</li>
              ))}
            </ul>
          </div>
        )}
      </div>

      {/* Card Footer Actions */}
      <div className="px-5 py-3 border-t border-zinc-100 dark:border-zinc-800/80 bg-zinc-50/70 dark:bg-zinc-900/60 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          {profile.profile_url ? (
            <a
              href={profile.profile_url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center space-x-1 text-xs font-medium text-zinc-600 dark:text-zinc-400 hover:text-emerald-700 dark:hover:text-emerald-400 transition-colors"
            >
              <span>Source URL</span>
              <ExternalLink className="w-3 h-3" />
            </a>
          ) : (
            <span className="text-xs text-zinc-400">Mock Record</span>
          )}
        </div>

        <div className="flex items-center space-x-2">
          {/* Notes Button */}
          <button
            onClick={() => onOpenNotes?.(profile.id, profile.candidate_code || `Candidate #${profile.id}`)}
            className="inline-flex items-center space-x-1 px-2.5 py-1.5 rounded-lg text-xs font-medium text-zinc-700 dark:text-zinc-300 hover:bg-zinc-200 dark:hover:bg-zinc-800 transition-colors"
            title="Private notes for candidate"
          >
            <FileText className="w-3.5 h-3.5 text-zinc-500" />
            <span>Notes</span>
          </button>

          {/* Shortlist Action */}
          <div className="relative">
            <button
              onClick={() => setShortlistMenuOpen(!shortlistMenuOpen)}
              className="inline-flex items-center space-x-1 px-3 py-1.5 rounded-lg text-xs font-medium bg-emerald-700 hover:bg-emerald-800 text-white shadow-xs transition-colors"
            >
              <Bookmark className="w-3.5 h-3.5" />
              <span>Shortlist</span>
            </button>

            {shortlistMenuOpen && (
              <div 
                className="absolute right-0 bottom-full mb-1 w-44 bg-white dark:bg-zinc-800 rounded-lg shadow-lg border border-zinc-200 dark:border-zinc-700 py-1 z-20"
                onMouseLeave={() => setShortlistMenuOpen(false)}
              >
                {(["Shortlisted", "Interesting", "Need Review", "Contact Later", "Archived"] as ShortlistStage[]).map((stage) => (
                  <button
                    key={stage}
                    onClick={() => {
                      onUpdateShortlist?.(profile.id, stage);
                      setShortlistMenuOpen(false);
                    }}
                    className="w-full text-left px-3 py-1.5 text-xs text-zinc-700 dark:text-zinc-200 hover:bg-emerald-50 dark:hover:bg-emerald-950/60 hover:text-emerald-800 dark:hover:text-emerald-300 flex items-center justify-between"
                  >
                    <span>{stage}</span>
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
