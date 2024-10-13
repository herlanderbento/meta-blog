from typing import Dict, List


class FilterExtractor:
    @staticmethod
    def extract_filters(query_params: Dict[str, str], filter_fields: List[str]) -> Dict[str, str]:
        filters = {}
        keys_to_remove = []

        for key, value in query_params.items():
            if key in filter_fields:
                filters[key] = value
                keys_to_remove.append(key)

        for key in keys_to_remove:
            query_params.pop(key)

        return filters
