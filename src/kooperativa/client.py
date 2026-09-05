"""Official Kooperativa API client."""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from ._http import HttpClient

DEFAULT_BASE_URL = "https://kooperativa.io/api/v1"


class PersonResource:
    """Endpoints under /person and /people."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def enrich(
        self,
        linkedin_url: Optional[str] = None,
        username: Optional[str] = None,
        id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Full profile lookup. Provide exactly one of linkedin_url, username, or id."""
        return self._http.get(
            "/person", {"linkedin_url": linkedin_url, "username": username, "id": id}
        )

    def check(
        self,
        linkedin_url: Optional[str] = None,
        username: Optional[str] = None,
        id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Cheap existence check before a full lookup. Raises KooperativaApiError (404) if not held."""
        return self._http.get(
            "/person/check", {"linkedin_url": linkedin_url, "username": username, "id": id}
        )

    def search(self, **filters: Any) -> Dict[str, Any]:
        """Filtered search across the people data lake.

        Common filters: title, location, industry, seniority, company,
        company_id, city, skills, tenure_min_months, job_changed_after,
        past_company, education, page, per_page. See docs.kooperativa.io.
        """
        return self._http.post("/people/search", filters)

    def bulk_enrich(self, profiles: List[Dict[str, str]]) -> Dict[str, Any]:
        """Enrich up to 100 profiles in one call.

        Each item must have exactly one of id, username, or linkedin_url.
        """
        return self._http.post("/people/bulk-enrich", {"profiles": profiles})

    def colleagues(self, id: str, page: int = 1, per_page: int = 25) -> Dict[str, Any]:
        """Current coworkers of a person (everyone at their current company right now)."""
        return self._http.get("/person/colleagues", {"id": id, "page": page, "per_page": per_page})

    def similar(self, id: str, page: int = 1, per_page: int = 25) -> Dict[str, Any]:
        """Lookalike profiles: same seniority, industry, and country."""
        return self._http.get("/person/similar", {"id": id, "page": page, "per_page": per_page})

    def job_changes(
        self,
        days: int = 90,
        company_id: Optional[str] = None,
        page: int = 1,
        per_page: int = 25,
    ) -> Dict[str, Any]:
        """People who recently started a new job, optionally filtered by previous employer."""
        return self._http.get(
            "/person/job-changes",
            {"days": days, "company_id": company_id, "page": page, "per_page": per_page},
        )


class CompanyResource:
    """Endpoints under /company and /companies."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def enrich(
        self,
        linkedin_url: Optional[str] = None,
        username: Optional[str] = None,
        company_id: Optional[str] = None,
        id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Full company profile lookup. Provide exactly one identifier."""
        return self._http.get(
            "/company",
            {"linkedin_url": linkedin_url, "username": username, "company_id": company_id, "id": id},
        )

    def check(
        self,
        linkedin_url: Optional[str] = None,
        username: Optional[str] = None,
        company_id: Optional[str] = None,
        id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Cheap existence check before a full lookup. Raises KooperativaApiError (404) if not held."""
        return self._http.get(
            "/company/check",
            {"linkedin_url": linkedin_url, "username": username, "company_id": company_id, "id": id},
        )

    def search(self, **filters: Any) -> Dict[str, Any]:
        """Filtered search across the company data lake. At least one filter is required.

        Common filters: query, country, city, industry, min_staff,
        max_staff, page, per_page. See docs.kooperativa.io.
        """
        return self._http.post("/companies/search", filters)

    def current_employees(self, company_id: str, page: int = 1, per_page: int = 25) -> Dict[str, Any]:
        """People currently working at a company."""
        return self._http.get(
            "/company/current-employees", {"company_id": company_id, "page": page, "per_page": per_page}
        )

    def past_employees(self, company_id: str, page: int = 1, per_page: int = 25) -> Dict[str, Any]:
        """People who previously worked at a company, with their past role there."""
        return self._http.get(
            "/company/past-employees", {"company_id": company_id, "page": page, "per_page": per_page}
        )

    def headcount_by_seniority(self, company_id: str) -> Dict[str, Any]:
        """Breakdown of a company's indexed profiles by seniority level."""
        return self._http.get("/company/headcount-by-seniority", {"company_id": company_id})

    def hiring_signals(
        self, company_id: str, days: int = 90, page: int = 1, per_page: int = 25
    ) -> Dict[str, Any]:
        """People who recently joined this company, a growth/expansion signal."""
        return self._http.get(
            "/company/hiring-signals",
            {"company_id": company_id, "days": days, "page": page, "per_page": per_page},
        )


class MonitorResource:
    """Webhook monitors under /monitors."""

    def __init__(self, http: HttpClient) -> None:
        self._http = http

    def list(self) -> Dict[str, Any]:
        """List all active webhook monitors for the workspace."""
        return self._http.get("/monitors")

    def create(
        self,
        type: str,
        subject_url: str,
        webhook_url: str,
        label: Optional[str] = None,
        events: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Subscribe to change events on a profile or company URL.

        type must be "person" or "company". webhook_url must be HTTPS.
        """
        body: Dict[str, Any] = {"type": type, "subject_url": subject_url, "webhook_url": webhook_url}
        if label is not None:
            body["label"] = label
        if events is not None:
            body["events"] = events
        return self._http.post("/monitors", body)

    def delete(self, id: str) -> Dict[str, Any]:
        """Stop monitoring and delete the monitor."""
        return self._http.delete("/monitors", {"id": id})


class Kooperativa:
    """Official Kooperativa API client.

    Example:
        >>> from kooperativa import Kooperativa
        >>> kooperativa = Kooperativa(api_key="kk_live_...")
        >>> profile = kooperativa.person.enrich(username="satyanadella")
        >>> print(profile["data"]["full_name"])
    """

    def __init__(self, api_key: str, base_url: str = DEFAULT_BASE_URL) -> None:
        if not api_key:
            raise ValueError("Kooperativa: api_key is required")
        self._http = HttpClient(api_key=api_key, base_url=base_url)
        self.person = PersonResource(self._http)
        self.company = CompanyResource(self._http)
        self.monitors = MonitorResource(self._http)

    def health(self) -> Dict[str, Any]:
        """No-auth liveness probe. Use to verify connectivity before a batch job."""
        return self._http.get("/health")

    def me(self) -> Dict[str, Any]:
        """Account info: license status and usage breakdown."""
        return self._http.get("/me")
