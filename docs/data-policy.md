# NikahLens Data & Ethics Policy

NikahLens is built upon strict principles of privacy, respect, Islamic ethics, and legal compliance.

## 1. Absolute Prohibitions

NikahLens will **NEVER**:

1. **Bypass Access Controls**: No bypassing of login systems, CAPTCHAs, paywalls, or authentication gates.
2. **Scrape Private Profiles**: No collecting data from profiles marked private, restricted, or hidden behind family approval walls.
3. **Collect Contact Information Unnecessarily**: No automatic harvesting of personal phone numbers, email addresses, or guardian contact details.
4. **Download Private Photographs**: No automated image scraping or facial recognition.
5. **Circumvent Anti-Bot Protections**: No browser spoofing or evasion of rate limiters.
6. **Automated Communication**: No automated messaging, automated contact, or bot interactions with candidates.
7. **Make Subjective Character Judgments**: No algorithmic labeling of individuals as "pious", "good", "impious", or "wealthy".

---

## 2. Permitted Data Ingestion

The system ingests and processes only:
- **Publicly accessible information** where automated collection is legally and technically permitted by the relevant platform.
- **Manual structured imports** provided directly by the user (JSON/CSV exports).
- **Official APIs and documented endpoints** with explicit authorization.
- **Synthetic mock datasets** for local development and algorithm testing.

The canonical original source URL or profile reference is always retained for provenance.

---

## 3. Deen Information Standards

- **Multi-Attribute Representation**: Deen is never reduced to a single boolean (`deen = true`).
- **Factual Distinctions**: Every religious attribute records:
  - `status`: `stated`, `not_stated`, `unknown`
  - `evidence_type`: `self_reported`, `verified`, `unknown`
  - `raw_text`: Quote snippet from the source profile.
- **Objective Phrasing**: The UI reports facts rather than appraisals:
  - *"Profile states that he regularly performs salah."* (Correct)
  - *"Candidate is very pious."* (Strictly Prohibited)

---

## 4. Career and Financial Stability Standards

- **No Inferred Wealth**: Profession does not equal financial stability.
  - `Software Engineer ≠ financially established`
  - `Businessman ≠ wealthy`
- **Separation of Stated vs Verified**:
  - `occupation_stated`
  - `career_stability_stated`
  - `income_stated`
  - `financial_stability_verified` (Always `false` unless official verification exists)

---

## 5. Local Private Notes Protection

Personal candidate notes and review tags are stored exclusively in the user's private database. They are never sent to external source platforms or telemetry servers.
