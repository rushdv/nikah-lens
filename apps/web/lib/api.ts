import {
  Profile,
  SearchResultItem,
  SearchCriteria,
  SearchProfile,
  ShortlistItem,
  ShortlistStage,
  Note,
  SourceStatus,
  ProfileVersion
} from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const url = `${API_BASE}${endpoint}`;
  const res = await fetch(url, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options.headers || {}),
    },
  });

  if (!res.ok) {
    const errorBody = await res.text();
    throw new Error(`API Error ${res.status}: ${errorBody || res.statusText}`);
  }

  return res.json();
}

export const api = {
  // Profiles
  async getProfiles(params: { gender?: string; location?: string; source?: string; query?: string; limit?: number; offset?: number } = {}) {
    const q = new URLSearchParams();
    if (params.gender) q.set("gender", params.gender);
    if (params.location) q.set("location", params.location);
    if (params.source) q.set("source", params.source);
    if (params.query) q.set("query", params.query);
    if (params.limit) q.set("limit", params.limit.toString());
    if (params.offset) q.set("offset", params.offset.toString());
    return request<Profile[]>(`/profiles?${q.toString()}`);
  },

  async getProfile(id: string) {
    return request<Profile>(`/profiles/${id}`);
  },

  async getProfileVersions(id: string) {
    return request<ProfileVersion[]>(`/profiles/${id}/versions`);
  },

  // Search
  async search(params: {
    criteria?: SearchCriteria;
    search_profile_id?: string;
    source_filter?: string;
    limit?: number;
    offset?: number;
    sort_by?: string;
  }) {
    return request<{
      total: number;
      results: SearchResultItem[];
      summary_counts: Record<string, number>;
    }>("/search", {
      method: "POST",
      body: JSON.stringify(params),
    });
  },

  // Search Profiles
  async getSearchProfiles() {
    return request<SearchProfile[]>("/search-profiles");
  },

  async getSearchProfile(id: string) {
    return request<SearchProfile>(`/search-profiles/${id}`);
  },

  async createSearchProfile(data: { name: string; description?: string; is_active?: boolean; criteria: SearchCriteria }) {
    return request<SearchProfile>("/search-profiles", {
      method: "POST",
      body: JSON.stringify(data),
    });
  },

  async updateSearchProfile(id: string, data: Partial<SearchProfile>) {
    return request<SearchProfile>(`/search-profiles/${id}`, {
      method: "PATCH",
      body: JSON.stringify(data),
    });
  },

  async deleteSearchProfile(id: string) {
    return request<{ message: string }>(`/search-profiles/${id}`, {
      method: "DELETE",
    });
  },

  // Shortlists
  async getShortlists(stage?: string) {
    const q = stage ? `?stage=${encodeURIComponent(stage)}` : "";
    return request<ShortlistItem[]>(`/shortlists${q}`);
  },

  async addToShortlist(profile_id: string, stage: ShortlistStage = "Shortlisted", notes?: string) {
    return request<ShortlistItem>("/shortlists", {
      method: "POST",
      body: JSON.stringify({ profile_id, stage, notes }),
    });
  },

  async updateShortlist(id: string, stage?: ShortlistStage, notes?: string) {
    return request<ShortlistItem>(`/shortlists/${id}`, {
      method: "PATCH",
      body: JSON.stringify({ stage, notes }),
    });
  },

  async deleteShortlist(id: string) {
    return request<{ message: string }>(`/shortlists/${id}`, {
      method: "DELETE",
    });
  },

  // Notes
  async getProfileNotes(profileId: string) {
    return request<Note[]>(`/profiles/${profileId}/notes`);
  },

  async createNote(profile_id: string, content: string) {
    return request<Note>("/notes", {
      method: "POST",
      body: JSON.stringify({ profile_id, content }),
    });
  },

  async deleteNote(id: string) {
    return request<{ message: string }>(`/notes/${id}`, {
      method: "DELETE",
    });
  },

  // Sources
  async getSources() {
    return request<SourceStatus[]>("/sources");
  },

  async toggleSource(name: string, enabled: boolean) {
    return request<SourceStatus>(`/sources/${name}/toggle`, {
      method: "PATCH",
      body: JSON.stringify({ enabled }),
    });
  },

  // Duplicates & System
  async getDuplicates() {
    return request<{
      total_duplicate_pairs: number;
      pairs: Array<{
        profile_a: Profile;
        profile_b: Profile;
        confidence: string;
        reasons: string[];
      }>;
    }>("/duplicates");
  },

  async resetSeed() {
    return request<{ status: string; message: string }>("/system/reset-seed", {
      method: "POST",
    });
  },
};
