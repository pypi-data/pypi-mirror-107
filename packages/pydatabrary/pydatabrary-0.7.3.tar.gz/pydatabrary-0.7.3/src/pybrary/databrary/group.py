from .record import Record
from .types.category import Category


class Group(Record):
    GROUP_METRICS = {
        "26": "name",
        "27": "description",
        "28": "info"
    }

    def __init__(self, key, id, name=None, description=None, info=None):
        super().__init__(key, id, Category.GROUP, name=name)
        self._description = description
        self._info = info

    @staticmethod
    def from_dict(group_dict):
        id = group_dict.get('key')
        name = group_dict.get('name')
        info = group_dict.get('info')
        description = group_dict.get('description')

        return Group(
            key=id,
            id=id,
            name=name,
            description=description,
            info=info
        )

    @staticmethod
    def from_databrary(group_dict):
        id = group_dict.get('id')
        measures = group_dict.get('measures')
        name = measures.get('26')
        info = measures.get('28')
        description = measures.get('27')

        return Group(
            key=id,
            id=id,
            name=name,
            description=description,
            info=info,
        )

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

    def to_json(self, indent=4):
        return json.dumps(self.to_dict(), indent=indent)

    def get_info(self):
        return self._info

    def get_description(self):
        return self._description