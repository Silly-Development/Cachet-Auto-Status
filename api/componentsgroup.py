import httpx

async def list_components_groups(base_url, apitoken):
    api_path = "/api/component-groups?per_page=100"
    headers = {"Authorization": f"Bearer {apitoken}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}{api_path}", headers=headers)
    return response