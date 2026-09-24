"use client";

import { useEffect, useState } from "react";
import { 
  Database, 
  ShieldCheck, 
  AlertTriangle, 
  CheckCircle, 
  XCircle, 
  Info,
  RefreshCw,
  Lock
} from "lucide-react";
import { api } from "@/lib/api";
import { SourceStatus } from "@/lib/types";

export default function SourcesPage() {
  const [sources, setSources] = useState<SourceStatus[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadSources();
  }, []);

  const loadSources = async () => {
    try {
      setLoading(true);
      const data = await api.getSources();
      setSources(data);
    } catch (err) {
      console.error("Failed to load sources", err);
    } finally {
      setLoading(false);
    }
  };

  const handleToggle = async (sourceName: string, currentEnabled: boolean) => {
    try {
      const updated = await api.toggleSource(sourceName, !currentEnabled);
      setSources(sources.map((s) => (s.name === sourceName ? updated : s)));
    } catch (err) {
      console.error("Failed to toggle source", err);
    }
  };

  return (
    <div className="space-y-6 pb-20">
      <div>
        <h1 className="text-2xl font-extrabold text-zinc-900 dark:text-zinc-100 flex items-center gap-2">
          <Database className="w-6 h-6 text-emerald-600" />
          <span>Matrimonial Source Adapters & Policy</span>
        </h1>
        <p className="text-xs text-zinc-500 mt-1">
          Independent source connectors. Each source strictly complies with access rules, robots.txt, and privacy terms.
        </p>
      </div>

      {/* Policy Disclaimer Banner */}
      <div className="p-5 rounded-2xl bg-zinc-900 text-white border border-zinc-800 shadow-xs flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
        <div className="flex items-start space-x-3.5">
          <div className="w-9 h-9 rounded-xl bg-emerald-500/20 text-emerald-400 flex items-center justify-center shrink-0">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm font-bold">Strict Ethical Data Collection Standard</h3>
            <p className="text-xs text-zinc-300 mt-0.5 leading-relaxed max-w-3xl">
              NikahLens does not bypass CAPTCHAs, paywalls, or login controls. We do not collect private contact numbers or private guardian details. If a source does not permit automated collection, the connector operates in manual import/export mode only.
            </p>
          </div>
        </div>
      </div>

      {/* Sources Grid */}
      {loading ? (
        <div className="py-20 text-center">
          <RefreshCw className="w-6 h-6 animate-spin mx-auto text-emerald-600 mb-2" />
          <p className="text-xs text-zinc-400">Loading source adapters...</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
          {sources.map((s) => (
            <div
              key={s.name}
              className="p-6 rounded-2xl bg-white dark:bg-zinc-900 border border-zinc-200 dark:border-zinc-800 shadow-xs flex flex-col justify-between space-y-4"
            >
              <div>
                <div className="flex items-start justify-between">
                  <div>
                    <div className="flex items-center space-x-2">
                      <h3 className="text-base font-bold text-zinc-900 dark:text-zinc-100">
                        {s.display_name}
                      </h3>
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider ${
                        s.enabled
                          ? "bg-emerald-100 dark:bg-emerald-950 text-emerald-800 dark:text-emerald-300"
                          : "bg-zinc-100 dark:bg-zinc-800 text-zinc-500"
                      }`}>
                        {s.enabled ? "Active" : "Disabled"}
                      </span>
                    </div>
                    <span className="text-[11px] text-zinc-400 mt-0.5 block font-mono">
                      Mode: {s.mode.replace("_", " ")}
                    </span>
                  </div>

                  {/* Toggle switch */}
                  <button
                    onClick={() => handleToggle(s.name, s.enabled)}
                    className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                      s.enabled ? "bg-emerald-600" : "bg-zinc-300 dark:bg-zinc-700"
                    }`}
                  >
                    <span
                      className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                        s.enabled ? "translate-x-6" : "translate-x-1"
                      }`}
                    />
                  </button>
                </div>

                <div className="mt-4 p-3 rounded-xl bg-zinc-50 dark:bg-zinc-800/40 border border-zinc-100 dark:border-zinc-800 text-xs text-zinc-600 dark:text-zinc-400 space-y-2">
                  <div className="flex items-start gap-1.5">
                    <Info className="w-3.5 h-3.5 text-zinc-400 shrink-0 mt-0.5" />
                    <p className="leading-relaxed text-[11px]">{s.terms_compliance_notes}</p>
                  </div>
                </div>
              </div>

              {/* Footer */}
              <div className="pt-3 border-t border-zinc-100 dark:border-zinc-800 flex items-center justify-between text-xs text-zinc-500">
                <span>Ingested Profiles: <strong className="text-zinc-900 dark:text-zinc-100">{s.profile_count}</strong></span>
                <span className="text-[11px]">
                  {s.permits_automated_collection ? "Automated Sync Permitted" : "Manual / Authorized Only"}
                </span>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
