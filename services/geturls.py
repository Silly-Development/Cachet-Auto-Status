from api import components
import json

async def get_urls(baseurl, apitoken):
    urls = {}
    response = await components.list_components(baseurl, apitoken)
    for component in json.loads(response.content)['data']:
        url = component['attributes']['meta'].get('url')
        if url:
            expectedstatuscode = component['attributes']['meta'].get('expectedstatuscode', 200)
            # Ensure expected status code is an integer
            expectedstatuscode = int(expectedstatuscode) if expectedstatuscode else 200
            urls[url] = {
                'expected_status': expectedstatuscode,
                'component_id': component['id'],
                'component_name': component['attributes']['name']
            }
    return urls