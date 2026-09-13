#!/usr/bin/env python3
import gzip
import hashlib
import json
from pathlib import Path
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parent
MANIFEST_URL = 'https://zanagamestudios-lgtm.github.io/muadililac/data/releases/latest/manifest.json'
EXPECTED_SHA = '20aaf0989cc6c3d74b378fdca359d85e973bff407b7ab1b351c407002780f19c'
EXPECTED_RECORDS = 18106
EXPECTED_ACTIVE = 7925
EXPECTED_PASSIVE = 10181

with urlopen(Request(MANIFEST_URL, headers={'Cache-Control': 'no-cache'}), timeout=30) as response:
    manifest = json.load(response)
file_info = manifest['files']['medicines.json.gz']
url = 'https://zanagamestudios-lgtm.github.io/muadililac/' + file_info['latestPath']
with urlopen(Request(url, headers={'Cache-Control': 'no-cache'}), timeout=60) as response:
    compressed = response.read()
assert hashlib.sha256(compressed).hexdigest() == file_info['sha256'] == EXPECTED_SHA
with gzip.GzipFile(fileobj=__import__('io').BytesIO(compressed)) as stream:
    payload = json.loads(stream.read().decode('utf-8'))
items = payload['medicines']
active = sum(1 for item in items if item['status'] == 'ACTIVE')
passive = sum(1 for item in items if item['status'] == 'PASSIVE')
assert len(items) == manifest['recordCount'] == EXPECTED_RECORDS
assert active == manifest['activeCount'] == EXPECTED_ACTIVE
assert passive == manifest['passiveCount'] == EXPECTED_PASSIVE

index = (ROOT / 'index.html').read_text(encoding='utf-8')
bundle_name = 'assets/index-live-v5.js'
assert f'src="/{bundle_name}"' in index
bundle = (ROOT / bundle_name).read_text(encoding='utf-8')
for marker in ('latest/manifest.json', 'medicines.json.gz', 'DecompressionStream("gzip")', 'SHA-256', 'recordCount', 'activeCount', 'passiveCount', 'muadililac-web-catalog-v4', 'localStorage.setItem(mlcPointerKey'):
    assert marker in bundle, marker
assert '18723' not in bundle
assert 'muadil-ilac-shell-v2' in (ROOT / 'service-worker.js').read_text(encoding='utf-8')
print(f'manifest_data_version={manifest["dataVersion"]}')
print(f'manifest_records={manifest["recordCount"]}')
print(f'json_records={len(items)}')
print(f'ui_dynamic_counters=verified_bundle_markers')
print(f'active={active} passive={passive}')
print(f'sha256={EXPECTED_SHA}')
print('validation=PASS')
