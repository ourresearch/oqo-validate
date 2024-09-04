import requests
import yaml

from oqo_validate import OQOValidator

r = requests.get(
    'https://raw.githubusercontent.com/ourresearch/oqo-search-tests/b484a7b0e7bf90ed47c06c3d81567deb26c99bce/new_tests.yaml')
r.raise_for_status()
tests = yaml.safe_load(r.content)

validator = OQOValidator()
for test in tests:
    ok, error = validator.validate(test['query'])
    if not ok:
        print((ok, error))