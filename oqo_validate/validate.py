from typing import List

import requests


def _get_entities_config():
    r = requests.get('https://api.openalex.org/entities/config')
    r.raise_for_status()
    return r.json()


def _safe_lower(o):
    if isinstance(o, str):
        return o.lower()
    return o


def _flatten_keys_and_values(dicts: List[dict]) -> List:
    dicts = [item for d in dicts for item in d.items()]
    return [_safe_lower(element) for pair in dicts for element in pair]


def _formatted_country_value(country_code):
    country_code = country_code.lower()
    if 'countries' in country_code:
        return country_code
    return f'countries/{country_code}'.lower()


ENTITIES_CONFIG = _get_entities_config()
BRANCH_OPERATORS = {'and', 'or'}
LEAF_OPERATORS = {'is', 'is not', 'contains', 'does not contain',
                  'is greater than', 'is less than', '>', '<'}
FILTER_TYPES = {'branch', 'leaf'}


def _entity_possible_values(entity):
    return set(_flatten_keys_and_values(
        ENTITIES_CONFIG[entity].get('values', []) or []))


def _get_entity_column(entity, column_id_or_name, actions=None):
    if not actions:
        actions = []
    for _, col in ENTITIES_CONFIG[entity].get('columns', {}).items():
        valid_names = {col['id'], col['displayName'],
                                  col.get('redshiftDisplayColumn')}
        if column_id_or_name in valid_names and all(
                [action in col.get('actions', []) for action in actions]):
            return col
    return None


def _validate_leaf(leaf_filter):
    subj_entity = leaf_filter['subjectEntity']
    col = _get_entity_column(subj_entity, leaf_filter['column_id'])
    if not col:
        return False, f'{subj_entity}.{leaf_filter["column_id"]} not a valid filter column'
    if leaf_filter['operator'] not in LEAF_OPERATORS:
        return False, f'{leaf_filter["operator"]} not a valid leaf operator'
    obj_entity = col.get('objectEntity')
    if obj_entity:
        possible_values = _entity_possible_values(obj_entity)
        value = leaf_filter[
            'value'] if not obj_entity == 'countries' else _formatted_country_value(leaf_filter['value'])
        if possible_values and value not in possible_values:
            return False, f'{leaf_filter["value"]} not a valid value for {obj_entity}'
    return True, None


def _validate_branch(branch_filter):
    if not branch_filter.get('children'):
        return False, f'Branch {branch_filter.get("id")} has empty children'
    if branch_filter['operator'] not in BRANCH_OPERATORS:
        return False, f'{branch_filter["operator"]} not a valid branch operator'
    return True, None


def _validate_filter(filter_node):
    if filter_node['type'] not in FILTER_TYPES:
        return False, f'{filter_node.get("type")} not a valid filter type'
    if filter_node['type'] == 'branch':
        return _validate_branch(filter_node)
    elif filter_node['type'] == 'leaf':
        return _validate_leaf(filter_node)
    return False, f'{filter_node.get("type")} not a valid filter type'


# entity='works' except in cases where summarize_by is not empty/unspecified/null
def _validate_sort_by(sort_by, entity='works'):
    col = _get_entity_column(entity, sort_by['column_id'])
    if not col:
        return False, f'{entity}.{sort_by["column_id"]} not a valid sort column'
    if sort_by['direction'] not in {'asc', 'desc'}:
        return False, f'{sort_by["direction"]} not a valid sort direction'
    return True, None


# entity='works' except in cases where summarize_by is not empty/unspecified/null
def validate_return_columns(return_columns, entity='works'):
    for column in return_columns:
        col = _get_entity_column(entity, column)
        if not col:
            return False, f'{entity}.{column} not a valid return column'
    return True, None


def _validate_summarize_by(summarize_by):
    if summarize_by not in ENTITIES_CONFIG.keys() and summarize_by != 'all':
        return False, f'works.{summarize_by} not a valid summary column'
    return True, None


def validate_oqo(oqo):
    for _filter in oqo.get('filters', []):
        ok, error = _validate_filter(_filter)
        if not ok:
            return False, error
    summarize_by_entity = oqo.get('summarize_by')
    if summarize_by_entity:
        ok, error = _validate_summarize_by(summarize_by_entity)
        if not ok:
            return False, error
    if return_cols := oqo.get('return_columns', []):
        ok, error = validate_return_columns(return_cols,
                                            summarize_by_entity or 'works')
        if not ok:
            return False, error
    if sort_by := oqo.get('sort_by'):
        ok, error = _validate_sort_by(sort_by, summarize_by_entity or 'works')
        if not ok:
            return False, error
    return True, None
