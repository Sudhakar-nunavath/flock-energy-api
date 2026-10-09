from fastapi import FastAPI, HTTPException, Query

from app.client import UrjaPortalClient
from app.models import (
    Meter,
    MeterListResponse,
    ConsumptionReading,
    ConsumptionResponse,
    Location,
    LocationResponse,
)

app = FastAPI(
    title="Flock Energy Meter API",
    description="REST API wrapper for the Urja Meter Ops portal",
    version="1.0.0",
)


def get_client():
    client = UrjaPortalClient()
    try:
        client.login()
        return client
    except Exception:
        client.close()
        raise


@app.get("/api/v1/health")
def health_check():
    return {
        "status": "ok",
        "message": "Flock Energy API is running",
    }


@app.get("/api/v1/meters", response_model=MeterListResponse)
def list_meters(
    q: str = Query(default="", description="Search meter records"),
    page: int = Query(default=1, ge=1, description="Page number"),
):
    client = None
    try:
        client = get_client()
        result = client.search_meters(query=q, page=page)

        meters = [
            Meter(
                meter_id=item["meterId"],
                serial_number=item.get("serialNo"),
                make=item.get("make"),
                phase_type=item.get("phaseType"),
                installation_status=item.get("installStatus"),
                dt_code=item.get("dtCode"),
            )
            for item in result.get("data", [])
        ]

        return MeterListResponse(
            data=meters,
            total=result.get("total", len(meters)),
            page=result.get("page", page),
            page_size=result.get("pageSize", len(meters)),
        )
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Unable to retrieve meters: {type(exc).__name__}",
        ) from exc
    finally:
        if client:
            client.close()


@app.get("/api/v1/meters/{meter_id}")
def get_meter(meter_id: str):
    client = None
    try:
        client = get_client()
        result = client.search_meters(query=meter_id, page=1)
        for item in result.get("data", []):
            if item.get("meterId") == meter_id:
                return {
                    "meter_id": item["meterId"],
                    "serial_number": item.get("serialNo"),
                    "make": item.get("make"),
                    "phase_type": item.get("phaseType"),
                    "installation_status": item.get("installStatus"),
                    "dt_code": item.get("dtCode"),
                }

        raise HTTPException(status_code=404, detail="Meter not found")
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Unable to retrieve meter: {type(exc).__name__}",
        ) from exc
    finally:
        if client:
            client.close()


@app.get(
    "/api/v1/meters/{meter_id}/consumption",
    response_model=ConsumptionResponse,
)
def get_consumption(meter_id: str):
    client = None
    try:
        client = get_client()
        result = client.get_meter_energy(meter_id)

        readings = [
            ConsumptionReading(
                timestamp=item["timestamp"],
                kwh=float(item["kwh"]),
                kvah=float(item["kvah"]),
                voltage_r=float(item["voltR"]),
            )
            for item in result.get("data", [])
        ]

        return ConsumptionResponse(
            meter_id=meter_id,
            readings=readings,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Unable to retrieve consumption: {type(exc).__name__}",
        ) from exc
    finally:
        if client:
            client.close()


@app.get(
    "/api/v1/meters/{meter_id}/location",
    response_model=LocationResponse,
)
def get_location(meter_id: str):
    client = None
    try:
        client = get_client()
        result = client.get_meter_geo(meter_id)
        data = result.get("data", {})

        if not data:
            raise HTTPException(
                status_code=404,
                detail="Location not found",
            )

        return LocationResponse(
            meter_id=meter_id,
            location=Location(
                latitude=float(data["latitude"]),
                longitude=float(data["longitude"]),
            ),
        )
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Unable to retrieve location: {type(exc).__name__}",
        ) from exc
    finally:
        if client:
            client.close()
