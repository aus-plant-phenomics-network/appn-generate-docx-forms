import json
from typing import Dict, Any, List

class FormDataMixin:
    @staticmethod
    def _build_value_map(data: List[dict]) -> Dict[str, Any]:
        return {item['alias']: item.get('value') for item in data if 'alias' in item}

    def load_from_json(self, data: List[dict]):
        value_map = self._build_value_map(data)
        for field_name in getattr(self, '_field_names', []):
            if field_name in value_map:
                setattr(self, field_name, value_map[field_name])
        for child_attr in getattr(self, '_child_sections', []):
            getattr(self, child_attr).load_from_json(data)
