
def prune_empty_children_branches(filters):
    return [_filter for _filter in filters if
            _filter['type'] != 'branch' or bool(_filter['children'])]