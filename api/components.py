import httpx

async def list_components(base_url, apitoken):
    api_path = "/api/components"
    headers = {"Authorization": f"Bearer {apitoken}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}{api_path}", headers=headers)
    return response

async def get_component_details(base_url, apitoken, component_id):
    api_path = f"/api/components/{component_id}"
    headers = {"Authorization": f"Bearer {apitoken}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}{api_path}", headers=headers)
    return response

async def update_component_status(base_url, apitoken, component_id, status):
    api_path = f"/api/components/{component_id}"
    headers = {"Authorization": f"Bearer {apitoken}",
               "Content-Type": "application/json"}
    status = {"status": int(status)}
    async with httpx.AsyncClient() as client:
        response = await client.put(f"{base_url}{api_path}", json=status, headers=headers)
    return response