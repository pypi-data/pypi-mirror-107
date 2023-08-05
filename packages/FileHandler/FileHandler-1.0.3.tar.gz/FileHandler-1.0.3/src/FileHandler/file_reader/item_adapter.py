from types import MappingProxyType
from typing import Any, MutableMapping, Iterator, KeysView


class ItemAdapter(MutableMapping):

    def __init__(self, item):
        self.item = item

    def get_item(self) -> Any:
        return self.item

    def __setitem__(self, field_name: str, value: Any) -> None:
        self.item[field_name] = value

    def __delitem__(self, field_name: str) -> None:
        del self.item[field_name]

    def __getitem__(self, field_name: str) -> Any:
        return self.item[field_name]

    def __len__(self) -> int:
        return len(self.item)

    def __iter__(self) -> Iterator:
        return iter(self.item)

    def get_field_meta(self, field_name: str) -> MappingProxyType:
        return MappingProxyType(self.item.fields[field_name])

    def field_names(self) -> KeysView:
        return KeysView(self.item.fields)
