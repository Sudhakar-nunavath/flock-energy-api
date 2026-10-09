# Flock Energy Meter API

A REST API wrapper around the legacy Urja Meter Ops portal. It provides
structured meter information, consumption readings, and geographic coordinates
without requiring API consumers to interact directly with the original portal.

## Technology Stack

- Python 3
- FastAPI — REST API framework and OpenAPI generation
- HTTPX — HTTP requests and session-cookie handling
- Beautiful Soup — available for HTML parsing if needed
- Pydantic — request/response data validation
- python-dotenv — environment configuration
- pytest — automated tests

## Project Structure

```text
flock-energy-api/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── client.py
│   ├── models.py
│   └── config.py
├── tests/
│   └── test_api.py
├── PROTOCOL.md
├── README.md
├── REFLECTION.md
├── openapi.json
├── requirements.txt
├── .env.example
└── .gitignore
```

## Setup

Requires Python 3.10 or newer.

1. Clone the repository.
2. Create and activate a virtual environment.
3. Install the dependencies.
4. Configure the environment variables.
5. Start the API.

### Example commands

Clone the repository and enter the project directory:

```bash
git clone https://github.com/Sudhakar-nunavath/flock-energy-api.git
cd flock-energy-api
```

Create and activate a virtual environment, then install dependencies:

```bash
python -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt
```

Create your local environment file:

```bash
cp .env.example .env
```

Edit `.env` with the authorized portal URL and credentials.

Start the server:

```bash
uvicorn app.main:app --reload
```

Open Swagger UI at http://127.0.0.1:8000/docs.

## Configuration

Set these variables in `.env`:

```text
URJA_BASE_URL=https://urja-ops.flockenergy.tech
URJA_USERNAME=your-authorized-username
URJA_PASSWORD=your-authorized-password
```

Never commit `.env` or real credentials to GitHub.

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/v1/health` | Health check |
| GET | `/api/v1/meters` | Search and list meters |
| GET | `/api/v1/meters/{meter_id}` | Retrieve meter information |
| GET | `/api/v1/meters/{meter_id}/consumption` | Retrieve energy readings |
| GET | `/api/v1/meters/{meter_id}/location` | Retrieve coordinates |

### Example requests

List meters:

```bash
curl "http://127.0.0.1:8000/api/v1/meters?page=1"
```

Search meters:

```bash
curl "http://127.0.0.1:8000/api/v1/meters?q=J100000&page=1"
```

Get consumption:

```bash
curl "http://127.0.0.1:8000/api/v1/meters/J100000/consumption"
```

Get location:

```bash
curl "http://127.0.0.1:8000/api/v1/meters/J100000/location"
```

## Design Decisions and Trade-offs

- FastAPI provides automatic validation and interactive API documentation.
- HTTPX retains session cookies for authenticated requests.
- Pydantic models provide consistent response schemas.
- Legacy field names are converted to snake_case, and numeric readings
  are converted from strings to numbers.
- The implementation prioritizes a small, readable wrapper over a more
  complex service with a database or background jobs.

## Assumptions and Limitations

- The portal is accessed only with authorized credentials and treated as read-only.
- The legacy portal's internal endpoints may change without notice.
- The meter detail endpoint currently searches the meter listing for an exact ID.
- Automatic retry after HTTP 401 or 403 may not resolve every portal error.
- Caching, hierarchy reconstruction, bulk extraction, and a frontend are
  not included in the initial implementation.

## Testing

Run automated tests with:

```bash
python -m pytest -q
```

The current tests cover the health check, OpenAPI availability, and invalid
pagination. More integration and failure-path tests would improve coverage.

## Documentation

- [PROTOCOL.md](PROTOCOL.md) — observed legacy portal behavior.
- [REFLECTION.md](REFLECTION.md) — engineering reflection.
- `openapi.json` — generated specification for this API.

Generate the OpenAPI file while the server is running:

```bash
curl http://127.0.0.1:8000/openapi.json -o openapi.json
```

## Future Improvements

- Add mocked tests for meter, consumption, and location responses.
- Verify session expiration and retry behavior with targeted tests.
- Improve error mapping and input validation.
- Parse direct meter detail pages and reconstruct the network hierarchy.
- Evaluate caching and bulk retrieval based on portal behavior and dataset size.
- Add CI to run tests automatically on every change.

## Reflection

See [REFLECTION.md](REFLECTION.md).
