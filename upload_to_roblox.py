#!/usr/bin/env python3
"""
Upload ModuleScript to Roblox asset using Open Cloud API
"""

import os
import sys
import urllib.request
import json

ASSET_ID = "91072619691201"

def upload_module_script(api_key, file_path):
    """Upload a Lua ModuleScript to Roblox using Open Cloud API"""

    # Read the Lua file
    with open(file_path, 'r') as f:
        lua_content = f.read()

    # Roblox Open Cloud API endpoint for updating assets
    url = f"https://apis.roblox.com/assets/v1/assets/{ASSET_ID}"

    # Prepare the request
    data = lua_content.encode('utf-8')

    headers = {
        'x-api-key': api_key,
        'Content-Type': 'application/octet-stream'
    }

    req = urllib.request.Request(url, data=data, headers=headers, method='PATCH')

    try:
        with urllib.request.urlopen(req) as response:
            result = response.read().decode('utf-8')
            print(f"[OK] Successfully uploaded ModuleScript to asset {ASSET_ID}")
            print(f"Response: {result}")
            return True
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        print(f"[ERROR] Failed to upload: HTTP {e.code}")
        print(f"Error details: {error_body}")
        return False
    except Exception as e:
        print(f"[ERROR] Upload failed: {e}")
        return False

def main():
    """Main function"""
    api_key = os.environ.get('ROBLOX_API_KEY')

    if not api_key:
        print("[ERROR] ROBLOX_API_KEY environment variable not set")
        sys.exit(1)

    file_path = 'StockData.lua'

    if not os.path.exists(file_path):
        print(f"[ERROR] {file_path} not found")
        sys.exit(1)

    success = upload_module_script(api_key, file_path)

    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
