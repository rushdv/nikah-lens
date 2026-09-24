"use client";

import { useState } from "react";
import { 
  Settings as SettingsIcon, 
  RotateCcw, 
  ShieldCheck, 
  Database, 
  Server, 
  Check, 
  ExternalLink 
} from "lucide-react";
import { api } from "@/lib/api";

export default function SettingsPage() {
  const [resetting, setResetting] = useState(false);
  const [resetMessage, setResetMessage] = useState("");

  const handleResetData = async () => {
    if (!confirm("This will reload the initial synthetic mock dataset (35 profiles) and restore default search profiles. Continue?")) {
      return;
    }

    try {
      setResetting(true);
      setResetMessage("");
      const res = await api.resetSeed();
      setResetMessage(res.message);
    } catch (err: any) {
      setResetMessage(`Failed: ${err.message}`);
    } finally {
      setResetting(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 pb-20">
      <div>
        <h1 className="text-2xl font-extrabold text-zinc-900 dark:text-zinc-100 flex items-center gap-2">
          <SettingsIcon className="w-6 h-6 text-emerald-600" />
          <span>System Settings & Preferences</span>
        </h1>
        <p className="text-xs text-zinc-500 mt-1">
          Configure engine parameters, manage synthetic test data, and review privacy controls.
        </p>
      </div>

      {/* Dataset & Seed Controls */}
      <div className="bg-white dark:bg-zinc-900 rounded-2xl border border-zinc-200 dark:border-zinc-800 p-6 shadow-xs space-y-4">
        <div>
          <h2 className="text-base font-bold text-zinc-900 dark:text-zinc-100 flex items-center gap-2">
            <RotateCcw className="w-4 h-4 text-emerald-600" />
            <span>Synthetic Dataset Management</span>
          </h2>
          <p className="text-xs text-zinc-500 mt-0.5">
            Reset and seed the 35 synthetic matrimonial profiles covering Rangpur, northern districts, duplicate test pairs, and edge cases.
          </p>
        </div>

        <div className="pt-2 flex items-center gap-4">
          <button
            onClick={handleResetData}
            disabled={resetting}
            className="px-4 py-2 rounded-xl text-xs font-semibold bg-emerald-700 hover:bg-emerald-800 text-white transition-colors disabled:opacity-50 flex items-center gap-1.5"
          >
            <span>{resetting ? "Resetting & Seeding..." : "Reload Synthetic Mock Dataset"}</span>
          </button>

          {resetMessage && (
            <span className="text-xs font-semibold text-emerald-700 dark:text-emerald-400 flex items-center gap-1">
              <Check className="w-4 h-4" />
              <span>{resetMessage}</span>
            </span>
          )}
        </div>
      </div>

      {/* Engine & Database Status */}
      <div className="bg-white dark:bg-zinc-900 rounded-2xl border border-zinc-200 dark:border-zinc-800 p-6 shadow-xs space-y-4">
        <div>
          <h2 className="text-base font-bold text-zinc-900 dark:text-zinc-100 flex items-center gap-2">
            <Server className="w-4 h-4 text-emerald-600" />
            <span>Architecture & Environment</span>
          </h2>
          <p className="text-xs text-zinc-500 mt-0.5">
            Current runtime connection parameters.
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs">
          <div className="p-3.5 rounded-xl bg-zinc-50 dark:bg-zinc-800/40 border border-zinc-100 dark:border-zinc-800">
            <span className="text-zinc-400 block mb-1">Backend API Target</span>
            <span className="font-mono font-medium text-zinc-800 dark:text-zinc-200">
              {process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1"}
            </span>
          </div>

          <div className="p-3.5 rounded-xl bg-zinc-50 dark:bg-zinc-800/40 border border-zinc-100 dark:border-zinc-800">
            <span className="text-zinc-400 block mb-1">Database Dialect</span>
            <span className="font-mono font-medium text-zinc-800 dark:text-zinc-200">
              PostgreSQL (Docker Compose) / SQLite (Fallback Dev)
            </span>
          </div>
        </div>
      </div>

      {/* Privacy Standards Card */}
      <div className="p-6 rounded-2xl bg-emerald-50/50 dark:bg-emerald-950/20 border border-emerald-500/30 space-y-3 text-xs text-emerald-950 dark:text-emerald-200">
        <h3 className="text-sm font-bold flex items-center gap-2">
          <ShieldCheck className="w-4 h-4 text-emerald-600 dark:text-emerald-400" />
          <span>NikahLens Ethical Rules Summary</span>
        </h3>
        <ul className="space-y-1.5 list-disc pl-4 text-emerald-900/80 dark:text-emerald-300/80 leading-relaxed">
          <li><strong>No Automated Contact:</strong> NikahLens never messages candidates or makes contact automatically.</li>
          <li><strong>No Circumvention:</strong> Never bypasses logins, CAPTCHAs, paywalls, or rate limiters.</li>
          <li><strong>Zero Opaque Scores:</strong> No fake 87% compatibility scores; transparent why-matched and gaps only.</li>
          <li><strong>Private Notes:</strong> Notes are stored in your local database only and are never transmitted externally.</li>
        </ul>
      </div>
    </div>
  );
}
