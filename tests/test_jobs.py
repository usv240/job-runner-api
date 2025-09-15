import pytest
from httpx import AsyncClient
from fastapi import status
from app.main import app

@pytest.mark.asyncio
async def test_submit_job():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/jobs", json={"command": "cmd /c echo test"})
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "job_id" in data
        assert data["status"] == "queued"

@pytest.mark.asyncio
async def test_list_jobs():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/jobs")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert isinstance(data, list)

@pytest.mark.asyncio
async def test_get_job_status():
    # Submit job first
    async with AsyncClient(app=app, base_url="http://test") as ac:
        post_response = await ac.post("/jobs", json={"command": "cmd /c echo test"})
        job_id = post_response.json()["job_id"]

        # Fetch status
        response = await ac.get(f"/jobs/{job_id}")
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["job_id"] == job_id
        assert data["status"] in ["queued", "running", "completed", "failed", "not_found"]
