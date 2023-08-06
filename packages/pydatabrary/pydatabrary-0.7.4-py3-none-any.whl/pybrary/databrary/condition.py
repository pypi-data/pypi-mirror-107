from .record import Record
from .types.category import Category


class Condition(Record):
    CONDITION_METRICS = {
        "23": "name",
        "24": "description",
        "25": "info",
    }

    def __init__(self, key, id, name=None, info=None, description=None):
        super().__init__(key, id, Category.CONDITION, name=name)
        self._info = info
        self._description = description

    @staticmethod
    def from_dict(condition_dict):
        id = condition_dict.get('key')
        name = condition_dict.get('name')
        description = condition_dict.get('description')
        info = condition_dict.get('info')

        return Condition(key=id, id=id, name=name, description=description, info=info)

    @staticmethod
    def from_databrary(condition_dict):
        id = condition_dict.get('id')
        measures = condition_dict.get('measures')
        name = measures.get('23')
        description = measures.get('24')
        info = measures.get('25')

        return Condition(key=id, id=id, name=name, description=description, info=info)

    def to_dict(self, template=False):
        result = {
            "key": "{}".format(self.get_key()),
            "name": self.get_name(),
            "category": self.get_category().value,
        }

        if template or self.get_info() is not None:
            result["info"] =  self.get_info()

        if template or self.get_description() is not None:
            result["descritption"] = self.get_description()

        return result

    def to_json(self):
        return json.dumps(self.to_dict())

    def get_info(self):
        return self._info

    def get_description(self):
        return self._description