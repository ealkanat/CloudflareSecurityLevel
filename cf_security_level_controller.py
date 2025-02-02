"""Script to update Cloudflare security level settings."""

import argparse
import requests
from config import CLOUDFLARE_ZONE_ID as ZONE_ID, CLOUDFLARE_EMAIL, CLOUDFLARE_API_KEY

SETTING_ID = "security_level"
PRIORITY = ["off", "essentially_off", "low", "medium", "high", "under_attack"]

def get_current_security_level():
    """Retrieve the current Cloudflare security level."""
    url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/settings/{SETTING_ID}"
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Email": CLOUDFLARE_EMAIL,
        "Authorization": "Bearer " + CLOUDFLARE_API_KEY
    }

    response = requests.get(url, headers=headers, timeout=30)
    if response.status_code == 200:
        result = response.json().get("result", {})
        current_value = result.get("value")
        return current_value
    return None

def set_security_level(new_value, forced=False):
    """Update the Cloudflare security level.
    
    Args:
        new_value (str): The new security level to set
        forced (bool): If True, bypasses the priority check
    
    Returns:
        bool: True if update successful, False otherwise
    """
    if not forced and new_value not in PRIORITY:
        print(f"Invalid security level. Must be one of: {', '.join(PRIORITY)}")
        return False

    url = f"https://api.cloudflare.com/client/v4/zones/{ZONE_ID}/settings/{SETTING_ID}"
    headers = {
        "Content-Type": "application/json",
        "X-Auth-Email": CLOUDFLARE_EMAIL,
        "Authorization": "Bearer " + CLOUDFLARE_API_KEY
    }
    
    data = {
        "id": "security_level",
        "value": new_value
    }
    
    response = requests.patch(url, headers=headers, json=data, timeout=30)
    if response.status_code == 200:
        print(f"Successfully updated security level to: {new_value}")
        return True
    else:
        print(f"Failed to update security level. Status code: {response.status_code}")
        return False

def main(security_level=None, forced=False):
    """Execute the main security level update logic.
    
    Args:
        security_level (str): Target security level to set
        forced (bool): If True, bypasses the priority check
    """
    if security_level is None:
        security_level = "low"  # default value
        
    if security_level not in PRIORITY:
        print(f"Invalid security level. Must be one of: {', '.join(PRIORITY)}")
        return

    current_value = get_current_security_level()
    
    if current_value is None:
        print("Failed to get current security level")
        return
        
    if current_value not in PRIORITY:
        print(f"Current security level '{current_value}' is not valid")
        return
        
    current_priority = PRIORITY.index(current_value)
    new_priority = PRIORITY.index(security_level)
    
    if new_priority > current_priority or forced:
        set_security_level(security_level, forced=forced)
    else:
        print(f"Update cancelled. New value '{security_level}' is lower than current level ({current_value}). Use --force to override.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Manage Cloudflare security level settings.')
    parser.add_argument('--security-level', choices=PRIORITY, help='Set security level')
    parser.add_argument('--force', action='store_true', help='Force security level change')
    
    args = parser.parse_args()
    main(security_level=args.security_level, forced=args.force)
