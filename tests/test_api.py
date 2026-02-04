import pytest
from httpx import AsyncClient
from parking_system.main import app

@pytest.mark.asyncio
async def test_list_slots():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/slots")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_register_and_checkin_vehicle():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Register vehicle
        response = await client.post("/api/vehicles", json={"license_plate": "TEST123", "vehicle_type": "car"})
        assert response.status_code == 200
        data = response.json()
        assert data["license_plate"] == "TEST123"

        # Check-in vehicle
        response = await client.post("/api/vehicles/checkin", json={"license_plate": "TEST123"})
        assert response.status_code == 200
        data = response.json()
        assert data["checked_in"] is True
