import requests
import yaml

from oqo_validate import OQOValidator

r = requests.get(
    'https://raw.githubusercontent.com/ourresearch/oqo-search-tests/main/new_tests.yaml')
r.raise_for_status()

# tests = yaml.safe_load(open('./tests.yaml').read())
tests = yaml.safe_load(r.content)

validator = OQOValidator()
for test in tests:
    ok, error = validator.validate(test['query'], return_exc=True)
    if not ok:
        print((ok, error), test['query'])