"""
Deterministic Matching and Filtering Engine.
Evaluates matrimonial profiles against user-defined criteria.
Adheres to strict transparency:
- Separates REQUIRED, PREFERRED, OPTIONAL, and EXCLUDED criteria.
- Categorizes results into: Strong Match, Potential Match, Needs Review, Hard Requirement Not Met.
- Clearly details WHY a profile appeared and WHAT needs human review.
- Never generates misleading single compatibility scores.
"""

from typing import List, Tuple, Optional
from packages.schemas.profile import ProfileResponse
from packages.schemas.search import (
    SearchCriteria, MatchStatus, SearchResultItem, RequirementPriority
)
from services.normalizer.height import format_height_display


class MatchEngine:
    """
    Evaluates profiles against search criteria deterministically.
    """

    @classmethod
    def evaluate(cls, profile: ProfileResponse, criteria: SearchCriteria) -> SearchResultItem:
        why_matched: List[str] = []
        needs_review: List[str] = []
        hard_failures: List[str] = []

        # 0. Gender Check
        if criteria.gender and profile.gender:
            if profile.gender.lower() != criteria.gender.lower():
                hard_failures.append(f"Gender '{profile.gender}' does not match required '{criteria.gender}'")

        # 1. Age Evaluation
        cls._evaluate_age(profile, criteria, why_matched, needs_review, hard_failures)

        # 2. Height Evaluation
        cls._evaluate_height(profile, criteria, why_matched, needs_review, hard_failures)

        # 3. Location Evaluation
        cls._evaluate_location(profile, criteria, why_matched, needs_review, hard_failures)

        # 4. Marital Status Evaluation
        cls._evaluate_marital_status(profile, criteria, why_matched, needs_review, hard_failures)

        # 5. Deen Evaluation
        cls._evaluate_deen(profile, criteria, why_matched, needs_review, hard_failures)

        # 6. Career Evaluation
        cls._evaluate_career(profile, criteria, why_matched, needs_review, hard_failures)

        # Determine overall match status
        if hard_failures:
            status = MatchStatus.HARD_REQUIREMENT_NOT_MET
        elif len(needs_review) >= 3 or any("Missing required" in r for r in needs_review):
            status = MatchStatus.NEEDS_REVIEW
        elif len(why_matched) >= 4 and len(needs_review) <= 1:
            status = MatchStatus.STRONG_MATCH
        else:
            status = MatchStatus.POTENTIAL_MATCH

        return SearchResultItem(
            profile=profile,
            match_status=status,
            why_matched=why_matched,
            needs_review=needs_review,
            hard_failures=hard_failures
        )

    @classmethod
    def _evaluate_age(
        cls, profile: ProfileResponse, criteria: SearchCriteria,
        why: List[str], review: List[str], failures: List[str]
    ):
        if profile.age is None:
            if criteria.age.priority == RequirementPriority.REQUIRED:
                if criteria.missing_data_disqualifies:
                    failures.append("Age is not stated in profile (required)")
                else:
                    review.append("Age is not stated in profile")
            return

        min_age = criteria.age.min or 18
        max_age = criteria.age.max or 100

        if min_age <= profile.age <= max_age:
            why.append(f"Age ({profile.age}) matches preferred range ({min_age}–{max_age})")
        else:
            msg = f"Age ({profile.age}) is outside preferred range ({min_age}–{max_age})"
            if criteria.age.priority == RequirementPriority.REQUIRED:
                failures.append(msg)
            else:
                review.append(msg)

    @classmethod
    def _evaluate_height(
        cls, profile: ProfileResponse, criteria: SearchCriteria,
        why: List[str], review: List[str], failures: List[str]
    ):
        min_cm = criteria.height.min_cm
        if min_cm is None:
            return

        min_display = format_height_display(min_cm) or f"{min_cm} cm"

        if profile.height_cm is None:
            if criteria.height.priority == RequirementPriority.REQUIRED:
                if criteria.missing_data_disqualifies:
                    failures.append(f"Height is not stated in profile (minimum required: {min_display})")
                else:
                    review.append(f"Height is not stated in profile (minimum preferred: {min_display})")
            return

        prof_display = profile.height_display or format_height_display(profile.height_cm) or f"{profile.height_cm} cm"

        if profile.height_cm >= min_cm:
            why.append(f"Height ({prof_display}) meets minimum requirement ({min_display})")
        else:
            msg = f"Height ({prof_display}) is below minimum requirement ({min_display})"
            if criteria.height.priority == RequirementPriority.REQUIRED:
                failures.append(msg)
            else:
                review.append(msg)

    @classmethod
    def _evaluate_location(
        cls, profile: ProfileResponse, criteria: SearchCriteria,
        why: List[str], review: List[str], failures: List[str]
    ):
        if not criteria.locations:
            return

        target_names = [loc.name.lower() for loc in criteria.locations]
        has_required = any(loc.priority == RequirementPriority.REQUIRED for loc in criteria.locations)

        matched_loc = None
        cand_locs = [loc.lower() for loc in [profile.current_location, profile.permanent_location] if loc]

        for cand_loc in cand_locs:
            for loc in criteria.locations:
                if loc.name.lower() in cand_loc or cand_loc in loc.name.lower():
                    matched_loc = loc
                    break
            if matched_loc:
                break

        if matched_loc:
            why.append(f"Location ({profile.current_location or profile.permanent_location}) matches target region ({matched_loc.name})")
        else:
            curr = profile.current_location or profile.permanent_location or "Unknown"
            if has_required:
                failures.append(f"Location '{curr}' is not in required locations")
            else:
                review.append(f"Location '{curr}' is outside initial preferred regions")

    @classmethod
    def _evaluate_marital_status(
        cls, profile: ProfileResponse, criteria: SearchCriteria,
        why: List[str], review: List[str], failures: List[str]
    ):
        if not criteria.marital_status.values:
            return

        status = profile.marital_status.lower() if profile.marital_status else None
        allowed = [v.lower() for v in criteria.marital_status.values]

        if not status:
            review.append("Marital status not explicitly specified")
            return

        if status in allowed:
            formatted_status = status.replace("_", " ").title()
            why.append(f"Marital status is {formatted_status}")
        else:
            msg = f"Marital status '{status}' not in preferred list"
            if criteria.marital_status.priority == RequirementPriority.REQUIRED:
                failures.append(msg)
            else:
                review.append(msg)

    @classmethod
    def _evaluate_deen(
        cls, profile: ProfileResponse, criteria: SearchCriteria,
        why: List[str], review: List[str], failures: List[str]
    ):
        deen = profile.deen

        # Salah
        if criteria.deen.require_salah:
            if deen.salah.is_present():
                why.append("Profile states regular performance of Salah")
            else:
                review.append("Regular Salah is not explicitly stated in profile")

        # Quran
        if criteria.deen.require_quran:
            if deen.quran.is_present():
                why.append(f"Quran practice stated: {deen.quran.value}")
            else:
                review.append("Quran recitation or memorization not stated")
        elif deen.quran.is_present():
            why.append("Quran recitation/memorization is mentioned")

        # Beard
        if criteria.deen.prefer_beard:
            if deen.beard.is_present() and deen.beard.value == "sunnah_beard_stated":
                why.append("Maintaining a Sunnah beard is explicitly stated")
            elif deen.beard.is_present() and deen.beard.value == "clean_shaven_stated":
                review.append("Profile states clean shaven")
            else:
                review.append("Beard is not mentioned in profile")

        # Other positive indicators
        if deen.halal_income.is_present():
            why.append("Halal income consciousness is stated")
        if deen.religious_environment.is_present():
            why.append("Practicing Islamic family environment mentioned")
        if deen.islamic_studies.is_present():
            why.append("Islamic studies / madrasa background stated")

    @classmethod
    def _evaluate_career(
        cls, profile: ProfileResponse, criteria: SearchCriteria,
        why: List[str], review: List[str], failures: List[str]
    ):
        career = profile.career

        if criteria.career.require_occupation_stated:
            if career.occupation_stated and career.occupation:
                why.append(f"Current occupation is stated: {career.occupation}")
            else:
                review.append("Occupation is not stated in profile")

        # Check employment status
        if career.employment_status.value in criteria.career.preferred_statuses:
            why.append(f"Employment category ({career.employment_status.value.replace('_', ' ').title()}) matches preference")
        elif career.employment_status.value != "unspecified":
            review.append(f"Employment category is {career.employment_status.value.replace('_', ' ')}")

        # Factual transparency on financial stability
        if not career.financial_stability_verified:
            review.append("Financial stability cannot be inferred or verified from available information")
