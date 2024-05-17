# -*- coding: utf-8 -*-

from typing import Dict, Iterator, List, Set, Union

from resources.lib.common.language import Language


def _normalize_mappings(mappings: Dict[Language, Union[Language, List[Language]]]) -> Dict[Language, List[Language]]:
    normalized_mappings: Dict[Language, List[Language]] = {}
    if not mappings:
        return normalized_mappings
    for key, value in mappings.items():
        normalized_mappings[key] = [value] if isinstance(value, Language) else value
    return normalized_mappings


def _reverse_mappings(custom_mappings: Dict[Language, List[Language]], implicit_mappings: List[Language]) -> Dict[Language, List[Language]]:
    reverse_mappings: Dict[Language, List[Language]] = {}
    for key, values in custom_mappings.items():
        for value in values:
            if value in reverse_mappings:
                reverse_mappings[value].append(key)
            else:
                reverse_mappings[value] = [key]
    for mapped_key, mapped_values in reverse_mappings.items():
        if mapped_key in implicit_mappings and mapped_key not in mapped_values:
            mapped_values.insert(0, mapped_key)
    return reverse_mappings


def _build_mapped_set(values: List[Language], mappings: Dict[Language, List[Language]]) -> Set[Language]:
    if not mappings:
        return set(values)  # nothing to map
    mapped_values: Set[Language] = set()
    for value in values:
        for mapped_value in mappings.get(value, [value]):
            mapped_values.add(mapped_value)
    return mapped_values


class MappedLanguages:
    def __init__(self,
                 # internal languages list
                 internal_values: List[Language],
                 # custom internal to external language mappings (these, implicitly, also define the external to internal mappings)
                 internal_to_external_mappings: Dict[Language, Union[Language, List[Language]]] = None):
        assert internal_values is not None
        self.internal_values: Set[Language] = set(internal_values)
        self.internal_to_external_mappings: Dict[Language, List[Language]] = _normalize_mappings(
            internal_to_external_mappings)
        self.external_to_internal_mappings: Dict[Language, List[Language]] = _reverse_mappings(
            self.internal_to_external_mappings, internal_values)
        self.external_values: Set[Language] = _build_mapped_set(
            internal_values, self.internal_to_external_mappings)

    # MAP EXTERNAL TO INTERNAL OPERATIONS

    def _to_internal_iterator(self, external_value_or_values: Union[Language, List[Language]]) -> Iterator[Language]:
        external_values = [external_value_or_values] if isinstance(
            external_value_or_values, Language) else external_value_or_values
        return (iv for ev in external_values for iv in self.external_to_internal_mappings.get(ev, [ev]))

    def to_internal(self, external_value_or_values: Union[Language, List[Language]]) -> List[Language]:
        return [l for l in self._to_internal_iterator(external_value_or_values)]

    def to_internal_first(self, external_value_or_values: Union[Language, List[Language]], default: Language = Language.unknown) -> Language:
        return next(self._to_internal_iterator(external_value_or_values), default)

    # MAP INTERNAL TO EXTERNAL OPERATIONS

    def _to_external_iterator(self, internal_value_or_values: List[Language]) -> Iterator[Language]:
        internal_values = [internal_value_or_values] if isinstance(
            internal_value_or_values, Language) else internal_value_or_values
        return (ev for iv in internal_values for ev in self.internal_to_external_mappings.get(iv, [iv]))

    def to_external(self, internal_value_or_values: Union[Language, List[Language]]) -> List[Language]:
        return [l for l in self._to_external_iterator(internal_value_or_values)]

    def to_external_first(self, internal_value_or_values: Union[Language, List[Language]], default: Language = Language.unknown) -> Language:
        return next(self._to_external_iterator(internal_value_or_values), default)

    # TEST/GET INTERNAL OPERATIONS

    def has_any_internal(self, value_or_values: Union[Language, List[Language]]) -> bool:
        values = [value_or_values] if isinstance(value_or_values, Language) else value_or_values
        return any(l for l in values if l in self.internal_values)

    def get_internal_by_name(self, name: str, default: Language = Language.unknown) -> Language:
        return next((l for l in self.internal_values if l.has_name(name)), default) if self.internal_values else default

    def get_internal_by_code(self, code: str, default: Language = Language.unknown) -> Language:
        return next((l for l in self.internal_values if l.has_code(code)), default) if self.internal_values else default

    # TEST/GET EXTERNAL OPERATIONS

    def has_any_external(self, value_or_values: Union[Language, List[Language]]) -> bool:
        values = [value_or_values] if isinstance(value_or_values, Language) else value_or_values
        return any(l for l in values if l in self.external_values)

    def get_external_by_name(self, name: str, default: Language = Language.unknown) -> Language:
        return next((l for l in self.external_values if l.has_name(name)), default) if self.external_values else default

    def get_external_by_code(self, code: str, default: Language = Language.unknown) -> Language:
        return next((l for l in self.external_values if l.has_code(code)), default) if self.external_values else default
