# kooperativa

Official Python SDK for the [Kooperativa](https://kooperativa.io) API. Enrich and search professional profiles and companies, track hiring signals and job changes, and manage webhook monitors.

## Installation

Install directly from GitHub:

```bash
pip install git+https://github.com/kooperativa-team/kooperativa-python.git
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
- `enrich_realtime(linkedin_url=None, username=None)` — from the live source, **metered**, see below
- `check(linkedin_url=None, username=None, id=None)`
- `search(**filters)` — e.g. `title`, `location`, `industry`, `seniority`
- `bulk_enrich(profiles)` — up to 100 identifiers per call
- `colleagues(id, page=1, per_page=25)`
- `similar(id, page=1, per_page=25)`
- `job_changes(days=90, company_id=None, page=1, per_page=25)`

**Company** (`kooperativa.company`)
- `enrich(linkedin_url=None, username=None, company_id=None, id=None)`
- `enrich_realtime(linkedin_url=None, username=None)` — from the live source, **metered**, see below
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

## Realtime enrichment and billing

Everything above is included in the flat license, with no per-request charge, except the two `enrich_realtime` methods. Those read from the live source rather than from our data lake, and are metered at **$0.001 per call** on top of the license, which is still required.

Three things are worth knowing before you call them in a loop:

- **A miss still costs.** A call is billed whenever the live source actually answered, so a `404` costs the same as a hit, because the lookup happened either way. Only a `503`, meaning we could not reach the source at all, is not billed.
- **A billed call can land in your `except`.** A `404` raises `KooperativaApiError`, so a call you handle as a failure has still been charged. If you are counting spend, count calls, not successes.
- **There is no cache in front of them.** Calling `enrich_realtime` twice for the same person bills twice. The result is written back to the data lake though, so a following plain `enrich` is free and returns what the realtime call just returned.

Reach for `enrich` first: it is included, and roughly 4x faster. Use `enrich_realtime` when the record is missing from the lake, or when its `fetched_at` is not recent enough for what you are doing.

Full parameter reference: [docs.kooperativa.io](https://docs.kooperativa.io).

## License

MIT
