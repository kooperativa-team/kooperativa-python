# kooperativa

Official Python SDK for the [Kooperativa](https://kooperativa.io) API. Enrich and search professional profiles and companies, track hiring signals and job changes, and manage webhook monitors.

## Installation

```bash
pip install kooperativa
```

Requires a Kooperativa API key. Get one from your [account dashboard](https://kooperativa.io/api-keys).

## Usage

```python
from kooperativa import Kooperativa

kooperativa = Kooperativa(api_key="kk_live_...")

profile = kooperativa.person.enrich(username="satyanadella")
print(profile["data"]["full_name"], profile["data"]["current_title"])
```

## Methods

**Account**
- `health()` — API liveness probe, no auth required
- `me()` — license status and usage breakdown

**Person** (`kooperativa.person`)
- `enrich(linkedin_url=None, username=None, id=None)`
- `check(linkedin_url=None, username=None, id=None)`
- `search(**filters)` — e.g. `title`, `location`, `industry`, `seniority`
- `bulk_enrich(profiles)` — up to 100 identifiers per call
- `colleagues(id, page=1, per_page=25)`
- `similar(id, page=1, per_page=25)`
- `job_changes(days=90, company_id=None, page=1, per_page=25)`

**Company** (`kooperativa.company`)
- `enrich(linkedin_url=None, username=None, company_id=None, id=None)`
- `check(linkedin_url=None, username=None, company_id=None, id=None)`
- `search(**filters)` — e.g. `country`, `industry`, `min_staff`, `max_staff`
- `current_employees(company_id, page=1, per_page=25)`
- `past_employees(company_id, page=1, per_page=25)`
- `headcount_by_seniority(company_id)`
- `hiring_signals(company_id, days=90, page=1, per_page=25)`

**Monitors** (`kooperativa.monitors`, webhooks)
- `list()`
- `create(type, subject_url, webhook_url, label=None, events=None)`
- `delete(id)`

Every method returns the parsed JSON response. Errors raise `KooperativaApiError` with `.status` and `.code` attributes.

Full parameter reference: [docs.kooperativa.io](https://docs.kooperativa.io).

## License

MIT
