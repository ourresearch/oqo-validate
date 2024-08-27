Installation:

```
pip install git+https://github.com/ourresearch/oqo-validate
```

Add line to requirements.txt:
```
git+https://github.com/ourresearch/oqo-validate
```

Update:

```
pip install -U git+https://github.com/ourresearch/oqo-validate
```

Uninstall:

```
pip uninstall oqo-validate
```

Example usages:
```
from oqo_validate import OQOValidator
validator = OQOValidator()
ok, error = validator.validate(query)
```

```
# Get config from somewhere else
from combined_config import all_entities_config
from oqo_validate import OQOValidator
validator = OQOValidator(all_entities_config)
ok, error = validator.validate(query)
```

```
from oqo_validate import OQOValidator
validator = OQOValidator()
from oqo_validate.modifiers import prune_empty_branches

>>> query = {
  "filters": [
    {
      "id": "br_2SeSEo",
      "subjectEntity": "works",
      "type": "branch",
      "operator": "and",
      "children": []
    },
    {
      "id": "br_v3qRsQ",
      "subjectEntity": "authors",
      "type": "branch",
      "operator": "and",
      "children": []
    }
  ],
  "summarize_by": "authors",
  "sort_by": {
    "column_id": "count(works)",
    "direction": "desc"
  },
  "return_columns": [
    "display_name",
    "ids.orcid",
    "last_known_institutions.id"
  ]
}
>>> validator.validate(query)
(False, 'Branch br_2SeSEo has empty children')
>>> query['filters'] = prune_empty_branches(query['filters'])
>>> validator.validate(query)
(True, None)
```
