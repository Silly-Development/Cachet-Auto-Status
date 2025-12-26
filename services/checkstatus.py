import httpx

async def check_status(url, expected_status=200):
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(url)
        return {
            'url': url,
            'status_code': response.status_code,
            'expected_status': expected_status,
            'is_up': response.status_code == expected_status,
            'response_time': response.elapsed.total_seconds()
        }
    except httpx.RequestError as e:
        return {
            'url': url,
            'status_code': None,
            'expected_status': expected_status,
            'is_up': False,
            'error': str(e)
        }