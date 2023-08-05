from file_reader.item_adapter import ItemAdapter


class Identity:
    def __call__(self, values):
        return values


class ItemLoader:
    def __init__(self, item):
        self._values = dict()
        self.item = item

    def _get_item_field_attr(self, field_name, key, default=None):
        field_meta = ItemAdapter(self.item).get_field_meta(field_name)
        return field_meta.get(key, default)

    def _get_input_processor(self, field_name):
        proc = self._get_item_field_attr(
            field_name,
            'input_processor',
            Identity()
        )
        return proc

    def _get_output_processor(self, field_name):
        proc = self._get_item_field_attr(
            field_name,
            'output_processor',
            Identity()
        )
        return proc

    def _get_input_value(self, field_name, value):
        proc = self._get_input_processor(field_name)
        return proc(value)

    def _get_output_value(self, field_name):
        proc = self._get_output_processor(field_name)
        value = self._values.get(field_name, [])
        return proc(value)

    def add_value(self, field_name, value):
        processed_value = self._get_input_value(field_name, value)
        if not self._values.get(field_name, None):
            self._values.setdefault(field_name, list())
        self._values[field_name].append(processed_value)

    def load_item(self):
        adapter = ItemAdapter(self.item)
        for field_name in tuple(self._values):
            value = self._get_output_value(field_name)
            if value is not None:
                adapter[field_name] = value
        return adapter.get_item()
