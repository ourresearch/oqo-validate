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
from oqo_validate.validate import validate_oqo
ok, error = validate_oqo(query)
```

```
from oqo_validate.validate import validate_oqo
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
>>> validate_oqo(query)
(False, 'Branch br_2SeSEo has empty children')
>>> query['filters'] = prune_empty_branches(query['filters'])
>>> validate_oqo(query)
(True, None)
```
