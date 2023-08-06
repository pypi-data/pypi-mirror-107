import json


class Record:
    def __init__(
            self,
            key,
            id,
            category,
            name=None
    ):
        if key is None or id is None:
            raise Exception('A valid id and key are required for a Record')
        if category is None:
            raise Exception('A category is required for a Record')
        self._key = int(key)
        self._id = int(id)
        self._category = category
        self._name = "{} {}".format(category.value, key) if name is None else name

    def get_id(self):
        return self._id

    def get_key(self):
        return self._key

    def get_name(self):
        return self._name

    def get_category(self):
        return self._category
