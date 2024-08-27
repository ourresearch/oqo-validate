import requests

from oqo_validate import OQOValidator

r = requests.get(
    'https://raw.githubusercontent.com/ourresearch/oqo-search-tests/main/tests.json')
r.raise_for_status()
tests = r.json()
validator = OQOValidator()
for test in tests:
    ok, error = validator.validate(test['query'])
    if not ok:
        print((ok, error))