import re
import requests
from pathlib import Path

HEADER_FILE = "Offsets.hpp"

ROBLOX_VERSION_URL = (
    "https://clientsettingscdn.roblox.com/"
    "v2/client-version/WindowsPlayer"
)

OFFSETS_URL = "https://offsets.imtheo.lol/FFlags.hpp"

content = Path(HEADER_FILE).read_text(
    encoding="utf-8"
)

match = re.search(
    r'ClientVersion\s*=\s*"([^"]+)"',
    content
)

if not match:
    raise Exception(
        "Could not find ClientVersion in offsets.hpp"
    )

local_version = match.group(1)

response = requests.get(
    ROBLOX_VERSION_URL,
    timeout=10
)

response.raise_for_status()

latest_version = response.json()[
    "clientVersionUpload"
]

print(f"Local Version : {local_version}")
print(f"Latest Version: {latest_version}")

if local_version != latest_version:
    print("New Roblox version detected.")
    print("Downloading new offsets...")

    offsets_response = requests.get(
        OFFSETS_URL,
        timeout=15
    )

    offsets_response.raise_for_status()

    Path(HEADER_FILE).write_text(
        offsets_response.text,
        encoding="utf-8"
    )

    print("offsets.hpp updated.")
else:
    print("Offsets already up to date.")
