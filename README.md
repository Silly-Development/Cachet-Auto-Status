# Cachet Auto Status

Automated status monitoring for [Cachet](https://cachethq.io/) status pages. Continuously checks URLs configured in your Cachet components and automatically updates their status.
This is a stripped-down open source version of what we use at Silly Developers for our own status page, we may sync those features back here in the future.
This script was made for our specific use case, so may not fit all needs out of the box, but feel free to modify it as needed.

## Features

- ✅ Automatic URL health monitoring
- ✅ Real-time Cachet component status updates
- ✅ Configurable status code expectations
- ✅ Concurrent status checking for performance
- ✅ Auto-sync with Cachet component configuration

## Requirements

- Python 3.7+
- Cachet instance with API access
- Required packages: `httpx`

## Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install httpx
   ```

## Configuration

Edit `app.py` to configure your Cachet instance (lines 9-10):

```python
baseurl = "https://status.example.com"  # Your Cachet URL
apitoken = "your-api-token-here"        # Get from Cachet: Settings → Manage API Keys
```

## Setting Up Components

In your Cachet dashboard, add metadata to components you want to monitor:

1. Create or edit a component
2. Add the following metadata fields:
   - `url`: The URL to monitor (e.g., `https://example.com`)
   - `expectedstatuscode`: Expected HTTP status code (default: `200`)

## Usage

Run the monitoring script:

```bash
python app.py
```

The script will:
- Check for component configuration updates every 60 seconds
- Monitor all configured URLs every 120 seconds
- Automatically update Cachet component statuses:
  - **Status 1 (Operational)**: Service is responding with expected status code
  - **Status 4 (Major Outage)**: Service is down or returning unexpected status code

## Project Structure

```
├── app.py                  # Main application
├── api/
│   ├── cachet.py          # Cachet API interactions
│   ├── components.py      # Component management
│   └── componentsgroup.py # Component group management
└── services/
    ├── checkstatus.py     # URL health checking
    └── geturls.py         # Component URL fetching
```

## Credits

Made by [Gamer3514](https://gamer3514.co.uk) for Silly Developers

- Website: https://sillydev.co.uk
- Discord: https://discord.gg/mUpVm596As

Parts of this project, mainly the README file, were generated with the help of AI tools.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
If you do not understand this license, please contact a legal professional for clarification.
