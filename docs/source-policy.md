# NikahLens Source Policy & Adapter Architecture

## 1. Adapter Philosophy

NikahLens interacts with external matrimonial sources exclusively through modular, decoupled **Source Adapters** implementing the `BaseSourceAdapter` interface.

Website-specific scraping or parsing logic is strictly separated from the application and API layers.

---

## 2. Adapter Operating Modes

Each source adapter operates in one of the following modes:

1. **`mock`**: Ingests synthetic, fictitious test profiles. Used for local testing, development, and unit test verification.
2. **`public_api`**: Integrates with official, authorized REST or GraphQL APIs provided by the matrimonial platform.
3. **`manual_import`**: Used when a platform does not provide an automated API or forbids automated web collection in its Terms of Service or `robots.txt`. In this mode, users manually import structured export files (JSON, CSV).
4. **`disabled`**: Adapter is inactive; no searches or queries are executed against it.

---

## 3. Registered Source Adapters

| Adapter Name | Display Name | Default State | Mode | Legal Compliance Status |
| :--- | :--- | :--- | :--- | :--- |
| `mock` | Synthetic Mock Source | **Enabled** | `mock` | 100% synthetic fictitious profiles for algorithm development. |
| `ahlia` | Ahlia Matrimony | Disabled | `manual_import` | Automated scraping is disabled in compliance with Terms of Service. |
| `ordhekdeen` | Ordhek Deen | Disabled | `manual_import` | Robots directives respected; live scraping disabled. |
| `idealnikah` | Ideal Nikah | Disabled | `manual_import` | Operates in manual import mode; no bypass of security mechanisms. |

---

## 4. Implementing a New Source Adapter

To add a new adapter:
1. Create a directory under `services/collectors/<source_name>/`.
2. Implement `adapter.py` subclassing `BaseSourceAdapter`.
3. Provide legal/compliance metadata:
   - `permits_automated_collection`: boolean
   - `terms_compliance_notes`: human-readable explanation
   - `mode`: `mock`, `public_api`, or `manual_import`
4. Register the adapter instance in `services/collectors/__init__.py`.
5. Write unit tests in `tests/test_<source_name>_adapter.py`.
