import httpx

from app.config import (
    URJA_BASE_URL,
    URJA_USERNAME,
    URJA_PASSWORD,
)


class UrjaPortalClient:
    def __init__(self):
        self.base_url = URJA_BASE_URL.rstrip("/")
        self.client = httpx.Client(
            base_url=self.base_url,
            timeout=15.0,
            follow_redirects=True,
        )
        self.logged_in = False

    def login(self):
        headers = {
            "Accept": "application/json",
            "Origin": self.base_url,
            "Referer": f"{self.base_url}/login",
            "X-Sveltekit-Action": "true",
        }

        response = self.client.post(
            "/login",
            data={
                "email": URJA_USERNAME,
                "password": URJA_PASSWORD,
            },
            headers=headers,
        )
        response.raise_for_status()
        self.logged_in = True

    def _request(self, method, path, **kwargs):
        if not self.logged_in:
            self.login()

        response = self.client.request(method, path, **kwargs)

        # Retry once after re-authentication if the session is rejected.
        if response.status_code in (401, 403):
            self.logged_in = False
            self.login()
            response = self.client.request(method, path, **kwargs)

        response.raise_for_status()

        # Detect redirects to the login page where applicable.
        if "/login" in str(response.url) and path != "/login":
            self.logged_in = False
            raise httpx.HTTPStatusError(
                "The portal redirected the request to its login page",
                request=response.request,
                response=response,
            )

        return response

    def search_meters(self, query="", page=1):
        response = self._request(
            "GET",
            "/portal/meters/search",
            params={"q": query, "page": page},
        )
        return response.json()

    def get_meter_energy(self, meter_id):
        response = self._request(
            "GET",
            f"/portal/meters/{meter_id}/energy",
        )
        return response.json()

    def get_meter_geo(self, meter_id):
        response = self._request(
            "GET",
            f"/portal/meters/{meter_id}/geo",
        )
        return response.json()

    def close(self):
        self.client.close()
