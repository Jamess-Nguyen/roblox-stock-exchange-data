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
    import mimetypes
    from io import BytesIO

    # Read the Lua file
    with open(file_path, 'rb') as f:
        lua_content = f.read()

    # Create multipart form data
    boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'

    body = BytesIO()
    body.write(f'--{boundary}\r\n'.encode('utf-8'))
    body.write(b'Content-Disposition: form-data; name="request"\r\n')
    body.write(b'Content-Type: application/json\r\n\r\n')
    body.write(json.dumps({
        "assetId": int(ASSET_ID),
        "assetType": "Model"
    }).encode('utf-8'))
    body.write(b'\r\n')

    body.write(f'--{boundary}\r\n'.encode('utf-8'))
    body.write(b'Content-Disposition: form-data; name="fileContent"; filename="StockData.lua"\r\n')
    body.write(b'Content-Type: application/octet-stream\r\n\r\n')
    body.write(lua_content)
    body.write(b'\r\n')
    body.write(f'--{boundary}--\r\n'.encode('utf-8'))

    # Roblox Open Cloud API endpoint for updating assets
    url = f"https://apis.roblox.com/assets/v1/assets/{ASSET_ID}"

    headers = {
        'x-api-key': api_key.strip(),
        'Content-Type': f'multipart/form-data; boundary={boundary}'
    }

    req = urllib.request.Request(url, data=body.getvalue(), headers=headers, method='PATCH')

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
