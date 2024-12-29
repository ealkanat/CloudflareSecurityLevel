# CF Security Level Controller

A Python script to manage Cloudflare's security level settings via their API.

## Description

This script allows you to:
- Check the current security level of your Cloudflare zone
- Update the security level to a new value
- Enforce stricter security levels only (prevents downgrading security unless forced)

## Security Levels

Available security levels from lowest to highest:
- off
- essentially_off
- low
- medium
- high
- under_attack

## Configuration

1. Copy `config.example.py` to `config.py`
2. Update `config.py` with your Cloudflare credentials:
```python
CLOUDFLARE_ZONE_ID = "your_zone_id"
CLOUDFLARE_EMAIL = "your_email@example.com"
CLOUDFLARE_API_KEY = "your_api_key"
```

## Usage

### Basic Usage

```bash
# Set security level to low (default)
python cf_security_level_controller.py

# Set specific security level
python cf_security_level_controller.py --security-level medium

# Force set security level (bypass priority check)
python cf_security_level_controller.py --security-level low --force
```

Available security levels: off, essentially_off, low, medium, high, under_attack

### Forced Update

Use the `--force` flag to bypass the security level priority check:
```bash
python cf_security_level_controller.py --security-level low --force
```

## Features

- Automatic timeout handling for API requests (30 seconds)
- Priority-based security level changes
- Force option to bypass security level restrictions
- Comprehensive error handling and status messages

## Requirements

- Python 3.x
- requests library (`pip install requests`)

## Security Notes

- Store your API credentials securely
- Never commit API keys to version control
- Use forced updates with caution

## Error Messages

- "Failed to get current security level": Unable to retrieve current settings
- "Invalid security level": Specified level not in allowed values
- "Update cancelled": New security level is lower than current (without force)

## API Documentation

For more details about the Cloudflare API endpoint used in this script, see:
[Cloudflare API - Edit Zone Setting](https://developers.cloudflare.com/api/resources/zones/subresources/settings/methods/edit/)