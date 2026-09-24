export type EvidenceType = "self_reported" | "verified" | "unknown";
export type StatedStatus = "stated" | "not_stated" | "unknown";

export interface DeenAttribute {
  value?: string | null;
  status: StatedStatus;
  evidence_type: EvidenceType;
  raw_text?: string | null;
}

export interface DeenProfile {
  salah: DeenAttribute;
  quran: DeenAttribute;
  islamic_studies: DeenAttribute;
  islamic_practice: DeenAttribute;
  halal_income: DeenAttribute;
  beard: DeenAttribute;
  religious_environment: DeenAttribute;
  self_description: DeenAttribute;
  other_notes?: string | null;
}

export type CareerStatus =
  | "student"
  | "employed"
  | "business_owner"
  | "professional"
  | "freelancer"
  | "entrepreneur"
  | "job_seeker"
  | "unemployed"
  | "unspecified";

export interface CareerInformation {
  occupation?: string | null;
  role_category?: string | null;
  industry?: string | null;
  employment_status: CareerStatus;
  career_stage?: string | null;
  raw_title?: string | null;
  occupation_stated: boolean;
  career_stability_stated: boolean;
  income_stated: boolean;
  financial_stability_verified: boolean;
}

export interface EducationInformation {
  degree?: string | null;
  field?: string | null;
  institution?: string | null;
  raw_text?: string | null;
}

export interface Profile {
  id: string;
  source: string;
  source_profile_id: string;
  candidate_code?: string | null;
  profile_url?: string | null;
  gender: string;
  age?: number | null;
  height_cm?: number | null;
  height_display?: string | null;
  marital_status: string;
  current_location?: string | null;
  permanent_location?: string | null;
  education: EducationInformation;
  career: CareerInformation;
  deen: DeenProfile;
  synthetic: boolean;
  raw_data?: Record<string, any> | null;
  first_seen: string;
  last_seen: string;
  last_updated?: string | null;
}

export type RequirementPriority = "REQUIRED" | "PREFERRED" | "OPTIONAL" | "EXCLUDED";
export type MatchStatus = "Strong Match" | "Potential Match" | "Needs Review" | "Hard Requirement Not Met";

export interface DuplicateSummary {
  is_duplicate: boolean;
  confidence?: "High" | "Medium" | "Low" | null;
  matched_profile_id?: string | null;
  matched_source?: string | null;
  reasons: string[];
}

export interface SearchResultItem {
  profile: Profile;
  match_status: MatchStatus;
  why_matched: string[];
  needs_review: string[];
  hard_failures: string[];
  duplicate_info?: DuplicateSummary | null;
}

export interface LocationItem {
  name: string;
  priority: RequirementPriority;
}

export interface SearchCriteria {
  gender: string;
  age: {
    min?: number | null;
    max?: number | null;
    priority: RequirementPriority;
  };
  height: {
    min_cm?: number | null;
    priority: RequirementPriority;
  };
  locations: LocationItem[];
  marital_status: {
    values: string[];
    priority: RequirementPriority;
  };
  deen: {
    priority: string;
    require_salah: boolean;
    require_quran: boolean;
    prefer_beard: boolean;
    prefer_islamic_studies: boolean;
  };
  career: {
    priority: string;
    require_occupation_stated: boolean;
    preferred_statuses: string[];
  };
  missing_data_disqualifies: boolean;
}

export interface SearchProfile {
  id: string;
  name: string;
  description?: string | null;
  is_active: boolean;
  criteria: SearchCriteria;
  created_at: string;
  updated_at?: string | null;
}

export type ShortlistStage =
  | "New"
  | "Interesting"
  | "Shortlisted"
  | "Need Review"
  | "Contact Later"
  | "Archived";

export interface ShortlistItem {
  id: string;
  profile_id: string;
  stage: ShortlistStage;
  notes?: string | null;
  created_at: string;
  updated_at?: string | null;
  profile?: Profile | null;
}

export interface Note {
  id: string;
  profile_id: string;
  content: string;
  created_at: string;
  updated_at?: string | null;
}

export interface SourceStatus {
  name: string;
  display_name: string;
  enabled: boolean;
  mode: string;
  description: string;
  terms_compliance_notes: string;
  permits_automated_collection: boolean;
  profile_count: number;
  last_synced_at?: string | null;
}

export interface ProfileVersion {
  id: string;
  profile_id: string;
  change_type: string;
  field_name: string;
  old_value?: string | null;
  new_value?: string | null;
  recorded_at: string;
}
