# Urja Meter Ops — Protocol Notes

## 1. Overview

Urja Meter Ops is a legacy web portal that provides meter information through
web pages and internal HTTP endpoints. This project wraps those endpoints in
a cleaner REST API.

## 2. Authentication

The portal accepts a POST request to `/login` with form fields `email` and
`password`.

A successful login returns HTTP 200 and sets a secure session cookie.
The Python client uses an HTTPX session to retain cookies between requests.

The login request required browser-like headers during investigation,
including `Accept: application/json`, `Origin`, `Referer`, and
`X-Sveltekit-Action: true`.

## 3. Discovered endpoints

| Method | Legacy path | Purpose |
|---|---|---|
| POST | `/login` | Authenticate |
| GET | `/portal/meters/search?q=&page=1` | Search and paginate meters |
| GET | `/portal/meters/{meter_id}/energy` | Retrieve consumption readings |
| GET | `/portal/meters/{meter_id}/geo` | Retrieve geographic coordinates |

The meter search response contains a `data` array. Meter fields include
`meterId`, `serialNo`, `make`, `phaseType`, `installStatus`, and `dtCode`.

The energy response contains readings with `timestamp`, `kwh`, `kvah`,
and `voltR`. These numeric measurements arrive as strings and are converted
to numbers by the wrapper.

The geo response contains latitude and longitude, also represented as strings.

## 4. Authentication and session behavior

HTTPX maintains the session cookie in its client. The wrapper logs in before
making a request when necessary and retries once after HTTP 401 or 403.

A 403 does not always mean that a session expired, so the retry may not
resolve every authentication or authorization failure.

## 5. Wrapper design

The new API uses snake_case field names and validates responses with Pydantic
models. FastAPI generates an OpenAPI specification and Swagger UI.

## 6. Observed limitations and follow-up work

- The portal is treated as read-only.
- Authentication and endpoint behavior were investigated using browser
  developer tools and local HTTP requests.
- Further testing should verify invalid meter IDs, pagination behavior,
  session expiry, malformed responses, and portal outages.
- The detail endpoint currently uses the meter search results to locate a
  meter. A direct detail-page parser would be a useful improvement.
- Network hierarchy reconstruction, caching, and a bulk data strategy remain
  possible extensions.
