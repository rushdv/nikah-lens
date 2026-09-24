"""
Duplicate Detection Service.
Detects potential duplicate matrimonial profiles across sources based on public attributes.
Never asserts definitive identity; provides confidence scores and transparent matching reasons.
"""

from typing import List, Tuple, Optional, Dict
from packages.schemas.profile import ProfileResponse
from packages.schemas.search import DuplicateSummary


class DuplicateDetector:
    """
    Compares profiles using multi-attribute heuristic signals.
    """

    @classmethod
    def compare_pair(cls, a: ProfileResponse, b: ProfileResponse) -> DuplicateSummary:
        """
        Compares two profiles and returns duplicate assessment.
        """
        if a.id == b.id:
            return DuplicateSummary(is_duplicate=False)

        score = 0
        reasons: List[str] = []

        # 1. Gender check
        if a.gender and b.gender and a.gender.lower() != b.gender.lower():
            return DuplicateSummary(is_duplicate=False)

        # 2. Age check
        if a.age is not None and b.age is not None:
            diff = abs(a.age - b.age)
            if diff == 0:
                score += 3
                reasons.append(f"Identical age ({a.age})")
            elif diff == 1:
                score += 1
                reasons.append(f"Similar age ({a.age} vs {b.age})")
            else:
                # Age discrepancy > 2 years makes duplicate unlikely
                score -= 4

        # 3. Height check
        if a.height_cm is not None and b.height_cm is not None:
            h_diff = abs(a.height_cm - b.height_cm)
            if h_diff <= 1.0:
                score += 3
                reasons.append(f"Matching height ({a.height_display or a.height_cm} cm)")
            elif h_diff <= 3.0:
                score += 1
                reasons.append(f"Very close height ({a.height_display} vs {b.height_display})")
            else:
                score -= 3

        # 4. Location check
        a_locs = {loc.lower() for loc in [a.current_location, a.permanent_location] if loc}
        b_locs = {loc.lower() for loc in [b.current_location, b.permanent_location] if loc}
        common_locs = a_locs.intersection(b_locs)
        if common_locs:
            score += 3
            reasons.append(f"Same district ({', '.join(sorted(common_locs)).title()})")

        # 5. Education check
        if a.education.field and b.education.field:
            if a.education.field.lower() == b.education.field.lower():
                score += 3
                reasons.append(f"Same study field ({a.education.field})")
        if a.education.degree and b.education.degree:
            if a.education.degree.lower() == b.education.degree.lower():
                score += 1
                reasons.append(f"Same degree ({a.education.degree})")

        # 6. Profession check
        if a.career.occupation and b.career.occupation:
            if a.career.occupation.lower() == b.career.occupation.lower():
                score += 3
                reasons.append(f"Identical occupation ({a.career.occupation})")

        # 7. Marital status check
        if a.marital_status and b.marital_status:
            if a.marital_status.lower() == b.marital_status.lower():
                score += 1

        # Evaluate score threshold
        if score >= 10:
            return DuplicateSummary(
                is_duplicate=True,
                confidence="High",
                matched_profile_id=b.id,
                matched_source=b.source,
                reasons=reasons
            )
        elif score >= 7:
            return DuplicateSummary(
                is_duplicate=True,
                confidence="Medium",
                matched_profile_id=b.id,
                matched_source=b.source,
                reasons=reasons
            )
        elif score >= 5:
            return DuplicateSummary(
                is_duplicate=True,
                confidence="Low",
                matched_profile_id=b.id,
                matched_source=b.source,
                reasons=reasons
            )

        return DuplicateSummary(is_duplicate=False)

    @classmethod
    def find_duplicates_in_dataset(cls, profiles: List[ProfileResponse]) -> Dict[str, DuplicateSummary]:
        """
        Runs duplicate detection across a dataset and returns mapping from profile_id to its best duplicate match.
        """
        results: Dict[str, DuplicateSummary] = {}
        n = len(profiles)

        for i in range(n):
            best_summary: Optional[DuplicateSummary] = None
            p1 = profiles[i]
            for j in range(n):
                if i == j:
                    continue
                p2 = profiles[j]
                summary = cls.compare_pair(p1, p2)
                if summary.is_duplicate:
                    if best_summary is None or (summary.confidence == "High" and best_summary.confidence != "High"):
                        best_summary = summary

            if best_summary:
                results[p1.id] = best_summary

        return results
