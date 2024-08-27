import requests

from validate import validate_oqo

r = requests.get(
    'https://raw.githubusercontent.com/ourresearch/oqo-search-tests/main/tests.json')
r.raise_for_status()
tests = r.json()
for test in tests:
    ok, error = validate_oqo(test['query'])
    if not ok:
        print((ok, error))