import sys
sys.dont_write_bytecode = True
from api import cachet, components, componentsgroup
from services import geturls, checkstatus
import json
import asyncio
from datetime import datetime

baseurl = "https://status.sillydev.co.uk"
apitoken = "" # Get from Cachet dashboard -> Settings -> Manage API Keys
urls = {} # Do NOT touch this line

def log(level: str, message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [{level}] {message}")

async def start_script():
    starttime = datetime.now()
    log("INFO", "Starting Cachet Auto Status...")
    
    # Run all API calls concurrently for faster startup
    log("INFO", "Fetching API information...")
    apitest, version, systemstatus, componentcount, compontentgroupcount = await asyncio.gather(
        cachet.test_ping_api(baseurl, apitoken),
        cachet.get_version_info(baseurl, apitoken),
        cachet.get_system_status(baseurl, apitoken),
        components.list_components(baseurl, apitoken),
        componentsgroup.list_components_groups(baseurl, apitoken)
    )
    
    log("INFO", "Made by Gamer3514 for Silly Developers")
    log("INFO", "Web: https://sillydev.co.uk | Discord: https://discord.gg/mUpVm596As")
    log("INFO", f"API Version: {json.loads(version.content)['data']['version']}")
    log("INFO", f"System Status: {json.loads(systemstatus.content)['data']['message']} (HTTP {apitest.status_code})")
    log("INFO", f"Components: {len(json.loads(componentcount.content)['data'])} | Groups: {len(json.loads(compontentgroupcount.content)['data'])}")
    duration = datetime.now() - starttime
    mins, secs = divmod(duration.total_seconds(), 60)
    log("SUCCESS", f"Startup complete in {int(mins)}m {secs:.2f}s")

async def check_config_updates():
    """Every 60s compare local url db with API config"""
    global urls
    while True:
        log("INFO", "Checking for configuration updates...")
        try:
            new_urls = await geturls.get_urls(baseurl, apitoken)
            log("INFO", f"Fetched {len(new_urls)} URLs from API")
            
            if new_urls != urls:
                added = set(new_urls.keys()) - set(urls.keys())
                removed = set(urls.keys()) - set(new_urls.keys())
                
                if added:
                    log("INFO", f"New URLs added: {', '.join(added)}")
                if removed:
                    log("WARNING", f"URLs removed: {', '.join(removed)}")
                
                log("SUCCESS", f"Configuration updated: {len(urls)} → {len(new_urls)} URLs")
                urls = new_urls
            else:
                log("INFO", f"No configuration changes ({len(urls)} URLs)")
        except Exception as e:
            log("ERROR", f"Failed to check config: {str(e)}")
        
        await asyncio.sleep(60)

# Cachet status names for logging
CACHET_STATUS_NAMES = {
    1: "Operational",
    2: "Performance Issues",
    3: "Partial Outage",
    4: "Major Outage"
}

async def monitor_status():
    """Every 120s check status of all URLs"""
    while True:
        log("INFO", "Starting status check cycle...")
        
        if not urls:
            log("WARNING", "No URLs configured yet, waiting for config update...")
            await asyncio.sleep(10)  # Check more frequently when no URLs
            continue
        
        log("INFO", f"Checking {len(urls)} URLs...")
        
        # Check all URLs concurrently for faster monitoring
        tasks = [checkstatus.check_status(url, config['expected_status']) for url, config in urls.items()]
        results = await asyncio.gather(*tasks)
        
        # Process results and update storage
        up_count = 0
        down_count = 0
        api_updates = []
        
        for (url, config), status_data in zip(urls.items(), results):
            is_up = status_data['is_up']
            status_code = status_data.get('status_code')
            response_time = status_data.get('response_time')
            error = status_data.get('error')
            
            if is_up:
                up_count += 1
                log("SUCCESS", f"[{config['component_id']}] {config['component_name']}: UP (HTTP {status_code}, {response_time:.3f}s)")
                # Update Cachet to operational
                new_status = 1
            else:
                down_count += 1
                error_msg = f", Error: {error}" if error else ""
                status_msg = f"HTTP {status_code}" if status_code else "No response"
                log("ERROR", f"[{config['component_id']}] {config['component_name']}: DOWN ({status_msg}{error_msg})")
                # Update Cachet to major outage
                new_status = 4
            
            # Queue Cachet API update
            api_updates.append({
                'component_id': config['component_id'],
                'component_name': config['component_name'],
                'new_status': new_status
            })
        
        log("INFO", f"Status check complete: {up_count} UP, {down_count} DOWN")
        
        # Send Cachet API updates
        if api_updates:
            log("INFO", f"Sending {len(api_updates)} Cachet status updates...")
            for update in api_updates:
                try:
                    new_status_name = CACHET_STATUS_NAMES.get(update['new_status'], 'Unknown')
                    
                    await components.update_component_status(
                        baseurl, apitoken,
                        update['component_id'],
                        update['new_status']
                    )
                    
                    log("INFO", f"[{update['component_id']}] {update['component_name']}: Cachet → {new_status_name}")
                        
                except Exception as e:
                    log("ERROR", f"[{update['component_id']}] Failed to update Cachet: {str(e)}")
        
        await asyncio.sleep(120)

async def main():
    """Main async entry point"""
    await start_script()
    
    log("INFO", "Starting monitoring loops (config: 60s, status: 120s)")
    
    # Run both loops concurrently
    await asyncio.gather(
        check_config_updates(),
        monitor_status()
    )

if __name__ == "__main__":
    asyncio.run(main())