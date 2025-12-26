import httpx

async def test_ping_api(base_url, apitoken):
    api_path = "/api/ping"
    headers = {"Authorization": f"Bearer {apitoken}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}{api_path}", headers=headers)
    return response

async def get_version_info(base_url, apitoken):
    api_path = "/api/version"
    headers = {"Authorization": f"Bearer {apitoken}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}{api_path}", headers=headers)
    return response

async def get_system_status(base_url, apitoken):
    api_path = "/api/status"
    headers = {"Authorization": f"Bearer {apitoken}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}{api_path}", headers=headers)
    return response